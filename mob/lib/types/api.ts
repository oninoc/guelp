export type PermissionCode =
  | "manage_users"
  | "manage_roles"
  | "manage_permissions"
  | "manage_qualifications"
  | "view_students"
  | "view_teachers"
  | string;

export interface RequestedByMetadata {
  email: string;
  roles: string[];
  permissions: PermissionCode[];
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  expires_at: number;
}

export interface RoleWithPermissions {
  code: string;
  permissions: PermissionCode[];
}

export interface UserProfile {
  id: string;
  email: string;
  name: string;
  last_name: string;
  phone: string;
  address: string;
  roles: RoleWithPermissions[];
  teacher_id?: string | null;
  student_id?: string | null;
}

export type UserProfileEnvelope = UserProfile & {
  requested_by: RequestedByMetadata;
};

export type WithRequestedBy<T> = T & { requested_by: RequestedByMetadata };

export interface StudentSubjectSummary {
  classroom_subject_student_id: number;
  classroom_subject_id?: number | null;
  subject_id?: number | null;
  subject_name?: string | null;
  subject_description?: string | null;
  teacher_id?: string | null;
  teacher_full_name?: string | null;
  classroom_id?: string | null;
  classroom_level?: string | null;
  classroom_degree?: string | null;
  status?: string | null;
  is_active: boolean;
}

export type StudentSubjectsEnvelope = {
  subjects: StudentSubjectSummary[];
  requested_by: RequestedByMetadata;
};

export interface StudentProfile {
  id: string;
  code: string;
  names: string;
  father_last_name: string;
  mother_last_name: string;
  phone?: string | null;
  address?: string | null;
  email?: string | null;
  birth_date?: string | null;
  gender?: string | null;
  nationality?: string | null;
  document_type?: string | null;
  document_number?: string | null;
  responsible_name?: string | null;
  responsible_phone?: string | null;
  responsible_email?: string | null;
  responsible_address?: string | null;
  user_id: string;
  full_name: string;
}

export type StudentProfileEnvelope = StudentProfile & {
  requested_by: RequestedByMetadata;
};

export interface QualificationRecord {
  id?: number | null;
  grade?: GradeLetter | null;
  teacher_id?: string | null;
  teacher_full_name?: string | null;
  description?: string | null;
  created_at?: string | null;
}

export interface StudentSubjectQualification {
  classroom_subject_student_id: number;
  classroom_subject_id?: number | null;
  subject_id?: number | null;
  subject_name?: string | null;
  current_qualification?: string | null;
  status?: string | null;
  description?: string | null;
  is_active: boolean;
  records: QualificationRecord[];
}

export type StudentSubjectQualificationsEnvelope = {
  subjects: StudentSubjectQualification[];
  requested_by: RequestedByMetadata;
};

export type GradeLetter = "AD" | "A" | "B" | "C" | "D";

export interface TeacherClassroomSubject {
  classroom_subject_id: number;
  subject_id: number;
  subject_name: string;
  is_substitute: boolean;
  is_active: boolean;
  teacher_id?: string | null;
  teacher_name?: string | null;
}

export interface TeacherClassroomSummary {
  classroom_id: string;
  description: string;
  level: string;
  degree: string;
  is_tutor: boolean;
  subjects: TeacherClassroomSubject[];
}

export type TeacherClassroomsEnvelope = {
  classrooms: TeacherClassroomSummary[];
  requested_by: RequestedByMetadata;
};

export interface TeacherQualificationRecordSummary {
  id: number;
  grade?: GradeLetter | null;
  description?: string | null;
  teacher_id?: string | null;
  teacher_full_name?: string | null;
  created_at?: string | null;
}

export interface TeacherClassroomStudentSubjectSummary {
  classroom_subject_student_id: number;
  classroom_subject_id: number;
  subject_id: number;
  subject_name: string;
  teacher_id?: string | null;
  teacher_name?: string | null;
  qualification?: string | null;
  status?: string | null;
  is_active: boolean;
  can_manage: boolean;
  average_grade?: GradeLetter | null;
  average_score?: number | null;
  history: TeacherQualificationRecordSummary[];
}

export interface TeacherClassroomStudentSummary {
  student_id: string;
  student_code: string;
  full_name: string;
  email?: string | null;
  average_qualification?: number | null;
  subjects: TeacherClassroomStudentSubjectSummary[];
}

export type TeacherClassroomStudentsEnvelope = {
  students: TeacherClassroomStudentSummary[];
  requested_by: RequestedByMetadata;
};

export interface ManageStudentQualificationPayload {
  classroom_subject_student_id: number;
  qualification?: GradeLetter | null;
  description?: string;
  is_active?: boolean;
  qualification_record_id?: number;
  qualification_record_description?: string;
}

export interface CreateStudentPayload {
  code: string;
  names: string;
  father_last_name: string;
  mother_last_name: string;
  phone?: string | null;
  address?: string | null;
  email?: string | null;
  birth_date?: string | null;
  gender?: string | null;
  document_type?: string | null;
  document_number?: string | null;
  responsible_name?: string | null;
  responsible_phone?: string | null;
  responsible_email?: string | null;
  responsible_address?: string | null;
  user_email?: string | null;
  user_password?: string | null;
  user_id?: string | null;
}

export interface CreateTeacherPayload {
  names: string;
  father_last_name: string;
  mother_last_name: string;
  document_type: string;
  document_number: string;
  birth_date: string;
  gender: string;
  user_email?: string | null;
  user_password?: string | null;
  user_id?: string | null;
}

export interface CreateSubjectPayload {
  name: string;
  description?: string;
}

export interface CreateClassroomPayload {
  description: string;
  level: string;
  degree: string;
  start_time?: string | null;
  end_time?: string | null;
  tutor_id?: string;
}

export interface CreateUserPayload {
  email: string;
  password: string;
  name: string;
  last_name: string;
  phone: string;
  address: string;
}

export interface AssignRolePayload {
  user_id: string;
  role_code: string;
  relation_type?: string | null;
}

export interface AssignPermissionPayload {
  role_code: string;
  permission_code: string;
  relation_type?: string | null;
}

