from ...shared.base_auth_handler import BaseAuthHandler
from .create_student_request import CreateStudentRequest
from .create_student_response import CreateStudentResponse
from ....persistence.repositories.student_repository import StudentRepository
from ....models.students import Student
from fastapi import HTTPException


class CreateStudentHandler(BaseAuthHandler[CreateStudentRequest, CreateStudentResponse]):
    async def execute(self, request: CreateStudentRequest) -> CreateStudentResponse:
        repo = StudentRepository(self.session)
        
        student = Student(
            code=request.code,
            names=request.names,
            father_last_name=request.father_last_name,
            mother_last_name=request.mother_last_name,
            phone=request.phone,
            address=request.address,
            email=request.email,
            degree=request.degree,
            level=request.level,
            classroom=request.classroom,
            birth_date=request.birth_date,
            gender=request.gender,
            nationality=request.nationality,
            document_type=request.document_type,
            document_number=request.document_number,
            responsible_name=request.responsible_name,
            responsible_phone=request.responsible_phone,
            responsible_email=request.responsible_email,
            responsible_address=request.responsible_address,
            user_id=request.user_id,
        )
        
        created = await repo.create(student)
        return CreateStudentResponse(
            id=str(created.id),
            code=created.code,
            names=created.names,
            father_last_name=created.father_last_name,
            mother_last_name=created.mother_last_name,
            full_name=created.full_name,
            degree=created.degree,
            level=created.level,
            full_level=created.full_level,
        )
