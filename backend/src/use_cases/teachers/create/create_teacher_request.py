from typing import Optional
from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class CreateTeacherRequest(BaseDataTransfer):
    names: str
    father_last_name: str
    mother_last_name: str
    document_type: str = "DNI"  # Default to DNI
    document_number: str
    birth_date: str
    gender: str
    # User creation fields (auto-create user if provided)
    user_email: Optional[str] = None
    user_password: Optional[str] = None
    user_id: Optional[UUID] = None  # Optional: if not provided, user will be auto-created
