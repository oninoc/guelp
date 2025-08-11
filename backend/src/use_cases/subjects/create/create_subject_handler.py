from ...shared.base_auth_handler import BaseAuthHandler
from .create_subject_request import CreateSubjectRequest
from .create_subject_response import CreateSubjectResponse
from ....persistence.repositories.subject_repository import SubjectRepository
from ....models.subjects import Subject
from fastapi import HTTPException


class CreateSubjectHandler(BaseAuthHandler[CreateSubjectRequest, CreateSubjectResponse]):
    async def execute(self, request: CreateSubjectRequest) -> CreateSubjectResponse:
        repo = SubjectRepository(self.session)
        
        subject = Subject(
            name=request.name,
            description=request.description,
        )
        
        created = await repo.create(subject)
        return CreateSubjectResponse(
            id=created.id,
            name=created.name,
            description=created.description,
        )
