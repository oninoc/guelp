import React from "react";
import { StyleSheet, Text, View, Pressable } from "react-native";

type Option = {
  id: string | number;
  label: string;
  subtitle?: string;
};

type DynamicSelectProps = {
  label: string;
  value: string | number | null;
  options: Option[];
  onValueChange: (value: string | number | null) => void;
  placeholder?: string;
  isLoading?: boolean;
};

export const DynamicSelect: React.FC<DynamicSelectProps> = ({
  label,
  value,
  options,
  onValueChange,
  placeholder = "Select an option",
  isLoading = false,
}) => {
  const [isOpen, setIsOpen] = React.useState(false);

  const selectedOption = options.find((opt) => String(opt.id) === String(value));

  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <Pressable
        style={styles.select}
        onPress={() => setIsOpen(!isOpen)}
        disabled={isLoading}
      >
        <Text style={[styles.selectText, !value && styles.placeholder]}>
          {isLoading
            ? "Loading..."
            : selectedOption
            ? selectedOption.label + (selectedOption.subtitle ? ` - ${selectedOption.subtitle}` : "")
            : placeholder}
        </Text>
        <Text style={styles.arrow}>{isOpen ? "▲" : "▼"}</Text>
      </Pressable>
      {isOpen && !isLoading && (
        <View style={styles.optionsContainer}>
          <Pressable
            style={styles.option}
            onPress={() => {
              onValueChange(null);
              setIsOpen(false);
            }}
          >
            <Text style={styles.optionText}>None</Text>
          </Pressable>
          {options.map((option) => (
            <Pressable
              key={String(option.id)}
              style={[
                styles.option,
                String(value) === String(option.id) && styles.optionSelected,
              ]}
              onPress={() => {
                onValueChange(option.id);
                setIsOpen(false);
              }}
            >
              <Text
                style={[
                  styles.optionText,
                  String(value) === String(option.id) && styles.optionTextSelected,
                ]}
              >
                {option.label}
                {option.subtitle ? ` - ${option.subtitle}` : ""}
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
    marginBottom: 16,
    zIndex: 1,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 8,
    color: "#000",
  },
  select: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    padding: 12,
    backgroundColor: "#fff",
  },
  selectText: {
    fontSize: 16,
    color: "#000",
    flex: 1,
  },
  placeholder: {
    color: "#999",
  },
  arrow: {
    fontSize: 12,
    color: "#666",
    marginLeft: 8,
  },
  optionsContainer: {
    marginTop: 4,
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    backgroundColor: "#fff",
    maxHeight: 200,
    overflow: "hidden",
  },
  option: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
  optionSelected: {
    backgroundColor: "#E3F2FD",
  },
  optionText: {
    fontSize: 16,
    color: "#000",
  },
  optionTextSelected: {
    fontWeight: "600",
    color: "#007AFF",
  },
});

