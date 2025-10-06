from typing import Optional
from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class ManageStudentQualificationRequest(BaseDataTransfer):
    teacher_id: Optional[UUID] = None
    classroom_subject_student_id: int
    qualification: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    qualification_record_id: Optional[int] = None
    qualification_record_description: Optional[str] = None

