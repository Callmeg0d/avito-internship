from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import Any

from app.config import settings

DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS: dict[str, Any] = {}

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
# Создание движка (небольших транзакций)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Dependency для получения сессии БД"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
