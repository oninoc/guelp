from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class ClassroomSubjectSummary(BaseDataTransfer):
    id: int
    classroom_id: str
    classroom_description: str
    subject_id: int
    subject_name: str
    teacher_id: Optional[str] = None
    teacher_name: Optional[str] = None
    substitute_teacher_id: Optional[str] = None
    substitute_teacher_name: Optional[str] = None
    is_active: bool
    student_count: int


class GetAllClassroomSubjectsResponse(BaseDataTransfer):
    classroom_subjects: List[ClassroomSubjectSummary]

