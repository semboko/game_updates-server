from fastapi import FastAPI, HTTPException, status, Depends
from uvicorn import run

from db.connection import init_database
from sqlalchemy.orm import Session
from schema import SignUpRequest
from deps import get_db
from manager.user import create_user, UserError


app = FastAPI(
    title="Game Server",
    version="0.0.1",
    summary="This is a summary"
)


@app.on_event("startup")
def onstarup():
    init_database()


@app.post("/signup", tags=["authorization"])
async def create_new_user(data: SignUpRequest, session: Session = Depends(get_db)):
    try:
        create_user(session, data.username, data.password)
    except UserError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Signup Failed",
        )


@app.post("/signin", response_model=str, tags=["authorization"])
async def authorize_user() -> str:
    pass


def start_server():
    run(app, host="0.0.0.0", port=8072)
