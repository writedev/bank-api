from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)

    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name = mapped_column(String(50), nullable=True)

    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(index=True, server_default=func.now())

    bank_accounts = relationship("BankAccount", back_populates="owner_accounts")


###########################################################################


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(index=True, server_default=func.now())

    owner_accounts = relationship("User", back_populates="bank_accounts")
    transaction = relationship("Transaction", back_populates="account")


###########################################################################


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    sender_id: Mapped[int] = mapped_column(ForeignKey("bank_accounts.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("bank_accounts.id"))

    amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(index=True, server_default=func.now())

    account = relationship("BankAccount", back_populates="transactions")

    __table_args__ = (
        CheckConstraint("sender_id != receiver_id", name="sender_receiver_not_equal"),
    )
