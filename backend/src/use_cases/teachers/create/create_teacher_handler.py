from ...shared.base_auth_handler import BaseAuthHandler
from .create_teacher_request import CreateTeacherRequest
from .create_teacher_response import CreateTeacherResponse
from ....models.teachers import Teacher


class CreateTeacherHandler(BaseAuthHandler[CreateTeacherRequest, CreateTeacherResponse]):
    async def execute(self, request: CreateTeacherRequest) -> CreateTeacherResponse:
        teacher = Teacher(
            names=request.names,
            father_last_name=request.father_last_name,
            mother_last_name=request.mother_last_name,
            document_type=request.document_type,
            document_number=request.document_number,
            birth_date=request.birth_date,
            gender=request.gender,
            nationality=request.nationality,
            user_id=request.user_id,
        )
        
        created = await self.unit_of_work.teacher_repository.create(teacher)
        return CreateTeacherResponse(
            id=str(created.id),
            names=created.names,
            father_last_name=created.father_last_name,
            mother_last_name=created.mother_last_name,
            document_type=created.document_type,
            document_number=created.document_number,
            birth_date=created.birth_date,
            gender=created.gender,
            nationality=created.nationality,
            user_id=str(created.user_id),
        )
