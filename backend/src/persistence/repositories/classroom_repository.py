from typing import List
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select

from ...models.classrooms import Classroom
from ...models.teachers import Teacher
from .base_repository import BaseRepository


class ClassroomRepository(BaseRepository[Classroom]):
    _entity_class = Classroom

    async def get_for_tutor(self, tutor_id: UUID) -> List[Classroom]:
        result = await self._session.execute(
            select(self._entity_class).where(self._entity_class.tutor_id == tutor_id)
        )
        return list(result.scalars().all())

    async def get_all_with_relations(self) -> List[Classroom]:
        query = select(self._entity_class).options(
            selectinload(Classroom.tutor)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())