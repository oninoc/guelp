import React from "react";
import { FlatList, StyleSheet, Text, View } from "react-native";

const actions = [
  {
    title: "Create student",
    description: "Register a new student profile and link it to a user account.",
  },
  {
    title: "Assign teacher",
    description: "Add or update classroom teachers and their subjects.",
  },
  {
    title: "Manage roles",
    description: "Grant or revoke roles and permissions across the system.",
  },
  {
    title: "Review enrollments",
    description: "Track classroom rosters and qualification audits.",
  },
];

const AdminDashboardScreen: React.FC = () => {
  return (
    <FlatList
      style={styles.container}
      contentContainerStyle={styles.content}
      data={actions}
      keyExtractor={(item) => item.title}
      ListHeaderComponent={
        <View style={styles.header}>
          <Text style={styles.title}>Admin shortcuts</Text>
          <Text style={styles.subtitle}>
            Quickly jump into the most common administration workflows.
          </Text>
        </View>
      }
      renderItem={({ item }) => (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>{item.title}</Text>
          <Text style={styles.cardDescription}>{item.description}</Text>
        </View>
      )}
    />
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F9FAFB",
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 8,
  },
  subtitle: {
    color: "#6B7280",
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: "#E5E7EB",
    marginBottom: 16,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 8,
  },
  cardDescription: {
    color: "#4B5563",
  },
});

export default AdminDashboardScreen;

