from ..shared.base_auth_handler import BaseAuthHandler
from .assign_permission_request import AssignPermissionRequest
from .assign_permission_response import AssignPermissionResponse
from ...persistence.repositories.role_repository import RoleRepository
from ...persistence.repositories.permission_repository import PermissionRepository
from ...persistence.repositories.role_permission_relation_repository import RolePermissionRelationRepository
from fastapi import HTTPException


class AssignPermissionHandler(BaseAuthHandler[AssignPermissionRequest, AssignPermissionResponse]):
    async def execute(self, request: AssignPermissionRequest) -> AssignPermissionResponse:
        role_repo = RoleRepository(self.session)
        perm_repo = PermissionRepository(self.session)
        rpr_repo = RolePermissionRelationRepository(self.session)

        role = await role_repo.get_by_code(request.role_code)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        permission = await perm_repo.get_by_code(request.permission_code)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")

        if not await rpr_repo.exists(role.id, permission.id):
            await rpr_repo.link(role.id, permission.id, request.relation_type or "direct")

        return AssignPermissionResponse(
            role_id=role.id,
            role_code=role.code,
            permission_id=permission.id,
            permission_code=permission.code,
        )


