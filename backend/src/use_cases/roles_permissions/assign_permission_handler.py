from ..shared.base_auth_handler import BaseAuthHandler
from .assign_permission_request import AssignPermissionRequest
from .assign_permission_response import AssignPermissionResponse
from fastapi import HTTPException


class AssignPermissionHandler(BaseAuthHandler[AssignPermissionRequest, AssignPermissionResponse]):
    async def execute(self, request: AssignPermissionRequest) -> AssignPermissionResponse:
        role = await self.unit_of_work.role_repository.get_by_code(
            request.role_code
        )
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        permission = await self.unit_of_work.permission_repository.get_by_code(
            request.permission_code
        )
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")

        if not await self.unit_of_work.role_permission_relation_repository.exists(
            role.id, permission.id
        ):
            await self.unit_of_work.role_permission_relation_repository.link(
                role.id, permission.id, request.relation_type or "direct"
            )

        return AssignPermissionResponse(
            role_id=role.id,
            role_code=role.code,
            permission_id=permission.id,
            permission_code=permission.code,
        )


