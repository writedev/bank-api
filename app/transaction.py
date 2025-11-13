from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth_current_user
from core.db import get_db
from core.models import DoTransaction, TransactionList
from core.tables import BankAccount, Transaction, User

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    responses={404: {"description": "Not found"}},
)


async def is_owner(db: AsyncSession, user_id: int, bank_account_id: str) -> bool:
    """DO THIS IN DB BEGIN"""
    result = await db.execute(
        select(BankAccount)
        .where(BankAccount.id == bank_account_id)
        .where(BankAccount.owner_id == user_id)
    )

    result = result.scalars().all()

    if not result:
        return False

    return True


@router.get("/do")
async def do_transaction(
    content: DoTransaction,
    auth_current_user: Annotated[User, Depends(auth_current_user)],
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():

        # check if the sender is the owner

        if not await is_owner(db, auth_current_user.id, content.sender_bcc_id):
            return JSONResponse(
                content={"message": "You are not the owner of this bank account"},
                status_code=403,
            )

        # Get the balance of the sender

        sender_balance_result = await db.execute(
            select(BankAccount.balance).where(BankAccount.id == content.sender_bcc_id)
        )

        sender_balance: float = sender_balance_result.scalar_one()

        if sender_balance < content.amount:
            return JSONResponse(
                content={"message": "Not enough balance"}, status_code=400
            )

        # Get the balance of the receiver

        receiver_balance_result = await db.execute(
            select(BankAccount.balance).where(BankAccount.id == content.receiver_bcc_id)
        )

        receiver_balance: float = receiver_balance_result.scalar_one()

        # Update the balance of the sender & receiver

        sender_balance -= content.amount

        receiver_balance += content.amount

        update_sender_balance = (
            update(BankAccount)
            .where(BankAccount.id == content.sender_bcc_id)
            .values(balance=sender_balance)
        )

        await db.execute(update_sender_balance)

        update_receiver_balance = (
            update(BankAccount)
            .where(BankAccount.id == content.receiver_bcc_id)
            .values(balance=receiver_balance)
        )

        await db.execute(update_receiver_balance)

        # Create the transaction

        transaction = Transaction(
            sender_id=content.sender_bcc_id,
            receiver_id=content.receiver_bcc_id,
            amount=content.amount,
        )

        db.add(transaction)

    return JSONResponse(
        content={
            "message": "Transaction done",
            "balance": sender_balance,
        },
        status_code=200,
    )


@router.get("/list")
async def list_transactions(
    content: TransactionList,
    auth_current_user: Annotated[User, Depends(auth_current_user)],
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        result = await db.execute(
            select(Transaction).where(Transaction.receiver_id == content.bcc_id)
        )
        transactions = result.scalars().all()

    if not transactions:
        return JSONResponse(content={"transactions": []}, status_code=200)

    transactions_json = []

    for transaction in transactions:
        transactions_json.append(
            {
                "id": str(transaction.id),
                "sender_id": transaction.sender_id,
                "receiver_id": transaction.receiver_id,
                "amount": transaction.amount,
                "created_at": transaction.created_at.strftime("%Y-%m-%d--%H:%M:%S"),
            }
        )

    return JSONResponse(content={"transactions": transactions_json}, status_code=200)
