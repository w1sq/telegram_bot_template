from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db import DatabaseManager


class RedisMiddleware(BaseMiddleware):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["redis"] = self.db_manager.redis
        return await handler(event, data)
