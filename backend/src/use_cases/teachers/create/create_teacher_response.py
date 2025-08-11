from ...shared.base_data_transfer import BaseDataTransfer


class CreateTeacherResponse(BaseDataTransfer):
    id: str
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
