from typing import TypeVar, Generic, Type, Optional, Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession):
        self.session = session
        self._model: Optional[Type[ModelType]] = None

    @property
    def model(self) -> Type[ModelType]:
        if self._model is None:
            raise ValueError("Model class must be set")
        return self._model

    async def get(self, id: int) -> Optional[ModelType]:
        model_class = self.model
        statement = select(model_class).where(model_class.id == id)
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        model_class = self.model
        statement = select(model_class).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(
        self,
        id: int,
        data: dict,
    ) -> Optional[ModelType]:
        instance = await self.get(id)
        if instance is None:
            return None

        for key, value in data.items():
            if value is not None:
                setattr(instance, key, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: int) -> Optional[ModelType]:
        instance = await self.get(id)
        if instance is None:
            return None
        await self.session.delete(instance)
        await self.session.commit()
        return instance
