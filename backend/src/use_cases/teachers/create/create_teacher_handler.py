from ...shared.base_auth_handler import BaseAuthHandler
from .create_teacher_request import CreateTeacherRequest
from .create_teacher_response import CreateTeacherResponse
from ....persistence.repositories.teacher_repository import TeacherRepository
from ....models.teachers import Teacher
from fastapi import HTTPException


class CreateTeacherHandler(BaseAuthHandler[CreateTeacherRequest, CreateTeacherResponse]):
    async def execute(self, request: CreateTeacherRequest) -> CreateTeacherResponse:
        repo = TeacherRepository(self.session)
        
        teacher = Teacher(
            code=request.code,
            names=request.names,
            father_last_name=request.father_last_name,
            mother_last_name=request.mother_last_name,
            document_type=request.document_type,
            document_number=request.document_number,
            birth_date=request.birth_date,
            gender=request.gender,
            nationality=request.nationality,
            principal_subject=request.principal_subject,
            secondary_subject=request.secondary_subject,
            start_time=request.start_time,
            end_time=request.end_time,
            user_id=request.user_id,
        )
        
        created = await repo.create(teacher)
        return CreateTeacherResponse(
            id=str(created.id),
            code=created.code,
            names=created.names,
            father_last_name=created.father_last_name,
            mother_last_name=created.mother_last_name,
        )
