from ...shared.base_data_transfer import BaseDataTransfer
from typing import List


class TeacherSummary(BaseDataTransfer):
    id: str
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    principal_subject: str
    secondary_subject: str


class GetAllTeachersResponse(BaseDataTransfer):
    teachers: List[TeacherSummary]
