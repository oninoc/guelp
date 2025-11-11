from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class QualificationRecordSummary(BaseDataTransfer):
    id: int
    grade: Optional[str] = None
    description: Optional[str] = None
    teacher_id: Optional[str] = None
    teacher_full_name: Optional[str] = None
    created_at: Optional[str] = None


class ManageStudentQualificationResponse(BaseDataTransfer):
    classroom_subject_student_id: int
    qualification: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    records: List[QualificationRecordSummary]

