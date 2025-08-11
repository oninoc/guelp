from sqlmodel import SQLModel
from sqlalchemy.orm import declared_attr
from .snake_case import snake_case


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return snake_case(cls.__name__)
