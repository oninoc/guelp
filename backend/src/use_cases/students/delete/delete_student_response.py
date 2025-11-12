from ...shared.base_data_transfer import BaseDataTransfer


class DeleteStudentResponse(BaseDataTransfer):
    deleted: bool
    student_id: str

