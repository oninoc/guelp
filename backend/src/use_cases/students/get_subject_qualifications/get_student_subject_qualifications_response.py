from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class QualificationRecord(BaseDataTransfer):
    id: Optional[int] = None
    teacher_id: Optional[str] = None
    teacher_full_name: Optional[str] = None
    description: Optional[str] = None


class StudentSubjectQualification(BaseDataTransfer):
    classroom_subject_student_id: int
    classroom_subject_id: Optional[int] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    current_qualification: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    records: List[QualificationRecord]


class GetStudentSubjectQualificationsResponse(BaseDataTransfer):
    subjects: List[StudentSubjectQualification]

