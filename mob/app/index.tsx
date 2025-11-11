import React from "react";
import { Redirect } from "expo-router";
import LoadingScreen from "@/lib/screens/shared/LoadingScreen";
import { useAuth } from "@/lib/hooks/useAuth";
import { determineDestination } from "@/lib/navigation/roleRouting";

const Index = () => {
  const { status, user } = useAuth();
  const destination = determineDestination(user);

  if (status === "loading") {
    return <LoadingScreen />;
  }

  if (status !== "authenticated" || !destination) {
    return <Redirect href="/auth/login" />;
  }

  return <Redirect href={`/${destination}`} />;
};

export default Index;


