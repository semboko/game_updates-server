from fastapi import FastAPI, HTTPException, status, Depends
from uvicorn import run
from typing import List

from db.connection import init_database
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schema import Credentials, CurrencyModel, TopUpRequest
from deps import get_db, get_async_db, get_jwt, get_user_id
from manager.user import (
    create_user,
    UserError,
    create_user_sync as _create_user,
    check_user,
    get_user_by_id,
)
from manager.money import (
    get_user_accounts,
    get_available_currencies,
    create_account,
    create_balance_entry,
)
from datetime import datetime, UTC
from settings import settings
from jwt import encode, decode


app = FastAPI(title="Game Server", version="0.0.1", summary="This is a summary")


@app.on_event("startup")
def onstarup():
    init_database()


@app.post("/signup/sync", tags=["authorization"])
def create_new_user_sync(data: Credentials, session: Session = Depends(get_db)):
    try:
        _create_user(session, data.username, data.password)
    except UserError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Signup Failed",
        )


@app.post("/signup", tags=["authorization"])
async def create_new_user(data: Credentials, session: AsyncSession = Depends(get_async_db)):
    try:
        async with session.begin():
            user = await create_user(session, data.username, data.password)
            account = await create_account(session, user.id, 1)
            await create_balance_entry(session, account.id)

    except UserError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Signup Failed",
        )


@app.post("/signin", response_model=str, tags=["authorization"])
async def authorize_user(
    data: Credentials,
    session: AsyncSession = Depends(get_async_db),
) -> str:
    try:
        user = await check_user(session, data.username, data.password)
    except UserError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Authorization failed")

    result = encode(
        payload={"sub": str(user.id), "username": user.username, "iat": datetime.now(UTC).timestamp()},
        key=settings.jwt_secret,
        algorithm="HS256",
    )

    return result


@app.get("/token/verify")
async def verify_token(
    token: str = Depends(get_jwt),
    db: AsyncSession = Depends(get_async_db),
) -> None:
    claims = decode(token, key=settings.jwt_secret, algorithms=["HS256"])

    now = datetime.now(UTC).timestamp()
    if now - claims["iat"] > 60 * 24 * 60:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    try:
        user = await get_user_by_id(db, claims["sub"])
    except UserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist",
        )

    if user.username != claims["username"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Wrong username for user with id {claims['sub']}"
        )


@app.get("/currency", response_model=List[CurrencyModel])
async def get_all_currencies(db: AsyncSession = Depends(get_async_db)) -> List[CurrencyModel]:
    result = await get_available_currencies(db)
    return [CurrencyModel(id=c.id, name_short=c.name_short) for c in result]


@app.get("/balance")
async def check_balance(
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    accounts = await get_user_accounts(db, user_id)
    return accounts


@app.post("/user/topup")
async def topup_user(
    data: TopUpRequest,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_async_db),
):
    # TODO: Check user_id = admin
    pass


def start_server():
    run(app, host="0.0.0.0", port=8073)
