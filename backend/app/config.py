from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Volcengine Image Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    # Volcengine Credentials
    VOLCENGINE_ACCESS_KEY: str = ""
    VOLCENGINE_SECRET_KEY: str = ""
    VOLCENGINE_REGION: str = "cn-beijing"
    
    # Image Generation Settings
    DEFAULT_WIDTH: int = 512
    DEFAULT_HEIGHT: int = 512
    DEFAULT_STEPS: int = 20
    DEFAULT_SCALE: float = 7.5
    MAX_BATCH_SIZE: int = 4
    
    # Storage
    OUTPUT_DIR: str = "/app/data/output"
    HISTORY_FILE: str = "/app/data/history.json"
    MAX_HISTORY_SIZE: int = 1000
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
