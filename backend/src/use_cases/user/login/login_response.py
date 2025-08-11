from ...shared.base_data_transfer import BaseDataTransfer


class LoginResponse(BaseDataTransfer):
    access_token: str
    refresh_token: str
    expires_at: int
