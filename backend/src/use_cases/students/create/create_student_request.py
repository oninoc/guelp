from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class CreateStudentRequest(BaseDataTransfer):
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    document_type: Optional[str] = "DNI"  # Default to DNI
    document_number: Optional[str] = None
    responsible_name: Optional[str] = None
    responsible_phone: Optional[str] = None
    responsible_email: Optional[str] = None
    responsible_address: Optional[str] = None
    # User creation fields (auto-create user if provided)
    user_email: Optional[str] = None
    user_password: Optional[str] = None
    user_id: Optional[str] = None  # Optional: if not provided, user will be auto-created
