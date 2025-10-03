from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class GetStudentSubjectQualificationsRequest(BaseDataTransfer):
    student_id: UUID

