from ..shared.base_data_transfer import BaseDataTransfer


class AssignPermissionResponse(BaseDataTransfer):
    role_id: int
    role_code: str
    permission_id: int
    permission_code: str


