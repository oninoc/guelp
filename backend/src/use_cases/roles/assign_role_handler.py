from ..shared.base_auth_handler import BaseAuthHandler
from .assign_role_request import AssignRoleRequest
from .assign_role_response import AssignRoleResponse
from ...persistence.repositories.role_repository import RoleRepository
from ...persistence.repositories.user_repository import UserRepository
from ...persistence.repositories.user_role_relation_repository import UserRoleRelationRepository
from fastapi import HTTPException


class AssignRoleHandler(BaseAuthHandler[AssignRoleRequest, AssignRoleResponse]):
    async def execute(self, request: AssignRoleRequest) -> AssignRoleResponse:
        user_repo = UserRepository(self.session)
        role_repo = RoleRepository(self.session)
        urr_repo = UserRoleRelationRepository(self.session)

        user = await user_repo.get_by_id(str(request.user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        role = await role_repo.get_by_code(request.role_code)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        if not await urr_repo.exists(user.id, role.id):
            await urr_repo.link(user.id, role.id, request.relation_type or "direct")

        return AssignRoleResponse(user_id=str(user.id), role_id=role.id, role_code=role.code)


