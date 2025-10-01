from typing import List
from uuid import UUID

from sqlmodel import select

from ...models.classroom_subject import ClassroomSubject
from .base_repository import BaseRepository


class ClassroomSubjectRepository(BaseRepository[ClassroomSubject]):
    _entity_class = ClassroomSubject

    async def get_for_classroom(self, classroom_id: UUID) -> List[ClassroomSubject]:
        result = await self._session.execute(
            select(self._entity_class).where(
                self._entity_class.classroom_id == classroom_id
            )
        )
        return list(result.scalars().all())

    async def get_for_teacher(self, teacher_id: UUID) -> List[ClassroomSubject]:
        result = await self._session.execute(
            select(self._entity_class).where(
                self._entity_class.teacher_id == teacher_id
            )
        )
        return list(result.scalars().all())

    async def get_by_classroom_and_subject(
        self, classroom_id: UUID, subject_id: int
    ) -> ClassroomSubject | None:
        result = await self._session.execute(
            select(self._entity_class).where(
                (self._entity_class.classroom_id == classroom_id)
                & (self._entity_class.subject_id == subject_id)
            )
        )
        return result.scalars().first()

