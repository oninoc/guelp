import { Tabs } from "expo-router";
import Ionicons from "@expo/vector-icons/Ionicons";

const StudentTabsLayout = () => {
  return (
    <Tabs
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: "#2563EB",
        tabBarInactiveTintColor: "#6B7280",
        tabBarIcon: ({ color, size }) => {
          const iconName: React.ComponentProps<typeof Ionicons>["name"] = (() => {
            switch (route.name) {
              case "index":
                return "home-outline";
              case "schedule":
                return "calendar-outline";
              case "profile":
                return "person-circle-outline";
              case "settings":
                return "settings-outline";
              default:
                return "ellipse-outline";
            }
          })();
          return <Ionicons name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tabs.Screen name="index" options={{ title: "Dashboard" }} />
      <Tabs.Screen name="schedule" options={{ title: "Schedule" }} />
      <Tabs.Screen name="profile" options={{ title: "Profile" }} />
      <Tabs.Screen name="settings" options={{ title: "Settings" }} />
    </Tabs>
  );
};

export default StudentTabsLayout;


