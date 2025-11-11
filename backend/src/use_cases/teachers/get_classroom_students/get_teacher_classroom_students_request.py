from ...shared.base_data_transfer import BaseDataTransfer


class GetTeacherClassroomStudentsRequest(BaseDataTransfer):
    teacher_id: str
    classroom_id: str
    requesting_user_id: str
    can_manage_any: bool = False
    include_inactive: bool = False

