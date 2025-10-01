from typing import List

from sqlmodel import select

from ...models.files import Files, FileType
from .base_repository import BaseRepository


class FilesRepository(BaseRepository[Files]):
    _entity_class = Files

    async def get_for_class(self, class_id: int) -> List[Files]:
        result = await self._session.execute(
            select(self._entity_class).where(self._entity_class.class_id == class_id)
        )
        return list(result.scalars().all())

    async def get_by_type(self, file_type: FileType) -> List[Files]:
        result = await self._session.execute(
            select(self._entity_class).where(self._entity_class.type == file_type)
        )
        return list(result.scalars().all())

