from typing import Optional
from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class UpdateClassroomRequest(BaseDataTransfer):
    classroom_id: Optional[str] = None  # Will be set from path parameter
    description: Optional[str] = None
    level: Optional[str] = None
    degree: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    tutor_id: Optional[UUID] = None

