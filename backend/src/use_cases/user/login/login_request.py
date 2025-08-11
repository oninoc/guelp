from ...shared.base_data_transfer import BaseDataTransfer


class LoginRequest(BaseDataTransfer):
    email: str
    password: str