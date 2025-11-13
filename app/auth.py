from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.db import AsyncSession, get_db
from core.models import CreateUserModel, LoginModel, Token, TokenData
from core.tables import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
# openssl rand -hex 32
SECRET_KEY = "1ca858931ea16a60933560ecaff28e641b10388659fea88070287d7c3c49ba0c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """Verifies a plain password against a hash."""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Returns a hash for the given password."""
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates an JWT token."""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def auth_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)
):
    """Authenticates a user by email. Return a User object."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    async with db.begin():
        user = await db.execute(select(User).where(User.email == email))
        user = user.scalars().first()

    if user is None:
        raise credentials_exception
    return user


async def auth_required(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)
):
    """Authenticates a user by email. Return just a Bool."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception
    async with db.begin():
        user_id = await db.scalar(select(User.id).where(User.email == email))

    if user_id is None:
        raise credentials_exception

    return True


@router.post("/create")
async def create_account(content: CreateUserModel, db: AsyncSession = Depends(get_db)):

    password_hash = get_password_hash(password=content.password)
    try:
        async with db.begin():
            user = User(
                first_name=content.first_name,
                last_name=content.last_name,
                email=content.email,
                hashed_password=password_hash,
            )
            db.add(user)
    except IntegrityError:
        return JSONResponse(content={"message": "User already exists"}, status_code=400)

    return JSONResponse(content={"id": user.id}, status_code=201)


async def authenticate_user(db: AsyncSession, email: str, password: str):
    """Authenticates in db a user by email and password."""

    user = await db.execute(select(User).where(User.email == email))
    user = user.scalars().first()

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        print("bad")
        return False

    return user


@router.post("/token")
async def login_for_access_token(
    content: LoginModel,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Create a JWT token and return it."""

    user = await authenticate_user(db, content.email, content.password)
    if user == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": content.email}, expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_expires.seconds,
    )


@router.get("/login")
async def login(is_authenticated: Annotated[bool, Depends(auth_required)]):
    """Authenticates a user by email."""
    return JSONResponse(content={"content": "You are authenticated"}, status_code=202)


@router.get("/test")
async def test():
    """Authenticates a user by email."""
    return JSONResponse(content={"content": "You are authenticated"}, status_code=202)
