from typing import Annotated

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth_current_user
from core.db import get_db
from core.tables import BankAccount, User

router = APIRouter(
    prefix="/bank_account",
    tags=["bank_account"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_bank_account(
    current_user: Annotated[User, Depends(auth_current_user)],
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        bank_account = BankAccount(owner_id=current_user.id)
        db.add(bank_account)

    return JSONResponse(content={"id": bank_account.id}, status_code=201)


@router.get("/list")
async def list_bank_accounts(
    current_user: Annotated[User, Depends(auth_current_user)],
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        result = await db.execute(
            select(BankAccount).where(BankAccount.owner_id == current_user.id)
        )
        bank_accounts = result.scalars().all()

    if not bank_accounts:
        return JSONResponse(content={"bank_accounts": []}, status_code=200)

    bank_accounts_json = []

    for bank_account in bank_accounts:
        bank_accounts_json.append(
            {"id": bank_account.id, "balance": bank_account.balance}
        )

    return JSONResponse(content={"bank_accounts": bank_accounts_json}, status_code=200)
