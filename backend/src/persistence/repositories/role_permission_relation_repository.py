from ...models.role_permission_relation import RolePermissionRelation
from .base_repository import BaseRepository
from sqlmodel import select


class RolePermissionRelationRepository(BaseRepository[RolePermissionRelation]):
    _entity_class = RolePermissionRelation

    async def link(self, role_id: int, permission_id: int, relation_type: str = "direct") -> RolePermissionRelation:
        relation = RolePermissionRelation(role_id=role_id, permission_id=permission_id, relation_type=relation_type)
        return await self.create(relation)

    async def exists(self, role_id: int, permission_id: int) -> bool:
        entities = await self._session.execute(
            select(self._entity_class).where(
                (self._entity_class.role_id == role_id) & (self._entity_class.permission_id == permission_id)
            )
        )
        return entities.scalars().first() is not None

