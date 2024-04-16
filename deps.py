from db.connection import SessionLocal, AsyncSessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generator, AsyncGenerator, Annotated
from fastapi import Header


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    # session = await AsyncSessionLocal().__aenter__()
    # ....yield... pause...
    # await session.__aexit__()

    async with AsyncSessionLocal() as session:
        yield session


def get_jwt(token: Annotated[str, Header()]) -> str:
    return token
