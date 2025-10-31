from pydantic import BaseModel, EmailStr


class CreateAccountModel(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
