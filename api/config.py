"""Backend configuration and environment settings."""

import os
from functools import lru_cache
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application runtime configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Ritucast Agricultural Intelligence API"
    APP_NAME: str = "Ritucast Agricultural Intelligence API"
    APP_VERSION: str = "1.0.0-phase10"
    API_V1_STR: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Allowed CORS Origins (Restricted for frontend development)
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://ritucast.app",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # File and Data Storage Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    SAMPLE_DIR: Path = DATA_DIR / "sample"

    # Operational Parameters
    DEFAULT_DANGER_LEVEL_M: float = 8.25
    MAX_WEATHER_AGE_HOURS: float = 36.0
    CACHE_TTL_SECONDS: int = 3600
    RATE_LIMIT_PER_MINUTE: int = 60
    ENABLE_RATE_LIMIT: bool = True
    MAX_REQUEST_SIZE_BYTES: int = 1048576  # 1 MB max payload


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()
