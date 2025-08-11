from ...shared.base_data_transfer import BaseDataTransfer


class CreateSubjectResponse(BaseDataTransfer):
    id: int
    name: str
    description: str
