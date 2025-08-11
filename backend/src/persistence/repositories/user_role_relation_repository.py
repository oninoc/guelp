from ...models.user_role_relation import UserRoleRelation
from .base_repository import BaseRepository
from sqlmodel import select
from uuid import UUID


class UserRoleRelationRepository(BaseRepository[UserRoleRelation]):
    _entity_class = UserRoleRelation

    async def link(self, user_id: UUID, role_id: int, relation_type: str = "direct") -> UserRoleRelation:
        relation = UserRoleRelation(user_id=user_id, role_id=role_id, relation_type=relation_type)
        return await self.create(relation)

    async def exists(self, user_id: UUID, role_id: int) -> bool:
        entities = await self._session.execute(
            select(self._entity_class).where(
                (self._entity_class.user_id == user_id) & (self._entity_class.role_id == role_id)
            )
        )
        return entities.scalars().first() is not None

