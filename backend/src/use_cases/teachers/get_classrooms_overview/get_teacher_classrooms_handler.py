from collections import defaultdict
from typing import Optional

from ...shared.base_auth_handler import BaseAuthHandler
from .get_teacher_classrooms_request import GetTeacherClassroomsRequest
from .get_teacher_classrooms_response import (
    GetTeacherClassroomsResponse,
    TeacherClassroomSubject,
    TeacherClassroomSummary,
)


class GetTeacherClassroomsHandler(
    BaseAuthHandler[
        GetTeacherClassroomsRequest,
        GetTeacherClassroomsResponse,
    ]
):
    async def execute(
        self, request: GetTeacherClassroomsRequest
    ) -> GetTeacherClassroomsResponse:
        classroom_subjects = await self.unit_of_work.classroom_subject_repository.get_for_teacher(
            request.teacher_id,
            include_substitute=True,
            with_relations=True,
            only_active=not request.include_inactive,
        )

        tutor_classrooms = {
            classroom.id
            for classroom in await self.unit_of_work.classroom_repository.get_for_tutor(
                request.teacher_id
            )
        }

        def build_subject_entry(relation) -> Optional[TeacherClassroomSubject]:
            classroom = relation.classroom
            subject = relation.subject
            if not classroom or not subject:
                return None

            teacher_name = None
            if relation.teacher and relation.teacher.names:
                teacher_name = (
                    f"{relation.teacher.names} {relation.teacher.father_last_name or ''}".strip()
                )

            return TeacherClassroomSubject(
                classroom_subject_id=relation.id,
                subject_id=subject.id,
                subject_name=subject.name,
                is_substitute=relation.substitute_teacher_id == request.teacher_id,
                is_active=relation.is_active,
                teacher_id=str(relation.teacher_id) if relation.teacher_id else None,
                teacher_name=teacher_name,
            )

        grouped = defaultdict(list)
        classroom_cache = {}

        for relation in classroom_subjects:
            entry = build_subject_entry(relation)
            if not entry:
                continue
            classroom = relation.classroom
            classroom_cache[classroom.id] = classroom
            grouped[classroom.id].append(entry)

        # Augment with classroom subjects for classrooms where the teacher is a tutor
        for tutor_classroom_id in tutor_classrooms:
            extra_relations = await self.unit_of_work.classroom_subject_repository.get_for_classroom(
                tutor_classroom_id,
                with_relations=True,
                only_active=not request.include_inactive,
            )
            existing_ids = {
                subject.classroom_subject_id for subject in grouped[tutor_classroom_id]
            }
            for relation in extra_relations:
                entry = build_subject_entry(relation)
                if not entry or entry.classroom_subject_id in existing_ids:
                    continue
                classroom_cache[relation.classroom.id] = relation.classroom
                grouped[relation.classroom.id].append(entry)

        classrooms: list[TeacherClassroomSummary] = []
        for classroom_id, subjects in grouped.items():
            classroom = classroom_cache.get(classroom_id)
            if not classroom:
                continue
            classrooms.append(
                TeacherClassroomSummary(
                    classroom_id=str(classroom.id),
                    description=classroom.description,
                    level=classroom.level,
                    degree=classroom.degree,
                    is_tutor=classroom.id in tutor_classrooms,
                    subjects=subjects,
                )
            )

        classrooms.sort(key=lambda item: (item.description, item.level, item.degree))
        return GetTeacherClassroomsResponse(classrooms=classrooms)

