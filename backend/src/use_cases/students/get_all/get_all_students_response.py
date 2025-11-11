from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class StudentSummary(BaseDataTransfer):
    id: str
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    email: Optional[str]


class GetAllStudentsResponse(BaseDataTransfer):
    students: List[StudentSummary]


