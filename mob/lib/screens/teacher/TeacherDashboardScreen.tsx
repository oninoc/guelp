import React from "react";
import { FlatList, Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "expo-router";
import { useAuth } from "@/lib/hooks/useAuth";
import { fetchTeacherClassrooms } from "@/lib/api/teachers";
import { TeacherClassroomSummary, TeacherClassroomSubject } from "@/lib/types/api";

type TeacherSubjectCard = {
  classroomId: string;
  classroomSubjectId: number;
  classroomDescription: string;
  level: string;
  degree: string;
  subjectName: string;
  isActive: boolean;
  isTutor: boolean;
  isSubstitute: boolean;
  teacherName?: string | null;
  canManage: boolean;
};

const TeacherDashboardScreen: React.FC = () => {
  const { user } = useAuth();
  const teacherId = user?.teacherId ?? null;
  const router = useRouter();
  const [includeInactive, setIncludeInactive] = React.useState(false);

  const { data, isLoading, refetch } = useQuery({
    queryKey: ["teacher-classrooms", teacherId, includeInactive],
    queryFn: () => {
      if (!teacherId) {
        throw new Error("Missing teacher identifier");
      }
      return fetchTeacherClassrooms(teacherId, includeInactive);
    },
    enabled: Boolean(teacherId),
  });

  const handleToggle = () => setIncludeInactive((previous) => !previous);

  const flattenedSubjects = React.useMemo<TeacherSubjectCard[]>(() => {
    if (!data?.classrooms?.length || !teacherId) {
      return [];
    }
    const cards: TeacherSubjectCard[] = [];
    data.classrooms.forEach((classroom: TeacherClassroomSummary) => {
      classroom.subjects.forEach((subject: TeacherClassroomSubject) => {
        const canManage =
          subject.is_substitute ||
          !subject.teacher_id ||
          subject.teacher_id === teacherId;
        cards.push({
          classroomId: classroom.classroom_id,
          classroomSubjectId: subject.classroom_subject_id,
          classroomDescription: classroom.description,
          level: classroom.level,
          degree: classroom.degree,
          subjectName: subject.subject_name,
          isActive: subject.is_active,
          isTutor: classroom.is_tutor,
          isSubstitute: subject.is_substitute,
          teacherName: subject.teacher_name,
          canManage,
        });
      });
    });
    return cards.sort((a, b) =>
      `${a.classroomDescription}-${a.subjectName}`.localeCompare(
        `${b.classroomDescription}-${b.subjectName}`
      )
    );
  }, [data?.classrooms, teacherId]);

  const handlePress = (subjectCard: TeacherSubjectCard) => {
    const encodedDescription = encodeURIComponent(subjectCard.classroomDescription);
    const encodedClassroomId = encodeURIComponent(subjectCard.classroomId);
    const encodedSubjectName = encodeURIComponent(subjectCard.subjectName);
    router.push(
      `/teacher/classroom/${encodedClassroomId}/subject/${subjectCard.classroomSubjectId}?description=${encodedDescription}&subjectName=${encodedSubjectName}`
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Mis clases</Text>
        <View style={styles.toggleRow}>
          <Text style={styles.toggleLabel}>Mostrar inactivas</Text>
          <Switch
            value={includeInactive}
            onValueChange={handleToggle}
            accessibilityLabel="Alternar clases inactivas"
          />
        </View>
      </View>
      <FlatList
        data={flattenedSubjects}
        keyExtractor={(item) =>
          `${item.classroomId}-${item.classroomSubjectId}`
        }
        refreshing={isLoading}
        onRefresh={refetch}
        ListEmptyComponent={
          <Text style={styles.empty}>
            {isLoading
              ? "Cargando asignaciones…"
              : "No hay asignaturas asignadas."}
          </Text>
        }
        renderItem={({ item }) => (
          <Pressable
            onPress={() => handlePress(item)}
            style={({ pressed }) => [styles.card, pressed && styles.cardPressed]}
            accessibilityRole="button"
          >
            <Text style={styles.cardTitle}>{item.classroomDescription}</Text>
            <Text style={styles.cardSubtitle}>
              {item.level} · {item.degree}
            </Text>
            <Text style={styles.cardMeta}>
              Asignatura: {item.subjectName}
            </Text>
            <Text style={styles.cardMeta}>
              {item.isActive ? "Activa" : "Inactiva"}
            </Text>
            <View style={styles.badgeRow}>
              {item.isTutor ? <Text style={[styles.badge, styles.badgeTutor]}>Tutor</Text> : null}
              {item.isSubstitute ? (
                <Text style={[styles.badge, styles.badgeSubstitute]}>Suplente</Text>
              ) : null}
              {!item.canManage ? (
                <Text style={[styles.badge, styles.badgeReadOnly]}>Solo lectura</Text>
              ) : null}
            </View>
            {item.teacherName ? (
              <Text style={styles.cardMeta}>Asignada a: {item.teacherName}</Text>
            ) : null}
          </Pressable>
        )}
        contentContainerStyle={styles.list}
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
    marginBottom: 8,
  },
  toggleRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  toggleLabel: {
    fontSize: 16,
  },
  list: {
    padding: 20,
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
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 3,
    elevation: 1,
  },
  cardPressed: {
    opacity: 0.92,
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
  },
  badgeRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginTop: 8,
    gap: 8,
  },
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 999,
    fontSize: 12,
    fontWeight: "600",
  },
  badgeTutor: {
    backgroundColor: "#DBEAFE",
    color: "#1D4ED8",
  },
  badgeSubstitute: {
    backgroundColor: "#FEF3C7",
    color: "#B45309",
  },
  badgeReadOnly: {
    backgroundColor: "#F3F4F6",
    color: "#4B5563",
  },
});

export default TeacherDashboardScreen;

