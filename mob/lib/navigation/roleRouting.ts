import { AuthUser } from "@/lib/context/AuthContext";

export type RoleDestination = "student" | "teacher" | "admin";

export const determineDestination = (user: AuthUser | null): RoleDestination | null => {
  if (!user) {
    return null;
  }

  const normalizedRoles = user.roles.map((role) => role.toLowerCase());
  const normalizedPermissions = user.permissions.map((permission) => permission.toLowerCase());
  const hasRole = (needle: string) => normalizedRoles.some((role) => role.includes(needle));
  const hasPermission = (needle: string) =>
    normalizedPermissions.includes(needle.toLowerCase());

  if (
    hasRole("admin") ||
    hasPermission("manage_users") ||
    hasPermission("manage_roles") ||
    hasPermission("manage_permissions")
  ) {
    return "admin";
  }

  if (hasRole("teacher") || hasPermission("manage_qualifications") || hasPermission("view_teachers")) {
    return "teacher";
  }

  return "student";
};


