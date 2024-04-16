from enum import Enum
from decimal import Decimal
from pydantic import BaseModel


class GameState(Enum):
    WAITING: int = 0
    RUNNING: int = 1
    FINISHED: int = -1


class PublicEvent(BaseModel):
    state: GameState = GameState.WAITING
    coef: Decimal = Decimal("1.00")


class Game(PublicEvent):
    final_coef: Decimal
    waiting_left: float = 10.0


class Credentials(BaseModel):
    username: str
    password: str
