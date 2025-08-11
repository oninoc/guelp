from ...shared.base_data_transfer import BaseDataTransfer


class CreateSubjectRequest(BaseDataTransfer):
    name: str
    description: str
