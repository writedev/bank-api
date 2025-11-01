from typing import Annotated

import uvicorn
from asyncpg.exceptions import CheckViolationError
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth_current_user, auth_required
from app.auth import router as auth_router
from app.bank_account import router as router_bank_account
from app.middleware import MyMiddleware
from core.db import AsyncSessionLocal, get_db
from core.tables import BankAccount, Transaction, User

app = FastAPI()

app.include_router(auth_router)
app.include_router(router_bank_account)
app.add_middleware(MyMiddleware)
