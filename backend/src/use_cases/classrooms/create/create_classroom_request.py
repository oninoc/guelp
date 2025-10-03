from typing import Optional
from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class CreateClassroomRequest(BaseDataTransfer):
    description: str
    level: str
    degree: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    tutor_id: Optional[UUID] = None
