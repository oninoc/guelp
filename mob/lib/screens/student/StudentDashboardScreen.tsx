import React from "react";
import { FlatList, Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "expo-router";
import { useAuth } from "@/lib/hooks/useAuth";
import { fetchStudentSubjects } from "@/lib/api/students";
import { StudentSubjectSummary } from "@/lib/types/api";

const StudentDashboardScreen: React.FC = () => {
  const { user } = useAuth();
  const router = useRouter();
  const [includeInactive, setIncludeInactive] = React.useState(false);

  const studentId = user?.studentId ?? null;

  const { data, isLoading, refetch } = useQuery({
    queryKey: ["student-subjects", studentId, includeInactive],
    queryFn: () => {
      if (!studentId) {
        throw new Error("Missing student identifier");
      }
      return fetchStudentSubjects(studentId, includeInactive);
    },
    enabled: Boolean(studentId),
  });

  const handleToggle = () => {
    setIncludeInactive((current) => !current);
  };

  const handleSelect = (subject: StudentSubjectSummary) => {
    const subjectId = subject.subject_id ?? subject.classroom_subject_id;
    if (!subjectId) {
      return;
    }
    const encodedName = encodeURIComponent(subject.subject_name ?? "");
    router.push(`/student/subject/${encodeURIComponent(String(subjectId))}?subjectName=${encodedName}`);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Asignaturas</Text>
        <View style={styles.toggleRow}>
          <Text style={styles.toggleLabel}>Mostrar inactivas</Text>
          <Switch
            value={includeInactive}
            onValueChange={handleToggle}
            accessibilityLabel="Alternar asignaturas inactivas"
          />
        </View>
      </View>
      <FlatList
        data={data?.subjects ?? []}
        keyExtractor={(subject) =>
          `${subject.classroom_subject_student_id}-${subject.subject_id ?? "unknown"}`
        }
        refreshing={isLoading}
        onRefresh={refetch}
        ListEmptyComponent={
          <Text style={styles.empty}>
            {isLoading ? "Cargando asignaturas…" : "No se encontraron asignaturas."}
          </Text>
        }
        renderItem={({ item }) => (
          <Pressable
            onPress={() => handleSelect(item)}
            style={({ pressed }) => [styles.card, pressed && styles.cardPressed]}
            accessibilityRole="button"
          >
            <Text style={styles.cardTitle}>{item.subject_name ?? "Asignatura sin nombre"}</Text>
            <Text style={styles.cardSubtitle}>
              {item.classroom_level ?? "—"} {item.classroom_degree ?? ""}
            </Text>
            <Text style={styles.cardMeta}>
              Docente: {item.teacher_full_name ?? "Por asignar"}
            </Text>
            <Text style={[styles.status, !item.is_active && styles.inactive]}>
              {item.status ?? (item.is_active ? "Activa" : "Inactiva")}
            </Text>
          </Pressable>
        )}
        contentContainerStyle={styles.listContent}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F9FAFB",
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 24,
    paddingBottom: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 12,
  },
  toggleRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  toggleLabel: {
    fontSize: 16,
  },
  listContent: {
    padding: 20,
    paddingBottom: 32,
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 3,
    elevation: 2,
  },
  cardPressed: {
    opacity: 0.9,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 4,
  },
  cardSubtitle: {
    color: "#6B7280",
    marginBottom: 4,
  },
  cardMeta: {
    color: "#6B7280",
    marginBottom: 8,
  },
  status: {
    fontWeight: "600",
    color: "#047857",
  },
  inactive: {
    color: "#B91C1C",
  },
  empty: {
    textAlign: "center",
    color: "#6B7280",
    marginTop: 64,
  },
});

export default StudentDashboardScreen;

