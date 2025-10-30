from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, engine


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, init=False)

    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)

    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        index=True, server_default=func.now(), init=False
    )

    bank_accounts: Mapped[list["BankAccount"]] = relationship(
        "BankAccount",
        back_populates="owner_accounts",
        foreign_keys="BankAccount.owner_id",
        init=False,
    )


###########################################################################


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, init=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=None)
    owner_accounts: Mapped[User] = relationship(
        "User",
        back_populates="bank_accounts",
        foreign_keys="BankAccount.owner_id",
        init=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        index=True, server_default=func.now(), default=None, init=False
    )

    sent_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="sender",
        foreign_keys="Transaction.sender_id",
        init=False,
    )

    received_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="receiver",
        foreign_keys="Transaction.receiver_id",
        init=False,
    )


###########################################################################


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, init=False)

    sender_id: Mapped[int] = mapped_column(ForeignKey("bank_accounts.id"), default=None)
    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("bank_accounts.id"), default=None
    )

    amount: Mapped[float] = mapped_column(nullable=False, default=None)

    created_at: Mapped[datetime] = mapped_column(
        index=True, server_default=func.now(), default=None, init=False
    )

    sender: Mapped[BankAccount] = relationship(
        "BankAccount",
        back_populates="sent_transactions",
        foreign_keys="Transaction.sender_id",
        init=False,
    )

    receiver: Mapped[BankAccount] = relationship(
        "BankAccount",
        back_populates="received_transactions",
        foreign_keys="Transaction.receiver_id",
        init=False,
    )

    __table_args__ = (
        CheckConstraint("sender_id != receiver_id", name="sender_receiver_not_equal"),
    )


# for create the tables in postgres db


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Tables deleted successfully.")
