from typing import List

from ...shared.base_data_transfer import BaseDataTransfer


class TeacherSummary(BaseDataTransfer):
    id: str
    names: str
    father_last_name: str
    mother_last_name: str
    document_type: str
    document_number: str


class GetAllTeachersResponse(BaseDataTransfer):
    teachers: List[TeacherSummary]
