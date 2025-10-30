import asyncio

from core.db import AsyncSessionLocal


async def test_connect_db():
    async with AsyncSessionLocal() as session:
        await session.commit()
        print("Connected to DB")


asyncio.run(test_connect_db())
