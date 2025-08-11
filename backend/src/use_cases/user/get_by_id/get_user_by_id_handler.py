from ...shared.base_auth_handler import BaseAuthHandler
from .get_user_by_id_request import GetUserByIdRequest
from .get_user_by_id_response import GetUserByIdResponse, RoleWithPermissions
from ....persistence.repositories.user_repository import UserRepository
from fastapi import HTTPException


class GetUserByIdHandler(BaseAuthHandler[GetUserByIdRequest, GetUserByIdResponse]):
    async def execute(self, request: GetUserByIdRequest) -> GetUserByIdResponse:
        repo = UserRepository(self.session)
        user = await repo.get_with_roles_permissions_by_id(request.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        roles_output: list[RoleWithPermissions] = []
        for rel in getattr(user, "roles", []):
            role = rel.role
            if role is None:
                continue
            perm_codes = [rp.permission.code for rp in getattr(role, "permissions", []) if rp.permission is not None]
            roles_output.append(RoleWithPermissions(code=role.code, permissions=sorted(set(perm_codes))))

        return GetUserByIdResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            last_name=user.last_name,
            phone=user.phone,
            address=user.address,
            roles=roles_output,
        )


