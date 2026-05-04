from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "YOLO11 Inference Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Model Settings
    MODEL_PATH: str = "models/yolo11n.pt"
    CONFIDENCE_THRESHOLD: float = 0.40
    DEVICE: str | None = None  # Auto-detected if None
    
    # Performance Settings
    MAX_QUEUE_SIZE: int = 10
    LATENCY_HISTORY_SIZE: int = 100
    
    # API Security
    API_KEY: str | None = None  # If set, all requests must include X-API-Key header
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
