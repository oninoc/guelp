from ...shared.base_data_transfer import BaseDataTransfer


class DeleteTeacherRequest(BaseDataTransfer):
    teacher_id: str

