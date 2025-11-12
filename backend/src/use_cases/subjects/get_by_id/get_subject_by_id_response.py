from ...shared.base_data_transfer import BaseDataTransfer


class GetSubjectByIdResponse(BaseDataTransfer):
    id: int
    name: str
    description: str

