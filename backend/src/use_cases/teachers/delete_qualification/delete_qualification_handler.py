from datetime import datetime

from fastapi import HTTPException

from ...shared.base_auth_handler import BaseAuthHandler
from .delete_qualification_request import DeleteQualificationRequest
from .delete_qualification_response import DeleteQualificationResponse


class DeleteQualificationHandler(
    BaseAuthHandler[DeleteQualificationRequest, DeleteQualificationResponse]
):
    async def execute(
        self, request: DeleteQualificationRequest
    ) -> DeleteQualificationResponse:
        record = await self.unit_of_work.qualification_repository.get_by_id(
            request.qualification_id
        )
        if record is None:
            raise HTTPException(status_code=404, detail="Qualification record not found")

        enrollment_id = record.classroom_subject_student_id
        if enrollment_id is None:
            raise HTTPException(status_code=400, detail="Record is not linked to enrollment")

        enrollment = await self.unit_of_work.classroom_subject_student_repository.get_by_id_with_relations(
            enrollment_id
        )
        if enrollment is None:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        relation = enrollment.classroom_subject
        authorized_teacher_ids = {
            relation.teacher_id if relation else None,
            relation.substitute_teacher_id if relation else None,
        }
        if request.teacher_id not in authorized_teacher_ids:
            raise HTTPException(status_code=403, detail="Teacher not authorized")

        await self.unit_of_work.qualification_repository.delete(record.id)

        refreshed = (
            await self.unit_of_work.classroom_subject_student_repository.get_by_id_with_relations(
                enrollment_id
            )
        )
        if not refreshed:
            return DeleteQualificationResponse(deleted=True)

        remaining = [
            q for q in refreshed.qualifications if q.id != record.id
        ]
        if remaining:
            remaining.sort(key=lambda item: item.created_at or datetime.min)
            latest_grade = remaining[-1].grade
        else:
            latest_grade = None

        await self.unit_of_work.classroom_subject_student_repository.update_final_grade(
            enrollment_id, latest_grade
        )

        return DeleteQualificationResponse(deleted=True)

