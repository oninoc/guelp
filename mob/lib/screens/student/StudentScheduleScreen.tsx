import React from "react";
import { FlatList, StyleSheet, Text, View } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useAuth } from "@/lib/hooks/useAuth";
import { fetchStudentSubjects } from "@/lib/api/students";

type ScheduleItem = {
  id: string;
  subjectName: string;
  classroom: string;
  teacher: string;
  status: string;
  isActive: boolean;
};

const StudentScheduleScreen: React.FC = () => {
  const { user } = useAuth();

  const studentId = user?.studentId ?? null;

  const { data, isLoading, refetch } = useQuery({
    queryKey: ["student-schedule", studentId],
    queryFn: () => {
      if (!studentId) {
        throw new Error("Missing student identifier");
      }
      return fetchStudentSubjects(studentId, true);
    },
    enabled: Boolean(studentId),
  });

  const schedule: ScheduleItem[] =
    data?.subjects.map((subject) => ({
      id: `${subject.classroom_subject_student_id}`,
      subjectName: subject.subject_name ?? "Asignatura",
      classroom: `${subject.classroom_level ?? ""} ${subject.classroom_degree ?? ""}`.trim(),
      teacher: subject.teacher_full_name ?? "Por asignar",
      status: subject.status ?? (subject.is_active ? "Activa" : "Inactiva"),
      isActive: subject.is_active,
    })) ?? [];

  return (
    <FlatList
      style={styles.container}
      contentContainerStyle={styles.content}
      data={schedule}
      keyExtractor={(item) => item.id}
      refreshing={isLoading}
      onRefresh={refetch}
      ListHeaderComponent={<Text style={styles.title}>Horario</Text>}
      ListEmptyComponent={
        <Text style={styles.empty}>
          {isLoading ? "Cargando horario…" : "No hay clases programadas."}
        </Text>
      }
      renderItem={({ item }) => (
        <View
          style={[
            styles.card,
            !item.isActive && styles.cardInactive,
          ]}
        >
          <Text style={styles.subject}>{item.subjectName}</Text>
          <Text style={styles.meta}>Aula: {item.classroom || "Por asignar"}</Text>
          <Text style={styles.meta}>Docente: {item.teacher}</Text>
          <Text style={[styles.status, !item.isActive && styles.statusInactive]}>
            {item.status}
          </Text>
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
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 16,
  },
  empty: {
    textAlign: "center",
    color: "#6B7280",
    marginTop: 64,
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  cardInactive: {
    opacity: 0.75,
  },
  subject: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 8,
  },
  meta: {
    color: "#4B5563",
    marginBottom: 4,
  },
  status: {
    marginTop: 8,
    fontWeight: "600",
    color: "#047857",
  },
  statusInactive: {
    color: "#B91C1C",
  },
});

export default StudentScheduleScreen;

