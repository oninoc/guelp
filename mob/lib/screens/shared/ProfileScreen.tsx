import React from "react";
import { FlatList, RefreshControl, StyleSheet, Text, View } from "react-native";
import { useAuth } from "@/lib/hooks/useAuth";

const ProfileScreen: React.FC = () => {
  const { user, refreshProfile, status } = useAuth();
  const [isRefreshing, setIsRefreshing] = React.useState(false);

  const handleRefresh = React.useCallback(async () => {
    setIsRefreshing(true);
    try {
      await refreshProfile();
    } finally {
      setIsRefreshing(false);
    }
  }, [refreshProfile]);

  const data = [
    { label: "Email", value: user?.email ?? "—" },
    { label: "Name", value: `${user?.name ?? ""} ${user?.lastName ?? ""}`.trim() || "—" },
    { label: "Phone", value: user?.phone || "—" },
    { label: "Address", value: user?.address || "—" },
    { label: "Roles", value: user?.roles.join(", ") || "—" },
    { label: "Permissions", value: user?.permissions.join(", ") || "—" },
  ];

  return (
    <FlatList
      style={styles.container}
      data={data}
      keyExtractor={(item) => item.label}
      refreshControl={
        <RefreshControl
          refreshing={isRefreshing || status === "loading"}
          onRefresh={handleRefresh}
          accessibilityLabel="Refresh profile"
        />
      }
      renderItem={({ item }) => (
        <View style={styles.row}>
          <Text style={styles.label}>{item.label}</Text>
          <Text style={styles.value}>{item.value}</Text>
        </View>
      )}
      ListHeaderComponent={
        <View style={styles.header}>
          <Text style={styles.title}>Profile</Text>
          <Text style={styles.subtitle}>
            {user?.requestedBy
              ? `Accessed as ${user.requestedBy.email}`
              : "Details synced with server"}
          </Text>
        </View>
      }
    />
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  header: {
    paddingHorizontal: 24,
    paddingVertical: 24,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: "#E5E7EB",
  },
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 4,
  },
  subtitle: {
    color: "#6B7280",
  },
  row: {
    paddingHorizontal: 24,
    paddingVertical: 16,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: "#E5E7EB",
  },
  label: {
    fontSize: 14,
    color: "#6B7280",
    marginBottom: 4,
  },
  value: {
    fontSize: 16,
    color: "#111827",
  },
});

export default ProfileScreen;

