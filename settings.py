from pydantic_settings import BaseSettings
from json import load
from typing import Optional


class Settings(BaseSettings):
    step_delay: float = 0.1
    waiting_time: int = 10

    cent_apikey: Optional[str] = None
    cent_url: str = "http://0.0.0.0:8910"

    postgres_host: str = "0.0.0.0"
    postgres_port: int = 8911
    postgres_user: str = "admin"
    postgres_password: str = "admin"
    postgres_db: str = "app"

    def load_cent_config(self):
        with open("./config.json", "r") as conf_file:
            conf = load(conf_file)
            self.cent_apikey = conf["api_key"]

    def get_postgres_url(self):
        return (
            "postgresql://" +
            self.postgres_user +
            ":" +
            self.postgres_password +
            "@" +
            self.postgres_host +
            ":" +
            str(self.postgres_port) +
            "/" +
            self.postgres_db
        )

    def get_postgres_async_url(self):
        return (
            "postgresql+asyncpg://" +
            self.postgres_user +
            ":" +
            self.postgres_password +
            "@" +
            self.postgres_host +
            ":" +
            str(self.postgres_port) +
            "/" +
            self.postgres_db
        )


settings = Settings()
settings.load_cent_config()
