from ...shared.base_data_transfer import BaseDataTransfer


class CreateTeacherRequest(BaseDataTransfer):
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    document_type: str
    document_number: str
    birth_date: str
    gender: str
    nationality: str
    principal_subject: str
    secondary_subject: str
    start_time: str
    end_time: str
    user_id: str
