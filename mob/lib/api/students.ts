import { apiClient } from "./client";
import {
  StudentProfileEnvelope,
  StudentSubjectsEnvelope,
  StudentSubjectQualificationsEnvelope,
} from "../types/api";

export const fetchStudentSubjects = async (
  studentId: string,
  includeInactive = false
): Promise<StudentSubjectsEnvelope> => {
  const response = await apiClient.get<StudentSubjectsEnvelope>(
    `/students/${studentId}/subjects`,
    {
      params: { include_inactive: includeInactive },
    }
  );

  return response.data;
};

export const fetchStudentById = async (
  studentId: string
): Promise<StudentProfileEnvelope> => {
  const response = await apiClient.get<StudentProfileEnvelope>(`/students/${studentId}`);
  return response.data;
};

export const fetchStudentSubjectQualifications = async (
  studentId: string,
  includeInactive = false
): Promise<StudentSubjectQualificationsEnvelope> => {
  const response = await apiClient.get<StudentSubjectQualificationsEnvelope>(
    `/students/${studentId}/subjects/qualifications`,
    {
      params: { include_inactive: includeInactive },
    }
  );

  return response.data;
};

