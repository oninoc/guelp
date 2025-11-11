import React from "react";
import { Alert, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { MaterialIcons } from "@expo/vector-icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useLocalSearchParams } from "expo-router";
import { fetchTeacherClassroomStudents, updateStudentQualification, deleteTeacherQualification } from "@/lib/api/teachers";
import { GradeLetter, TeacherQualificationRecordSummary } from "@/lib/types/api";
import { useAuth } from "@/lib/hooks/useAuth";

const GRADE_SCALE: Array<{ grade: GradeLetter; value: number }> = [
  { grade: "AD", value: 20 },
  { grade: "A", value: 17 },
  { grade: "B", value: 14 },
  { grade: "C", value: 10 },
  { grade: "D", value: 5 },
];

const gradeFromScore = (score?: number | null): GradeLetter | null => {
  if (score === undefined || score === null) {
    return null;
  }
  for (let index = 0; index < GRADE_SCALE.length; index += 1) {
    const current = GRADE_SCALE[index];
    const next = GRADE_SCALE[index + 1];
    if (!next) {
      return current.grade;
    }
    const midpoint = (current.value + next.value) / 2;
    if (score >= midpoint) {
      return current.grade;
    }
  }
  return GRADE_SCALE[GRADE_SCALE.length - 1].grade;
};

const TeacherGradingScreen: React.FC = () => {
  const {
    classroomSubjectStudentId: idParam,
    subjectName: subjectNameParam,
    initialQualification: initialQualificationParam,
    history: historyParam,
    studentName: studentNameParam,
    studentCode: studentCodeParam,
    classroomSubjectId: classroomSubjectIdParam,
    studentId: studentIdParam,
    classroomId: classroomIdParam,
    averageScore: averageScoreParam,
  } = useLocalSearchParams<{
    classroomSubjectStudentId?: string;
    subjectName?: string;
    initialQualification?: string;
    history?: string;
    studentName?: string;
    studentCode?: string;
    classroomSubjectId?: string;
    studentId?: string;
    classroomId?: string;
    averageScore?: string;
  }>();
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const parsedEnrollmentId = idParam ? Number(idParam) : undefined;
  const classroomSubjectStudentId =
    parsedEnrollmentId && !Number.isNaN(parsedEnrollmentId) ? parsedEnrollmentId : undefined;
  const subjectName = subjectNameParam ? decodeURIComponent(subjectNameParam) : undefined;
  const studentName = studentNameParam ? decodeURIComponent(studentNameParam) : undefined;
  const studentCode = studentCodeParam ? decodeURIComponent(studentCodeParam) : undefined;
  const classroomSubjectId = classroomSubjectIdParam
    ? Number(classroomSubjectIdParam)
    : undefined;
  const studentId = studentIdParam ? decodeURIComponent(studentIdParam) : undefined;
  const classroomId = classroomIdParam ? decodeURIComponent(classroomIdParam) : undefined;
  const averageScoreInitial =
    averageScoreParam && !Number.isNaN(Number(averageScoreParam))
      ? Number(averageScoreParam)
      : null;

  const decodedQualification = initialQualificationParam
    ? decodeURIComponent(initialQualificationParam)
    : "";
  const allowedGrades: GradeLetter[] = ["AD", "A", "B", "C", "D"];
  const normalizedInitial = decodedQualification.toUpperCase();
  const initialGrade = allowedGrades.includes(normalizedInitial as GradeLetter)
    ? (normalizedInitial as GradeLetter)
    : null;

  const initialHistory: TeacherQualificationRecordSummary[] = React.useMemo(() => {
    if (!historyParam) {
      return [];
    }
    try {
      return JSON.parse(decodeURIComponent(historyParam));
    } catch (error) {
      console.warn("Failed to parse history", error);
      return [];
    }
  }, [historyParam]);

  const [historyRecords, setHistoryRecords] = React.useState<TeacherQualificationRecordSummary[]>(
    initialHistory
  );
  const [currentScore, setCurrentScore] = React.useState<number | null>(averageScoreInitial);
  const [currentGrade, setCurrentGrade] = React.useState<GradeLetter | null>(
    gradeFromScore(averageScoreInitial) ?? initialGrade
  );
  const [qualification, setQualification] = React.useState<GradeLetter | null>(
    gradeFromScore(averageScoreInitial) ?? initialGrade
  );
  const [description, setDescription] = React.useState("");
  const [feedbackMessage, setFeedbackMessage] = React.useState<string | null>(null);

  const { refetch: refetchRoster, isFetching: isRefreshingHistory } = useQuery({
    queryKey: [
      "teacher-classroom-student-history",
      user?.teacherId,
      classroomId,
      classroomSubjectStudentId,
    ],
    queryFn: () => {
      if (!user?.teacherId || !classroomId) {
        throw new Error("Missing identifiers for history refresh.");
      }
      return fetchTeacherClassroomStudents(user.teacherId, classroomId, true);
    },
    enabled: false,
  });

  const updateHistoryFromEnvelope = React.useCallback(
    (envelope?: Awaited<ReturnType<typeof fetchTeacherClassroomStudents>>) => {
      if (!envelope || !classroomSubjectStudentId) {
        return;
      }
      const studentMatch = envelope.students.find(
        (candidate) => candidate.student_id === studentId
      );
      if (!studentMatch) {
        return;
      }
      const subjectMatch = studentMatch.subjects.find(
        (candidate) =>
          candidate.classroom_subject_student_id === classroomSubjectStudentId
      );
      if (!subjectMatch) {
        return;
      }
      setHistoryRecords(subjectMatch.history ?? []);
      setCurrentScore(subjectMatch.average_score ?? null);
      const derivedGrade =
        subjectMatch.average_grade ??
        gradeFromScore(subjectMatch.average_score) ??
        (subjectMatch.qualification as GradeLetter | null) ??
        null;
      setCurrentGrade(derivedGrade);
      setQualification(derivedGrade);
    },
    [classroomSubjectStudentId, studentId]
  );

  const refreshHistory = React.useCallback(async () => {
    try {
      const result = await refetchRoster();
      if (result.data) {
        updateHistoryFromEnvelope(result.data);
      }
    } catch (error) {
      console.error("Failed to refresh history", error);
    }
  }, [refetchRoster, updateHistoryFromEnvelope]);

  const invalidateRelatedQueries = React.useCallback(() => {
    if (user?.teacherId) {
      queryClient.invalidateQueries({ queryKey: ["teacher-classroom-students"] });
      queryClient.invalidateQueries({ queryKey: ["teacher-classrooms"] });
    }
    if (studentId) {
      queryClient.invalidateQueries({ queryKey: ["student-subject-qualifications"] });
      queryClient.invalidateQueries({ queryKey: ["student-subjects"] });
      queryClient.invalidateQueries({ queryKey: ["student-schedule"] });
    }
  }, [queryClient, studentId, user?.teacherId]);

  const mutation = useMutation({
    mutationFn: () => {
      if (!user?.teacherId || !classroomSubjectStudentId) {
        throw new Error("Missing teacher identifier");
      }
      return updateStudentQualification(user.teacherId, {
        classroom_subject_student_id: classroomSubjectStudentId,
        qualification: qualification ?? undefined,
        description: description.trim() || undefined,
      });
    },
    onSuccess: async () => {
      Alert.alert("Calificación guardada", "El registro del estudiante ha sido actualizado.");
      setQualification(null);
      setDescription("");
      setFeedbackMessage("Calificación registrada correctamente.");
      invalidateRelatedQueries();
      await refreshHistory();
    },
    onError: (error) => {
      console.error("Error al actualizar la calificación", error);
      Alert.alert(
        "Error al actualizar",
        "No pudimos actualizar la calificación. Verifica tus permisos."
      );
      setFeedbackMessage("Hubo un error al guardar la calificación.");
    },
  });

  const handleSubmit = () => {
    setFeedbackMessage(null);
    const hasChanges = qualification !== null || description.trim().length > 0;
    if (!hasChanges) {
      setFeedbackMessage("Realiza un cambio antes de guardar.");
      return;
    }
    mutation.mutate();
  };

  const handleDelete = (recordId?: number | null) => {
    if (!recordId || !user?.teacherId) {
      return;
    }

    const performDelete = async () => {
      try {
        await deleteTeacherQualification(user.teacherId!, recordId);
        setHistoryRecords((previous) =>
          previous.filter((entry) => entry.id !== recordId)
        );
        setFeedbackMessage("Calificación eliminada.");
        invalidateRelatedQueries();
        await refreshHistory();
      } catch (error) {
        console.error("Error al eliminar calificación", error);
        Alert.alert(
          "Error al eliminar",
          "No fue posible eliminar la calificación. Inténtalo de nuevo."
        );
      }
    };

    if (Platform.OS === "web") {
      const confirmed =
        typeof window !== "undefined" &&
        window.confirm("Esta acción no se puede deshacer. ¿Deseas continuar?");
      if (confirmed) {
        void performDelete();
      }
      return;
    }

    Alert.alert(
      "Eliminar calificación",
      "Esta acción no se puede deshacer. ¿Deseas continuar?",
      [
        { text: "Cancelar", style: "cancel" },
        {
          text: "Eliminar",
          style: "destructive",
          onPress: () => void performDelete(),
        },
      ]
    );
  };

  if (!classroomSubjectStudentId) {
    return (
      <View style={[styles.container, styles.centered]}>
        <Text style={styles.errorText}>Falta el identificador de la inscripción.</Text>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.select({ ios: "padding", android: undefined })}
    >
      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        <Text style={styles.title}>{subjectName ?? "Actualizar calificación"}</Text>
        <View style={styles.studentSummary}>
          <Text style={styles.studentName}>{studentName ?? "Estudiante"}</Text>
          {studentCode ? <Text style={styles.studentCode}>{studentCode}</Text> : null}
          <Text style={styles.currentGrade}>
            {currentGrade
              ? `Nota final: ${currentGrade}${
                  currentScore !== null && currentScore !== undefined
                    ? ` (${currentScore.toFixed(1)})`
                    : ""
                }`
              : "Aún no hay calificaciones registradas"}
          </Text>
        </View>
        <View style={styles.field}>
          <Text style={styles.label}>Calificación</Text>
          <View style={styles.gradeRow}>
            {allowedGrades.map((grade) => {
              const isSelected = qualification === grade;
              return (
                <Text
                  key={grade}
                  onPress={() =>
                    setQualification((current) =>
                      current === grade ? null : grade
                    )
                  }
                  style={[styles.gradeChip, isSelected && styles.gradeChipSelected]}
                  accessibilityRole="button"
                >
                  {grade}
                </Text>
              );
            })}
          </View>
        </View>
        <View style={styles.field}>
          <Text style={styles.label}>Descripción</Text>
          <TextInput
            value={description}
            onChangeText={setDescription}
            style={[styles.input, styles.multiline]}
            multiline
          />
        </View>
        <Text
          onPress={handleSubmit}
          accessibilityRole="button"
          style={[
            styles.submit,
            (mutation.isPending || !user?.id) && styles.submitDisabled,
          ]}
        >
          {mutation.isPending ? "Guardando…" : "Guardar calificación"}
        </Text>
        {feedbackMessage ? (
          <Text style={styles.feedback}>{feedbackMessage}</Text>
        ) : null}
        <View style={styles.historySection}>
          <Text style={styles.sectionHeading}>Calificaciones registradas</Text>
          {isRefreshingHistory ? (
            <Text style={styles.historyMeta}>Actualizando…</Text>
          ) : historyRecords.length === 0 ? (
            <Text style={styles.historyEmpty}>Aún no se registran notas.</Text>
          ) : (
            historyRecords.map((record) => (
              <View key={record.id ?? `${record.grade}-${record.created_at}`} style={styles.historyEntry}>
                <Text style={styles.historyGrade}>{record.grade ?? "—"}</Text>
                <View style={styles.historyTextWrapper}>
                  {record.description ? (
                    <Text style={styles.historyDescription}>{record.description}</Text>
                  ) : (
                    <Text style={styles.historyDescriptionMuted}>Sin notas</Text>
                  )}
                  {record.teacher_full_name ? (
                    <Text style={styles.historyMeta}>{record.teacher_full_name}</Text>
                  ) : null}
                  {record.created_at ? (
                    <Text style={styles.historyMeta}>{record.created_at}</Text>
                  ) : null}
                </View>
                <MaterialIcons
                  name="delete-outline"
                  size={20}
                  color="#DC2626"
                  style={styles.historyDelete}
                  onPress={() => handleDelete(record.id)}
                />
              </View>
            ))
          )}
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  flex: {
    flex: 1,
  },
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  centered: {
    alignItems: "center",
    justifyContent: "center",
  },
  content: {
    padding: 20,
    paddingBottom: 32,
  },
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 24,
  },
  studentSummary: {
    marginBottom: 24,
  },
  studentName: {
    fontSize: 20,
    fontWeight: "600",
  },
  studentCode: {
    fontSize: 14,
    color: "#6B7280",
    marginTop: 4,
  },
  currentGrade: {
    fontSize: 16,
    color: "#1F2937",
    marginTop: 8,
  },
  field: {
    marginBottom: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: "500",
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
  },
  multiline: {
    minHeight: 96,
    textAlignVertical: "top",
  },
  gradeRow: {
    flexDirection: "row",
    gap: 12,
  },
  gradeChip: {
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 999,
    paddingHorizontal: 16,
    paddingVertical: 8,
    fontSize: 16,
    fontWeight: "600",
    color: "#1F2937",
  },
  gradeChipSelected: {
    backgroundColor: "#2563EB",
    borderColor: "#2563EB",
    color: "#FFFFFF",
  },
  submit: {
    backgroundColor: "#2563EB",
    borderRadius: 10,
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
    textAlign: "center",
    paddingVertical: 14,
    marginTop: 12,
  },
  submitDisabled: {
    backgroundColor: "#9CA3AF",
  },
  errorText: {
    color: "#DC2626",
    fontSize: 16,
  },
  historySection: {
    marginTop: 32,
    gap: 12,
  },
  sectionHeading: {
    fontSize: 18,
    fontWeight: "600",
  },
  historyEmpty: {
    color: "#6B7280",
  },
  historyEntry: {
    flexDirection: "row",
    alignItems: "flex-start",
    borderWidth: 1,
    borderColor: "#E5E7EB",
    borderRadius: 12,
    padding: 12,
    gap: 12,
  },
  historyGrade: {
    fontSize: 18,
    fontWeight: "700",
    color: "#2563EB",
  },
  historyTextWrapper: {
    flex: 1,
    gap: 4,
  },
  historyDelete: {
    marginLeft: 8,
    alignSelf: "center",
  },
  historyDescription: {
    fontSize: 15,
    color: "#1F2937",
  },
  historyDescriptionMuted: {
    fontSize: 15,
    color: "#9CA3AF",
  },
  historyMeta: {
    fontSize: 12,
    color: "#6B7280",
  },
  feedback: {
    marginTop: 12,
    fontSize: 14,
    color: "#047857",
  },
});

export default TeacherGradingScreen;

