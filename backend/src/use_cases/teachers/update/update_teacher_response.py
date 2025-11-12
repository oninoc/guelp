from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class UpdateTeacherResponse(BaseDataTransfer):
    id: str
    names: str
    father_last_name: str
    mother_last_name: str
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    user_id: str

