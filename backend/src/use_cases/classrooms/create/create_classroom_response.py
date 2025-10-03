from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class CreateClassroomResponse(BaseDataTransfer):
    id: str
    description: str
    level: str
    degree: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    tutor_id: Optional[str] = None
