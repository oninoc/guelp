from ...shared.base_data_transfer import BaseDataTransfer


class DeleteSubjectRequest(BaseDataTransfer):
    subject_id: int

