from typing import Optional
from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class CreateClassroomSubjectRequest(BaseDataTransfer):
    classroom_id: str
    subject_id: int
    teacher_id: Optional[str] = None
    substitute_teacher_id: Optional[str] = None
    is_active: bool = True

