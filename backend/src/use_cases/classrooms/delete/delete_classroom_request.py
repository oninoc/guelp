from ...shared.base_data_transfer import BaseDataTransfer


class DeleteClassroomRequest(BaseDataTransfer):
    classroom_id: str

