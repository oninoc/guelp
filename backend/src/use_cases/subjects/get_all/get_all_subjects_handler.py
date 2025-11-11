from ...shared.base_handler import BaseHandler
from ....persistence.unit_of_work import UnitOfWork
from .get_all_subjects_request import GetAllSubjectsRequest
from .get_all_subjects_response import GetAllSubjectsResponse, SubjectSummary


class GetAllSubjectsHandler(BaseHandler[GetAllSubjectsRequest, GetAllSubjectsResponse]):
    async def execute(self, request: GetAllSubjectsRequest) -> GetAllSubjectsResponse:
        unit_of_work = UnitOfWork(self.session)
        subjects = await unit_of_work.subject_repository.get_all()

        summaries = [
            SubjectSummary(
                id=subject.id,
                name=subject.name,
                description=subject.description,
            )
            for subject in subjects
        ]
        return GetAllSubjectsResponse(subjects=summaries)


