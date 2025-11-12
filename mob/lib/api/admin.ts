import { apiClient } from "./client";
import {
  AssignPermissionPayload,
  AssignRolePayload,
  CreateClassroomPayload,
  CreateStudentPayload,
  CreateSubjectPayload,
  CreateTeacherPayload,
  CreateUserPayload,
} from "../types/api";

export const createUser = async (payload: CreateUserPayload) => {
  const response = await apiClient.post("/users", payload);
  return response.data;
};

export const createStudent = async (payload: CreateStudentPayload) => {
  const response = await apiClient.post("/students", payload);
  return response.data;
};

export const createTeacher = async (payload: CreateTeacherPayload) => {
  const response = await apiClient.post(`/teachers`, payload);
  return response.data;
};

export const createClassroom = async (payload: CreateClassroomPayload) => {
  const response = await apiClient.post(`/classrooms`, payload);
  return response.data;
};

export const createSubject = async (payload: CreateSubjectPayload) => {
  const response = await apiClient.post(`/subjects`, payload);
  return response.data;
};

export const assignRole = async (payload: AssignRolePayload) => {
  const response = await apiClient.post(`/roles`, payload);
  return response.data;
};

export const assignPermission = async (payload: AssignPermissionPayload) => {
  const response = await apiClient.post(`/roles/permissions`, payload);
  return response.data;
};

// List fetching functions
export const fetchAllStudents = async () => {
  const response = await apiClient.get<{ students: Array<{ id: string; code: string; names: string; father_last_name: string; mother_last_name: string; email?: string | null }> }>("/students");
  return response.data.students;
};

export const fetchAllTeachers = async () => {
  const response = await apiClient.get<{ teachers: Array<{ id: string; names: string; father_last_name: string; mother_last_name: string; document_type: string; document_number: string }> }>("/teachers");
  return response.data.teachers;
};

export const fetchAllSubjects = async () => {
  const response = await apiClient.get<{ subjects: Array<{ id: number; name: string; description: string }> }>("/subjects");
  return response.data.subjects;
};

export const fetchAllClassrooms = async () => {
  const response = await apiClient.get<{ classrooms: Array<{ id: string; description: string; level: string; degree: string; tutor_id?: string | null; tutor_name?: string | null }> }>("/classrooms");
  return response.data.classrooms;
};

// Update functions
export const updateStudent = async (studentId: string, payload: Partial<CreateStudentPayload>) => {
  const response = await apiClient.put(`/students/${studentId}`, payload);
  return response.data;
};

export const updateTeacher = async (teacherId: string, payload: Partial<CreateTeacherPayload>) => {
  const response = await apiClient.put(`/teachers/${teacherId}`, payload);
  return response.data;
};

export const updateSubject = async (subjectId: number, payload: Partial<CreateSubjectPayload>) => {
  const response = await apiClient.put(`/subjects/${subjectId}`, payload);
  return response.data;
};

export const updateClassroom = async (classroomId: string, payload: Partial<CreateClassroomPayload>) => {
  const response = await apiClient.put(`/classrooms/${classroomId}`, payload);
  return response.data;
};

// Delete functions
export const deleteStudent = async (studentId: string) => {
  const response = await apiClient.delete(`/students/${studentId}`);
  return response.data;
};

export const deleteTeacher = async (teacherId: string) => {
  const response = await apiClient.delete(`/teachers/${teacherId}`);
  return response.data;
};

export const deleteSubject = async (subjectId: number) => {
  const response = await apiClient.delete(`/subjects/${subjectId}`);
  return response.data;
};

export const deleteClassroom = async (classroomId: string) => {
  const response = await apiClient.delete(`/classrooms/${classroomId}`);
  return response.data;
};

// Classroom-subject and classroom-subject-student
export const createClassroomSubject = async (payload: { classroom_id: string; subject_id: number; teacher_id?: string | null; substitute_teacher_id?: string | null; is_active?: boolean }) => {
  const response = await apiClient.post("/classroom-subject", payload);
  return response.data;
};

export const createClassroomSubjectStudent = async (payload: { classroom_subject_id: number; student_id: string; status?: string; is_active?: boolean }) => {
  const response = await apiClient.post("/classroom-subject-student", payload);
  return response.data;
};

// Get by ID functions for editing
export const getStudentById = async (studentId: string) => {
  const response = await apiClient.get(`/students/${studentId}`);
  return response.data;
};

export const getTeacherById = async (teacherId: string) => {
  const response = await apiClient.get(`/teachers/${teacherId}`);
  return response.data;
};

export const getSubjectById = async (subjectId: number) => {
  const response = await apiClient.get(`/subjects/${subjectId}`);
  return response.data;
};

export const getClassroomById = async (classroomId: string) => {
  const response = await apiClient.get(`/classrooms/${classroomId}`);
  return response.data;
};

// Get all classroom-subjects
export const fetchAllClassroomSubjects = async () => {
  const response = await apiClient.get<{ classroom_subjects: Array<{ id: number; classroom_id: string; classroom_description: string; subject_id: number; subject_name: string; teacher_id?: string | null; teacher_name?: string | null; substitute_teacher_id?: string | null; substitute_teacher_name?: string | null; is_active: boolean; student_count: number }> }>("/classroom-subject");
  return response.data.classroom_subjects;
};

// Get all students in a classroom-subject
export const fetchClassroomSubjectStudents = async (classroomSubjectId: number) => {
  const response = await apiClient.get<{ students: Array<{ id: number; student_id: string; student_code: string; student_name: string; student_email?: string | null; status?: string | null; is_active: boolean; qualification?: string | null }> }>(`/classroom-subject-student/classroom-subject/${classroomSubjectId}`);
  return response.data.students;
};

