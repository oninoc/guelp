from ...shared.base_auth_handler import BaseAuthHandler
from .get_student_subjects_request import GetStudentSubjectsRequest
from .get_student_subjects_response import (
    GetStudentSubjectsResponse,
    StudentSubjectSummary,
)


class GetStudentSubjectsHandler(
    BaseAuthHandler[GetStudentSubjectsRequest, GetStudentSubjectsResponse]
):
    async def execute(
        self, request: GetStudentSubjectsRequest
    ) -> GetStudentSubjectsResponse:
        enrollments = await (
            self.unit_of_work.classroom_subject_student_repository.get_for_student(
                request.student_id,
                with_relations=True,
                only_active=not request.include_inactive,
            )
        )

        subjects = []
        for enrollment in enrollments:
            classroom_subject = enrollment.classroom_subject
            subject = classroom_subject.subject if classroom_subject else None
            teacher = classroom_subject.teacher if classroom_subject else None
            classroom = classroom_subject.classroom if classroom_subject else None

            subjects.append(
                StudentSubjectSummary(
                    classroom_subject_student_id=enrollment.id,
                    classroom_subject_id=classroom_subject.id if classroom_subject else None,
                    subject_id=subject.id if subject else None,
                    subject_name=subject.name if subject else None,
                    subject_description=subject.description if subject else None,
                    teacher_id=str(teacher.id) if teacher else None,
                    teacher_full_name=(
                        f"{teacher.names} {teacher.father_last_name} {teacher.mother_last_name}".strip()
                        if teacher
                        else None
                    ),
                    classroom_id=str(classroom.id) if classroom else None,
                    classroom_level=classroom.level if classroom else None,
                    classroom_degree=classroom.degree if classroom else None,
                    status=enrollment.status,
                    is_active=enrollment.is_active,
                )
            )

        return GetStudentSubjectsResponse(subjects=subjects)

