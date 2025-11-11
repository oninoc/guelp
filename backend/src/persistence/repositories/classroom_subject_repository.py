from typing import List
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select

from ...models.classroom_subject import ClassroomSubject
from ...models.subjects import Subject
from ...models.classrooms import Classroom
from ...models.teachers import Teacher
from ...models.classroom_subject_student import ClassroomSubjectStudent
from ...models.qualifications import Qualification
from ...models.students import Student
from ...models.user import User
from .base_repository import BaseRepository


class ClassroomSubjectRepository(BaseRepository[ClassroomSubject]):
    _entity_class = ClassroomSubject

    def _default_options(self):
        return [
            selectinload(self._entity_class.subject),
            selectinload(self._entity_class.classroom),
            selectinload(self._entity_class.teacher).selectinload(Teacher.user),
            selectinload(self._entity_class.substitute_teacher),
            selectinload(self._entity_class.students).options(
                selectinload(ClassroomSubjectStudent.student)
                .selectinload(Student.user),
                selectinload(ClassroomSubjectStudent.qualifications).options(
                    selectinload(Qualification.teacher)
                ),
            ),
        ]

    async def get_for_classroom(
        self,
        classroom_id: UUID,
        with_relations: bool = False,
        only_active: bool = True,
    ) -> List[ClassroomSubject]:
        query = select(self._entity_class).where(
            self._entity_class.classroom_id == classroom_id
        )
        if only_active:
            query = query.where(self._entity_class.is_active.is_(True))
        if with_relations:
            query = query.options(*self._default_options())
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_for_teacher(
        self,
        teacher_id: UUID,
        include_substitute: bool = True,
        with_relations: bool = False,
        only_active: bool = True,
    ) -> List[ClassroomSubject]:
        condition = self._entity_class.teacher_id == teacher_id
        if include_substitute:
            condition = condition | (
                self._entity_class.substitute_teacher_id == teacher_id
            )
        query = select(self._entity_class).where(condition)
        if only_active:
            query = query.where(self._entity_class.is_active.is_(True))
        if with_relations:
            query = query.options(*self._default_options())
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_classroom_and_subject(
        self,
        classroom_id: UUID,
        subject_id: int,
        with_relations: bool = False,
        only_active: bool = True,
    ) -> ClassroomSubject | None:
        query = select(self._entity_class).where(
            (self._entity_class.classroom_id == classroom_id)
            & (self._entity_class.subject_id == subject_id)
        )
        if only_active:
            query = query.where(self._entity_class.is_active.is_(True))
        if with_relations:
            query = query.options(*self._default_options())
        result = await self._session.execute(query)
        return result.scalars().first()

