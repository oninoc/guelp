from ...database import AsyncSession
from typing import Generic, List, TypeVar, Type, Union
from sqlmodel import select
from ...models.base.base_model import BaseModel

TEntity = TypeVar("TEntity", bound=BaseModel)


class BaseRepository(Generic[TEntity]):
    _entity_class: Type[TEntity]
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> List[TEntity]:
        entities = await self._session.execute(
            select(self._entity_class).order_by(self._entity_class.id)
        )
        return list(entities.scalars().all())

    async def create(self, data: TEntity) -> TEntity:
        self._session.add(data)
        await self._session.commit()
        await self._session.refresh(data)
        return data

    async def get_by_id(self, entity_id: Union[str, int]) -> TEntity:
        entities = await self._session.execute(
            select(self._entity_class).where(self._entity_class.id == entity_id)
        )
        return entities.scalars().first()

    async def delete(self, entity_id: Union[str, int]) -> None:
        entity = await self.get_by_id(entity_id)
        await self._session.delete(entity)
        await self._session.commit()

    async def update(self, data: TEntity) -> TEntity:
        self._session.add(data)
        await self._session.commit()
        await self._session.refresh(data)
        return data

    async def bulk_create(self, data: List[TEntity]) -> List[TEntity]:
        for item in data:
            self._session.add(item)
        await self._session.commit()
        return data
