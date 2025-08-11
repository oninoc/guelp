from ...shared.base_data_transfer import BaseDataTransfer
from uuid import UUID


class GetStudentByIdRequest(BaseDataTransfer):
    id: UUID
