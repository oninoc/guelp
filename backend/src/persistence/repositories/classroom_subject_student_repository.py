from typing import List
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select, update

from ...models.classroom_subject import ClassroomSubject
from ...models.classroom_subject_student import ClassroomSubjectStudent
from ...models.qualifications import Qualification
from ...models.students import Student
from ...models.user import User
from .base_repository import BaseRepository


class ClassroomSubjectStudentRepository(
    BaseRepository[ClassroomSubjectStudent]
):
    _entity_class = ClassroomSubjectStudent

    def _with_relations(self):
        return (
            selectinload(self._entity_class.classroom_subject).options(
                selectinload(ClassroomSubject.subject),
                selectinload(ClassroomSubject.teacher),
                selectinload(ClassroomSubject.substitute_teacher),
                selectinload(ClassroomSubject.classroom),
                selectinload(ClassroomSubject.classes),
            ),
            selectinload(self._entity_class.student).selectinload(Student.user),
        )

    async def get_for_student(
        self,
        student_id: UUID,
        with_relations: bool = False,
        only_active: bool = True,
    ) -> List[ClassroomSubjectStudent]:
        query = select(self._entity_class).where(
            self._entity_class.student_id == student_id
        )
        if only_active:
            query = query.where(self._entity_class.is_active.is_(True))
        if with_relations:
            loader_options = list(self._with_relations())
            loader_options.append(
                selectinload(self._entity_class.qualifications).options(
                    selectinload(Qualification.teacher)
                )
            )
            query = query.options(*loader_options)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_for_classroom_subject(
        self,
        classroom_subject_id: int,
        with_relations: bool = False,
        only_active: bool = True,
    ) -> List[ClassroomSubjectStudent]:
        query = select(self._entity_class).where(
            self._entity_class.classroom_subject_id == classroom_subject_id
        )
        if only_active:
            query = query.where(self._entity_class.is_active.is_(True))
        if with_relations:
            loader_options = list(self._with_relations())
            loader_options.append(
                selectinload(self._entity_class.qualifications).options(
                    selectinload(Qualification.teacher)
                )
            )
            query = query.options(*loader_options)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_unique_relation(
        self,
        classroom_subject_id: int,
        student_id: UUID,
        with_relations: bool = False,
        only_active: bool = True,
    ) -> ClassroomSubjectStudent | None:
        query = select(self._entity_class).where(
            (self._entity_class.classroom_subject_id == classroom_subject_id)
            & (self._entity_class.student_id == student_id)
        )
        if only_active:
            query = query.where(self._entity_class.is_active.is_(True))
        if with_relations:
            loader_options = list(self._with_relations())
            loader_options.append(
                selectinload(self._entity_class.qualifications).options(
                    selectinload(Qualification.teacher)
                )
            )
            query = query.options(*loader_options)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def get_by_id_with_relations(
        self, enrollment_id: int
    ) -> ClassroomSubjectStudent | None:
        query = (
            select(self._entity_class)
            .where(self._entity_class.id == enrollment_id)
            .options(
                *self._with_relations(),
                selectinload(self._entity_class.qualifications).options(
                    selectinload(Qualification.teacher)
                ),
            )
        )
        result = await self._session.execute(query)
        return result.scalars().first()

    async def update_final_grade(
        self, enrollment_id: int, qualification: str | None
    ) -> None:
        await self._session.execute(
            update(self._entity_class)
            .where(self._entity_class.id == enrollment_id)
            .values(qualification=qualification)
        )
        await self._session.commit()

