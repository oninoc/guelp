from typing import Optional
from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class CreateClassroomSubjectStudentRequest(BaseDataTransfer):
    classroom_subject_id: int
    student_id: str
    status: Optional[str] = "enrolled"
    is_active: bool = True

