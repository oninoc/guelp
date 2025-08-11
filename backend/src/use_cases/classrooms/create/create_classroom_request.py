from ...shared.base_data_transfer import BaseDataTransfer


class CreateClassroomRequest(BaseDataTransfer):
    name: str
    description: str
    level: str
    degree: str
    start_time: str
    end_time: str
    tutor_id: str
