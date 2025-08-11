from ...shared.base_data_transfer import BaseDataTransfer


class CreateUserRequest(BaseDataTransfer):
    name: str
    last_name: str
    phone: str
    address: str
    email: str
    password: str


