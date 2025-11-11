import { Stack } from "expo-router";

const StudentSubjectLayout = () => {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="index" />
      <Stack.Screen name="history/index" />
    </Stack>
  );
};

export default StudentSubjectLayout;


