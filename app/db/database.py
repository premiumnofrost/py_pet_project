import os
# Импортируем асинхронные аналоги из sqlalchemy.ext.asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# 2. ДВИЖОК:
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# 3. ФАБРИКА СЕССИЙ:
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False 
)

class Base(DeclarativeBase):
    pass

# 4. ЗАВИСИМОСТЬ:
async def get_db():
   
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

