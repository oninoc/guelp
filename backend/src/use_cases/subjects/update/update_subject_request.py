from typing import Optional

from ...shared.base_data_transfer import BaseDataTransfer


class UpdateSubjectRequest(BaseDataTransfer):
    subject_id: Optional[int] = None  # Will be set from path parameter
    name: Optional[str] = None
    description: Optional[str] = None

