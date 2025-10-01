from typing import List
from uuid import UUID

from sqlmodel import select

from ...models.classes import Classes
from .base_repository import BaseRepository


class ClassesRepository(BaseRepository[Classes]):
    _entity_class = Classes

    async def get_for_classroom(self, classroom_id: UUID) -> List[Classes]:
        result = await self._session.execute(
            select(self._entity_class).where(
                self._entity_class.classroom_id == classroom_id
            )
        )
        return list(result.scalars().all())

    async def get_for_teacher(self, teacher_id: UUID) -> List[Classes]:
        result = await self._session.execute(
            select(self._entity_class).where(
                self._entity_class.teacher_id == teacher_id
            )
        )
        return list(result.scalars().all())

    async def get_for_classroom_subject(
        self, classroom_subject_id: int
    ) -> List[Classes]:
        result = await self._session.execute(
            select(self._entity_class).where(
                self._entity_class.classroom_subject_id == classroom_subject_id
            )
        )
        return list(result.scalars().all())

