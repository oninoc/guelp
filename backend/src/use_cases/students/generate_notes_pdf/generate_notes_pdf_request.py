from ...shared.base_data_transfer import BaseDataTransfer


class GenerateNotesPdfRequest(BaseDataTransfer):
    student_id: str
    include_inactive: bool = False

