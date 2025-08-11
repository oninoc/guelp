from ...models.students import Student
from .base_repository import BaseRepository

class StudentRepository(BaseRepository[Student]):
    _entity_class = Student