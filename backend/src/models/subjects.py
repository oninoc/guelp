from typing import TYPE_CHECKING, List
from sqlmodel import Relationship

from .base.base_int_model import BaseIntModel

if TYPE_CHECKING:
    from .classroom_subject import ClassroomSubject
    from .classes import Classes
    from .teachers import Teacher


class Subject(BaseIntModel, table=True):
    name: str
    description: str

    classroom_subjects: List["ClassroomSubject"] = Relationship(
        back_populates="subject"
    )
    classes: List["Classes"] = Relationship(back_populates="subject")

    @property
    def teachers(self) -> List["Teacher"]:
        teachers: List["Teacher"] = []
        for classroom_subject in self.classroom_subjects:
            if classroom_subject.teacher and classroom_subject.teacher not in teachers:
                teachers.append(classroom_subject.teacher)
            if (
                classroom_subject.substitute_teacher
                and classroom_subject.substitute_teacher not in teachers
            ):
                teachers.append(classroom_subject.substitute_teacher)
        return teachers