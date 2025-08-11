from ...shared.base_data_transfer import BaseDataTransfer
from typing import List


class RoleWithPermissions(BaseDataTransfer):
    code: str
    permissions: List[str]


class GetUserByIdResponse(BaseDataTransfer):
    id: str
    email: str
    name: str
    last_name: str
    phone: str
    address: str
    roles: List[RoleWithPermissions]


