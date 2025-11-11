import { Platform } from "react-native";
import * as SecureStore from "expo-secure-store";

const canUseSecureStore = Platform.OS !== "web";

const setItem = async (key: string, value: string) => {
  if (canUseSecureStore) {
    await SecureStore.setItemAsync(key, value);
    return;
  }
  if (typeof window !== "undefined" && window?.localStorage) {
    window.localStorage.setItem(key, value);
  }
};

const getItem = async (key: string): Promise<string | null> => {
  if (canUseSecureStore) {
    return SecureStore.getItemAsync(key);
  }
  if (typeof window !== "undefined" && window?.localStorage) {
    return window.localStorage.getItem(key);
  }
  return null;
};

const deleteItem = async (key: string) => {
  if (canUseSecureStore) {
    await SecureStore.deleteItemAsync(key);
    return;
  }
  if (typeof window !== "undefined" && window?.localStorage) {
    window.localStorage.removeItem(key);
  }
};

const STORAGE_KEY = "guelp-auth-state";

export type PersistedAuthState = {
  accessToken: string;
  refreshToken: string | null;
  expiresAt?: number;
  userId: string;
  email: string;
  roles: string[];
  permissions: string[];
  teacherId?: string | null;
  studentId?: string | null;
};

export const persistAuthState = async (state: PersistedAuthState) => {
  await setItem(STORAGE_KEY, JSON.stringify(state));
};

export const readPersistedAuthState = async (): Promise<PersistedAuthState | null> => {
  try {
    const raw = await getItem(STORAGE_KEY);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw) as PersistedAuthState;
    return parsed;
  } catch {
    await deleteItem(STORAGE_KEY);
    return null;
  }
};

export const clearPersistedAuthState = async () => {
  await deleteItem(STORAGE_KEY);
};

