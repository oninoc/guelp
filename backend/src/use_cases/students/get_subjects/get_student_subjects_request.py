from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class GetStudentSubjectsRequest(BaseDataTransfer):
    student_id: UUID

