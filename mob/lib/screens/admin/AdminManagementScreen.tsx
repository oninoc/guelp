import React from "react";
import {
  Alert,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { useMutation } from "@tanstack/react-query";
import {
  assignPermission,
  assignRole,
  createClassroom,
  createStudent,
  createSubject,
  createTeacher,
  createUser,
} from "@/lib/api/admin";

type FormKey =
  | "user"
  | "student"
  | "teacher"
  | "subject"
  | "classroom"
  | "role"
  | "permission";

const AdminManagementScreen: React.FC = () => {
  const [activeForm, setActiveForm] = React.useState<FormKey>("user");

  const [userForm, setUserForm] = React.useState({
    email: "",
    password: "",
    name: "",
    lastName: "",
    phone: "",
    address: "",
  });

  const [studentForm, setStudentForm] = React.useState({
    code: "",
    names: "",
    fatherLastName: "",
    motherLastName: "",
    phone: "",
    address: "",
    email: "",
    birthDate: "",
    gender: "",
    nationality: "",
    documentType: "",
    documentNumber: "",
    responsibleName: "",
    responsiblePhone: "",
    responsibleEmail: "",
    responsibleAddress: "",
    userId: "",
  });

  const [teacherForm, setTeacherForm] = React.useState({
    names: "",
    fatherLastName: "",
    motherLastName: "",
    documentType: "",
    documentNumber: "",
    birthDate: "",
    gender: "",
    nationality: "",
    userId: "",
  });

  const [subjectForm, setSubjectForm] = React.useState({
    name: "",
    description: "",
  });

  const [classroomForm, setClassroomForm] = React.useState({
    description: "",
    level: "",
    degree: "",
    startTime: "",
    endTime: "",
    tutorId: "",
  });

  const [roleForm, setRoleForm] = React.useState({
    userId: "",
    roleCode: "",
    relationType: "direct",
  });

  const [permissionForm, setPermissionForm] = React.useState({
    roleCode: "",
    permissionCode: "",
    relationType: "direct",
  });

  const userMutation = useMutation({
    mutationFn: () =>
      createUser({
        email: userForm.email,
        password: userForm.password,
        name: userForm.name,
        last_name: userForm.lastName,
        phone: userForm.phone || "",
        address: userForm.address || "",
      }),
    onSuccess: () => {
      Alert.alert("User created", "The user has been created successfully.");
    },
  });

  const studentMutation = useMutation({
    mutationFn: () =>
      createStudent({
        code: studentForm.code,
        names: studentForm.names,
        father_last_name: studentForm.fatherLastName,
        mother_last_name: studentForm.motherLastName,
        phone: studentForm.phone || undefined,
        address: studentForm.address || undefined,
        email: studentForm.email || undefined,
        birth_date: studentForm.birthDate || undefined,
        gender: studentForm.gender || undefined,
        nationality: studentForm.nationality || undefined,
        document_type: studentForm.documentType || undefined,
        document_number: studentForm.documentNumber || undefined,
        responsible_name: studentForm.responsibleName || undefined,
        responsible_phone: studentForm.responsiblePhone || undefined,
        responsible_email: studentForm.responsibleEmail || undefined,
        responsible_address: studentForm.responsibleAddress || undefined,
        user_id: studentForm.userId,
      }),
    onSuccess: () => {
      Alert.alert("Student created", "The student has been registered.");
    },
  });

  const teacherMutation = useMutation({
    mutationFn: () =>
      createTeacher({
        names: teacherForm.names,
        father_last_name: teacherForm.fatherLastName,
        mother_last_name: teacherForm.motherLastName,
        document_type: teacherForm.documentType,
        document_number: teacherForm.documentNumber,
        birth_date: teacherForm.birthDate,
        gender: teacherForm.gender,
        nationality: teacherForm.nationality,
        user_id: teacherForm.userId,
      }),
    onSuccess: () => {
      Alert.alert("Teacher created", "The teacher has been registered.");
    },
  });

  const subjectMutation = useMutation({
    mutationFn: () =>
      createSubject({
        name: subjectForm.name,
        description: subjectForm.description || undefined,
      }),
    onSuccess: () => {
      Alert.alert("Subject created", "The subject has been added.");
    },
  });

  const classroomMutation = useMutation({
    mutationFn: () =>
      createClassroom({
        description: classroomForm.description,
        level: classroomForm.level,
        degree: classroomForm.degree,
        start_time: classroomForm.startTime || undefined,
        end_time: classroomForm.endTime || undefined,
        tutor_id: classroomForm.tutorId || undefined,
      }),
    onSuccess: () => {
      Alert.alert("Classroom created", "The classroom has been added.");
    },
  });

  const roleMutation = useMutation({
    mutationFn: () =>
      assignRole({
        user_id: roleForm.userId,
        role_code: roleForm.roleCode,
        relation_type: roleForm.relationType || undefined,
      }),
    onSuccess: () => {
      Alert.alert("Role assigned", "The role was assigned successfully.");
    },
  });

  const permissionMutation = useMutation({
    mutationFn: () =>
      assignPermission({
        role_code: permissionForm.roleCode,
        permission_code: permissionForm.permissionCode,
        relation_type: permissionForm.relationType || undefined,
      }),
    onSuccess: () => {
      Alert.alert("Permission assigned", "The permission was linked to the role.");
    },
  });

  const mutationByForm: Record<FormKey, { mutate: () => void; loading: boolean }> = {
    user: { mutate: userMutation.mutate, loading: userMutation.isPending },
    student: { mutate: studentMutation.mutate, loading: studentMutation.isPending },
    teacher: { mutate: teacherMutation.mutate, loading: teacherMutation.isPending },
    subject: { mutate: subjectMutation.mutate, loading: subjectMutation.isPending },
    classroom: { mutate: classroomMutation.mutate, loading: classroomMutation.isPending },
    role: { mutate: roleMutation.mutate, loading: roleMutation.isPending },
    permission: { mutate: permissionMutation.mutate, loading: permissionMutation.isPending },
  };

  const handleSubmit = () => {
    mutationByForm[activeForm].mutate();
  };

  const isLoading = mutationByForm[activeForm].loading;

  const renderForm = () => {
    switch (activeForm) {
      case "user":
        return (
          <>
            <Input
              label="Email"
              value={userForm.email}
              onChangeText={(text) => setUserForm((prev) => ({ ...prev, email: text }))}
              keyboardType="email-address"
            />
            <Input
              label="Password"
              value={userForm.password}
              onChangeText={(text) => setUserForm((prev) => ({ ...prev, password: text }))}
              secureTextEntry
            />
            <Input
              label="First name"
              value={userForm.name}
              onChangeText={(text) => setUserForm((prev) => ({ ...prev, name: text }))}
            />
            <Input
              label="Last name"
              value={userForm.lastName}
              onChangeText={(text) => setUserForm((prev) => ({ ...prev, lastName: text }))}
            />
            <Input
              label="Phone"
              value={userForm.phone}
              onChangeText={(text) => setUserForm((prev) => ({ ...prev, phone: text }))}
              keyboardType="phone-pad"
            />
            <Input
              label="Address"
              value={userForm.address}
              onChangeText={(text) => setUserForm((prev) => ({ ...prev, address: text }))}
            />
          </>
        );
      case "student":
        return (
          <>
            <Input
              label="Student code"
              value={studentForm.code}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, code: text }))
              }
            />
            <Input
              label="Names"
              value={studentForm.names}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, names: text }))
              }
            />
            <Input
              label="Father last name"
              value={studentForm.fatherLastName}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, fatherLastName: text }))
              }
            />
            <Input
              label="Mother last name"
              value={studentForm.motherLastName}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, motherLastName: text }))
              }
            />
            <Input
              label="Phone"
              value={studentForm.phone}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, phone: text }))
              }
              keyboardType="phone-pad"
            />
            <Input
              label="Address"
              value={studentForm.address}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, address: text }))
              }
            />
            <Input
              label="Email"
              value={studentForm.email}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, email: text }))
              }
              keyboardType="email-address"
            />
            <Input
              label="Birth date (ISO 8601)"
              value={studentForm.birthDate}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, birthDate: text }))
              }
            />
            <Input
              label="Gender"
              value={studentForm.gender}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, gender: text }))
              }
            />
            <Input
              label="Nationality"
              value={studentForm.nationality}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, nationality: text }))
              }
            />
            <Input
              label="Document type"
              value={studentForm.documentType}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, documentType: text }))
              }
            />
            <Input
              label="Document number"
              value={studentForm.documentNumber}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, documentNumber: text }))
              }
            />
            <Input
              label="Responsible name"
              value={studentForm.responsibleName}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, responsibleName: text }))
              }
            />
            <Input
              label="Responsible phone"
              value={studentForm.responsiblePhone}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, responsiblePhone: text }))
              }
              keyboardType="phone-pad"
            />
            <Input
              label="Responsible email"
              value={studentForm.responsibleEmail}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, responsibleEmail: text }))
              }
              keyboardType="email-address"
            />
            <Input
              label="Responsible address"
              value={studentForm.responsibleAddress}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, responsibleAddress: text }))
              }
            />
            <Input
              label="User UUID"
              value={studentForm.userId}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, userId: text }))
              }
            />
          </>
        );
      case "teacher":
        return (
          <>
            <Input
              label="Names"
              value={teacherForm.names}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, names: text }))
              }
            />
            <Input
              label="Father last name"
              value={teacherForm.fatherLastName}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, fatherLastName: text }))
              }
            />
            <Input
              label="Mother last name"
              value={teacherForm.motherLastName}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, motherLastName: text }))
              }
            />
            <Input
              label="Document type"
              value={teacherForm.documentType}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, documentType: text }))
              }
            />
            <Input
              label="Document number"
              value={teacherForm.documentNumber}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, documentNumber: text }))
              }
            />
            <Input
              label="Birth date (ISO 8601)"
              value={teacherForm.birthDate}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, birthDate: text }))
              }
            />
            <Input
              label="Gender"
              value={teacherForm.gender}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, gender: text }))
              }
            />
            <Input
              label="Nationality"
              value={teacherForm.nationality}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, nationality: text }))
              }
            />
            <Input
              label="User UUID"
              value={teacherForm.userId}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, userId: text }))
              }
            />
          </>
        );
      case "subject":
        return (
          <>
            <Input
              label="Name"
              value={subjectForm.name}
              onChangeText={(text) =>
                setSubjectForm((prev) => ({ ...prev, name: text }))
              }
            />
            <Input
              label="Description"
              value={subjectForm.description}
              onChangeText={(text) =>
                setSubjectForm((prev) => ({ ...prev, description: text }))
              }
            />
          </>
        );
      case "classroom":
        return (
          <>
            <Input
              label="Description"
              value={classroomForm.description}
              onChangeText={(text) =>
                setClassroomForm((prev) => ({ ...prev, description: text }))
              }
            />
            <Input
              label="Level"
              value={classroomForm.level}
              onChangeText={(text) =>
                setClassroomForm((prev) => ({ ...prev, level: text }))
              }
            />
            <Input
              label="Degree"
              value={classroomForm.degree}
              onChangeText={(text) =>
                setClassroomForm((prev) => ({ ...prev, degree: text }))
              }
            />
            <Input
              label="Start time"
              value={classroomForm.startTime}
              onChangeText={(text) =>
                setClassroomForm((prev) => ({ ...prev, startTime: text }))
              }
            />
            <Input
              label="End time"
              value={classroomForm.endTime}
              onChangeText={(text) =>
                setClassroomForm((prev) => ({ ...prev, endTime: text }))
              }
            />
            <Input
              label="Tutor UUID (optional)"
              value={classroomForm.tutorId}
              onChangeText={(text) =>
                setClassroomForm((prev) => ({ ...prev, tutorId: text }))
              }
            />
          </>
        );
      case "role":
        return (
          <>
            <Input
              label="User UUID"
              value={roleForm.userId}
              onChangeText={(text) =>
                setRoleForm((prev) => ({ ...prev, userId: text }))
              }
            />
            <Input
              label="Role code"
              value={roleForm.roleCode}
              onChangeText={(text) =>
                setRoleForm((prev) => ({ ...prev, roleCode: text }))
              }
            />
            <Input
              label="Relation type"
              value={roleForm.relationType}
              onChangeText={(text) =>
                setRoleForm((prev) => ({ ...prev, relationType: text }))
              }
            />
          </>
        );
      case "permission":
        return (
          <>
            <Input
              label="Role code"
              value={permissionForm.roleCode}
              onChangeText={(text) =>
                setPermissionForm((prev) => ({ ...prev, roleCode: text }))
              }
            />
            <Input
              label="Permission code"
              value={permissionForm.permissionCode}
              onChangeText={(text) =>
                setPermissionForm((prev) => ({ ...prev, permissionCode: text }))
              }
            />
            <Input
              label="Relation type"
              value={permissionForm.relationType}
              onChangeText={(text) =>
                setPermissionForm((prev) => ({ ...prev, relationType: text }))
              }
            />
          </>
        );
      default:
        return null;
    }
  };

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      keyboardShouldPersistTaps="handled"
    >
      <Text style={styles.title}>Management hub</Text>
      <Text style={styles.subtitle}>
        Create and manage users, enrolments, and permissions.
      </Text>
      <View style={styles.tabContainer}>
        {(
          [
            ["user", "User"],
            ["student", "Student"],
            ["teacher", "Teacher"],
            ["subject", "Subject"],
            ["classroom", "Classroom"],
            ["role", "Role"],
            ["permission", "Permission"],
          ] as Array<[FormKey, string]>
        ).map(([key, label]) => (
          <Text
            key={key}
            onPress={() => setActiveForm(key)}
            style={[
              styles.tab,
              activeForm === key && styles.tabActive,
            ]}
            accessibilityRole="button"
          >
            {label}
          </Text>
        ))}
      </View>
      <View style={styles.form}>{renderForm()}</View>
      <Text
        onPress={handleSubmit}
        style={[styles.submit, isLoading && styles.submitDisabled]}
        accessibilityRole="button"
      >
        {isLoading ? "Submitting…" : "Submit"}
      </Text>
    </ScrollView>
  );
};

type InputProps = React.ComponentProps<typeof TextInput> & { label: string };

const Input: React.FC<InputProps> = ({ label, style, ...props }) => (
  <View style={styles.inputContainer}>
    <Text style={styles.inputLabel}>{label}</Text>
    <TextInput
      style={[styles.input, style]}
      autoCapitalize="none"
      {...props}
    />
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  title: {
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 8,
  },
  subtitle: {
    color: "#6B7280",
    marginBottom: 24,
  },
  tabContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginBottom: 16,
  },
  tab: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 999,
    borderWidth: 1,
    borderColor: "#D1D5DB",
    marginRight: 8,
    marginBottom: 8,
    color: "#374151",
  },
  tabActive: {
    backgroundColor: "#2563EB",
    borderColor: "#2563EB",
    color: "#FFFFFF",
  },
  form: {
    marginBottom: 24,
  },
  inputContainer: {
    marginBottom: 16,
  },
  inputLabel: {
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
  submit: {
    textAlign: "center",
    backgroundColor: "#2563EB",
    color: "#FFFFFF",
    paddingVertical: 14,
    borderRadius: 10,
    fontSize: 16,
    fontWeight: "600",
  },
  submitDisabled: {
    backgroundColor: "#9CA3AF",
  },
});

export default AdminManagementScreen;

