from typing import List, Optional

from ...shared.base_data_transfer import BaseDataTransfer


class ClassroomSummary(BaseDataTransfer):
    id: str
    description: str
    level: str
    degree: str
    tutor_id: Optional[str] = None
    tutor_name: Optional[str] = None


class GetAllClassroomsResponse(BaseDataTransfer):
    classrooms: List[ClassroomSummary]

