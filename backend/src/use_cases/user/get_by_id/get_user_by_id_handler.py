from ...shared.base_auth_handler import BaseAuthHandler
from .get_user_by_id_request import GetUserByIdRequest
from .get_user_by_id_response import GetUserByIdResponse, RoleWithPermissions
from fastapi import HTTPException
from uuid import UUID


class GetUserByIdHandler(BaseAuthHandler[GetUserByIdRequest, GetUserByIdResponse]):
    async def execute(self, request: GetUserByIdRequest) -> GetUserByIdResponse:
        user_id = request.id if isinstance(request.id, UUID) else UUID(str(request.id))
        user = await self.unit_of_work.user_repository.get_with_roles_permissions_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        roles_output: list[RoleWithPermissions] = []
        for rel in getattr(user, "roles", []):
            role = rel.role
            if role is None:
                continue
            perm_codes = [rp.permission.code for rp in getattr(role, "permissions", []) if rp.permission is not None]
            roles_output.append(RoleWithPermissions(code=role.code, permissions=sorted(set(perm_codes))))

        teacher_id = getattr(getattr(user, "teacher", None), "id", None)
        student_id = getattr(getattr(user, "student", None), "id", None)

        return GetUserByIdResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            last_name=user.last_name,
            phone=user.phone,
            address=user.address,
            roles=roles_output,
            teacher_id=str(teacher_id) if teacher_id else None,
            student_id=str(student_id) if student_id else None,
        )


