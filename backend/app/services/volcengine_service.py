import asyncio
import time
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

try:
    from volcengine.visual.VisualService import VisualService
    VOLCENGINE_AVAILABLE = True
except ImportError:
    VOLCENGINE_AVAILABLE = False


class VolcengineImageService:
    """Service for interacting with Volcengine Image Generation API"""
    
    def __init__(self, access_key: str, secret_key: str, region: str = "cn-beijing"):
        if not VOLCENGINE_AVAILABLE:
            raise ImportError("volcengine SDK not installed")
        
        self.service = VisualService()
        self.service.set_ak(access_key)
        self.service.set_sk(secret_key)
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def text_to_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        scale: float = 7.5,
        seed: Optional[int] = None,
        style_preset: str = "none",
        num_images: int = 1,
    ) -> dict:
        """Generate image from text using Volcengine API"""
        
        payload = {
            "req_key": "text2image",
            "prompt": prompt,
            "width": width,
            "height": height,
            "scale": scale,
            "steps": steps,
            "return_url": True,
            "logo_info": {
                "add_logo": False
            }
        }
        
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        if seed is not None and seed >= 0:
            payload["seed"] = seed
        
        if style_preset and style_preset != "none":
            payload["style_preset"] = style_preset
        
        loop = asyncio.get_event_loop()
        results = []
        
        for i in range(num_images):
            current_payload = payload.copy()
            if seed is not None and seed >= 0:
                current_payload["seed"] = seed + i
            current_payload["req_key"] = "text2image"
            
            try:
                result = await loop.run_in_executor(
                    self.executor,
                    self._call_text2image_sync,
                    current_payload
                )
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        
        return {
            "success": all("error" not in r for r in results),
            "results": results,
            "count": len(results)
        }
    
    def _call_text2image_sync(self, payload: dict) -> dict:
        """Synchronous call to Volcengine text2image API"""
        try:
            response = self.service.cv_process(payload)
            return response
        except Exception as e:
            return {"error": str(e)}
    
    async def image_to_image(
        self,
        image_base64: str,
        prompt: str,
        negative_prompt: Optional[str] = None,
        strength: float = 0.75,
        steps: int = 20,
        scale: float = 7.5,
        seed: Optional[int] = None,
        style_preset: str = "none",
    ) -> dict:
        """Generate image from image using Volcengine API"""
        
        if image_base64.startswith("data:image"):
            image_base64 = image_base64.split(",")[1]
        
        payload = {
            "req_key": "img2img",
            "prompt": prompt,
            "binary_data_base64": [image_base64],
            "strength": strength,
            "scale": scale,
            "steps": steps,
            "return_url": True,
            "logo_info": {
                "add_logo": False
            }
        }
        
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        if seed is not None and seed >= 0:
            payload["seed"] = seed
        
        if style_preset and style_preset != "none":
            payload["style_preset"] = style_preset
        
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                self._call_image2image_sync,
                payload
            )
            return {
                "success": "error" not in result,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "result": {"error": str(e)}
            }
    
    def _call_image2image_sync(self, payload: dict) -> dict:
        """Synchronous call to Volcengine image2image API"""
        try:
            response = self.service.cv_process(payload)
            return response
        except Exception as e:
            return {"error": str(e)}
    
    async def close(self):
        """Close executor"""
        self.executor.shutdown(wait=False)


class MockVolcengineImageService:
    """Mock service for testing without real API credentials"""
    
    def __init__(self, *args, **kwargs):
        pass
    
    async def text_to_image(self, prompt: str, **kwargs) -> dict:
        """Mock text to image generation"""
        import random
        
        await self._simulate_delay()
        
        num_images = kwargs.get("num_images", 1)
        width = kwargs.get("width", 512)
        height = kwargs.get("height", 512)
        
        images = []
        for i in range(num_images):
            seed = kwargs.get("seed", random.randint(0, 999999))
            if seed is not None and seed >= 0:
                seed = seed + i
            
            image_url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
            images.append({
                "data": {
                    "image_urls": [image_url]
                },
                "code": 10000,
                "message": "Success"
            })
        
        return {
            "success": True,
            "results": images,
            "count": len(images)
        }
    
    async def image_to_image(self, image_base64: str, prompt: str, **kwargs) -> dict:
        """Mock image to image generation"""
        import random
        
        await self._simulate_delay()
        
        seed = kwargs.get("seed", random.randint(0, 999999))
        width = 512
        height = 512
        
        image_url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
        
        return {
            "success": True,
            "result": {
                "data": {
                    "image_urls": [image_url]
                },
                "code": 10000,
                "message": "Success"
            }
        }
    
    async def _simulate_delay(self):
        """Simulate API processing time"""
        import random
        await asyncio.sleep(random.uniform(0.5, 2.0))
    
    async def close(self):
        """No-op for mock service"""
        pass
