from ...models.classrooms import Classroom
from .base_repository import BaseRepository

class ClassroomRepository(BaseRepository[Classroom]):
    _entity_class = Classroom