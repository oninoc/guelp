from ...shared.base_data_transfer import BaseDataTransfer


class DeleteClassroomResponse(BaseDataTransfer):
    deleted: bool
    classroom_id: str

