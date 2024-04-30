from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Account


async def get_user_accounts(db: AsyncSession, user_id: int) -> List[Account]:
    query = select(Account).where(Account.user_id == user_id)
    result = await db.execute(query)
    return result
