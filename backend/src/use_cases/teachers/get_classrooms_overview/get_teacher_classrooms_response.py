from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class TeacherClassroomSubject(BaseDataTransfer):
    classroom_subject_id: int
    subject_id: int
    subject_name: str
    is_substitute: bool


class TeacherClassroomSummary(BaseDataTransfer):
    classroom_id: str
    description: str
    level: str
    degree: str
    is_tutor: bool
    subjects: List[TeacherClassroomSubject]


class GetTeacherClassroomsResponse(BaseDataTransfer):
    classrooms: List[TeacherClassroomSummary]

