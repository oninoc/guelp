from ...shared.base_data_transfer import BaseDataTransfer


class CreateStudentRequest(BaseDataTransfer):
    code: str
    names: str
    father_last_name: str
    mother_last_name: str
    phone: str
    address: str
    email: str
    degree: str
    level: str
    classroom: str
    birth_date: str
    gender: str
    nationality: str
    document_type: str
    document_number: str
    responsible_name: str
    responsible_phone: str
    responsible_email: str
    responsible_address: str
    user_id: str
