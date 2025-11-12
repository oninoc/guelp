from ...shared.base_data_transfer import BaseDataTransfer


class DeleteSubjectResponse(BaseDataTransfer):
    deleted: bool
    subject_id: int

