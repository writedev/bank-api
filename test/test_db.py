import asyncio

from core.tables import create_tables, delete_tables

if __name__ == "__main__":
    asyncio.run(create_tables())
