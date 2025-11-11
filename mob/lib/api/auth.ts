import axios, { AxiosError } from "axios";
import { API_BASE_URL, API_TIMEOUT_MS } from "../config/env";
import {
  LoginResponse,
  RequestedByMetadata,
  UserProfileEnvelope,
} from "../types/api";

const authHttp = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT_MS,
});

export interface LoginRequestPayload {
  email: string;
  password: string;
}

type RawLoginResponse = {
  access_token?: string;
  refresh_token?: string;
  expires_at?: number;
  accessToken?: string;
  refreshToken?: string;
  expiresAt?: number;
  requested_by?: RequestedByMetadata;
  requestedBy?: RequestedByMetadata;
};

const normalizeLoginResponse = (raw: RawLoginResponse): LoginResponse & {
  requested_by?: RequestedByMetadata;
} => {
  const accessToken = raw.access_token ?? raw.accessToken;
  const refreshToken = raw.refresh_token ?? raw.refreshToken;
  const expiresAt = raw.expires_at ?? raw.expiresAt;

  if (!accessToken || !refreshToken || typeof expiresAt !== "number") {
    throw new Error("Received malformed login response from server.");
  }

  return {
    access_token: accessToken,
    refresh_token: refreshToken,
    expires_at: expiresAt,
    requested_by: raw.requested_by ?? raw.requestedBy,
  };
};

export const login = async (
  payload: LoginRequestPayload
): Promise<LoginResponse & { requested_by?: RequestedByMetadata }> => {
  const response = await authHttp.post<RawLoginResponse>(
    "/auth/login",
    payload
  );

  return normalizeLoginResponse(response.data);
};

export const refreshAccessToken = async (
  refreshToken: string
): Promise<LoginResponse | null> => {
  try {
    const response = await authHttp.post<LoginResponse>(
      "/auth/refresh",
      {
        refresh_token: refreshToken,
      }
    );
    return response.data;
  } catch (error) {
    if (
      axios.isAxiosError(error) &&
      (error.response?.status === 404 || error.response?.status === 405)
    ) {
      // Backend does not yet expose a refresh endpoint; treat as unsupported.
      return null;
    }
    throw error;
  }
};

export const getUserProfile = async (
  userId: string,
  accessToken: string
): Promise<UserProfileEnvelope> => {
  const response = await authHttp.get<UserProfileEnvelope>(`/users/${userId}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  return response.data;
};

