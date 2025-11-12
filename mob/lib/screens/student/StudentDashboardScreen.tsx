import React from "react";
import { FlatList, Pressable, StyleSheet, Switch, Text, View, Platform, Alert } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "expo-router";
import { useAuth } from "@/lib/hooks/useAuth";
import { fetchStudentSubjects, downloadNotesPdf } from "@/lib/api/students";
import { StudentSubjectSummary } from "@/lib/types/api";
import * as Sharing from "expo-sharing";

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

  const handleDownloadPdf = async () => {
    if (!studentId) {
      Alert.alert("Error", "No se pudo identificar al estudiante.");
      return;
    }

    try {
      if (Platform.OS === "web") {
        // For web, download using fetch with auth token
        const apiBaseUrl = process.env.EXPO_PUBLIC_API_BASE_URL || "https://zwftj3xpti.us-east-1.awsapprunner.com";
        const url = `${apiBaseUrl}/students/${studentId}/notes-pdf?include_inactive=${includeInactive}`;
        
        // Get token from storage
        const { readPersistedAuthState } = await import("@/lib/storage/tokenStorage");
        const authState = await readPersistedAuthState();
        const token = authState?.accessToken;
        
        if (!token) {
          Alert.alert("Error", "No se encontró el token de autenticación. Por favor, inicia sesión nuevamente.");
          return;
        }
        
        const response = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const blob = await response.blob();
        const blobUrl = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = blobUrl;
        link.download = `notas_${studentId}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(blobUrl);
      } else {
        // For mobile, download and share
        const pdfUri = await downloadNotesPdf(studentId, includeInactive);
        
        if (await Sharing.isAvailableAsync()) {
          await Sharing.shareAsync(pdfUri);
        } else {
          Alert.alert("Éxito", "PDF descargado correctamente.");
        }
      }
    } catch (error) {
      console.error("Error downloading PDF:", error);
      Alert.alert("Error", "No se pudo descargar el PDF. Por favor, inténtalo de nuevo.");
    }
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
        <Pressable
          style={styles.downloadButton}
          onPress={handleDownloadPdf}
          accessibilityRole="button"
          accessibilityLabel="Descargar PDF de notas"
        >
          <Text style={styles.downloadButtonText}>📄 Descargar PDF de Notas</Text>
        </Pressable>
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
  downloadButton: {
    backgroundColor: "#2563EB",
    borderRadius: 8,
    padding: 12,
    marginTop: 16,
    alignItems: "center",
  },
  downloadButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
});

export default StudentDashboardScreen;

