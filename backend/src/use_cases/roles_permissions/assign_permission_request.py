from ..shared.base_data_transfer import BaseDataTransfer


class AssignPermissionRequest(BaseDataTransfer):
    role_code: str
    permission_code: str
    relation_type: str | None = "direct"


