from fastapi import FastAPI

from core.db import AsyncSessionLocal
from core.tables import BankAccount, User

app = FastAPI()


@app.get("/db/create_user")
async def root():
    async with AsyncSessionLocal() as session:
        user = User(first_name="John", last_name="Doe", email="2Xx0F@example.com")
