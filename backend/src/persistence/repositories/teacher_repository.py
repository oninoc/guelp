from ...models.teachers import Teacher
from .base_repository import BaseRepository

class TeacherRepository(BaseRepository[Teacher]):
    _entity_class = Teacher