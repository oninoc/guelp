from .base.base_int_model import BaseIntModel

class Subject(BaseIntModel, table=True):
    name: str
    description: str