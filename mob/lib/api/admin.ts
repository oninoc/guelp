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

