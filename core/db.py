from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Session,
    UOWTransaction,
    sessionmaker,
)


class Base(DeclarativeBase, MappedAsDataclass):
    pass


engine = create_async_engine(
    "postgresql+asyncpg://postgres:example@localhost:5432/postgres", echo=True
)

sync_maker = sessionmaker()

AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, sync_session_class=sync_maker
)


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
