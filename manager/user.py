from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from hashlib import sha256
from db.models import User, UserRole
from sqlalchemy.exc import IntegrityError, NoResultFound
from time import sleep
from asyncio import sleep as async_sleep


class UserError(Exception):
    pass


def create_user_sync(db: Session, username: str, password: str, role: UserRole = UserRole.USER):
    password_hash = sha256(password.encode("UTF-8")).hexdigest()
    try:
        new_user = User(username=username, password=password_hash, role=role.value)
        db.add(new_user)
        db.commit()
    except IntegrityError:
        raise UserError()


async def create_user(db: AsyncSession, username: str, password: str, role: UserRole = UserRole.USER) -> User:
    # await async_sleep(10)
    password_hash = sha256(password.encode("UTF-8")).hexdigest()
    try:
        new_user = User(username=username, password=password_hash, role=role.value)
        db.add(new_user)
        await db.flush()
        return new_user
    except IntegrityError:
        raise UserError()


async def check_user(db: AsyncSession, username: str, password: str) -> User:
    sql_statement = select(User).where(User.username == username)
    result = await db.execute(sql_statement)
    try:
        user = result.scalar_one()
    except NoResultFound:
        raise UserError()
    password_hash = sha256(password.encode("UTF-8")).hexdigest()
    if user.password != password_hash:
        raise UserError()

    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    sql_statement = select(User).where(User.id == user_id)
    result = await db.execute(sql_statement)
    try:
        user = result.scalar_one()
    except NoResultFound:
        raise UserError()
    return user
