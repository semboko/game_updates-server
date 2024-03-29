from sqlalchemy.orm import Session
from hashlib import sha256
from db.models import User
from sqlalchemy.exc import IntegrityError


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
