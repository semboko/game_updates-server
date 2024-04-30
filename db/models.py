from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_short = Column(String)


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = relationship("User")
    currency_id = relationship("Currency")
    is_active = Column(Boolean, default=True)


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_account_id = relationship("Account")
    to_account_id = relationship("Account")
    amount = Column(Numeric(20, 4))
    transaction_type = Column(Integer)
    date_time = Column(DateTime)


class Balance(Base):
    __tablename__ = "balance"

    account_id = relationship("Account")
    amount = Column(Numeric(20, 4))
