import axios, { AxiosError, AxiosRequestConfig } from "axios";
import { API_BASE_URL, API_TIMEOUT_MS, SHOULD_ATTEMPT_REFRESH } from "../config/env";
import { LoginResponse } from "../types/api";
import { refreshAccessToken } from "./auth";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT_MS,
});

type TokenBundle = {
  accessToken: string;
  refreshToken: string;
  expiresAt?: number;
};

type AuthHandlers = {
  getAccessToken: () => string | null;
  getRefreshToken: () => string | null;
  onTokensUpdated?: (tokens: TokenBundle) => void | Promise<void>;
  onUnauthorized: () => void | Promise<void>;
};

type RetriableConfig = AxiosRequestConfig & { _retry?: boolean };

let handlers: AuthHandlers = {
  getAccessToken: () => null,
  getRefreshToken: () => null,
  onTokensUpdated: undefined,
  onUnauthorized: () => undefined,
};

let refreshPromise: Promise<TokenBundle | null> | null = null;

export const configureClientAuth = (options: Partial<AuthHandlers>) => {
  handlers = {
    ...handlers,
    ...options,
  };
};

apiClient.interceptors.request.use((config) => {
  const token = handlers.getAccessToken();
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const response = error.response;
    const originalRequest = error.config as RetriableConfig | undefined;

    if (!response || !originalRequest) {
      return Promise.reject(error);
    }

    if (response.status === 401 && !originalRequest._retry) {
      const refreshToken = handlers.getRefreshToken();
      if (!refreshToken) {
        await handlers.onUnauthorized();
        return Promise.reject(error);
      }

      if (!refreshPromise && SHOULD_ATTEMPT_REFRESH) {
        refreshPromise = attemptRefresh(refreshToken);
      }

      const refreshed = await refreshPromise;
      refreshPromise = null;

      if (refreshed?.accessToken) {
        await handlers.onTokensUpdated?.(refreshed);
        originalRequest._retry = true;
        originalRequest.headers = originalRequest.headers ?? {};
        originalRequest.headers.Authorization = `Bearer ${refreshed.accessToken}`;
        return apiClient(originalRequest);
      }

      await handlers.onUnauthorized();
      return Promise.reject(error);
    }

    if (response.status === 403) {
      await handlers.onUnauthorized();
    }

    return Promise.reject(error);
  }
);

const attemptRefresh = async (refreshToken: string): Promise<TokenBundle | null> => {
  try {
    const refreshed = await refreshAccessToken(refreshToken);
    if (!refreshed) {
      return null;
    }

    return {
      accessToken: refreshed.access_token,
      refreshToken: refreshed.refresh_token,
      expiresAt: refreshed.expires_at,
    };
  } catch {
    return null;
  }
};

