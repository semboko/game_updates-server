from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from hashlib import sha256
from db.models import User
from sqlalchemy.exc import IntegrityError
from asyncio import sleep
import time


class UserError(Exception):
    pass


def create_user(db: Session, username: str, password: str):
    password_hash = sha256(password.encode("UTF-8")).hexdigest()
    try:
        new_user = User(username=username, password=password_hash)
        db.add(new_user)
        db.commit()
    except IntegrityError:
        raise UserError()


async def create_user_async(db: AsyncSession, username: str, password: str):
    password_hash = sha256(password.encode("UTF-8")).hexdigest()
    try:
        new_user = User(username=username, password=password_hash)
        db.add(new_user)
        await db.commit()
    except IntegrityError:
        raise UserError()
