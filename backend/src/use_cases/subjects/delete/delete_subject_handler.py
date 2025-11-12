from fastapi import HTTPException

from ...shared.base_auth_handler import BaseAuthHandler
from .delete_subject_request import DeleteSubjectRequest
from .delete_subject_response import DeleteSubjectResponse


class DeleteSubjectHandler(BaseAuthHandler[DeleteSubjectRequest, DeleteSubjectResponse]):
    async def execute(self, request: DeleteSubjectRequest) -> DeleteSubjectResponse:
        subject = await self.unit_of_work.subject_repository.get_by_id(request.subject_id)
        
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        await self.unit_of_work.subject_repository.delete(request.subject_id)
        
        return DeleteSubjectResponse(deleted=True, subject_id=request.subject_id)

