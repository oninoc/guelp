from ...shared.base_auth_handler import BaseAuthHandler
from .create_classroom_request import CreateClassroomRequest
from .create_classroom_response import CreateClassroomResponse
from ....models.classrooms import Classroom


class CreateClassroomHandler(BaseAuthHandler[CreateClassroomRequest, CreateClassroomResponse]):
    async def execute(self, request: CreateClassroomRequest) -> CreateClassroomResponse:
        classroom = Classroom(
            description=request.description,
            level=request.level,
            degree=request.degree,
            start_time=request.start_time,
            end_time=request.end_time,
            tutor_id=request.tutor_id,
        )

        created = await self.unit_of_work.classroom_repository.create(classroom)
        return CreateClassroomResponse(
            id=str(created.id),
            description=created.description,
            level=created.level,
            degree=created.degree,
            start_time=created.start_time,
            end_time=created.end_time,
            tutor_id=str(created.tutor_id) if created.tutor_id else None,
        )
