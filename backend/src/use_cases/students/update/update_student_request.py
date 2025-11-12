from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class UpdateStudentRequest(BaseDataTransfer):
    student_id: str
    code: Optional[str] = None
    names: Optional[str] = None
    father_last_name: Optional[str] = None
    mother_last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    responsible_name: Optional[str] = None
    responsible_phone: Optional[str] = None
    responsible_email: Optional[str] = None
    responsible_address: Optional[str] = None

