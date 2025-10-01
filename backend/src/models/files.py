from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship

from .base.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .classes import Classes


class FileType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    PDF = "PDF"
    WORD = "WORD"
    EXCEL = "EXCEL"
    POWERPOINT = "POWERPOINT"
    OTHER = "OTHER"


class Files(BaseUUIDModel, table=True):
    name: str
    description: Optional[str] = None
    size: Optional[int] = None
    extension: Optional[str] = None
    type: FileType
    path: Optional[str] = None
    class_id: Optional[int] = Field(default=None, foreign_key="classes.id")

    class_session: Optional["Classes"] = Relationship(
        back_populates="files", sa_relationship_kwargs={"uselist": False}
    )
