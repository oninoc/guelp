from typing import Optional
from sqlmodel import Field
from .base_model import BaseModel


class BaseIntModelWithoutDate(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
