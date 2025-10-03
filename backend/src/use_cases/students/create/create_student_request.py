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
    nationality: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    responsible_name: Optional[str] = None
    responsible_phone: Optional[str] = None
    responsible_email: Optional[str] = None
    responsible_address: Optional[str] = None
    user_id: str
