from ...shared.base_auth_handler import BaseAuthHandler
from .get_student_by_id_request import GetStudentByIdRequest
from .get_student_by_id_response import GetStudentByIdResponse
from ....persistence.repositories.student_repository import StudentRepository
from fastapi import HTTPException


class GetStudentByIdHandler(BaseAuthHandler[GetStudentByIdRequest, GetStudentByIdResponse]):
    async def execute(self, request: GetStudentByIdRequest) -> GetStudentByIdResponse:
        repo = StudentRepository(self.session)
        student = await repo.get_by_id(str(request.id))
        
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
            degree=student.degree,
            level=student.level,
            classroom=student.classroom,
            birth_date=student.birth_date,
            gender=student.gender,
            nationality=student.nationality,
            document_type=student.document_type,
            document_number=student.document_number,
            responsible_name=student.responsible_name,
            responsible_phone=student.responsible_phone,
            responsible_email=student.responsible_email,
            responsible_address=student.responsible_address,
            user_id=student.user_id,
            full_name=student.full_name,
            full_level=student.full_level,
        )
