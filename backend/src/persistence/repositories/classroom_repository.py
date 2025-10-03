from typing import List
from uuid import UUID

from sqlmodel import select

from ...models.classrooms import Classroom
from .base_repository import BaseRepository


class ClassroomRepository(BaseRepository[Classroom]):
    _entity_class = Classroom

    async def get_for_tutor(self, tutor_id: UUID) -> List[Classroom]:
        result = await self._session.execute(
            select(self._entity_class).where(self._entity_class.tutor_id == tutor_id)
        )
        return list(result.scalars().all())