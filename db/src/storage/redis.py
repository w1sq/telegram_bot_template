from typing import Optional
from redis.asyncio import Redis

from utils import settings


class RedisManager:
    _instance: Optional["RedisManager"] = None
    _redis: Optional[Redis] = None

    def __new__(cls) -> "RedisManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def init(self) -> None:
        if self._redis is None:
            self._redis = Redis.from_url(
                str(settings.redis_url.get_secret_value()),
                encoding="utf-8",
                decode_responses=True,
            )

    async def ping(self) -> None:
        if self._redis:
            await self._redis.ping()

    async def close(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None


redis_manager = RedisManager()
