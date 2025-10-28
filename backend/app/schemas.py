from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class StylePreset(str, Enum):
    """Style preset enumeration"""
    NONE = "none"
    ANIME = "anime"
    PHOTOGRAPHIC = "photographic"
    DIGITAL_ART = "digital_art"
    COMIC_BOOK = "comic_book"
    FANTASY_ART = "fantasy_art"
    LINE_ART = "line_art"
    ANALOG_FILM = "analog_film"
    NEON_PUNK = "neon_punk"
    ISOMETRIC = "isometric"
    LOW_POLY = "low_poly"
    ORIGAMI = "origami"
    MODELING_COMPOUND = "modeling_compound"
    CINEMATIC = "cinematic"
    THREE_D_MODEL = "3d_model"


class Text2ImageRequest(BaseModel):
    """Text to image generation request"""
    prompt: str = Field(..., min_length=1, max_length=1000, description="Text prompt for image generation")
    negative_prompt: Optional[str] = Field(None, max_length=1000, description="Negative prompt")
    width: int = Field(512, ge=64, le=2048, description="Image width")
    height: int = Field(512, ge=64, le=2048, description="Image height")
    steps: int = Field(20, ge=1, le=100, description="Number of sampling steps")
    scale: float = Field(7.5, ge=1.0, le=20.0, description="CFG scale")
    seed: Optional[int] = Field(None, ge=-1, description="Random seed, -1 for random")
    style_preset: StylePreset = Field(StylePreset.NONE, description="Style preset")
    num_images: int = Field(1, ge=1, le=4, description="Number of images to generate")


class Image2ImageRequest(BaseModel):
    """Image to image generation request"""
    image: str = Field(..., description="Base64 encoded input image")
    prompt: str = Field(..., min_length=1, max_length=1000, description="Text prompt")
    negative_prompt: Optional[str] = Field(None, max_length=1000, description="Negative prompt")
    strength: float = Field(0.75, ge=0.0, le=1.0, description="Transformation strength")
    steps: int = Field(20, ge=1, le=100, description="Number of sampling steps")
    scale: float = Field(7.5, ge=1.0, le=20.0, description="CFG scale")
    seed: Optional[int] = Field(None, ge=-1, description="Random seed")
    style_preset: StylePreset = Field(StylePreset.NONE, description="Style preset")


class TaskResponse(BaseModel):
    """Task creation response"""
    task_id: str = Field(..., description="Unique task identifier")
    status: TaskStatus = Field(TaskStatus.PENDING, description="Task status")
    message: str = Field("Task created successfully", description="Response message")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class TaskStatusResponse(BaseModel):
    """Task status query response"""
    task_id: str
    status: TaskStatus
    progress: Optional[int] = Field(None, ge=0, le=100, description="Progress percentage")
    images: Optional[list[str]] = Field(None, description="Generated image URLs")
    error: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime
    completed_at: Optional[datetime] = None


class GenerationHistory(BaseModel):
    """Generation history record"""
    id: str
    task_id: str
    type: str = Field(..., description="Generation type: text2image or image2image")
    prompt: str
    negative_prompt: Optional[str] = None
    parameters: dict
    images: list[str]
    created_at: datetime
    favorite: bool = False


class HistoryListResponse(BaseModel):
    """History list response"""
    total: int
    items: list[GenerationHistory]
    page: int
    page_size: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    volcengine_configured: bool


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
