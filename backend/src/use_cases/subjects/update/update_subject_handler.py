from fastapi import HTTPException

from ...shared.base_auth_handler import BaseAuthHandler
from .update_subject_request import UpdateSubjectRequest
from .update_subject_response import UpdateSubjectResponse


class UpdateSubjectHandler(BaseAuthHandler[UpdateSubjectRequest, UpdateSubjectResponse]):
    async def execute(self, request: UpdateSubjectRequest) -> UpdateSubjectResponse:
        if request.subject_id is None:
            raise HTTPException(status_code=400, detail="Subject ID is required")
        
        subject = await self.unit_of_work.subject_repository.get_by_id(request.subject_id)
        
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        if request.name is not None:
            subject.name = request.name
        if request.description is not None:
            subject.description = request.description

        updated = await self.unit_of_work.subject_repository.update(subject)
        
        return UpdateSubjectResponse(
            id=updated.id,
            name=updated.name,
            description=updated.description,
        )

