from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from utils import settings

engine: AsyncEngine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user.get_secret_value()}:{settings.postgres_password.get_secret_value()}"
    f"@{settings.postgres_host.get_secret_value()}:{settings.postgres_port}"
    f"/{settings.postgres_db.get_secret_value()}",
    echo=settings.debug,
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
