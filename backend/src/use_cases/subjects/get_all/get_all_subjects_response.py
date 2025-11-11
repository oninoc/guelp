from typing import List

from ...shared.base_data_transfer import BaseDataTransfer


class SubjectSummary(BaseDataTransfer):
    id: int
    name: str
    description: str


class GetAllSubjectsResponse(BaseDataTransfer):
    subjects: List[SubjectSummary]


