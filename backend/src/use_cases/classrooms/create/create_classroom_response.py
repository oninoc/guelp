from ...shared.base_data_transfer import BaseDataTransfer


class CreateClassroomResponse(BaseDataTransfer):
    id: str
    name: str
    description: str
    level: str
    degree: str
