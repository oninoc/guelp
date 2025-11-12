from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .delete_classroom_request import DeleteClassroomRequest
from .delete_classroom_response import DeleteClassroomResponse


class DeleteClassroomHandler(BaseAuthHandler[DeleteClassroomRequest, DeleteClassroomResponse]):
    async def execute(self, request: DeleteClassroomRequest) -> DeleteClassroomResponse:
        classroom_id = UUID(request.classroom_id)
        classroom = await self.unit_of_work.classroom_repository.get_by_id(classroom_id)
        
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")

        await self.unit_of_work.classroom_repository.delete(classroom_id)
        
        return DeleteClassroomResponse(deleted=True, classroom_id=request.classroom_id)

