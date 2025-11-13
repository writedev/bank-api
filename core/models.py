from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr, model_validator


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


class DoTransaction(BaseModel):
    sender_bcc_id: str
    receiver_bcc_id: str
    amount: float

    @model_validator(mode="after")
    def check_sender_receiver_not_equal(self):
        if self.sender_bcc_id == self.receiver_bcc_id:
            raise HTTPException(
                status_code=400, detail="Sender and receiver cannot be the same"
            )
        elif self.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        return self


class TransactionList(BaseModel):
    bcc_id: str
