from sqlmodel import Field
from datetime import datetime
from uuid import uuid4, UUID
from datetime import UTC
from .base_model import BaseModel


class BaseUUIDModel(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
