import React from "react";
import { Alert, Platform, ScrollView, StyleSheet, Text, View } from "react-native";
import { useAuth } from "@/lib/hooks/useAuth";

const SettingsScreen: React.FC = () => {
  const { signOut, user } = useAuth();

  const handleSignOut = React.useCallback(async () => {
    if (Platform.OS === "web") {
      const confirmed =
        typeof window === "undefined" || typeof window.confirm !== "function"
          ? true
          : window.confirm("Do you want to end the current session?");
      if (!confirmed) {
        return;
      }
      try {
        await signOut();
      } catch (error) {
        console.error("Failed to sign out", error);
      }
      return;
    }

    Alert.alert(
      "Sign out",
      "Do you want to end the current session?",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Sign out",
          style: "destructive",
          onPress: () => {
            signOut().catch((error) => {
              console.error("Failed to sign out", error);
            });
          },
        },
      ],
      { cancelable: true }
    );
  }, [signOut]);

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      accessibilityLabel="Settings"
    >
      <Text style={styles.title}>Settings</Text>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account</Text>
        <Text style={styles.sectionDescription}>
          Signed in as {user?.email ?? "unknown user"}.
        </Text>
        <Text
          onPress={handleSignOut}
          style={styles.link}
          accessibilityRole="button"
        >
          Sign out
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  content: {
    padding: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 24,
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 8,
  },
  sectionDescription: {
    color: "#6B7280",
    marginBottom: 12,
  },
  link: {
    color: "#DC2626",
    fontSize: 16,
  },
});

export default SettingsScreen;

