import React, { useEffect, useState } from "react";
import {
  Alert,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { useRouter } from "expo-router";
import { useAuth } from "@/lib/hooks/useAuth";

const LoginScreen: React.FC = () => {
  const { signIn, status, lastError } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (status === "authenticated") {
      router.replace("/");
    }
  }, [router, status]);

  const handleSubmit = async () => {
    if (isSubmitting) {
      return;
    }
    setIsSubmitting(true);
    try {
      await signIn({ email, password });
    } catch (error) {
      console.error("Login failed", error);
      Alert.alert(
        "Error al iniciar sesión",
        "Verifica tus credenciales e inténtalo nuevamente."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const isDisabled =
    !email.trim() || !password.trim() || isSubmitting || status === "loading";

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.select({ ios: "padding", android: undefined })}
    >
      <View style={styles.container}>
        <Text style={styles.heading}>Bienvenido de nuevo</Text>
        <TextInput
          accessibilityLabel="Correo electrónico"
          autoCapitalize="none"
          autoComplete="email"
          autoCorrect={false}
          inputMode="email"
          keyboardType="email-address"
          placeholder="correo@ejemplo.com"
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          textContentType="username"
        />
        <TextInput
          accessibilityLabel="Contraseña"
          autoCapitalize="none"
          autoComplete="password"
          autoCorrect={false}
          placeholder="********"
          secureTextEntry
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          textContentType="password"
        />
        <Pressable
          accessibilityRole="button"
          accessibilityState={{ disabled: isDisabled }}
          onPress={handleSubmit}
          disabled={isDisabled}
          style={({ pressed }) => [
            styles.button,
            isDisabled && styles.buttonDisabled,
            pressed && !isDisabled && styles.buttonPressed,
          ]}
        >
          <Text style={styles.buttonLabel}>
            {isSubmitting || status === "loading" ? "Iniciando sesión…" : "Iniciar sesión"}
          </Text>
        </Pressable>
        {lastError ? <Text style={styles.error}>{lastError}</Text> : null}
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  flex: {
    flex: 1,
  },
  container: {
    flex: 1,
    justifyContent: "center",
    paddingHorizontal: 24,
    backgroundColor: "#FFFFFF",
  },
  heading: {
    fontSize: 28,
    fontWeight: "600",
    marginBottom: 24,
  },
  input: {
    borderColor: "#D1D5DB",
    borderRadius: 8,
    borderWidth: 1,
    fontSize: 16,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginBottom: 16,
  },
  button: {
    alignItems: "center",
    backgroundColor: "#2563EB",
    borderRadius: 8,
    paddingVertical: 14,
  },
  buttonLabel: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  buttonDisabled: {
    backgroundColor: "#9CA3AF",
  },
  buttonPressed: {
    opacity: 0.85,
  },
  error: {
    marginTop: 16,
    color: "#DC2626",
  },
});

export default LoginScreen;

