from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class CreateClassroomSubjectResponse(BaseDataTransfer):
    id: int
    classroom_id: str
    subject_id: int
    teacher_id: Optional[str] = None
    substitute_teacher_id: Optional[str] = None
    is_active: bool

