from fastapi import HTTPException

from ...shared.base_auth_handler import BaseAuthHandler
from .get_subject_by_id_request import GetSubjectByIdRequest
from .get_subject_by_id_response import GetSubjectByIdResponse


class GetSubjectByIdHandler(BaseAuthHandler[GetSubjectByIdRequest, GetSubjectByIdResponse]):
    async def execute(self, request: GetSubjectByIdRequest) -> GetSubjectByIdResponse:
        subject = await self.unit_of_work.subject_repository.get_by_id(request.id)
        
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        
        return GetSubjectByIdResponse(
            id=subject.id,
            name=subject.name,
            description=subject.description,
        )

