import React from "react";
import { Redirect, Stack } from "expo-router";
import LoadingScreen from "@/lib/screens/shared/LoadingScreen";
import { useAuth } from "@/lib/hooks/useAuth";

const TeacherLayout = () => {
  const { status, destination } = useAuth();

  if (status === "loading") {
    return <LoadingScreen />;
  }

  if (status !== "authenticated" || destination !== "teacher") {
    return <Redirect href="/" />;
  }

  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen
        name="classroom/[classroomId]"
        options={{ headerShown: true, title: "Classroom" }}
      />
      <Stack.Screen
        name="classroom/[classroomId]/grading/[classroomSubjectStudentId]"
        options={{ headerShown: true, title: "Update qualification" }}
      />
    </Stack>
  );
};

export default TeacherLayout;

