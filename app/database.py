from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from .config import settings

DATABASE_URL = settings.DATABASE_URL

# Crea un motor de base de datos asincrono
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# crea una sesion
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_db():
    """
    Crea la base de datos y sus tablas de forma asincrona
    """
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
