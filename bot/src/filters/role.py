from typing import Optional, Callable, Any

from aiogram.types import Message
from aiogram.filters import BaseFilter

from db import UserRepository


class BaseUserFilter(BaseFilter):

    def __init__(self, check_func: Optional[Callable[[Any], bool]] = None):
        self.check_func = check_func

    async def __call__(
        self, message: Message, user_repo: UserRepository
    ) -> Optional[bool]:
        if not message.from_user:
            return False

        user = await user_repo.get(message.from_user.id)

        if not user:
            user = await user_repo.create(
                id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )

        if self.check_func is None:
            return True

        return self.check_func(user)


class IsAdmin(BaseUserFilter):
    def __init__(self):
        super().__init__(lambda user: user.is_admin())


class IsUser(BaseUserFilter):
    def __init__(self):
        super().__init__(lambda user: user.is_user())
