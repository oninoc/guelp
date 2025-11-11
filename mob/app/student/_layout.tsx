import React from "react";
import { Redirect, Stack } from "expo-router";
import LoadingScreen from "@/lib/screens/shared/LoadingScreen";
import { useAuth } from "@/lib/hooks/useAuth";

const StudentLayout = () => {
  const { status, destination } = useAuth();

  if (status === "loading") {
    return <LoadingScreen />;
  }

  if (status !== "authenticated" || destination !== "student") {
    return <Redirect href="/" />;
  }

  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen
        name="subject/[subjectId]"
        options={{ headerShown: true, title: "Subject details" }}
      />
      <Stack.Screen
        name="subject/[subjectId]/history"
        options={{ headerShown: true, title: "Grade history" }}
      />
    </Stack>
  );
};

export default StudentLayout;

