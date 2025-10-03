from ...shared.base_auth_handler import BaseAuthHandler
from .create_student_request import CreateStudentRequest
from .create_student_response import CreateStudentResponse
from ....models.students import Student


class CreateStudentHandler(BaseAuthHandler[CreateStudentRequest, CreateStudentResponse]):
    async def execute(self, request: CreateStudentRequest) -> CreateStudentResponse:
        student = Student(
            code=request.code,
            names=request.names,
            father_last_name=request.father_last_name,
            mother_last_name=request.mother_last_name,
            phone=request.phone,
            address=request.address,
            email=request.email,
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

        created = await self.unit_of_work.student_repository.create(student)
        return CreateStudentResponse(
            id=str(created.id),
            code=created.code,
            names=created.names,
            father_last_name=created.father_last_name,
            mother_last_name=created.mother_last_name,
            full_name=created.full_name,
            email=created.email,
            phone=created.phone,
        )
