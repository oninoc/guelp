import React from "react";
import { Redirect, Stack } from "expo-router";
import LoadingScreen from "@/lib/screens/shared/LoadingScreen";
import { useAuth } from "@/lib/hooks/useAuth";

const StudentLayout = () => {
  const { status, destination, user } = useAuth();

  if (status === "loading") {
    return <LoadingScreen />;
  }

  // Extra check: if user has admin/teacher roles or permissions, redirect them
  const isAdmin = user?.roles?.some((r) => r.toLowerCase().includes("admin")) ||
    user?.permissions?.some((p) => 
      p.toLowerCase().includes("manage_users") ||
      p.toLowerCase().includes("manage_roles") ||
      p.toLowerCase().includes("manage_permissions")
    );
  
  const isTeacher = user?.roles?.some((r) => r.toLowerCase().includes("teacher")) ||
    user?.permissions?.some((p) => 
      p.toLowerCase().includes("manage_qualifications") ||
      p.toLowerCase().includes("view_teachers")
    );

  if (status !== "authenticated" || destination !== "student" || isAdmin || isTeacher) {
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

