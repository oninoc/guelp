import React from "react";
import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useLocalSearchParams, useRouter } from "expo-router";
import { fetchStudentSubjectQualifications } from "@/lib/api/students";
import { useAuth } from "@/lib/hooks/useAuth";
import { StudentSubjectQualification } from "@/lib/types/api";

const StudentSubjectDetailScreen: React.FC = () => {
  const { subjectId: subjectIdParam, subjectName: subjectNameParam } = useLocalSearchParams<{
    subjectId?: string;
    subjectName?: string;
  }>();
  const router = useRouter();
  const { user } = useAuth();
  const parsedSubjectId = subjectIdParam ? Number(subjectIdParam) : undefined;
  const subjectId = parsedSubjectId && !Number.isNaN(parsedSubjectId) ? parsedSubjectId : undefined;
  const subjectName = subjectNameParam ? decodeURIComponent(subjectNameParam) : undefined;

  const studentId = user?.studentId ?? null;

  const { data, isLoading } = useQuery({
    queryKey: ["student-subject-qualifications", studentId, subjectId],
    queryFn: () => {
      if (!studentId) {
        throw new Error("Missing student identifier");
      }
      return fetchStudentSubjectQualifications(studentId, false);
    },
    enabled: Boolean(studentId && subjectId),
  });

  const qualification = data?.subjects.find(
    (item) =>
      item.subject_id === subjectId || item.classroom_subject_id === subjectId
  );

  const handleViewHistory = (item: StudentSubjectQualification) => {
    const targetId = item.subject_id ?? item.classroom_subject_id;
    if (!targetId) {
      return;
    }
    const encodedName = encodeURIComponent(item.subject_name ?? subjectName ?? "");
    router.push(
      `/student/subject/${encodeURIComponent(String(targetId))}/history?subjectName=${encodedName}`
    );
  };

  if (!qualification && !isLoading) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{subjectName ?? "Asignatura"}</Text>
        <Text style={styles.message}>Aún no hay datos de calificaciones.</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{subjectName ?? qualification?.subject_name ?? "Asignatura"}</Text>
      {qualification ? (
        <View style={styles.card}>
          <Text style={styles.label}>Calificación actual</Text>
          <Text style={styles.value}>
            {qualification.current_qualification ?? "Sin calificar"}
          </Text>
          <Text style={styles.label}>Estado</Text>
          <Text style={styles.value}>{qualification.status ?? "Pendiente"}</Text>
          <Text style={styles.label}>Notas</Text>
          <Text style={styles.value}>{qualification.description ?? "—"}</Text>
          <Pressable
            onPress={() => handleViewHistory(qualification)}
            style={({ pressed }) => [styles.button, pressed && styles.buttonPressed]}
            accessibilityRole="button"
          >
            <Text style={styles.buttonLabel}>Ver historial completo</Text>
          </Pressable>
        </View>
      ) : (
        <Text style={styles.message}>
          {isLoading ? "Cargando calificación…" : "Calificación no disponible."}
        </Text>
      )}
      <FlatList
        data={qualification?.records ?? []}
        keyExtractor={(item, index) => `${item.id ?? index}`}
        ListHeaderComponent={
          qualification?.records?.length ? (
            <Text style={styles.subheading}>Actualizaciones recientes</Text>
          ) : null
        }
        renderItem={({ item }) => (
          <View style={styles.record}>
            <View style={styles.recordHeader}>
              <Text style={styles.recordGrade}>{item.grade ?? "—"}</Text>
              <Text style={styles.recordTeacher}>
                {item.teacher_full_name ?? "Docente"}
              </Text>
            </View>
            <Text style={styles.recordDescription}>
              {item.description && item.description.trim().length > 0 ? item.description : "Sin notas"}
            </Text>
            {item.created_at ? (
              <Text style={styles.recordDate}>{item.created_at}</Text>
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
  card: {
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#E5E7EB",
    padding: 16,
    marginBottom: 24,
    backgroundColor: "#F9FAFB",
  },
  label: {
    fontSize: 14,
    color: "#6B7280",
    marginBottom: 4,
  },
  value: {
    fontSize: 18,
    fontWeight: "500",
    marginBottom: 12,
  },
  button: {
    backgroundColor: "#2563EB",
    borderRadius: 8,
    alignItems: "center",
    paddingVertical: 12,
    marginTop: 8,
  },
  buttonLabel: {
    color: "#FFFFFF",
    fontWeight: "600",
  },
  buttonPressed: {
    opacity: 0.92,
  },
  subheading: {
    fontSize: 20,
    fontWeight: "600",
    marginBottom: 12,
  },
  record: {
    paddingVertical: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: "#E5E7EB",
  },
  recordHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 4,
    gap: 12,
  },
  recordGrade: {
    fontWeight: "700",
    fontSize: 18,
    color: "#2563EB",
  },
  recordTeacher: {
    fontWeight: "600",
    flex: 1,
  },
  recordDescription: {
    color: "#374151",
  },
  recordDate: {
    marginTop: 4,
    fontSize: 12,
    color: "#6B7280",
  },
  message: {
    fontSize: 16,
    color: "#6B7280",
  },
});

export default StudentSubjectDetailScreen;

