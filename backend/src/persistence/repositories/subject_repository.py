from ...models.subjects import Subject
from .base_repository import BaseRepository

class SubjectRepository(BaseRepository[Subject]):
    _entity_class = Subject