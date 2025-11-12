import React from "react";
import { Platform, Pressable, StyleSheet, Text, View } from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";

type DatePickerProps = {
  label: string;
  value: string | null;
  onChange: (date: string | null) => void;
  placeholder?: string;
};

export const DatePicker: React.FC<DatePickerProps> = ({
  label,
  value,
  onChange,
  placeholder = "Select date",
}) => {
  const [showPicker, setShowPicker] = React.useState(false);
  const [internalDate, setInternalDate] = React.useState<Date | null>(
    value ? new Date(value) : null
  );

  React.useEffect(() => {
    if (value) {
      const parsed = new Date(value);
      if (!isNaN(parsed.getTime())) {
        setInternalDate(parsed);
      }
    } else {
      setInternalDate(null);
    }
  }, [value]);

  const handleDateChange = (event: any, selectedDate?: Date) => {
    if (Platform.OS === "android") {
      setShowPicker(false);
    }
    if (Platform.OS === "web") {
      // On web, use HTML5 date input
      return;
    }
    if (selectedDate) {
      setInternalDate(selectedDate);
      const year = selectedDate.getFullYear();
      const month = String(selectedDate.getMonth() + 1).padStart(2, "0");
      const day = String(selectedDate.getDate()).padStart(2, "0");
      onChange(`${year}-${month}-${day}`);
    }
  };

  const formatDate = (date: Date | null): string => {
    if (!date) return "";
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  if (Platform.OS === "web") {
    const inputRef = React.useRef<HTMLInputElement | null>(null);
    
    React.useEffect(() => {
      // Create input element on mount
      const input = document.createElement("input");
      input.type = "date";
      input.value = value || "";
      input.style.position = "absolute";
      input.style.opacity = "0";
      input.style.pointerEvents = "none";
      input.style.width = "0";
      input.style.height = "0";
      input.style.zIndex = "-1";
      
      input.onchange = (e: any) => {
        onChange(e.target.value || null);
      };
      
      document.body.appendChild(input);
      inputRef.current = input;
      
      return () => {
        if (inputRef.current && inputRef.current.parentNode) {
          inputRef.current.parentNode.removeChild(inputRef.current);
        }
      };
    }, [value, onChange]);
    
    return (
      <View style={styles.container}>
        <Text style={styles.label}>{label}</Text>
        <Pressable
          style={styles.picker}
          onPress={() => {
            if (inputRef.current) {
              // Update value before showing
              inputRef.current.value = value || "";
              // Try showPicker first (modern browsers), fallback to click
              if (typeof (inputRef.current as any).showPicker === "function") {
                (inputRef.current as any).showPicker();
              } else {
                inputRef.current.click();
              }
            }
          }}
        >
          <Text style={[styles.pickerText, !value && styles.placeholder]}>
            {value || placeholder}
          </Text>
          <Text style={styles.arrow}>▼</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <Pressable
        style={styles.picker}
        onPress={() => setShowPicker(true)}
      >
        <Text style={[styles.pickerText, !internalDate && styles.placeholder]}>
          {internalDate ? formatDate(internalDate) : placeholder}
        </Text>
        <Text style={styles.arrow}>▼</Text>
      </Pressable>
      {showPicker && (
        <DateTimePicker
          value={internalDate || new Date()}
          mode="date"
          display={Platform.OS === "ios" ? "spinner" : "default"}
          onChange={handleDateChange}
          maximumDate={new Date()}
        />
      )}
      {Platform.OS === "ios" && showPicker && (
        <Pressable
          style={styles.doneButton}
          onPress={() => setShowPicker(false)}
        >
          <Text style={styles.doneButtonText}>Done</Text>
        </Pressable>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 8,
    color: "#000",
  },
  picker: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    padding: 12,
    backgroundColor: "#fff",
  },
  pickerText: {
    fontSize: 16,
    color: "#000",
  },
  placeholder: {
    color: "#999",
  },
  arrow: {
    fontSize: 12,
    color: "#666",
  },
  doneButton: {
    marginTop: 8,
    padding: 12,
    backgroundColor: "#007AFF",
    borderRadius: 8,
    alignItems: "center",
  },
  doneButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});

