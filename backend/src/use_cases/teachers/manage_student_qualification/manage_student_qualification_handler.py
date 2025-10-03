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

        authorized_teacher_ids = {
            relation.teacher_id,
            relation.substitute_teacher_id,
        }
        if request.teacher_id not in authorized_teacher_ids:
            raise HTTPException(status_code=403, detail="Teacher not authorized")

        updated = False
        if request.qualification is not None:
            enrollment.qualification = request.qualification
            updated = True
        if request.status is not None:
            enrollment.status = request.status
            updated = True
        if request.description is not None:
            enrollment.description = request.description
            updated = True

        if updated:
            await self.unit_of_work.classroom_subject_student_repository.update(
                enrollment
            )

        if request.qualification_record_description is not None:
            if request.qualification_record_id is not None:
                record = await self.unit_of_work.qualification_repository.get_by_id(
                    request.qualification_record_id
                )
                if not record or record.classroom_subject_student_id != enrollment.id:
                    raise HTTPException(
                        status_code=404, detail="Qualification record not found"
                    )
                record.description = request.qualification_record_description
                record.teacher_id = request.teacher_id
                await self.unit_of_work.qualification_repository.update(record)
            else:
                record = Qualification(
                    classroom_subject_student_id=enrollment.id,
                    teacher_id=request.teacher_id,
                    description=request.qualification_record_description,
                )
                await self.unit_of_work.qualification_repository.create(record)

            # refresh enrollment to include latest records
            enrollment = (
                await self.unit_of_work.classroom_subject_student_repository.get_by_id_with_relations(
                    enrollment.id
                )
            )

        records = [
            QualificationRecordSummary(
                id=record.id,
                description=record.description,
                teacher_id=str(record.teacher_id) if record.teacher_id else None,
                teacher_full_name=(
                    f"{record.teacher.names} {record.teacher.father_last_name} {record.teacher.mother_last_name}".strip()
                    if record.teacher
                    else None
                ),
            )
            for record in enrollment.qualifications
        ]

        return ManageStudentQualificationResponse(
            classroom_subject_student_id=enrollment.id,
            qualification=enrollment.qualification,
            status=enrollment.status,
            description=enrollment.description,
            records=records,
        )

