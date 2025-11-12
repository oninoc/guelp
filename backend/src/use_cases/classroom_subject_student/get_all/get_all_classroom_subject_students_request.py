from ...shared.base_data_transfer import BaseDataTransfer


class GetAllClassroomSubjectStudentsRequest(BaseDataTransfer):
    classroom_subject_id: int

