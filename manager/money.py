from typing import List, Tuple
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Account, Currency, Balance
from schema import AccountBalance


async def get_available_currencies(db: AsyncSession) -> List[Currency]:
    query = select(Currency)
    result = await db.execute(query)
    return result.scalars().all()


async def add_currency(db: AsyncSession, name_short: str) -> Currency:
    new_currency = Currency(name_short=name_short)
    db.add(new_currency)
    await db.commit()
    return new_currency


async def get_user_accounts(db: AsyncSession, user_id: int) -> List[AccountBalance]:
    query = (
        select(Account.id, Currency.name_short, Balance.amount)
        .join(Currency)
        .join(Balance)
        .where(Account.user_id == user_id)
    )
    result = await db.execute(query)

    balances = []
    for entry in result.all():
        balances.append(
            AccountBalance(
                account_id=entry[0],
                currency_name=entry[1],
                amount=entry[2],
            )
        )

    return balances


async def create_account(db: AsyncSession, user_id: int, currency_id: int) -> Account:
    new_account = Account(user_id=user_id, currency_id=currency_id)
    db.add(new_account)
    await db.flush()
    return new_account


async def create_balance_entry(db: AsyncSession, account_id: int) -> Balance:
    balance = Balance(account_id=account_id, amount=0)
    db.add(balance)
    await db.flush()
    return balance
