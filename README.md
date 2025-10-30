# Bank Api Project

```ps1
uvicorn main:app --port 8000 --host 127.0.0.1 --reload
```

## system

A user may have multiple bank accounts, and transactions are made from bank account to bank account, not from user to user.

## Create The Tables

```py
import asyncio
from core.db import Base, engine
from models import User, BankAccount, Transaction # and other if there are

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())

```
