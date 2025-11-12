from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class UpdateStudentResponse(BaseDataTransfer):
    id: str
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None

