from ...shared.base_data_transfer import BaseDataTransfer


class UpdateSubjectResponse(BaseDataTransfer):
    id: int
    name: str
    description: str

