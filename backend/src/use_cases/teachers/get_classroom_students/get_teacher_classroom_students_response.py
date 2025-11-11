from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class TeacherClassroomStudentSubject(BaseDataTransfer):
    classroom_subject_student_id: int
    classroom_subject_id: int
    subject_id: int
    subject_name: str
    teacher_id: Optional[str] = None
    teacher_name: Optional[str] = None
    qualification: Optional[str] = None
    status: Optional[str] = None
    is_active: bool
    can_manage: bool
    average_grade: Optional[str] = None
    average_score: Optional[float] = None
    history: List["TeacherQualificationRecord"]


class TeacherClassroomStudentSummary(BaseDataTransfer):
    student_id: str
    student_code: str
    full_name: str
    email: Optional[str]
    average_qualification: Optional[float]
    subjects: List[TeacherClassroomStudentSubject]


class GetTeacherClassroomStudentsResponse(BaseDataTransfer):
    students: List[TeacherClassroomStudentSummary]


class TeacherQualificationRecord(BaseDataTransfer):
    id: Optional[int]
    grade: Optional[str]
    description: Optional[str]
    teacher_id: Optional[str]
    teacher_full_name: Optional[str]
    created_at: Optional[str]

