import { useEffect } from "react";
import { DarkTheme, DefaultTheme, ThemeProvider } from "@react-navigation/native";
import { Stack, useRouter, useSegments } from "expo-router";
import { StatusBar } from "expo-status-bar";
import "react-native-reanimated";

import { useColorScheme } from "@/hooks/use-color-scheme";
import { AppProviders } from "@/lib/providers/AppProviders";
import { useAuth } from "@/lib/hooks/useAuth";

const AuthNavigationSync = () => {
  const { status, destination } = useAuth();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (status === "loading") {
      return;
    }

    const inAuthGroup = segments[0] === "auth";

    if (status !== "authenticated" || !destination) {
      if (!inAuthGroup) {
        router.replace("/auth/login");
      }
      return;
    }

    if (inAuthGroup) {
      router.replace(`/${destination}`);
    }
  }, [destination, router, segments, status]);

  return null;
};

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <AppProviders>
      <ThemeProvider value={colorScheme === "dark" ? DarkTheme : DefaultTheme}>
      <StatusBar style="auto" />
        <AuthNavigationSync />
        <Stack screenOptions={{ headerShown: false }} />
    </ThemeProvider>
    </AppProviders>
  );
}
