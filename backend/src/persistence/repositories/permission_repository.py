from ...models.permission import Permission
from .base_repository import BaseRepository
from sqlmodel import select

class PermissionRepository(BaseRepository[Permission]):
    _entity_class = Permission
    
    async def get_by_code(self, code: str) -> Permission | None:
        entities = await self._session.execute(
            select(self._entity_class).where(self._entity_class.code == code)
        )
        return entities.scalars().first()
