from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class CreateClassroomSubjectStudentResponse(BaseDataTransfer):
    id: int
    classroom_subject_id: int
    student_id: str
    status: Optional[str] = None
    is_active: bool

