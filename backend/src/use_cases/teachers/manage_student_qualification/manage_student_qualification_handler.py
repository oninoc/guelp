from datetime import datetime
from fastapi import HTTPException

from ...shared.base_auth_handler import BaseAuthHandler
from ....models.qualifications import Qualification
from .manage_student_qualification_request import (
    ManageStudentQualificationRequest,
)
from .manage_student_qualification_response import (
    ManageStudentQualificationResponse,
    QualificationRecordSummary,
)

GRADE_TO_SCORE = {
    "AD": 20,
    "A": 17,
    "B": 14,
    "C": 10,
    "D": 5,
}
GRADE_ORDER = ["AD", "A", "B", "C", "D"]


def normalize_grade(raw: str | None) -> str | None:
    if raw is None:
        return None
    value = raw.strip().upper()
    return value if value in GRADE_TO_SCORE else None


class ManageStudentQualificationHandler(
    BaseAuthHandler[
        ManageStudentQualificationRequest, ManageStudentQualificationResponse
    ]
):
    async def execute(
        self, request: ManageStudentQualificationRequest
    ) -> ManageStudentQualificationResponse:
        enrollment = (
            await self.unit_of_work.classroom_subject_student_repository.get_by_id_with_relations(
                request.classroom_subject_student_id
            )
        )

        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        relation = enrollment.classroom_subject
        if not relation or not relation.classroom:
            raise HTTPException(
                status_code=404, detail="Classroom subject relation not found"
            )

        existing_grade = normalize_grade(enrollment.qualification)

        authorized_teacher_ids = {
            relation.teacher_id,
            relation.substitute_teacher_id,
        }
        if request.teacher_id not in authorized_teacher_ids:
            raise HTTPException(status_code=403, detail="Teacher not authorized")

        updated = False
        grade_value = None
        if request.qualification is not None:
            grade = normalize_grade(request.qualification)
            if grade is None:
                raise HTTPException(status_code=400, detail="Invalid qualification value")
            enrollment.qualification = grade
            grade_value = grade
            updated = True
        record_description = request.qualification_record_description
        if record_description is None and request.description is not None:
            stripped_description = request.description.strip()
            record_description = stripped_description or None

        if request.status is not None:
            enrollment.status = request.status
            updated = True
        if request.is_active is not None:
            enrollment.is_active = request.is_active
            updated = True

        if updated:
            await self.unit_of_work.classroom_subject_student_repository.update(
                enrollment
            )

        should_create_record = grade_value is not None

        if should_create_record:
            if request.qualification_record_id is not None:
                record = await self.unit_of_work.qualification_repository.get_by_id(
                    request.qualification_record_id
                )
                if not record or record.classroom_subject_student_id != enrollment.id:
                    raise HTTPException(
                        status_code=404, detail="Qualification record not found"
                    )
                if record_description is not None:
                    record.description = record_description
                record.teacher_id = request.teacher_id
                if grade_value is not None:
                    record.grade = grade_value
                await self.unit_of_work.qualification_repository.update(record)
            else:
                record = Qualification(
                    classroom_subject_student_id=enrollment.id,
                    teacher_id=request.teacher_id,
                    description=record_description,
                    grade=grade_value,
                )
                await self.unit_of_work.qualification_repository.create(record)

            # refresh enrollment to include latest records
            enrollment = (
                await self.unit_of_work.classroom_subject_student_repository.get_by_id_with_relations(
                    enrollment.id
                )
            )

        records = []
        for record in enrollment.qualifications:
            grade_letter = normalize_grade(record.grade)
            records.append(
                QualificationRecordSummary(
                    id=record.id,
                    grade=grade_letter,
                    description=record.description,
                    teacher_id=str(record.teacher_id) if record.teacher_id else None,
                    teacher_full_name=(
                        f"{record.teacher.names} {record.teacher.father_last_name} {record.teacher.mother_last_name}".strip()
                        if record.teacher
                        else None
                    ),
                    created_at=record.created_at.isoformat()
                    if isinstance(record.created_at, datetime)
                    else None,
                )
            )

        return ManageStudentQualificationResponse(
            classroom_subject_student_id=enrollment.id,
            qualification=enrollment.qualification,
            status=enrollment.status,
            description=None,
            is_active=enrollment.is_active,
            records=records,
        )

