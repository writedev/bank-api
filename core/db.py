from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    pass


engine = create_async_engine(
    "postgresql+asyncpg://postgres:example@localhost:5432/postgres", echo=True
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
