from typing import List
from uuid import UUID

from sqlmodel import select

from ...models.classroom_subject_student import ClassroomSubjectStudent
from .base_repository import BaseRepository


class ClassroomSubjectStudentRepository(
    BaseRepository[ClassroomSubjectStudent]
):
    _entity_class = ClassroomSubjectStudent

    async def get_for_student(
        self, student_id: UUID
    ) -> List[ClassroomSubjectStudent]:
        result = await self._session.execute(
            select(self._entity_class).where(
                self._entity_class.student_id == student_id
            )
        )
        return list(result.scalars().all())

    async def get_for_classroom_subject(
        self, classroom_subject_id: int
    ) -> List[ClassroomSubjectStudent]:
        result = await self._session.execute(
            select(self._entity_class).where(
                self._entity_class.classroom_subject_id == classroom_subject_id
            )
        )
        return list(result.scalars().all())

    async def get_by_unique_relation(
        self, classroom_subject_id: int, student_id: UUID
    ) -> ClassroomSubjectStudent | None:
        result = await self._session.execute(
            select(self._entity_class).where(
                (self._entity_class.classroom_subject_id == classroom_subject_id)
                & (self._entity_class.student_id == student_id)
            )
        )
        return result.scalars().first()

