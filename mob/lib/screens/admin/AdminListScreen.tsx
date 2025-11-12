import React from "react";
import {
  FlatList,
  StyleSheet,
  Text,
  View,
  Pressable,
  Alert,
  Platform,
} from "react-native";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchAllStudents,
  fetchAllTeachers,
  fetchAllSubjects,
  fetchAllClassrooms,
  deleteStudent,
  deleteTeacher,
  deleteSubject,
  deleteClassroom,
} from "@/lib/api/admin";

type EntityType = "student" | "teacher" | "subject" | "classroom";

type AdminListScreenProps = {
  entityType: EntityType;
  onEdit?: (id: string | number) => void;
  onCreate?: () => void;
};

export const AdminListScreen: React.FC<AdminListScreenProps> = ({
  entityType,
  onEdit,
  onCreate,
}) => {
  const queryClient = useQueryClient();

  const getQueryKey = () => {
    switch (entityType) {
      case "student":
        return ["admin-students"];
      case "teacher":
        return ["admin-teachers"];
      case "subject":
        return ["admin-subjects"];
      case "classroom":
        return ["admin-classrooms"];
    }
  };

  const getFetchFn = () => {
    switch (entityType) {
      case "student":
        return fetchAllStudents;
      case "teacher":
        return fetchAllTeachers;
      case "subject":
        return fetchAllSubjects;
      case "classroom":
        return fetchAllClassrooms;
    }
  };

  const getDeleteFn = () => {
    switch (entityType) {
      case "student":
        return deleteStudent;
      case "teacher":
        return deleteTeacher;
      case "subject":
        return deleteSubject;
      case "classroom":
        return deleteClassroom;
    }
  };

  const getTitle = () => {
    switch (entityType) {
      case "student":
        return "Students";
      case "teacher":
        return "Teachers";
      case "subject":
        return "Subjects";
      case "classroom":
        return "Classrooms";
    }
  };

  const { data, isLoading, refetch } = useQuery({
    queryKey: getQueryKey(),
    queryFn: getFetchFn(),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string | number) => getDeleteFn()(id as any),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: getQueryKey() });
      Alert.alert("Success", `${getTitle().slice(0, -1)} deleted successfully`);
    },
    onError: (error: any) => {
      Alert.alert("Error", error?.response?.data?.detail || "Failed to delete");
    },
  });

  const handleDelete = (id: string | number, name: string) => {
    const confirmDelete = () => {
      deleteMutation.mutate(id);
    };

    if (Platform.OS === "web") {
      if (window.confirm(`Are you sure you want to delete ${name}?`)) {
        confirmDelete();
      }
    } else {
      Alert.alert(
        "Confirm Delete",
        `Are you sure you want to delete ${name}?`,
        [
          { text: "Cancel", style: "cancel" },
          { text: "Delete", onPress: confirmDelete, style: "destructive" },
        ]
      );
    }
  };

  const renderItem = ({ item }: { item: any }) => {
    let displayName = "";
    let subtitle = "";

    switch (entityType) {
      case "student":
        displayName = `${item.names} ${item.father_last_name} ${item.mother_last_name}`.trim();
        subtitle = item.code || item.email || "";
        break;
      case "teacher":
        displayName = `${item.names} ${item.father_last_name} ${item.mother_last_name}`.trim();
        subtitle = item.document_number || "";
        break;
      case "subject":
        displayName = item.name;
        subtitle = item.description || "";
        break;
      case "classroom":
        displayName = item.description;
        subtitle = `${item.level} ${item.degree}`.trim() + (item.tutor_name ? ` - ${item.tutor_name}` : "");
        break;
    }

    return (
      <View style={styles.item}>
        <Pressable
          style={styles.itemContent}
          onPress={() => onEdit?.(item.id)}
        >
          <View style={styles.itemText}>
            <Text style={styles.itemTitle}>{displayName}</Text>
            {subtitle ? <Text style={styles.itemSubtitle}>{subtitle}</Text> : null}
          </View>
        </Pressable>
        <View style={styles.itemActions}>
          {onEdit && (
            <Pressable
              style={[styles.actionButton, styles.editButton]}
              onPress={() => onEdit(item.id)}
            >
              <Text style={styles.actionButtonText}>Edit</Text>
            </Pressable>
          )}
          <Pressable
            style={[styles.actionButton, styles.deleteButton]}
            onPress={() => handleDelete(item.id, displayName)}
          >
            <Text style={[styles.actionButtonText, styles.deleteButtonText]}>
              Delete
            </Text>
          </Pressable>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{getTitle()}</Text>
        {onCreate && (
          <Pressable style={styles.createButton} onPress={onCreate}>
            <Text style={styles.createButtonText}>+ Create</Text>
          </Pressable>
        )}
      </View>
      <FlatList
        data={data || []}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderItem}
        refreshing={isLoading}
        onRefresh={refetch}
        ListEmptyComponent={
          <Text style={styles.empty}>
            {isLoading ? "Loading..." : `No ${getTitle().toLowerCase()} found`}
          </Text>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#000",
  },
  createButton: {
    backgroundColor: "#007AFF",
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  createButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  item: {
    flexDirection: "row",
    alignItems: "center",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
  itemContent: {
    flex: 1,
  },
  itemText: {
    flex: 1,
  },
  itemTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#000",
    marginBottom: 4,
  },
  itemSubtitle: {
    fontSize: 14,
    color: "#666",
  },
  itemActions: {
    flexDirection: "row",
    gap: 8,
  },
  actionButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  editButton: {
    backgroundColor: "#007AFF",
  },
  deleteButton: {
    backgroundColor: "#FF3B30",
  },
  actionButtonText: {
    color: "#fff",
    fontSize: 14,
    fontWeight: "600",
  },
  deleteButtonText: {
    color: "#fff",
  },
  empty: {
    textAlign: "center",
    marginTop: 32,
    fontSize: 16,
    color: "#999",
  },
});

