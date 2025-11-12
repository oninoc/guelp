from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .update_teacher_request import UpdateTeacherRequest
from .update_teacher_response import UpdateTeacherResponse


class UpdateTeacherHandler(BaseAuthHandler[UpdateTeacherRequest, UpdateTeacherResponse]):
    async def execute(self, request: UpdateTeacherRequest) -> UpdateTeacherResponse:
        teacher_id = UUID(request.teacher_id)
        teacher = await self.unit_of_work.teacher_repository.get_by_id(teacher_id)
        
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        if request.names is not None:
            teacher.names = request.names
        if request.father_last_name is not None:
            teacher.father_last_name = request.father_last_name
        if request.mother_last_name is not None:
            teacher.mother_last_name = request.mother_last_name
        if request.document_type is not None:
            teacher.document_type = request.document_type
        if request.document_number is not None:
            teacher.document_number = request.document_number
        if request.birth_date is not None:
            teacher.birth_date = request.birth_date
        if request.gender is not None:
            teacher.gender = request.gender

        updated = await self.unit_of_work.teacher_repository.update(teacher)
        
        return UpdateTeacherResponse(
            id=str(updated.id),
            names=updated.names,
            father_last_name=updated.father_last_name,
            mother_last_name=updated.mother_last_name,
            document_type=updated.document_type,
            document_number=updated.document_number,
            birth_date=updated.birth_date,
            gender=updated.gender,
            user_id=str(updated.user_id),
        )

