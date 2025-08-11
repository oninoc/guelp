from ..shared.base_data_transfer import BaseDataTransfer
from uuid import UUID


class AssignRoleRequest(BaseDataTransfer):
    user_id: UUID
    role_code: str
    relation_type: str | None = "direct"


