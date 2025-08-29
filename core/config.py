# Configuration settings

from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache
import json


class Settings(BaseSettings):
    """Application settings"""

    # Application - Bu değerler .env dosyasından okunacak
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = False

    # API - Bu değerler .env dosyasından okunacak
    API_V1_STR: str
    PROJECT_NAME: str

    # Database - Bu değer .env dosyasından okunacak
    DATABASE_URL: str

    # Docker Database Configuration - Docker için gerekli
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    # CORS - Bu değer .env dosyasından okunacak
    BACKEND_CORS_ORIGINS: str  # JSON string olarak .env'den gelecek

    # Security - Bu değerler .env dosyasından okunacak
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Redis (for caching)
    REDIS_URL: Optional[str] = None

    # PgAdmin Configuration - Docker için gerekli
    PGADMIN_DEFAULT_EMAIL: Optional[str] = None
    PGADMIN_DEFAULT_PASSWORD: Optional[str] = None

    # External APIs - Bu değerler .env dosyasından okunacak
    UEFA_API_BASE_URL: str
    UEFA_API_KEY: Optional[str] = None

    # Logging - Bu değerler .env dosyasından okunacak
    LOG_LEVEL: str
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @property
    def cors_origins(self) -> List[str]:
        """CORS origins listesini JSON string'den parse eder"""
        try:
            return json.loads(self.BACKEND_CORS_ORIGINS)
        except (json.JSONDecodeError, TypeError):
            return ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings()