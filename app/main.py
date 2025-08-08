from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.database import get_db
from app.api.routes import deals, contacts, companies, webhooks
from app.core.logging import setup_logging

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
setup_logging()

# Создание приложения FastAPI
app = FastAPI(
    title="Аналитическая Платформа-Прослойка",
    description="Центральный мост данных для интеграции с Bitrix24",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Функция для проверки API ключа
async def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != settings.SERVICE_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Неверный API ключ"
        )
    return x_api_key

# Подключение роутов
app.include_router(
    deals.router,
    prefix="/api/v1",
    tags=["deals"],
    dependencies=[Depends(verify_api_key)]
)

app.include_router(
    contacts.router,
    prefix="/api/v1",
    tags=["contacts"],
    dependencies=[Depends(verify_api_key)]
)

app.include_router(
    companies.router,
    prefix="/api/v1",
    tags=["companies"],
    dependencies=[Depends(verify_api_key)]
)

app.include_router(
    webhooks.router,
    prefix="/api/v1",
    tags=["webhooks"]
)

@app.get("/")
async def root():
    return {"message": "Аналитическая Платформа-Прослойка v1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )