from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class ClassroomSubjectStudentSummary(BaseDataTransfer):
    id: int
    student_id: str
    student_code: str
    student_name: str
    student_email: Optional[str] = None
    status: Optional[str] = None
    is_active: bool
    qualification: Optional[str] = None


class GetAllClassroomSubjectStudentsResponse(BaseDataTransfer):
    students: List[ClassroomSubjectStudentSummary]

