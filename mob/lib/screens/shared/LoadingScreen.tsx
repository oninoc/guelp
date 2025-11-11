import React from "react";
import { ActivityIndicator, StyleSheet, View } from "react-native";

const LoadingScreen: React.FC = () => {
  return (
    <View style={styles.container} accessibilityLabel="loading-indicator">
      <ActivityIndicator size="large" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
});

export default LoadingScreen;

