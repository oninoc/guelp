from ..shared.base_auth_handler import BaseAuthHandler
from .assign_role_request import AssignRoleRequest
from .assign_role_response import AssignRoleResponse
from fastapi import HTTPException


class AssignRoleHandler(BaseAuthHandler[AssignRoleRequest, AssignRoleResponse]):
    async def execute(self, request: AssignRoleRequest) -> AssignRoleResponse:
        user = await self.unit_of_work.user_repository.get_by_id(
            str(request.user_id)
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        role = await self.unit_of_work.role_repository.get_by_code(
            request.role_code
        )
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        if not await self.unit_of_work.user_role_relation_repository.exists(
            user.id, role.id
        ):
            await self.unit_of_work.user_role_relation_repository.link(
                user.id, role.id, request.relation_type or "direct"
            )

        return AssignRoleResponse(
            user_id=str(user.id), role_id=role.id, role_code=role.code
        )


