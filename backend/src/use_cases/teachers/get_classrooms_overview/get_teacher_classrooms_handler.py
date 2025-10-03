from collections import defaultdict

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
            request.teacher_id, include_substitute=True, with_relations=True
        )
        tutor_classrooms = {
            classroom.id
            for classroom in await self.unit_of_work.classroom_repository.get_for_tutor(
                request.teacher_id
            )
        }

        grouped = defaultdict(list)
        for relation in classroom_subjects:
            classroom = relation.classroom
            subject = relation.subject
            if not classroom or not subject:
                continue

            grouped[classroom.id].append(
                TeacherClassroomSubject(
                    classroom_subject_id=relation.id,
                    subject_id=subject.id,
                    subject_name=subject.name,
                    is_substitute=relation.substitute_teacher_id == request.teacher_id,
                )
            )

        classrooms = []
        for classroom_id, subjects in grouped.items():
            classroom = next(
                (rel.classroom for rel in classroom_subjects if rel.classroom and rel.classroom.id == classroom_id),
                None,
            )
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

        # Ensure classrooms where teacher is tutor but not currently teaching a subject are included
        for classroom in await self.unit_of_work.classroom_repository.get_for_tutor(
            request.teacher_id
        ):
            if classroom.id not in grouped:
                classrooms.append(
                    TeacherClassroomSummary(
                        classroom_id=str(classroom.id),
                        description=classroom.description,
                        level=classroom.level,
                        degree=classroom.degree,
                        is_tutor=True,
                        subjects=[],
                    )
                )

        classrooms.sort(key=lambda item: item.description)
        return GetTeacherClassroomsResponse(classrooms=classrooms)

