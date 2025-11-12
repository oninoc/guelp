import { apiClient } from "./client";
import {
  StudentProfileEnvelope,
  StudentSubjectsEnvelope,
  StudentSubjectQualificationsEnvelope,
} from "../types/api";
import * as FileSystem from "expo-file-system";
import { readPersistedAuthState } from "../storage/tokenStorage";

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

export const downloadNotesPdf = async (
  studentId: string,
  includeInactive = false
): Promise<string> => {
  const apiBaseUrl = process.env.EXPO_PUBLIC_API_BASE_URL || "https://zwftj3xpti.us-east-1.awsapprunner.com";
  const url = `${apiBaseUrl}/students/${studentId}/notes-pdf?include_inactive=${includeInactive}`;
  
  // Get the token from storage
  const authState = await readPersistedAuthState();
  const token = authState?.accessToken || null;
  
  const fileUri = `${FileSystem.documentDirectory}notas_${studentId}_${Date.now()}.pdf`;
  
  const downloadResult = await FileSystem.downloadAsync(url, fileUri, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  
  if (downloadResult.status !== 200) {
    throw new Error(`Failed to download PDF: ${downloadResult.status}`);
  }
  
  return downloadResult.uri;
};

