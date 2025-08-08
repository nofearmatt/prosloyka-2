from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Основные настройки приложения
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API ключ
    SERVICE_API_KEY: str = "super-secret-key"
    
    # Настройки базы данных
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/prosloyka"
    
    # Настройки Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Настройки Bitrix24
    BITRIX24_WEBHOOK_URL: Optional[str] = None
    
    # Настройки логирования
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"

settings = Settings()