from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from .base.base_int_model import BaseIntModel

if TYPE_CHECKING:
    from .classroom_subject_student import ClassroomSubjectStudent
    from .teachers import Teacher


class Qualification(BaseIntModel, table=True):
    classroom_subject_student_id: Optional[int] = Field(
        default=None, foreign_key="classroom_subject_student.id"
    )
    teacher_id: Optional[UUID] = Field(
        default=None, foreign_key="teacher.id"
    )
    description: Optional[str] = None

    classroom_subject_student: Optional["ClassroomSubjectStudent"] = Relationship(
        back_populates="qualifications"
    )
    teacher: Optional["Teacher"] = Relationship(back_populates="qualifications")
