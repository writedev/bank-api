from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    "postgresql+asyncpg://postgres:example@localhost:5432/postgres", echo=False
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
