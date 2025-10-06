from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class StudentSubjectSummary(BaseDataTransfer):
    classroom_subject_student_id: int
    classroom_subject_id: Optional[int] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    subject_description: Optional[str] = None
    teacher_id: Optional[str] = None
    teacher_full_name: Optional[str] = None
    classroom_id: Optional[str] = None
    classroom_level: Optional[str] = None
    classroom_degree: Optional[str] = None
    status: Optional[str] = None
    is_active: bool


class GetStudentSubjectsResponse(BaseDataTransfer):
    subjects: List[StudentSubjectSummary]

