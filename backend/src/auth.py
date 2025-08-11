from dataclasses import dataclass
from typing import List
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from src.services.auth import AuthService
from src.persistence.repositories.user_repository import UserRepository
from src.database import AsyncSQLSession


@dataclass
class CurrentUserContext:
    user_id: str
    email: str
    roles: List[str]
    permissions: List[str]


async def get_current_user(
    request: Request,
    session: AsyncSQLSession,
    auth: AuthService = Depends(AuthService),
) -> CurrentUserContext:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, auth.secret_key, algorithms=[auth.algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    subject = payload.get("sub")
    email = payload.get("email")
    if subject is None or email is None:
        raise HTTPException(status_code=401, detail="Invalid token claims")

    # Use repository with eager loading to fetch user, roles, and permissions in one ORM call
    user_repo = UserRepository(session)
    user = await user_repo.get_with_roles_permissions_by_id(subject)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ensure provided token matches what is currently stored for the user (access or refresh)
    if token not in {user.token, user.refresh_token}:
        raise HTTPException(status_code=401, detail="Token invalid or expired")

    role_codes = [rel.role.code for rel in user.roles if rel.role is not None]
    permission_codes: List[str] = []
    for rel in getattr(user, "roles", []):
        role = rel.role
        if role is None:
            continue
        for rp in getattr(role, "permissions", []):
            if rp.permission is not None:
                permission_codes.append(rp.permission.code)

    return CurrentUserContext(
        user_id=str(user.id),
        email=user.email,
        roles=sorted(set(role_codes)),
        permissions=sorted(set(permission_codes)),
    )


