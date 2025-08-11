from sqlmodel import Field
from datetime import datetime
from datetime import UTC
from .base_model import BaseModel


class BaseIntModel(BaseModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
