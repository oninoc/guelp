import { useMemo } from "react";
import { useAuthContext } from "@/lib/context/AuthContext";
import { determineDestination } from "@/lib/navigation/roleRouting";

export const useAuth = () => {
  const context = useAuthContext();
  const destination = useMemo(
    () => determineDestination(context.user),
    [context.user]
  );

  return {
    ...context,
    destination,
  };
};

