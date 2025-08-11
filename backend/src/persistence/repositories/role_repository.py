from ...models.role import Role
from .base_repository import BaseRepository
from sqlmodel import select

class RoleRepository(BaseRepository[Role]):
    _entity_class = Role
    
    async def get_by_code(self, code: str) -> Role | None:
        entities = await self._session.execute(
            select(self._entity_class).where(self._entity_class.code == code)
        )
        return entities.scalars().first()
