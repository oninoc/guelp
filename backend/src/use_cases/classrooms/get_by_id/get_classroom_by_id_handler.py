from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .get_classroom_by_id_request import GetClassroomByIdRequest
from .get_classroom_by_id_response import GetClassroomByIdResponse


class GetClassroomByIdHandler(BaseAuthHandler[GetClassroomByIdRequest, GetClassroomByIdResponse]):
    async def execute(self, request: GetClassroomByIdRequest) -> GetClassroomByIdResponse:
        classroom_id = UUID(request.id)
        classroom = await self.unit_of_work.classroom_repository.get_by_id(classroom_id)
        
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")
        
        return GetClassroomByIdResponse(
            id=str(classroom.id),
            description=classroom.description,
            level=classroom.level,
            degree=classroom.degree,
            start_time=classroom.start_time,
            end_time=classroom.end_time,
            tutor_id=str(classroom.tutor_id) if classroom.tutor_id else None,
        )

