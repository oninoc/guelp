from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class UpdateTeacherRequest(BaseDataTransfer):
    teacher_id: str
    names: Optional[str] = None
    father_last_name: Optional[str] = None
    mother_last_name: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None

