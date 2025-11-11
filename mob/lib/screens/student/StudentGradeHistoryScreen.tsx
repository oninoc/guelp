import React from "react";
import { FlatList, StyleSheet, Text, View } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useLocalSearchParams } from "expo-router";
import { useAuth } from "@/lib/hooks/useAuth";
import { fetchStudentSubjectQualifications } from "@/lib/api/students";

const StudentGradeHistoryScreen: React.FC = () => {
  const { subjectId: subjectIdParam, subjectName: subjectNameParam } = useLocalSearchParams<{
    subjectId?: string;
    subjectName?: string;
  }>();
  const { user } = useAuth();
  const parsedSubjectId = subjectIdParam ? Number(subjectIdParam) : undefined;
  const subjectId =
    parsedSubjectId && !Number.isNaN(parsedSubjectId) ? parsedSubjectId : undefined;
  const subjectName = subjectNameParam ? decodeURIComponent(subjectNameParam) : undefined;

  const studentId = user?.studentId ?? null;

  const { data, isLoading } = useQuery({
    queryKey: ["student-subject-qualifications", studentId, subjectId, "history"],
    queryFn: () => {
      if (!studentId) {
        throw new Error("Missing student identifier");
      }
      return fetchStudentSubjectQualifications(studentId, true);
    },
    enabled: Boolean(studentId && subjectId),
  });

  const records = data?.subjects.find(
    (subject) =>
      subject.subject_id === subjectId || subject.classroom_subject_id === subjectId
  )?.records;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{subjectName ?? "Historial de calificaciones"}</Text>
      <FlatList
        data={records ?? []}
        keyExtractor={(item, index) => `${item.id ?? index}`}
        ListEmptyComponent={
          <Text style={styles.empty}>
            {isLoading ? "Cargando historial de calificaciones…" : "No se encontraron calificaciones históricas."}
          </Text>
        }
        renderItem={({ item }) => (
          <View style={styles.row}>
            <View style={styles.rowHeader}>
              <Text style={styles.grade}>{item.grade ?? "—"}</Text>
              <Text style={styles.teacher}>{item.teacher_full_name ?? "Docente"}</Text>
            </View>
            <Text style={styles.description}>
              {item.description && item.description.trim().length > 0 ? item.description : "Sin notas"}
            </Text>
            {item.created_at ? (
              <Text style={styles.date}>{item.created_at}</Text>
            ) : null}
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 16,
  },
  row: {
    paddingVertical: 16,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: "#E5E7EB",
  },
  rowHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    marginBottom: 6,
  },
  grade: {
    fontWeight: "700",
    fontSize: 18,
    color: "#2563EB",
  },
  teacher: {
    fontWeight: "600",
    flex: 1,
  },
  description: {
    color: "#4B5563",
  },
  date: {
    marginTop: 4,
    color: "#6B7280",
    fontSize: 12,
  },
  empty: {
    textAlign: "center",
    color: "#6B7280",
    marginTop: 64,
  },
});

export default StudentGradeHistoryScreen;

