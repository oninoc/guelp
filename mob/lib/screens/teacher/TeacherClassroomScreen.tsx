import React from "react";
import { ActivityIndicator, FlatList, Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useLocalSearchParams, useRouter } from "expo-router";

import { useAuth } from "@/lib/hooks/useAuth";
import { fetchTeacherClassroomStudents } from "@/lib/api/teachers";
import {
  GradeLetter,
  TeacherClassroomStudentSubjectSummary,
  TeacherClassroomStudentSummary,
  TeacherQualificationRecordSummary,
} from "@/lib/types/api";

type RosterRow = {
  key: string;
  studentId: string;
  name: string;
  code: string;
  gradeLabel: string;
  averageScore?: number | null;
  canManage: boolean;
  classroomSubjectStudentId?: number;
  history: TeacherQualificationRecordSummary[];
};

const TeacherClassroomScreen: React.FC = () => {
  const router = useRouter();
  const {
    classroomId: classroomIdParam,
    description: descriptionParam,
    classroomSubjectId: classroomSubjectIdParam,
    subjectName: subjectNameParam,
  } = useLocalSearchParams<{
    classroomId?: string;
    description?: string;
    classroomSubjectId?: string;
    subjectName?: string;
  }>();

  const classroomId = classroomIdParam
    ? decodeURIComponent(classroomIdParam)
    : "";
  const description = descriptionParam
    ? decodeURIComponent(descriptionParam)
    : "Aula";
  const parsedClassroomSubjectId = classroomSubjectIdParam
    ? Number(classroomSubjectIdParam)
    : undefined;
  const selectedClassroomSubjectId =
    parsedClassroomSubjectId !== undefined && !Number.isNaN(parsedClassroomSubjectId)
      ? parsedClassroomSubjectId
      : undefined;
  const subjectName = subjectNameParam
    ? decodeURIComponent(subjectNameParam)
    : undefined;

  const { user } = useAuth();
  const teacherId = user?.teacherId ?? null;

  const [includeInactive, setIncludeInactive] = React.useState(false);

  const {
    data: rosterData,
    isLoading,
    isFetching,
    refetch,
  } = useQuery({
    queryKey: [
      "teacher-classroom-students",
      teacherId,
      classroomId,
      includeInactive,
    ],
    queryFn: () => {
      if (!teacherId || !classroomId) {
        throw new Error("Missing identifiers for classroom roster.");
      }
      return fetchTeacherClassroomStudents(
        teacherId,
        classroomId,
        includeInactive
      );
    },
    enabled: Boolean(teacherId && classroomId),
    refetchOnMount: "always",
    refetchOnWindowFocus: true,
  });

  const students = rosterData?.students ?? [];

  const gradeFromScore = React.useCallback((score?: number | null): GradeLetter | null => {
    if (score === undefined || score === null) {
      return null;
    }
    const thresholds: Array<{ grade: GradeLetter; value: number }> = [
      { grade: "AD", value: 20 },
      { grade: "A", value: 17 },
      { grade: "B", value: 14 },
      { grade: "C", value: 10 },
      { grade: "D", value: 5 },
    ];
    for (let index = 0; index < thresholds.length; index += 1) {
      const current = thresholds[index];
      const next = thresholds[index + 1];
      if (!next) {
        return current.grade;
      }
      const midpoint = (current.value + next.value) / 2;
      if (score >= midpoint) {
        return current.grade;
      }
    }
    return thresholds[thresholds.length - 1].grade;
  }, []);

  const rosterRows = React.useMemo<RosterRow[]>(() => {
    if (!students.length) {
      return [];
    }

    if (selectedClassroomSubjectId) {
      return students
        .map((student: TeacherClassroomStudentSummary) => {
          const subject = student.subjects.find(
            (entry: TeacherClassroomStudentSubjectSummary) =>
              entry.classroom_subject_id === selectedClassroomSubjectId
          );
          if (!subject) {
            return null;
          }
          return {
            key: `${student.student_id}-${subject.classroom_subject_student_id}`,
            studentId: student.student_id,
            name: student.full_name,
            code: student.student_code,
            gradeLabel:
              subject.average_grade ??
              gradeFromScore(subject.average_score) ??
              "—",
            averageScore: subject.average_score,
            canManage: subject.can_manage,
            classroomSubjectStudentId: subject.classroom_subject_student_id,
            history: subject.history ?? [],
          };
        })
        .filter(Boolean) as RosterRow[];
    }

    return students.map((student: TeacherClassroomStudentSummary) => ({
      key: student.student_id,
      studentId: student.student_id,
      name: student.full_name,
      code: student.student_code,
      gradeLabel: gradeFromScore(student.average_qualification) ?? "—",
      averageScore: student.average_qualification,
      canManage: false,
      history: [],
    }));
  }, [students, selectedClassroomSubjectId, gradeFromScore]);

  const handleOpenGrading = (row: RosterRow) => {
    if (!teacherId || !row.classroomSubjectStudentId || !row.canManage) {
      return;
    }
    const encodedSubjectName = encodeURIComponent(subjectName ?? "Asignatura");
    const encodedQualification = encodeURIComponent(row.gradeLabel ?? "");
    const encodedHistory = encodeURIComponent(JSON.stringify(row.history ?? []));
    const encodedStudentName = encodeURIComponent(row.name);
    const encodedStudentCode = encodeURIComponent(row.code);
    const encodedClassroomId = encodeURIComponent(classroomId);
    const encodedClassroomSubjectId = encodeURIComponent(
      String(selectedClassroomSubjectId ?? "")
    );
    const encodedStudentId = encodeURIComponent(row.studentId);
    const averageScoreParam =
      row.averageScore !== undefined && row.averageScore !== null
        ? `&averageScore=${row.averageScore}`
        : "";

    router.push(
      `/teacher/classroom/${encodedClassroomId}/grading/${row.classroomSubjectStudentId}?subjectName=${encodedSubjectName}&initialQualification=${encodedQualification}&history=${encodedHistory}&studentName=${encodedStudentName}&studentCode=${encodedStudentCode}&classroomSubjectId=${encodedClassroomSubjectId}&studentId=${encodedStudentId}&classroomId=${encodedClassroomId}${averageScoreParam}`
    );
  };

  const renderRosterRow = ({ item }: { item: RosterRow }) => (
    <Pressable
      onPress={() => handleOpenGrading(item)}
      disabled={!item.canManage}
      style={({ pressed }) => [
        styles.studentRow,
        pressed && item.canManage && styles.studentRowPressed,
      ]}
      accessibilityRole={item.canManage ? "button" : undefined}
    >
      <Text style={styles.studentName}>
        {item.code ? `${item.name} · ${item.code}` : item.name}
      </Text>
      <Text
        style={[
          styles.studentGrade,
          !item.canManage && styles.studentGradeReadOnly,
        ]}
      >
        {item.averageScore !== undefined && item.averageScore !== null
          ? `${item.gradeLabel} (${item.averageScore.toFixed(1)})`
          : item.gradeLabel}
      </Text>
    </Pressable>
  );

  if (!classroomId) {
    return (
      <View style={[styles.container, styles.missing]}>
        <Text style={styles.warning}>Falta el identificador del aula.</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{description}</Text>
        {subjectName ? (
          <Text style={styles.subtitle}>Asignatura: {subjectName}</Text>
        ) : null}
        <View style={styles.toggleRow}>
          <Text style={styles.toggleLabel}>Mostrar inscripciones inactivas</Text>
          <Switch
            value={includeInactive}
            onValueChange={setIncludeInactive}
            accessibilityLabel="Alternar inscripciones inactivas"
          />
        </View>
      </View>
      {isLoading ? (
        <View style={styles.loading}>
          <ActivityIndicator size="large" color="#2563EB" />
        </View>
      ) : (
        <FlatList
          data={rosterRows}
          keyExtractor={(item) => item.key}
          refreshing={isFetching}
          onRefresh={refetch}
          contentContainerStyle={styles.list}
          ListEmptyComponent={
            <Text style={styles.empty}>
              No se encontraron estudiantes para este aula.
            </Text>
          }
          renderItem={renderRosterRow}
        />
      )}
      {!selectedClassroomSubjectId && subjectName && (
        <Text style={styles.infoNote}>
          Selecciona una asignatura específica desde el panel para gestionar calificaciones.
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 24,
    paddingBottom: 16,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: "#E5E7EB",
  },
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 4,
  },
  subtitle: {
    color: "#4B5563",
    marginBottom: 16,
    fontSize: 16,
  },
  toggleRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  toggleLabel: {
    color: "#374151",
    fontSize: 16,
  },
  list: {
    padding: 20,
  },
  loading: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  empty: {
    textAlign: "center",
    color: "#6B7280",
    marginTop: 32,
  },
  studentRow: {
    borderWidth: 1,
    borderColor: "#E5E7EB",
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    marginBottom: 12,
    backgroundColor: "#FFFFFF",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  studentRowPressed: {
    opacity: 0.92,
  },
  studentName: {
    fontSize: 18,
    fontWeight: "600",
    flex: 1,
    marginRight: 12,
  },
  studentGrade: {
    fontSize: 18,
    fontWeight: "700",
    color: "#111827",
  },
  studentGradeReadOnly: {
    color: "#9CA3AF",
  },
  warning: {
    color: "#DC2626",
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  missing: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  infoNote: {
    padding: 20,
    color: "#6B7280",
    textAlign: "center",
  },
});

export default TeacherClassroomScreen;

