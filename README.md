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

----

## CheckList

- [ ] Add websocket system

```py
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
```
