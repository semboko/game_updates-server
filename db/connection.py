from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from yoyo import read_migrations, get_backend

POSTGRES_URL = settings.get_postgres_url()
POSTGRES_ASYNC_URL = settings.get_postgres_async_url()

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

async_engine = create_async_engine(POSTGRES_ASYNC_URL)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False)


def init_database():
    database = get_backend(POSTGRES_URL)
    migrations = read_migrations("./migrations")
    with database.lock():
        database.apply_migrations(database.to_apply(migrations))
