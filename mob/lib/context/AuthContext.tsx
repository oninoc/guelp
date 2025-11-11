import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { jwtDecode } from "jwt-decode";
import { configureClientAuth } from "../api/client";
import { login as loginRequest, getUserProfile } from "../api/auth";
import {
  LoginResponse,
  RequestedByMetadata,
  RoleWithPermissions,
  UserProfileEnvelope,
} from "../types/api";
import {
  clearPersistedAuthState,
  PersistedAuthState,
  persistAuthState,
  readPersistedAuthState,
} from "../storage/tokenStorage";

type AuthStatus = "loading" | "authenticated" | "unauthenticated";

export type AuthUser = {
  id: string;
  email: string;
  name: string;
  lastName: string;
  phone: string;
  address: string;
  teacherId: string | null;
  studentId: string | null;
  roles: string[];
  permissions: string[];
  requestedBy?: RequestedByMetadata;
};

type AuthTokens = {
  accessToken: string;
  refreshToken: string | null;
  expiresAt?: number;
};

type SignInPayload = {
  email: string;
  password: string;
};

type AuthContextValue = {
  status: AuthStatus;
  user: AuthUser | null;
  tokens: AuthTokens | null;
  signIn: (payload: SignInPayload) => Promise<void>;
  signOut: () => Promise<void>;
  refreshProfile: () => Promise<void>;
  hasRole: (role: string) => boolean;
  hasPermission: (permission: string) => boolean;
  lastError: string | null;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

type JwtPayload = {
  sub: string;
  email: string;
  exp?: number;
};

const mapProfileToUser = (
  profile: UserProfileEnvelope
): Omit<AuthUser, "requestedBy"> & { requestedBy?: RequestedByMetadata } => {
  const roles = profile.roles?.map((role: RoleWithPermissions) => role.code) ?? [];
  const permissions = profile.roles
    ?.flatMap((role) => role.permissions ?? [])
    .filter(Boolean) ?? [];

  return {
    id: profile.id,
    email: profile.email,
    name: profile.name,
    lastName: profile.last_name,
    phone: profile.phone,
    address: profile.address,
    teacherId: profile.teacher_id ?? null,
    studentId: profile.student_id ?? null,
    roles,
    permissions,
    requestedBy: profile.requested_by,
  };
};

export const AuthProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [status, setStatus] = useState<AuthStatus>("loading");
  const [user, setUser] = useState<AuthUser | null>(null);
  const [tokens, setTokens] = useState<AuthTokens | null>(null);
  const [lastError, setLastError] = useState<string | null>(null);
  const tokensRef = useRef<AuthTokens | null>(null);
  const userRef = useRef<AuthUser | null>(null);

  useEffect(() => {
    tokensRef.current = tokens;
    userRef.current = user;
  }, [tokens, user]);

  const persistSnapshot = useCallback(
    async (currentUser: AuthUser, currentTokens: AuthTokens) => {
      const snapshot: PersistedAuthState = {
        accessToken: currentTokens.accessToken,
        refreshToken: currentTokens.refreshToken,
        expiresAt: currentTokens.expiresAt,
        userId: currentUser.id,
        email: currentUser.email,
        roles: currentUser.roles,
        permissions: currentUser.permissions,
        teacherId: currentUser.teacherId,
        studentId: currentUser.studentId,
      };
      await persistAuthState(snapshot);
    },
    []
  );

  const bootstrap = useCallback(async () => {
    try {
      setStatus("loading");
      setLastError(null);
      const snapshot = await readPersistedAuthState();
      if (snapshot?.accessToken && snapshot.userId) {
        const bootstrapTokens: AuthTokens = {
          accessToken: snapshot.accessToken,
          refreshToken: snapshot.refreshToken,
          expiresAt: snapshot.expiresAt,
        };
        const bootstrapUser: AuthUser = {
          id: snapshot.userId,
          email: snapshot.email,
          name: "",
          lastName: "",
          phone: "",
          address: "",
          teacherId: snapshot.teacherId ?? null,
          studentId: snapshot.studentId ?? null,
          roles: snapshot.roles ?? [],
          permissions: snapshot.permissions ?? [],
        };
        setTokens(bootstrapTokens);
        setUser(bootstrapUser);
        setStatus("authenticated");
      } else {
        setStatus("unauthenticated");
      }
    } catch (error) {
      console.error("Failed to bootstrap auth state", error);
      setLastError("We could not restore your previous session. Please sign in again.");
      await clearPersistedAuthState();
      setStatus("unauthenticated");
    }
  }, []);

  useEffect(() => {
    bootstrap();
  }, [bootstrap]);

  const signOut = useCallback(async () => {
    setStatus("unauthenticated");
    setTokens(null);
    setUser(null);
    setLastError(null);
    tokensRef.current = null;
    userRef.current = null;
    await clearPersistedAuthState();
  }, []);

  const refreshProfile = useCallback(async () => {
    if (!tokensRef.current?.accessToken || !userRef.current?.id) {
      return;
    }

    const profile = await getUserProfile(
      userRef.current.id,
      tokensRef.current.accessToken
    );
    const mapped = mapProfileToUser(profile);
    const updatedUser: AuthUser = {
      ...mapped,
      requestedBy: userRef.current.requestedBy ?? mapped.requestedBy,
    };
    setUser(updatedUser);
    if (tokensRef.current) {
      await persistSnapshot(updatedUser, tokensRef.current);
    }
  }, [persistSnapshot]);

  useEffect(() => {
    if (
      status === "authenticated" &&
      tokensRef.current?.accessToken &&
      userRef.current?.id &&
      !userRef.current.name
    ) {
      refreshProfile().catch(() => {
        // If profile refresh fails, fall back to signing out to avoid inconsistent state.
        signOut();
      });
    }
  }, [refreshProfile, signOut, status]);

  useEffect(() => {
    configureClientAuth({
      getAccessToken: () => tokensRef.current?.accessToken ?? null,
      getRefreshToken: () => tokensRef.current?.refreshToken ?? null,
      onTokensUpdated: async (updated) => {
        const nextTokens: AuthTokens = {
          accessToken: updated.accessToken,
          refreshToken: updated.refreshToken,
          expiresAt: updated.expiresAt,
        };
        setTokens(nextTokens);
        if (userRef.current) {
          await persistSnapshot(userRef.current, nextTokens);
        }
      },
      onUnauthorized: signOut,
    });
  }, [persistSnapshot, signOut]);

  const signIn = useCallback(
    async ({ email, password }: SignInPayload) => {
      setStatus("loading");
      try {
        const loginResponse = await loginRequest({ email, password });
        const tokensFromLogin: AuthTokens = {
          accessToken: loginResponse.access_token,
          refreshToken: loginResponse.refresh_token,
          expiresAt: loginResponse.expires_at,
        };

        const token = loginResponse.access_token;
        if (typeof token !== "string" || !token.trim()) {
          throw new Error("Received invalid access token.");
        }

        const decoded = jwtDecode<JwtPayload>(token);
        const userId = decoded.sub;
        if (!userId) {
          throw new Error("Unable to parse authenticated user identifier.");
        }

        const profile = await getUserProfile(userId, token);
        const mapped = mapProfileToUser(profile);
        const authUser: AuthUser = {
          ...mapped,
          requestedBy: loginResponse.requested_by ?? mapped.requestedBy,
        };

        setTokens(tokensFromLogin);
        setUser(authUser);
        await persistSnapshot(authUser, tokensFromLogin);
        setStatus("authenticated");
        setLastError(null);
      } catch (error) {
        await signOut();
        setStatus("unauthenticated");
        setLastError(error instanceof Error ? error.message : "Sign-in failed.");
        throw error;
      }
    },
    [persistSnapshot, signOut]
  );

  const hasRole = useCallback(
    (role: string) => user?.roles?.includes(role) ?? false,
    [user?.roles]
  );

  const hasPermission = useCallback(
    (permission: string) => user?.permissions?.includes(permission) ?? false,
    [user?.permissions]
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      status,
      user,
      tokens,
      signIn,
      signOut,
      refreshProfile,
      hasRole,
      hasPermission,
      lastError,
    }),
    [status, user, tokens, signIn, signOut, refreshProfile, hasRole, hasPermission, lastError]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuthContext = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuthContext must be used within an AuthProvider");
  }
  return context;
};

