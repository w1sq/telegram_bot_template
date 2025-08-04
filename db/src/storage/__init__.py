from typing import Optional, AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from .redis import redis_manager
from .postgres import async_session_maker, engine, init_models


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _initialized: bool = False
    _engine: AsyncEngine = engine

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def init(self):
        if not self._initialized:
            await init_models()
            await redis_manager.init()
            self._initialized = True

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._initialized:
            await self.init()
        return async_session_maker()

    async def close(self):
        if self._initialized:
            await self._engine.dispose()
            await redis_manager.close()
            self._initialized = False

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def redis(self) -> Redis:
        return redis_manager._redis


db_manager = DatabaseManager()
