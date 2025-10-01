from typing import TYPE_CHECKING, List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from .base.base_int_model import BaseIntModel

if TYPE_CHECKING:
    from .classroom_subject import ClassroomSubject
    from .students import Student
    from .qualifications import Qualification
    
class ClassroomSubjectStudent(BaseIntModel, table=True):
    classroom_subject_id: int = Field(foreign_key="classroom_subject.id")
    student_id: UUID = Field(foreign_key="student.id")
    qualification: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

    classroom_subject: "ClassroomSubject" = Relationship(back_populates="students")
    student: "Student" = Relationship(back_populates="classroom_subject_students")
    qualifications: List["Qualification"] = Relationship(
        back_populates="classroom_subject_student"
    )