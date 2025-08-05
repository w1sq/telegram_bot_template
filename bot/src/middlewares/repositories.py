from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db import (
    DatabaseManager,
    UserRepository,
)


class RepositoriesMiddleware(BaseMiddleware):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self._user_repo = None
        super().__init__()

    def _get_user_repo(self, session) -> UserRepository:
        if not self._user_repo or self._user_repo.session != session:
            self._user_repo = UserRepository(session)
        return self._user_repo

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with await self.db_manager.get_session() as session:
            data["session"] = session
            data["user_repo"] = self._get_user_repo(session)
            return await handler(event, data)
