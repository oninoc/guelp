from ...shared.base_data_transfer import BaseDataTransfer


class CreateUserResponse(BaseDataTransfer):
    id: str
    email: str


