from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

from .base.base_int_model import BaseIntModel

if TYPE_CHECKING:
    from .classrooms import Classroom
    from .subjects import Subject
    from .teachers import Teacher
    from .students import Student


class Qualification(BaseIntModel, table=True):
    classroom_id: str = Field(foreign_key="classroom.id")
    subject_id: int = Field(foreign_key="subject.id")
    teacher_id: str = Field(foreign_key="teacher.id")
    student_id: str = Field(foreign_key="student.id")
    score: str
    date: str
    description: str

    classroom: "Classroom" = Relationship(back_populates="qualifications")
    subject: "Subject" = Relationship(back_populates="qualifications")
    teacher: "Teacher" = Relationship(back_populates="qualifications")
    student: "Student" = Relationship(back_populates="qualifications")