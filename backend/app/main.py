from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .routers import generate, task
from .schemas import HealthResponse

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Image Generation API powered by Volcengine",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix=settings.API_V1_PREFIX)
app.include_router(task.router, prefix=settings.API_V1_PREFIX)

output_dir = Path(settings.OUTPUT_DIR)
output_dir.mkdir(parents=True, exist_ok=True)

try:
    app.mount("/images", StaticFiles(directory=str(output_dir)), name="images")
except Exception:
    pass


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        volcengine_configured=bool(
            settings.VOLCENGINE_ACCESS_KEY and settings.VOLCENGINE_SECRET_KEY
        ),
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
