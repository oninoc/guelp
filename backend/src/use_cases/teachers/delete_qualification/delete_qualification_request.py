from typing import Optional
from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class DeleteQualificationRequest(BaseDataTransfer):
    teacher_id: UUID
    qualification_id: int

