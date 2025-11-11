from datetime import datetime

from ...shared.base_handler import BaseHandler
from .get_student_subject_qualifications_request import (
    GetStudentSubjectQualificationsRequest,
)
from .get_student_subject_qualifications_response import (
    GetStudentSubjectQualificationsResponse,
    QualificationRecord,
    StudentSubjectQualification,
)


class GetStudentSubjectQualificationsHandler(
    BaseHandler[
        GetStudentSubjectQualificationsRequest,
        GetStudentSubjectQualificationsResponse,
    ]
):
    async def execute(
        self, request: GetStudentSubjectQualificationsRequest
    ) -> GetStudentSubjectQualificationsResponse:
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

            records = []
            for record in enrollment.qualifications:
                teacher = record.teacher
                records.append(
                    QualificationRecord(
                        id=record.id,
                        grade=record.grade,
                        teacher_id=str(teacher.id) if teacher else None,
                        teacher_full_name=(
                            f"{teacher.names} {teacher.father_last_name} {teacher.mother_last_name}".strip()
                            if teacher
                            else None
                        ),
                        description=record.description,
                        created_at=record.created_at.isoformat()
                        if isinstance(record.created_at, datetime)
                        else None,
                    )
                )

            subjects.append(
                StudentSubjectQualification(
                    classroom_subject_student_id=enrollment.id,
                    classroom_subject_id=classroom_subject.id if classroom_subject else None,
                    subject_id=subject.id if subject else None,
                    subject_name=subject.name if subject else None,
                    current_qualification=enrollment.qualification,
                    status=enrollment.status,
                    description=enrollment.description,
                    is_active=enrollment.is_active,
                    records=records,
                )
            )

        return GetStudentSubjectQualificationsResponse(subjects=subjects)

