import React from "react";
import { Redirect, Stack } from "expo-router";
import LoadingScreen from "@/lib/screens/shared/LoadingScreen";
import { useAuth } from "@/lib/hooks/useAuth";

const AdminLayout = () => {
  const { status, destination } = useAuth();

  if (status === "loading") {
    return <LoadingScreen />;
  }

  if (status !== "authenticated" || destination !== "admin") {
    return <Redirect href="/" />;
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="(tabs)" />
    </Stack>
  );
};

export default AdminLayout;

