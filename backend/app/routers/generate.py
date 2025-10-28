import asyncio
import base64
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from ..config import Settings, get_settings
from ..schemas import (
    Text2ImageRequest,
    Image2ImageRequest,
    TaskResponse,
    TaskStatus,
    ErrorResponse,
)
from ..services.volcengine_service import VolcengineImageService, MockVolcengineImageService
from ..utils.task_store import TaskStore

router = APIRouter(prefix="/generate", tags=["generation"])

_task_store: Optional[TaskStore] = None
_volcengine_service: Optional[VolcengineImageService] = None
_output_dir: Optional[Path] = None


def _get_output_dir(settings: Settings) -> Path:
    """Ensure output directory exists"""
    global _output_dir
    if _output_dir is None:
        path = Path(settings.OUTPUT_DIR)
        path.mkdir(parents=True, exist_ok=True)
        _output_dir = path
    return _output_dir


def get_task_store(settings: Settings = Depends(get_settings)) -> TaskStore:
    """Get task store instance"""
    global _task_store
    if _task_store is None:
        _get_output_dir(settings)
        _task_store = TaskStore(
            history_file=Path(settings.HISTORY_FILE),
            max_history_size=settings.MAX_HISTORY_SIZE,
        )
    return _task_store


def get_volcengine_service(settings: Settings = Depends(get_settings)):
    """Get Volcengine service instance"""
    global _volcengine_service
    if _volcengine_service is None:
        _get_output_dir(settings)
        # Check if credentials are configured
        if not settings.VOLCENGINE_ACCESS_KEY or not settings.VOLCENGINE_SECRET_KEY:
            # Use mock service for demo
            _volcengine_service = MockVolcengineImageService()
        else:
            _volcengine_service = VolcengineImageService(
                access_key=settings.VOLCENGINE_ACCESS_KEY,
                secret_key=settings.VOLCENGINE_SECRET_KEY,
                region=settings.VOLCENGINE_REGION,
            )
    return _volcengine_service


def _normalize_base64(data: str) -> Optional[str]:
    try:
        if "," in data:
            data = data.split(",", 1)[1]
        data = data.strip()
        if not data:
            return None
        # Add padding if necessary
        missing_padding = len(data) % 4
        if missing_padding:
            data += "=" * (4 - missing_padding)
        # Validate by decoding
        base64.b64decode(data, validate=True)
        return data
    except Exception:
        return None


def _save_base64_image(data: str, output_dir: Path) -> Optional[str]:
    normalized = _normalize_base64(data)
    if not normalized:
        return None
    try:
        image_bytes = base64.b64decode(normalized)
        filename = f"{uuid4().hex}.png"
        file_path = output_dir / filename
        file_path.write_bytes(image_bytes)
        return f"/images/{filename}"
    except Exception:
        return None


def _extract_image_urls(payload: dict, output_dir: Path) -> list[str]:
    urls: set[str] = set()
    base64_items: list[str] = []

    def walk(value, key: Optional[str] = None):
        if isinstance(value, dict):
            for k, v in value.items():
                walk(v, k)
        elif isinstance(value, list):
            for item in value:
                walk(item, key)
        elif isinstance(value, str):
            if key:
                key_lower = key.lower()
                if key_lower in {"image_urls", "urls", "url_list"}:
                    urls.add(value)
                elif key_lower in {"image_url", "url"}:
                    urls.add(value)
                elif key_lower in {"image_base64", "binary_data_base64", "binary_data", "image"}:
                    base64_items.append(value)
                elif key_lower in {"result", "data"}:
                    if value.startswith("http"):
                        urls.add(value)
            else:
                if value.startswith("http://") or value.startswith("https://"):
                    urls.add(value)
                else:
                    maybe_base64 = _normalize_base64(value)
                    if maybe_base64:
                        base64_items.append(value)

    walk(payload)

    for item in base64_items:
        saved = _save_base64_image(item, output_dir)
        if saved:
            urls.add(saved)

    return list(urls)


async def process_text2image_task(
    task_id: str,
    request: Text2ImageRequest,
    store: TaskStore,
    service: VolcengineImageService,
):
    """Background task to process text-to-image generation"""
    try:
        # Mark as processing
        await store.set_processing(task_id)
        
        # Call Volcengine API
        result = await service.text_to_image(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            steps=request.steps,
            scale=request.scale,
            seed=request.seed,
            style_preset=request.style_preset.value,
            num_images=request.num_images,
        )
        
        if result.get("success"):
            # Extract image URLs from results
            image_urls = []
            for res in result.get("results", []):
                if isinstance(res, dict) and "data" in res:
                    urls = res["data"].get("image_urls", [])
                    image_urls.extend(urls)
            
            await store.complete_task(task_id, image_urls)
        else:
            error_msg = "Failed to generate image"
            if result.get("results"):
                first_error = next((r for r in result["results"] if "error" in r), None)
                if first_error:
                    error_msg = first_error.get("error", error_msg)
            await store.fail_task(task_id, error_msg)
    
    except Exception as e:
        await store.fail_task(task_id, f"Internal error: {str(e)}")


async def process_image2image_task(
    task_id: str,
    request: Image2ImageRequest,
    store: TaskStore,
    service: VolcengineImageService,
):
    """Background task to process image-to-image generation"""
    try:
        await store.set_processing(task_id)
        
        result = await service.image_to_image(
            image_base64=request.image,
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            strength=request.strength,
            steps=request.steps,
            scale=request.scale,
            seed=request.seed,
            style_preset=request.style_preset.value,
        )
        
        if result.get("success"):
            res_data = result.get("result", {})
            if isinstance(res_data, dict) and "data" in res_data:
                image_urls = res_data["data"].get("image_urls", [])
                await store.complete_task(task_id, image_urls)
            else:
                await store.fail_task(task_id, "Invalid response format")
        else:
            error_msg = result.get("result", {}).get("error", "Failed to generate image")
            await store.fail_task(task_id, error_msg)
    
    except Exception as e:
        await store.fail_task(task_id, f"Internal error: {str(e)}")


@router.post("/text2image", response_model=TaskResponse)
async def text_to_image(
    request: Text2ImageRequest,
    store: TaskStore = Depends(get_task_store),
    service: VolcengineImageService = Depends(get_volcengine_service),
):
    """
    Generate image from text prompt
    
    - **prompt**: Text description of the desired image
    - **negative_prompt**: Things to avoid in the image
    - **width/height**: Image dimensions (64-2048)
    - **steps**: Sampling steps (1-100)
    - **scale**: CFG scale (1.0-20.0)
    - **seed**: Random seed for reproducibility (-1 for random)
    - **style_preset**: Art style preset
    - **num_images**: Number of images to generate (1-4)
    """
    
    # Create task
    task = await store.create_task(
        task_type="text2image",
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        parameters=request.model_dump(),
    )
    
    # Schedule background processing
    asyncio.create_task(
        process_text2image_task(
            task.id,
            request,
            store,
            service,
        )
    )
    
    return TaskResponse(
        task_id=task.id,
        status=task.status,
        message="Image generation task created",
        created_at=task.created_at,
    )


@router.post("/image2image", response_model=TaskResponse)
async def image_to_image(
    request: Image2ImageRequest,
    store: TaskStore = Depends(get_task_store),
    service: VolcengineImageService = Depends(get_volcengine_service),
):
    """
    Generate image from input image and text prompt
    
    - **image**: Base64 encoded input image
    - **prompt**: Text description
    - **negative_prompt**: Things to avoid
    - **strength**: Transformation strength (0.0-1.0)
    - **steps**: Sampling steps
    - **scale**: CFG scale
    - **seed**: Random seed
    - **style_preset**: Art style preset
    """
    
    # Validate base64 image
    if not request.image or len(request.image) < 100:
        raise HTTPException(status_code=400, detail="Invalid image data")
    
    # Create task
    task = await store.create_task(
        task_type="image2image",
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        parameters=request.model_dump(exclude={"image"}),
    )
    
    # Schedule background processing
    asyncio.create_task(
        process_image2image_task(
            task.id,
            request,
            store,
            service,
        )
    )
    
    return TaskResponse(
        task_id=task.id,
        status=task.status,
        message="Image transformation task created",
        created_at=task.created_at,
    )
