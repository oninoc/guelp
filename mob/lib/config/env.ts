import Constants from "expo-constants";

type ExtraConfig = {
  apiBaseUrl?: string;
};

const extra: ExtraConfig =
  (Constants.expoConfig?.extra as ExtraConfig | undefined) ??
  (Constants.manifest?.extra as ExtraConfig | undefined) ??
  {};

export const API_BASE_URL =
  extra.apiBaseUrl?.replace(/\/+$/, "") ?? "https://zwftj3xpti.us-east-1.awsapprunner.com";

export const API_TIMEOUT_MS = 15000;

export const SHOULD_ATTEMPT_REFRESH = true;

