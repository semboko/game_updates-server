from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from yoyo import read_migrations, get_backend
from manager.user import create_user_sync, UserError
from db.models import UserRole
from logger import logger

POSTGRES_URL = settings.get_postgres_url()
POSTGRES_ASYNC_URL = settings.get_postgres_url("postgresql+asyncpg")

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

async_engine = create_async_engine(POSTGRES_ASYNC_URL)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False)


def init_database():
    database = get_backend(POSTGRES_URL)
    migrations = read_migrations("./migrations")
    with database.lock():
        database.apply_migrations(database.to_apply(migrations))
    with SessionLocal() as session:
        try:
            logger.info("Creating ADMIN...")
            create_user_sync(session, "admin", "admin", UserRole.ADMIN)
        except UserError:
            logger.warning("ADMIN user already exists. Skipped.")
