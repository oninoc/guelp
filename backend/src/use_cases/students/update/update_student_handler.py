from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .update_student_request import UpdateStudentRequest
from .update_student_response import UpdateStudentResponse


class UpdateStudentHandler(BaseAuthHandler[UpdateStudentRequest, UpdateStudentResponse]):
    async def execute(self, request: UpdateStudentRequest) -> UpdateStudentResponse:
        student_id = UUID(request.student_id)
        student = await self.unit_of_work.student_repository.get_by_id(student_id)
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Update only provided fields
        if request.code is not None:
            student.code = request.code
        if request.names is not None:
            student.names = request.names
        if request.father_last_name is not None:
            student.father_last_name = request.father_last_name
        if request.mother_last_name is not None:
            student.mother_last_name = request.mother_last_name
        if request.phone is not None:
            student.phone = request.phone
        if request.address is not None:
            student.address = request.address
        if request.email is not None:
            student.email = request.email
        if request.birth_date is not None:
            student.birth_date = request.birth_date
        if request.gender is not None:
            student.gender = request.gender
        if request.document_type is not None:
            student.document_type = request.document_type
        if request.document_number is not None:
            student.document_number = request.document_number
        if request.responsible_name is not None:
            student.responsible_name = request.responsible_name
        if request.responsible_phone is not None:
            student.responsible_phone = request.responsible_phone
        if request.responsible_email is not None:
            student.responsible_email = request.responsible_email
        if request.responsible_address is not None:
            student.responsible_address = request.responsible_address

        updated = await self.unit_of_work.student_repository.update(student)
        
        return UpdateStudentResponse(
            id=str(updated.id),
            code=updated.code,
            names=updated.names,
            father_last_name=updated.father_last_name,
            mother_last_name=updated.mother_last_name,
            full_name=updated.full_name,
            email=updated.email,
            phone=updated.phone,
        )

