import { apiClient } from "./client";
import {
  ManageStudentQualificationPayload,
  TeacherClassroomStudentsEnvelope,
  TeacherClassroomsEnvelope,
} from "../types/api";

export const fetchTeacherClassrooms = async (
  teacherId: string,
  includeInactive = false
): Promise<TeacherClassroomsEnvelope> => {
  const response = await apiClient.get<TeacherClassroomsEnvelope>(
    `/teachers/${teacherId}/classrooms`,
    {
      params: { include_inactive: includeInactive },
    }
  );

  return response.data;
};

export const updateStudentQualification = async (
  teacherId: string,
  payload: ManageStudentQualificationPayload
) => {
  await apiClient.post(`/teachers/${teacherId}/qualifications`, payload);
};

export const deleteTeacherQualification = async (
  teacherId: string,
  qualificationId: number
) => {
  await apiClient.delete(`/teachers/${teacherId}/qualifications/${qualificationId}`);
};

export const fetchTeacherClassroomStudents = async (
  teacherId: string,
  classroomId: string,
  includeInactive = false
): Promise<TeacherClassroomStudentsEnvelope> => {
  const response = await apiClient.get<TeacherClassroomStudentsEnvelope>(
    `/teachers/${teacherId}/classrooms/${classroomId}/students`,
    {
      params: { include_inactive: includeInactive },
    }
  );

  return response.data;
};

