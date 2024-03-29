from argparse import ArgumentParser
from enum import Enum

from game_loop import start_loop
from game_server import start_server


parser = ArgumentParser(
    prog="Game Server",
)


class ServerMode(Enum):
    GAME_LOOP = 0
    GAME_SERVER = 1


parser.add_argument(
    "--mode",
    type=int,
    choices=(0, 1),
    required=True,
    help="""
        Defines what process will be launched
    """
)

args = parser.parse_args()
mode = ServerMode(args.mode)

if mode == ServerMode.GAME_LOOP:
    start_loop()

if mode == ServerMode.GAME_SERVER:
    start_server()
