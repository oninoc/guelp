from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class CreateTeacherRequest(BaseDataTransfer):
    names: str
    father_last_name: str
    mother_last_name: str
    document_type: str
    document_number: str
    birth_date: str
    gender: str
    nationality: str
    user_id: UUID
