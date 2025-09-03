from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from .base import BaseRepository
from ..models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self._model = User

    async def get_filtered(
        self, conditions: list, skip: int = 0, limit: int = 100
    ) -> List[User]:
        statement = select(self._model)
        if conditions:
            statement = statement.where(and_(*conditions))
        statement = statement.offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all()
