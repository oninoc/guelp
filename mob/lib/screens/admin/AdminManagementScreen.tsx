import React from "react";
import {
  Alert,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  Pressable,
} from "react-native";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  assignPermission,
  assignRole,
  createClassroom,
  createStudent,
  createSubject,
  createTeacher,
  createUser,
  fetchAllStudents,
  fetchAllTeachers,
  fetchAllSubjects,
  fetchAllClassrooms,
  createClassroomSubject,
  createClassroomSubjectStudent,
  fetchAllClassroomSubjects,
  fetchClassroomSubjectStudents,
  updateStudent,
  updateTeacher,
  updateSubject,
  updateClassroom,
  deleteStudent,
  deleteTeacher,
  deleteSubject,
  deleteClassroom,
  getStudentById,
  getTeacherById,
  getSubjectById,
  getClassroomById,
} from "@/lib/api/admin";
import { DatePicker } from "@/lib/components/DatePicker";
import { DynamicSelect } from "@/lib/components/DynamicSelect";
import { useQueryClient } from "@tanstack/react-query";

type FormKey =
  | "user"
  | "student"
  | "teacher"
  | "subject"
  | "classroom"
  | "classroom-subject"
  | "classroom-subject-student"
  | "role"
  | "permission";

type ViewMode = "create" | "list";

const AdminManagementScreen: React.FC = () => {
  const queryClient = useQueryClient();
  const [viewMode, setViewMode] = React.useState<ViewMode>("create");
  const [activeForm, setActiveForm] = React.useState<FormKey>("user");
  const [editingId, setEditingId] = React.useState<string | number | null>(null);

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
    birthDate: null as string | null,
    gender: "",
    documentNumber: "",
    responsibleName: "",
    responsiblePhone: "",
    responsibleEmail: "",
    responsibleAddress: "",
    userEmail: "",
    userPassword: "",
  });

  const [teacherForm, setTeacherForm] = React.useState({
    names: "",
    fatherLastName: "",
    motherLastName: "",
    documentNumber: "",
    birthDate: null as string | null,
    gender: "",
    userEmail: "",
    userPassword: "",
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

  const [classroomSubjectForm, setClassroomSubjectForm] = React.useState({
    classroomId: null as string | null,
    subjectId: null as number | null,
    teacherId: null as string | null,
    substituteTeacherId: null as string | null,
    isActive: true,
  });

  const [classroomSubjectStudentForm, setClassroomSubjectStudentForm] = React.useState({
    classroomSubjectId: null as number | null,
    studentId: null as string | null,
    status: "enrolled",
    isActive: true,
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
    mutationFn: () => {
      if (editingId) {
        return updateStudent(editingId as string, {
          code: studentForm.code,
          names: studentForm.names,
          father_last_name: studentForm.fatherLastName,
          mother_last_name: studentForm.motherLastName,
          phone: studentForm.phone || undefined,
          address: studentForm.address || undefined,
          email: studentForm.email || undefined,
          birth_date: studentForm.birthDate || undefined,
          gender: studentForm.gender || undefined,
          document_number: studentForm.documentNumber || undefined,
          responsible_name: studentForm.responsibleName || undefined,
          responsible_phone: studentForm.responsiblePhone || undefined,
          responsible_email: studentForm.responsibleEmail || undefined,
          responsible_address: studentForm.responsibleAddress || undefined,
        });
      }
      return createStudent({
        code: studentForm.code,
        names: studentForm.names,
        father_last_name: studentForm.fatherLastName,
        mother_last_name: studentForm.motherLastName,
        phone: studentForm.phone || undefined,
        address: studentForm.address || undefined,
        email: studentForm.email || undefined,
        birth_date: studentForm.birthDate || undefined,
        gender: studentForm.gender || undefined,
        document_type: "DNI", // Default to DNI
        document_number: studentForm.documentNumber || undefined,
        responsible_name: studentForm.responsibleName || undefined,
        responsible_phone: studentForm.responsiblePhone || undefined,
        responsible_email: studentForm.responsibleEmail || undefined,
        responsible_address: studentForm.responsibleAddress || undefined,
        user_email: studentForm.userEmail || undefined,
        user_password: studentForm.userPassword || undefined,
      });
    },
    onSuccess: () => {
      Alert.alert(editingId ? "Student updated" : "Student created", editingId ? "The student has been updated." : "The student has been registered.");
      // Reset form
      setStudentForm({
        code: "",
        names: "",
        fatherLastName: "",
        motherLastName: "",
        phone: "",
        address: "",
        email: "",
        birthDate: null,
        gender: "",
        documentNumber: "",
        responsibleName: "",
        responsiblePhone: "",
        responsibleEmail: "",
        responsibleAddress: "",
        userEmail: "",
        userPassword: "",
      });
      setEditingId(null);
      queryClient.invalidateQueries({ queryKey: ["admin-students"] });
    },
  });

  const teacherMutation = useMutation({
    mutationFn: () => {
      if (editingId) {
        return updateTeacher(editingId as string, {
          names: teacherForm.names,
          father_last_name: teacherForm.fatherLastName,
          mother_last_name: teacherForm.motherLastName,
          document_number: teacherForm.documentNumber,
          birth_date: teacherForm.birthDate || undefined,
          gender: teacherForm.gender,
        });
      }
      return createTeacher({
        names: teacherForm.names,
        father_last_name: teacherForm.fatherLastName,
        mother_last_name: teacherForm.motherLastName,
        document_type: "DNI", // Default to DNI
        document_number: teacherForm.documentNumber,
        birth_date: teacherForm.birthDate || undefined,
        gender: teacherForm.gender,
        user_email: teacherForm.userEmail || undefined,
        user_password: teacherForm.userPassword || undefined,
      });
    },
    onSuccess: () => {
      Alert.alert(editingId ? "Teacher updated" : "Teacher created", editingId ? "The teacher has been updated." : "The teacher has been registered.");
      // Reset form
      setTeacherForm({
        names: "",
        fatherLastName: "",
        motherLastName: "",
        documentNumber: "",
        birthDate: null,
        gender: "",
        userEmail: "",
        userPassword: "",
      });
      setEditingId(null);
      queryClient.invalidateQueries({ queryKey: ["admin-teachers"] });
    },
  });

  const subjectMutation = useMutation({
    mutationFn: () => {
      if (editingId) {
        return updateSubject(editingId as number, {
          name: subjectForm.name,
          description: subjectForm.description || undefined,
        });
      }
      return createSubject({
        name: subjectForm.name,
        description: subjectForm.description || undefined,
      });
    },
    onSuccess: () => {
      Alert.alert(editingId ? "Subject updated" : "Subject created", editingId ? "The subject has been updated." : "The subject has been added.");
      setSubjectForm({ name: "", description: "" });
      setEditingId(null);
      queryClient.invalidateQueries({ queryKey: ["admin-subjects"] });
    },
  });

  const classroomMutation = useMutation({
    mutationFn: () => {
      if (editingId) {
        return updateClassroom(editingId as string, {
          description: classroomForm.description,
          level: classroomForm.level,
          degree: classroomForm.degree,
          start_time: classroomForm.startTime || undefined,
          end_time: classroomForm.endTime || undefined,
          tutor_id: classroomForm.tutorId || undefined,
        });
      }
      return createClassroom({
        description: classroomForm.description,
        level: classroomForm.level,
        degree: classroomForm.degree,
        start_time: classroomForm.startTime || undefined,
        end_time: classroomForm.endTime || undefined,
        tutor_id: classroomForm.tutorId || undefined,
      });
    },
    onSuccess: () => {
      Alert.alert(editingId ? "Classroom updated" : "Classroom created", editingId ? "The classroom has been updated." : "The classroom has been added.");
      setClassroomForm({
        description: "",
        level: "",
        degree: "",
        startTime: "",
        endTime: "",
        tutorId: "",
      });
      setEditingId(null);
      queryClient.invalidateQueries({ queryKey: ["admin-classrooms"] });
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

  const classroomSubjectMutation = useMutation({
    mutationFn: () =>
      createClassroomSubject({
        classroom_id: classroomSubjectForm.classroomId!,
        subject_id: classroomSubjectForm.subjectId!,
        teacher_id: classroomSubjectForm.teacherId || undefined,
        substitute_teacher_id: classroomSubjectForm.substituteTeacherId || undefined,
        is_active: classroomSubjectForm.isActive,
      }),
    onSuccess: () => {
      Alert.alert("Success", "Classroom-subject relation created successfully.");
      setClassroomSubjectForm({
        classroomId: null,
        subjectId: null,
        teacherId: null,
        substituteTeacherId: null,
        isActive: true,
      });
      queryClient.invalidateQueries({ queryKey: ["admin-classroom-subjects"] });
    },
  });

  const classroomSubjectStudentMutation = useMutation({
    mutationFn: () =>
      createClassroomSubjectStudent({
        classroom_subject_id: classroomSubjectStudentForm.classroomSubjectId!,
        student_id: classroomSubjectStudentForm.studentId!,
        status: classroomSubjectStudentForm.status || undefined,
        is_active: classroomSubjectStudentForm.isActive,
      }),
    onSuccess: () => {
      Alert.alert("Success", "Student enrolled successfully.");
      setClassroomSubjectStudentForm({
        classroomSubjectId: null,
        studentId: null,
        status: "enrolled",
        isActive: true,
      });
    },
  });

  // Queries for dynamic selects
  const { data: classroomsData } = useQuery({
    queryKey: ["admin-classrooms"],
    queryFn: fetchAllClassrooms,
  });

  const { data: subjectsData } = useQuery({
    queryKey: ["admin-subjects"],
    queryFn: fetchAllSubjects,
  });

  const { data: teachersData } = useQuery({
    queryKey: ["admin-teachers"],
    queryFn: fetchAllTeachers,
  });

  const { data: studentsData } = useQuery({
    queryKey: ["admin-students"],
    queryFn: fetchAllStudents,
  });

  const { data: classroomSubjectsData } = useQuery({
    queryKey: ["admin-classroom-subjects"],
    queryFn: fetchAllClassroomSubjects,
  });

  // Queries for loading data when editing
  const { data: editingStudentData } = useQuery({
    queryKey: ["admin-student", editingId],
    queryFn: () => getStudentById(editingId as string),
    enabled: editingId !== null && activeForm === "student",
  });

  const { data: editingTeacherData } = useQuery({
    queryKey: ["admin-teacher", editingId],
    queryFn: () => getTeacherById(editingId as string),
    enabled: editingId !== null && activeForm === "teacher",
  });

  const { data: editingSubjectData } = useQuery({
    queryKey: ["admin-subject", editingId],
    queryFn: () => getSubjectById(editingId as number),
    enabled: editingId !== null && activeForm === "subject",
  });

  const { data: editingClassroomData } = useQuery({
    queryKey: ["admin-classroom", editingId],
    queryFn: () => getClassroomById(editingId as string),
    enabled: editingId !== null && activeForm === "classroom",
  });

  // Load data into form when editing
  React.useEffect(() => {
    if (editingStudentData && activeForm === "student") {
      setStudentForm({
        code: editingStudentData.code || "",
        names: editingStudentData.names || "",
        fatherLastName: editingStudentData.father_last_name || "",
        motherLastName: editingStudentData.mother_last_name || "",
        phone: editingStudentData.phone || "",
        address: editingStudentData.address || "",
        email: editingStudentData.email || "",
        birthDate: editingStudentData.birth_date || null,
        gender: editingStudentData.gender || "",
        documentNumber: editingStudentData.document_number || "",
        responsibleName: editingStudentData.responsible_name || "",
        responsiblePhone: editingStudentData.responsible_phone || "",
        responsibleEmail: editingStudentData.responsible_email || "",
        responsibleAddress: editingStudentData.responsible_address || "",
        userEmail: "",
        userPassword: "",
      });
    }
  }, [editingStudentData, activeForm]);

  React.useEffect(() => {
    if (editingTeacherData && activeForm === "teacher") {
      setTeacherForm({
        names: editingTeacherData.names || "",
        fatherLastName: editingTeacherData.father_last_name || "",
        motherLastName: editingTeacherData.mother_last_name || "",
        documentNumber: editingTeacherData.document_number || "",
        birthDate: editingTeacherData.birth_date || null,
        gender: editingTeacherData.gender || "",
        userEmail: "",
        userPassword: "",
      });
    }
  }, [editingTeacherData, activeForm]);

  React.useEffect(() => {
    if (editingSubjectData && activeForm === "subject") {
      setSubjectForm({
        name: editingSubjectData.name || "",
        description: editingSubjectData.description || "",
      });
    }
  }, [editingSubjectData, activeForm]);

  React.useEffect(() => {
    if (editingClassroomData && activeForm === "classroom") {
      setClassroomForm({
        description: editingClassroomData.description || "",
        level: editingClassroomData.level || "",
        degree: editingClassroomData.degree || "",
        startTime: editingClassroomData.start_time || "",
        endTime: editingClassroomData.end_time || "",
        tutorId: editingClassroomData.tutor_id || "",
      });
    }
  }, [editingClassroomData, activeForm]);

  // Delete mutations
  const deleteStudentMutation = useMutation({
    mutationFn: (id: string) => deleteStudent(id),
    onSuccess: () => {
      Alert.alert("Success", "Student deleted successfully.");
      queryClient.invalidateQueries({ queryKey: ["admin-students"] });
    },
  });

  const deleteTeacherMutation = useMutation({
    mutationFn: (id: string) => deleteTeacher(id),
    onSuccess: () => {
      Alert.alert("Success", "Teacher deleted successfully.");
      queryClient.invalidateQueries({ queryKey: ["admin-teachers"] });
    },
  });

  const deleteSubjectMutation = useMutation({
    mutationFn: (id: number) => deleteSubject(id),
    onSuccess: () => {
      Alert.alert("Success", "Subject deleted successfully.");
      queryClient.invalidateQueries({ queryKey: ["admin-subjects"] });
    },
  });

  const deleteClassroomMutation = useMutation({
    mutationFn: (id: string) => deleteClassroom(id),
    onSuccess: () => {
      Alert.alert("Success", "Classroom deleted successfully.");
      queryClient.invalidateQueries({ queryKey: ["admin-classrooms"] });
    },
  });

  const handleEdit = (id: string | number) => {
    setEditingId(id);
    setViewMode("create");
  };

  const handleDelete = (id: string | number, name: string, type: FormKey) => {
    const confirmDelete = () => {
      switch (type) {
        case "student":
          deleteStudentMutation.mutate(id as string);
          break;
        case "teacher":
          deleteTeacherMutation.mutate(id as string);
          break;
        case "subject":
          deleteSubjectMutation.mutate(id as number);
          break;
        case "classroom":
          deleteClassroomMutation.mutate(id as string);
          break;
      }
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

  const [selectedClassroomSubjectId, setSelectedClassroomSubjectId] = React.useState<number | null>(null);
  const { data: classroomSubjectStudentsData } = useQuery({
    queryKey: ["admin-classroom-subject-students", selectedClassroomSubjectId],
    queryFn: () => fetchClassroomSubjectStudents(selectedClassroomSubjectId!),
    enabled: selectedClassroomSubjectId !== null && activeForm === "classroom-subject-student",
  });

  const renderListView = () => {
    let data: any[] = [];
    let getDisplayName = (item: any) => "";
    let getSubtitle = (item: any) => "";

    switch (activeForm) {
      case "student":
        data = studentsData || [];
        getDisplayName = (item) => `${item.names} ${item.father_last_name} ${item.mother_last_name}`.trim();
        getSubtitle = (item) => item.code || item.email || "";
        break;
      case "teacher":
        data = teachersData || [];
        getDisplayName = (item) => `${item.names} ${item.father_last_name} ${item.mother_last_name}`.trim();
        getSubtitle = (item) => item.document_number || "";
        break;
      case "subject":
        data = subjectsData || [];
        getDisplayName = (item) => item.name;
        getSubtitle = (item) => item.description || "";
        break;
      case "classroom":
        data = classroomsData || [];
        getDisplayName = (item) => item.description;
        getSubtitle = (item) => `${item.level} ${item.degree}`.trim() + (item.tutor_name ? ` - ${item.tutor_name}` : "");
        break;
      case "classroom-subject":
        data = classroomSubjectsData || [];
        getDisplayName = (item) => `${item.subject_name} - ${item.classroom_description}`;
        getSubtitle = (item) => {
          const parts = [];
          if (item.teacher_name) parts.push(`Teacher: ${item.teacher_name}`);
          if (item.student_count > 0) parts.push(`${item.student_count} students`);
          return parts.join(" • ") || "No teacher assigned";
        };
        break;
      case "classroom-subject-student":
        if (selectedClassroomSubjectId === null) {
          return (
            <View>
              <Text style={styles.sectionHeading}>Select a Classroom-Subject</Text>
              <Text style={styles.empty}>Please select a classroom-subject to view enrolled students.</Text>
              <View style={{ marginTop: 16 }}>
                {(classroomSubjectsData || []).map((cs: any) => (
                  <Pressable
                    key={cs.id}
                    style={[styles.listItem, selectedClassroomSubjectId === cs.id && styles.listItemSelected]}
                    onPress={() => setSelectedClassroomSubjectId(cs.id)}
                  >
                    <View style={styles.listItemContent}>
                      <Text style={styles.listItemTitle}>{cs.subject_name} - {cs.classroom_description}</Text>
                      <Text style={styles.listItemSubtitle}>{cs.student_count} students enrolled</Text>
                    </View>
                  </Pressable>
                ))}
              </View>
            </View>
          );
        }
        data = classroomSubjectStudentsData || [];
        getDisplayName = (item) => item.student_name;
        getSubtitle = (item) => {
          const parts = [];
          if (item.student_code) parts.push(`Code: ${item.student_code}`);
          if (item.qualification) parts.push(`Grade: ${item.qualification}`);
          return parts.join(" • ") || item.student_email || "";
        };
        break;
      default:
        return <Text style={styles.empty}>List view not available for this entity type.</Text>;
    }

    return (
      <View>
        {activeForm === "classroom-subject-student" && selectedClassroomSubjectId && (
          <Pressable
            style={styles.backButton}
            onPress={() => {
              setSelectedClassroomSubjectId(null);
              setActiveForm("classroom-subject");
            }}
          >
            <Text style={styles.backButtonText}>← Back to Classroom-Subjects</Text>
          </Pressable>
        )}
        <Text style={styles.sectionHeading}>
          {activeForm === "student" ? "Students" : activeForm === "teacher" ? "Teachers" : activeForm === "subject" ? "Subjects" : activeForm === "classroom" ? "Classrooms" : activeForm === "classroom-subject" ? "Classroom-Subjects" : "Enrolled Students"}
        </Text>
        {data.length === 0 ? (
          <Text style={styles.empty}>No records found.</Text>
        ) : (
          data.map((item) => {
            const displayName = getDisplayName(item);
            const subtitle = getSubtitle(item);
            return (
              <View key={String(item.id)} style={styles.listItem}>
                <View style={styles.listItemContent}>
                  <Text style={styles.listItemTitle}>{displayName}</Text>
                  {subtitle ? <Text style={styles.listItemSubtitle}>{subtitle}</Text> : null}
                </View>
                <View style={styles.listItemActions}>
                  {activeForm === "classroom-subject" ? (
                    <Pressable
                      style={[styles.actionButton, styles.viewButton]}
                      onPress={() => {
                        setSelectedClassroomSubjectId(item.id);
                        setActiveForm("classroom-subject-student");
                      }}
                    >
                      <Text style={styles.actionButtonText}>View Students</Text>
                    </Pressable>
                  ) : activeForm === "classroom-subject-student" ? null : (
                    <>
                      <Pressable
                        style={[styles.actionButton, styles.editButton]}
                        onPress={() => handleEdit(item.id)}
                      >
                        <Text style={styles.actionButtonText}>Edit</Text>
                      </Pressable>
                      <Pressable
                        style={[styles.actionButton, styles.deleteButton]}
                        onPress={() => handleDelete(item.id, displayName, activeForm)}
                      >
                        <Text style={[styles.actionButtonText, styles.deleteButtonText]}>Delete</Text>
                      </Pressable>
                    </>
                  )}
                </View>
              </View>
            );
          })
        )}
      </View>
    );
  };

  const mutationByForm: Record<FormKey, { mutate: () => void; loading: boolean }> = {
    user: { mutate: userMutation.mutate, loading: userMutation.isPending },
    student: { mutate: studentMutation.mutate, loading: studentMutation.isPending },
    teacher: { mutate: teacherMutation.mutate, loading: teacherMutation.isPending },
    subject: { mutate: subjectMutation.mutate, loading: subjectMutation.isPending },
    "classroom-subject": { mutate: classroomSubjectMutation.mutate, loading: classroomSubjectMutation.isPending },
    "classroom-subject-student": { mutate: classroomSubjectStudentMutation.mutate, loading: classroomSubjectStudentMutation.isPending },
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
              label="Student code *"
              value={studentForm.code}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, code: text }))
              }
            />
            <Input
              label="Names *"
              value={studentForm.names}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, names: text }))
              }
            />
            <Input
              label="Father last name *"
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
              onChangeText={(text) => {
                // Only allow numbers
                const numbersOnly = text.replace(/[^0-9]/g, "");
                setStudentForm((prev) => ({ ...prev, phone: numbersOnly }));
              }}
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
            <DatePicker
              label="Birth date"
              value={studentForm.birthDate}
              onChange={(date) =>
                setStudentForm((prev) => ({ ...prev, birthDate: date }))
              }
            />
            <GenderSelect
              label="Gender"
              value={studentForm.gender}
              onValueChange={(value) =>
                setStudentForm((prev) => ({ ...prev, gender: value }))
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
              onChangeText={(text) => {
                const numbersOnly = text.replace(/[^0-9]/g, "");
                setStudentForm((prev) => ({ ...prev, responsiblePhone: numbersOnly }));
              }}
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
            <Text style={styles.sectionDivider}>User Account (Auto-created)</Text>
            <Input
              label="User email *"
              value={studentForm.userEmail}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, userEmail: text }))
              }
              keyboardType="email-address"
            />
            <Input
              label="User password *"
              value={studentForm.userPassword}
              onChangeText={(text) =>
                setStudentForm((prev) => ({ ...prev, userPassword: text }))
              }
              secureTextEntry
            />
          </>
        );
      case "teacher":
        return (
          <>
            <Input
              label="Names *"
              value={teacherForm.names}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, names: text }))
              }
            />
            <Input
              label="Father last name *"
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
              label="Document number *"
              value={teacherForm.documentNumber}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, documentNumber: text }))
              }
            />
            <DatePicker
              label="Birth date *"
              value={teacherForm.birthDate}
              onChange={(date) =>
                setTeacherForm((prev) => ({ ...prev, birthDate: date }))
              }
            />
            <GenderSelect
              label="Gender *"
              value={teacherForm.gender}
              onValueChange={(value) =>
                setTeacherForm((prev) => ({ ...prev, gender: value }))
              }
            />
            <Text style={styles.sectionDivider}>User Account (Auto-created)</Text>
            <Input
              label="User email *"
              value={teacherForm.userEmail}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, userEmail: text }))
              }
              keyboardType="email-address"
            />
            <Input
              label="User password *"
              value={teacherForm.userPassword}
              onChangeText={(text) =>
                setTeacherForm((prev) => ({ ...prev, userPassword: text }))
              }
              secureTextEntry
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
      case "classroom-subject":
        return (
          <>
            <DynamicSelect
              label="Classroom *"
              value={classroomSubjectForm.classroomId}
              options={
                classroomsData?.map((c) => ({
                  id: c.id,
                  label: c.description,
                  subtitle: `${c.level} ${c.degree}`.trim(),
                })) || []
              }
              onValueChange={(value) =>
                setClassroomSubjectForm((prev) => ({
                  ...prev,
                  classroomId: value as string | null,
                }))
              }
              isLoading={!classroomsData}
            />
            <DynamicSelect
              label="Subject *"
              value={classroomSubjectForm.subjectId}
              options={
                subjectsData?.map((s) => ({
                  id: s.id,
                  label: s.name,
                  subtitle: s.description,
                })) || []
              }
              onValueChange={(value) =>
                setClassroomSubjectForm((prev) => ({
                  ...prev,
                  subjectId: value as number | null,
                }))
              }
              isLoading={!subjectsData}
            />
            <DynamicSelect
              label="Teacher (optional)"
              value={classroomSubjectForm.teacherId}
              options={
                teachersData?.map((t) => ({
                  id: t.id,
                  label: `${t.names} ${t.father_last_name} ${t.mother_last_name}`.trim(),
                  subtitle: t.document_number,
                })) || []
              }
              onValueChange={(value) =>
                setClassroomSubjectForm((prev) => ({
                  ...prev,
                  teacherId: value as string | null,
                }))
              }
              isLoading={!teachersData}
            />
            <DynamicSelect
              label="Substitute Teacher (optional)"
              value={classroomSubjectForm.substituteTeacherId}
              options={
                teachersData?.map((t) => ({
                  id: t.id,
                  label: `${t.names} ${t.father_last_name} ${t.mother_last_name}`.trim(),
                  subtitle: t.document_number,
                })) || []
              }
              onValueChange={(value) =>
                setClassroomSubjectForm((prev) => ({
                  ...prev,
                  substituteTeacherId: value as string | null,
                }))
              }
              isLoading={!teachersData}
            />
          </>
        );
      case "classroom-subject-student":
        return (
          <>
            <DynamicSelect
              label="Classroom-Subject *"
              value={classroomSubjectStudentForm.classroomSubjectId}
              options={
                classroomSubjectsData?.map((cs) => ({
                  id: cs.id,
                  label: `${cs.subject_name} - ${cs.classroom_description}`,
                  subtitle: cs.teacher_name ? `Teacher: ${cs.teacher_name}` : "No teacher assigned",
                })) || []
              }
              onValueChange={(value) =>
                setClassroomSubjectStudentForm((prev) => ({
                  ...prev,
                  classroomSubjectId: value as number | null,
                }))
              }
              placeholder="Select classroom-subject relation"
              isLoading={!classroomSubjectsData}
            />
            <DynamicSelect
              label="Student *"
              value={classroomSubjectStudentForm.studentId}
              options={
                studentsData?.map((s) => ({
                  id: s.id,
                  label: `${s.names} ${s.father_last_name} ${s.mother_last_name}`.trim(),
                  subtitle: s.code || s.email || "",
                })) || []
              }
              onValueChange={(value) =>
                setClassroomSubjectStudentForm((prev) => ({
                  ...prev,
                  studentId: value as string | null,
                }))
              }
              isLoading={!studentsData}
            />
            <Input
              label="Status"
              value={classroomSubjectStudentForm.status}
              onChangeText={(text) =>
                setClassroomSubjectStudentForm((prev) => ({
                  ...prev,
                  status: text,
                }))
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
      <View style={styles.modeContainer}>
        <Pressable
          style={[styles.modeButton, viewMode === "create" && styles.modeButtonActive]}
          onPress={() => {
            setViewMode("create");
            setEditingId(null);
          }}
        >
          <Text style={[styles.modeButtonText, viewMode === "create" && styles.modeButtonTextActive]}>
            {editingId ? "Edit" : "Create"}
          </Text>
        </Pressable>
        <Pressable
          style={[styles.modeButton, viewMode === "list" && styles.modeButtonActive]}
          onPress={() => setViewMode("list")}
        >
          <Text style={[styles.modeButtonText, viewMode === "list" && styles.modeButtonTextActive]}>
            List
          </Text>
        </Pressable>
      </View>
      <View style={styles.tabContainer}>
        {(
          [
            ["user", "User"],
            ["student", "Student"],
            ["teacher", "Teacher"],
            ["subject", "Subject"],
            ["classroom", "Classroom"],
            ["classroom-subject", "Classroom-Subject"],
            ["classroom-subject-student", "Enroll Student"],
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
      {viewMode === "list" ? (
        renderListView()
      ) : (
        <>
          <View style={styles.form}>{renderForm()}</View>
          <Text
            onPress={handleSubmit}
            style={[styles.submit, isLoading && styles.submitDisabled]}
            accessibilityRole="button"
          >
            {isLoading ? "Submitting…" : editingId ? "Update" : "Submit"}
          </Text>
          {editingId && (
            <Text
              onPress={() => {
                setEditingId(null);
                // Reset form based on activeForm
                switch (activeForm) {
                  case "student":
                    setStudentForm({
                      code: "",
                      names: "",
                      fatherLastName: "",
                      motherLastName: "",
                      phone: "",
                      address: "",
                      email: "",
                      birthDate: null,
                      gender: "",
                      documentNumber: "",
                      responsibleName: "",
                      responsiblePhone: "",
                      responsibleEmail: "",
                      responsibleAddress: "",
                      userEmail: "",
                      userPassword: "",
                    });
                    break;
                  case "teacher":
                    setTeacherForm({
                      names: "",
                      fatherLastName: "",
                      motherLastName: "",
                      documentNumber: "",
                      birthDate: null,
                      gender: "",
                      userEmail: "",
                      userPassword: "",
                    });
                    break;
                  case "subject":
                    setSubjectForm({ name: "", description: "" });
                    break;
                  case "classroom":
                    setClassroomForm({
                      description: "",
                      level: "",
                      degree: "",
                      startTime: "",
                      endTime: "",
                      tutorId: "",
                    });
                    break;
                }
              }}
              style={[styles.submit, styles.cancelButton]}
              accessibilityRole="button"
            >
              Cancel Edit
            </Text>
          )}
        </>
      )}
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

type GenderSelectProps = {
  label: string;
  value: string;
  onValueChange: (value: string) => void;
};

const GenderSelect: React.FC<GenderSelectProps> = ({ label, value, onValueChange }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const genders = ["Male", "Female", "Other"];

  return (
    <View style={styles.inputContainer}>
      <Text style={styles.inputLabel}>{label}</Text>
      <Pressable
        style={styles.select}
        onPress={() => setIsOpen(!isOpen)}
      >
        <Text style={[styles.selectText, !value && styles.selectPlaceholder]}>
          {value || "Select gender"}
        </Text>
        <Text style={styles.selectArrow}>{isOpen ? "▲" : "▼"}</Text>
      </Pressable>
      {isOpen && (
        <View style={styles.selectOptions}>
          {genders.map((gender) => (
            <Pressable
              key={gender}
              style={[
                styles.selectOption,
                value === gender && styles.selectOptionSelected,
              ]}
              onPress={() => {
                onValueChange(gender);
                setIsOpen(false);
              }}
            >
              <Text
                style={[
                  styles.selectOptionText,
                  value === gender && styles.selectOptionTextSelected,
                ]}
              >
                {gender}
              </Text>
            </Pressable>
          ))}
        </View>
      )}
    </View>
  );
};

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
  sectionDivider: {
    fontSize: 16,
    fontWeight: "600",
    marginTop: 24,
    marginBottom: 8,
    color: "#374151",
  },
  select: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: "#FFFFFF",
  },
  selectText: {
    fontSize: 16,
    color: "#111827",
  },
  selectPlaceholder: {
    color: "#9CA3AF",
  },
  selectArrow: {
    fontSize: 12,
    color: "#6B7280",
  },
  selectOptions: {
    marginTop: 4,
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 8,
    backgroundColor: "#FFFFFF",
    overflow: "hidden",
  },
  selectOption: {
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#F3F4F6",
  },
  selectOptionSelected: {
    backgroundColor: "#EFF6FF",
  },
  selectOptionText: {
    fontSize: 16,
    color: "#111827",
  },
  selectOptionTextSelected: {
    color: "#2563EB",
    fontWeight: "600",
  },
  modeContainer: {
    flexDirection: "row",
    marginBottom: 16,
    gap: 8,
  },
  modeButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#D1D5DB",
    backgroundColor: "#FFFFFF",
    alignItems: "center",
  },
  modeButtonActive: {
    backgroundColor: "#2563EB",
    borderColor: "#2563EB",
  },
  modeButtonText: {
    fontSize: 16,
    fontWeight: "500",
    color: "#374151",
  },
  modeButtonTextActive: {
    color: "#FFFFFF",
  },
  sectionHeading: {
    fontSize: 20,
    fontWeight: "600",
    marginBottom: 16,
    color: "#111827",
  },
  empty: {
    textAlign: "center",
    color: "#6B7280",
    marginTop: 32,
    fontSize: 16,
  },
  listItem: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    marginBottom: 12,
    backgroundColor: "#F9FAFB",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  listItemContent: {
    flex: 1,
    marginRight: 12,
  },
  listItemTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#111827",
    marginBottom: 4,
  },
  listItemSubtitle: {
    fontSize: 14,
    color: "#6B7280",
  },
  listItemActions: {
    flexDirection: "row",
    gap: 8,
  },
  actionButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 6,
    borderWidth: 1,
  },
  editButton: {
    backgroundColor: "#2563EB",
    borderColor: "#2563EB",
  },
  deleteButton: {
    backgroundColor: "#FFFFFF",
    borderColor: "#EF4444",
  },
  actionButtonText: {
    fontSize: 14,
    fontWeight: "500",
    color: "#FFFFFF",
  },
  deleteButtonText: {
    color: "#EF4444",
  },
  cancelButton: {
    marginTop: 12,
    backgroundColor: "#6B7280",
  },
  backButton: {
    marginBottom: 16,
    padding: 12,
    backgroundColor: "#F3F4F6",
    borderRadius: 8,
  },
  backButtonText: {
    fontSize: 16,
    color: "#2563EB",
    fontWeight: "500",
  },
  listItemSelected: {
    backgroundColor: "#EFF6FF",
    borderColor: "#2563EB",
  },
  viewButton: {
    backgroundColor: "#10B981",
    borderColor: "#10B981",
  },
});

export default AdminManagementScreen;

