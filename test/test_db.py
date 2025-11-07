import asyncio

from core.tables import create_tables, delete_tables


async def main():
    await delete_tables()
    await create_tables()


if __name__ == "__main__":
    asyncio.run(main())
