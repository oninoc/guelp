from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

from .base.base_int_model import BaseIntModel

if TYPE_CHECKING:
    from .classrooms import Classroom
    from .subjects import Subject
    from .teachers import Teacher

class ClassroomSubjectRelation(BaseIntModel, table=True):
    name: str
    description: str
    document_path: str = Field(nullable=True)
    video_path: str = Field(nullable=True)
    additional_information: str = Field(nullable=True)
    classroom_id: str = Field(foreign_key="classroom.id")
    subject_id: int = Field(foreign_key="subject.id")
    teacher_id: str = Field(foreign_key="teacher.id")

    classroom: "Classroom" = Relationship(back_populates="subjects")
    subject: "Subject" = Relationship(back_populates="classrooms")
    teacher: "Teacher" = Relationship(back_populates="subjects")