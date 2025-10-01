from typing import TYPE_CHECKING, List, Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from .base.base_int_model import BaseIntModel

if TYPE_CHECKING:
    from .classrooms import Classroom
    from .subjects import Subject
    from .teachers import Teacher
    from .classroom_subject_student import ClassroomSubjectStudent
    from .classes import Classes
        
class ClassroomSubject(BaseIntModel, table=True):
    classroom_id: UUID = Field(foreign_key="classroom.id")
    subject_id: int = Field(foreign_key="subject.id")
    teacher_id: Optional[UUID] = Field(default=None, foreign_key="teacher.id")
    substitute_teacher_id: Optional[UUID] = Field(
        default=None, foreign_key="teacher.id"
    )

    classroom: "Classroom" = Relationship(back_populates="classroom_subjects")
    subject: "Subject" = Relationship(back_populates="classroom_subjects")
    teacher: Optional["Teacher"] = Relationship(
        back_populates="classroom_subjects",
        sa_relationship_kwargs={"foreign_keys": "ClassroomSubject.teacher_id"},
    )
    substitute_teacher: Optional["Teacher"] = Relationship(
        back_populates="substitute_classroom_subjects",
        sa_relationship_kwargs={
            "foreign_keys": "ClassroomSubject.substitute_teacher_id"
        },
    )
    students: List["ClassroomSubjectStudent"] = Relationship(
        back_populates="classroom_subject"
    )
    classes: List["Classes"] = Relationship(back_populates="classroom_subject")