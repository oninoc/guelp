from ...shared.base_data_transfer import BaseDataTransfer


class DeleteStudentRequest(BaseDataTransfer):
    student_id: str

