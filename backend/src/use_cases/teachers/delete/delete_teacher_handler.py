from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .delete_teacher_request import DeleteTeacherRequest
from .delete_teacher_response import DeleteTeacherResponse


class DeleteTeacherHandler(BaseAuthHandler[DeleteTeacherRequest, DeleteTeacherResponse]):
    async def execute(self, request: DeleteTeacherRequest) -> DeleteTeacherResponse:
        teacher_id = UUID(request.teacher_id)
        teacher = await self.unit_of_work.teacher_repository.get_by_id(teacher_id)
        
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        await self.unit_of_work.teacher_repository.delete(teacher_id)
        
        return DeleteTeacherResponse(deleted=True, teacher_id=request.teacher_id)

