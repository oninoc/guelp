from ...shared.base_auth_handler import BaseAuthHandler
from .create_classroom_request import CreateClassroomRequest
from .create_classroom_response import CreateClassroomResponse
from ....persistence.repositories.classroom_repository import ClassroomRepository
from ....models.classrooms import Classroom
from fastapi import HTTPException


class CreateClassroomHandler(BaseAuthHandler[CreateClassroomRequest, CreateClassroomResponse]):
    async def execute(self, request: CreateClassroomRequest) -> CreateClassroomResponse:
        repo = ClassroomRepository(self.session)
        
        classroom = Classroom(
            name=request.name,
            description=request.description,
            level=request.level,
            degree=request.degree,
            start_time=request.start_time,
            end_time=request.end_time,
            tutor_id=request.tutor_id,
        )
        
        created = await repo.create(classroom)
        return CreateClassroomResponse(
            id=str(created.id),
            name=created.name,
            description=created.description,
            level=created.level,
            degree=created.degree,
        )
