from ...models.qualifications import Qualification
from .base_repository import BaseRepository


class QualificationRepository(BaseRepository[Qualification]):
    _entity_class = Qualification

