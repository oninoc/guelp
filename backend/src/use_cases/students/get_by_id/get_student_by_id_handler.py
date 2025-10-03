from ...shared.base_auth_handler import BaseAuthHandler
from .get_student_by_id_request import GetStudentByIdRequest
from .get_student_by_id_response import GetStudentByIdResponse
from fastapi import HTTPException


class GetStudentByIdHandler(BaseAuthHandler[GetStudentByIdRequest, GetStudentByIdResponse]):
    async def execute(self, request: GetStudentByIdRequest) -> GetStudentByIdResponse:
        student = await self.unit_of_work.student_repository.get_by_id(
            str(request.id)
        )
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return GetStudentByIdResponse(
            id=str(student.id),
            code=student.code,
            names=student.names,
            father_last_name=student.father_last_name,
            mother_last_name=student.mother_last_name,
            phone=student.phone,
            address=student.address,
            email=student.email,
            birth_date=student.birth_date,
            gender=student.gender,
            nationality=student.nationality,
            document_type=student.document_type,
            document_number=student.document_number,
            responsible_name=student.responsible_name,
            responsible_phone=student.responsible_phone,
            responsible_email=student.responsible_email,
            responsible_address=student.responsible_address,
            full_name=student.full_name,
            user_id=str(student.user_id),
        )
