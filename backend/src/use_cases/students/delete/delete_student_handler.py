from fastapi import HTTPException
from uuid import UUID

from ...shared.base_auth_handler import BaseAuthHandler
from .delete_student_request import DeleteStudentRequest
from .delete_student_response import DeleteStudentResponse


class DeleteStudentHandler(BaseAuthHandler[DeleteStudentRequest, DeleteStudentResponse]):
    async def execute(self, request: DeleteStudentRequest) -> DeleteStudentResponse:
        student_id = UUID(request.student_id)
        student = await self.unit_of_work.student_repository.get_by_id(student_id)
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        await self.unit_of_work.student_repository.delete(student_id)
        
        return DeleteStudentResponse(deleted=True, student_id=request.student_id)

