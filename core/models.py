from pydantic import BaseModel, EmailStr


class CreateUserModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    email: EmailStr


class CreateBankAccount(BaseModel):
    name: str | None = None
