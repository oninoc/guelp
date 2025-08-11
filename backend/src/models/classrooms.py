from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .teachers import Teacher


class Classroom(BaseUUIDModel, table=True):
    name: str
    description: str
    level: str
    degree: str
    start_time: str
    end_time: str
    tutor_id: str = Field(foreign_key="teacher.id")

    tutor: "Teacher" = Relationship(back_populates="classroom")
