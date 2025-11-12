from ...shared.base_data_transfer import BaseDataTransfer


class DeleteTeacherResponse(BaseDataTransfer):
    deleted: bool
    teacher_id: str

