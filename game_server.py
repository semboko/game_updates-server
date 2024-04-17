from fastapi import FastAPI, HTTPException, status, Depends
from uvicorn import run

from db.connection import init_database
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schema import Credentials
from deps import get_db, get_async_db, get_jwt
from manager.user import (
    create_user,
    UserError,
    create_user_sync as _create_user,
    check_user,
    get_user_by_id,
)
from datetime import datetime, UTC
from settings import settings
from jwt import encode, decode


app = FastAPI(
    title="Game Server",
    version="0.0.1",
    summary="This is a summary"
)


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
        await create_user(session, data.username, data.password)
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
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Authorization failed"
        )

    result = encode(payload={
        "sub": str(user.id),
        "username": user.username,
        "iat": datetime.now(UTC).timestamp()
    }, key=settings.jwt_secret, algorithm="HS256")

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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Wrong username for user with id {claims["sub"]}"
        )


def start_server():
    run(app, host="0.0.0.0", port=8072)
