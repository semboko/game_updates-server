from time import sleep

from settings import settings
from decimal import Decimal
from schema import PublicEvent, GameState, Game
from utils import genCoef
import requests


def start_loop():
    game = Game(final_coef=genCoef())

    while True:
        # 1. Change the state
        if game.state == GameState.WAITING:
            if game.waiting_left <= 0:
                game.state = GameState.RUNNING
            game.waiting_left -= settings.step_delay

        if game.state == GameState.RUNNING:
            if game.coef >= game.final_coef:
                game.state = GameState.FINISHED
            else:
                game.coef += Decimal("0.01")

        # 2. Send the new state to the consumers
        public = PublicEvent(state=game.state, coef=game.coef)

        res = requests.post(
            settings.cent_url + "/api/publish",
            json={"channel": "public_updates", "data": public.model_dump_json()},
            headers={"X-API-Key": settings.cent_apikey},
            timeout=1,
        )
        print(res.status_code, res.content, public.model_dump_json())
        assert res.status_code == 200

        if game.state == GameState.FINISHED:
            game = Game(final_coef=genCoef())

        sleep(settings.step_delay)
