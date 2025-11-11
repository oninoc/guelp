from ...models.user import User
from ...models.user_role_relation import UserRoleRelation
from ...models.role import Role
from ...models.role_permission_relation import RolePermissionRelation
from .base_repository import BaseRepository
from sqlmodel import select
from sqlalchemy.orm import joinedload
from uuid import UUID

class UserRepository(BaseRepository[User]):
    _entity_class = User
    
    async def get_by_email(self, email: str) -> User:
        entities = await self._session.execute(
            select(self._entity_class).where(self._entity_class.email == email)
        )
        return entities.scalars().first()

    async def get_with_roles_permissions_by_id(self, user_id: UUID) -> User | None:
        query = (
            select(self._entity_class)
            .where(self._entity_class.id == user_id)
            .options(
                joinedload(self._entity_class.roles)
                .joinedload(UserRoleRelation.role)
                .joinedload(Role.permissions)
                .joinedload(RolePermissionRelation.permission),
                joinedload(self._entity_class.teacher),
                joinedload(self._entity_class.student),
            )
        )
        result = await self._session.execute(query)
        return result.scalars().first()
