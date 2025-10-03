from ...shared.base_auth_handler import BaseAuthHandler
from .create_subject_request import CreateSubjectRequest
from .create_subject_response import CreateSubjectResponse
from ....models.subjects import Subject


class CreateSubjectHandler(BaseAuthHandler[CreateSubjectRequest, CreateSubjectResponse]):
    async def execute(self, request: CreateSubjectRequest) -> CreateSubjectResponse:
        subject = Subject(
            name=request.name,
            description=request.description,
        )

        created = await self.unit_of_work.subject_repository.create(subject)
        return CreateSubjectResponse(
            id=created.id,
            name=created.name,
            description=created.description,
        )
