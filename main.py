from asyncpg.exceptions import CheckViolationError
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import AsyncSessionLocal
from core.tables import BankAccount, Transaction, User

app = FastAPI()


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


class CreateBanckAccount(BaseModel):
    id: int
    balance: float


class Transfer(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float


@app.post("/db/create_user")
async def create_user(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        user = User(first_name="John", last_name="Doe", email="2Xx0F@example.com")
        db.add(user)

    return JSONResponse(content={"id": user.id}, status_code=201)


@app.post("/db/create_bank_account")
async def create_bank_account(
    content: CreateBanckAccount, db: AsyncSession = Depends(get_db)
):

    balance = content.balance
    id = content.id

    async with db.begin():
        bank_account = BankAccount(balance=balance, owner_id=id)
        db.add(bank_account)

    return JSONResponse(content={"id": bank_account.id}, status_code=201)


@app.post("/db/transfer")
async def transfer(content: Transfer, db: AsyncSession = Depends(get_db)):

    sender_id = content.sender_id
    receiver_id = content.receiver_id
    amount = content.amount

    # double check / security

    if sender_id == receiver_id:
        error_message = "Sender and receiver cannot be the same."
        return JSONResponse(content={"error": error_message}, status_code=400)

    try:
        async with db.begin():
            transaction = Transaction(
                sender_id=sender_id, receiver_id=receiver_id, amount=amount
            )
            db.add(transaction)

        return JSONResponse(content={"id": str(transaction.id)}, status_code=201)

    except IntegrityError as e:
        # double check / security
        if "sender_receiver_not_equal" in str(e.orig):
            error_message = "Sender and receiver cannot be the same."
            return JSONResponse(content={"error": error_message}, status_code=400)
