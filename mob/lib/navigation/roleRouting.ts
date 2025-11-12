import { AuthUser } from "@/lib/context/AuthContext";

export type RoleDestination = "student" | "teacher" | "admin";

export const determineDestination = (user: AuthUser | null): RoleDestination | null => {
  if (!user) {
    return null;
  }

  const normalizedRoles = user.roles.map((role) => role.toLowerCase().trim());
  const normalizedPermissions = user.permissions.map((permission) => permission.toLowerCase().trim());
  
  // Debug logging (remove in production)
  if (__DEV__) {
    console.log("[RoleRouting] User roles:", user.roles);
    console.log("[RoleRouting] User permissions:", user.permissions);
    console.log("[RoleRouting] Normalized roles:", normalizedRoles);
    console.log("[RoleRouting] Normalized permissions:", normalizedPermissions);
  }
  
  // Check for exact role match first, then substring match
  const hasRole = (needle: string) => {
    const lowerNeedle = needle.toLowerCase();
    return normalizedRoles.some((role) => role === lowerNeedle || role.includes(lowerNeedle));
  };
  
  const hasPermission = (needle: string) => {
    const lowerNeedle = needle.toLowerCase();
    return normalizedPermissions.some((perm) => perm === lowerNeedle || perm.includes(lowerNeedle));
  };

  // Admin check - prioritize exact matches and permissions
  // Check permissions first as they're more reliable
  const hasAdminPermission = 
    hasPermission("manage_users") ||
    hasPermission("manage_roles") ||
    hasPermission("manage_permissions");
  
  const hasAdminRole = 
    normalizedRoles.includes("admin") ||
    hasRole("admin");

  if (hasAdminPermission || hasAdminRole) {
    if (__DEV__) {
      console.log("[RoleRouting] Determined destination: admin");
    }
    return "admin";
  }

  // Teacher check
  const hasTeacherPermission = 
    hasPermission("manage_qualifications") ||
    hasPermission("view_teachers");
  
  const hasTeacherRole = 
    normalizedRoles.includes("teacher") ||
    hasRole("teacher");

  if (hasTeacherPermission || hasTeacherRole) {
    if (__DEV__) {
      console.log("[RoleRouting] Determined destination: teacher");
    }
    return "teacher";
  }

  // Default to student
  if (__DEV__) {
    console.log("[RoleRouting] Determined destination: student (default)");
  }
  return "student";
};


