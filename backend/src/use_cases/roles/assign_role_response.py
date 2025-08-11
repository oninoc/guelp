from ..shared.base_data_transfer import BaseDataTransfer


class AssignRoleResponse(BaseDataTransfer):
    user_id: str
    role_id: int
    role_code: str


