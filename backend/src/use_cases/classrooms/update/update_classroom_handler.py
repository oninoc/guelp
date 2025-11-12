from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .update_classroom_request import UpdateClassroomRequest
from .update_classroom_response import UpdateClassroomResponse


class UpdateClassroomHandler(BaseAuthHandler[UpdateClassroomRequest, UpdateClassroomResponse]):
    async def execute(self, request: UpdateClassroomRequest) -> UpdateClassroomResponse:
        if request.classroom_id is None:
            raise HTTPException(status_code=400, detail="Classroom ID is required")
        
        classroom_id = UUID(request.classroom_id)
        classroom = await self.unit_of_work.classroom_repository.get_by_id(classroom_id)
        
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")

        if request.description is not None:
            classroom.description = request.description
        if request.level is not None:
            classroom.level = request.level
        if request.degree is not None:
            classroom.degree = request.degree
        if request.start_time is not None:
            classroom.start_time = request.start_time
        if request.end_time is not None:
            classroom.end_time = request.end_time
        if request.tutor_id is not None:
            classroom.tutor_id = request.tutor_id

        updated = await self.unit_of_work.classroom_repository.update(classroom)
        
        return UpdateClassroomResponse(
            id=str(updated.id),
            description=updated.description,
            level=updated.level,
            degree=updated.degree,
            start_time=updated.start_time,
            end_time=updated.end_time,
            tutor_id=str(updated.tutor_id) if updated.tutor_id else None,
        )

