from uuid import UUID

from ...shared.base_data_transfer import BaseDataTransfer


class GetTeacherClassroomsRequest(BaseDataTransfer):
    teacher_id: UUID

