from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, mapped_column
import enum


Base = declarative_base()


class UserRole(enum.Enum):
    USER: int = 0
    ADMIN: int = 1


class User(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Integer)


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_short = Column(String)


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey("player.id"))
    currency_id = mapped_column(ForeignKey("currency.id"))
    is_active = Column(Boolean, default=True)


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_account_id = ForeignKey("account.id")
    to_account_id = ForeignKey("account.id")
    amount = Column(Numeric(20, 4))
    transaction_type = Column(Integer)
    date_time = Column(DateTime)


class Balance(Base):
    __tablename__ = "balance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = mapped_column(ForeignKey("account.id"))
    amount = Column(Numeric(20, 4))
