from ...shared.base_data_transfer import BaseDataTransfer
from uuid import UUID


class GetUserByIdRequest(BaseDataTransfer):
    id: UUID


