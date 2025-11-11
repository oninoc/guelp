from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class TeacherClassroomSubject(BaseDataTransfer):
    classroom_subject_id: int
    subject_id: int
    subject_name: str
    is_substitute: bool
    is_active: bool
    teacher_id: Optional[str] = None
    teacher_name: Optional[str] = None


class TeacherClassroomSummary(BaseDataTransfer):
    classroom_id: str
    description: str
    level: str
    degree: str
    is_tutor: bool
    subjects: List[TeacherClassroomSubject]


class GetTeacherClassroomsResponse(BaseDataTransfer):
    classrooms: List[TeacherClassroomSummary]

