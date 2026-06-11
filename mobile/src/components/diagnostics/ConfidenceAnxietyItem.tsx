import React, { useState } from "react";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
import type { DiagnosticItemProps } from "./types";

const RATINGS = [
  { key: "speaking", question: "I feel confident when speaking in the new language.", default: 3 },
  { key: "writing", question: "I feel confident when writing in the new language.", default: 3 },
  { key: "listening", question: "I feel anxious when listening to the new language.", default: 3 },
  { key: "mistakes", question: "I am afraid of making mistakes.", default: 3 },
];

const LEVELS = [
  { value: 1, label: "Strongly Disagree" },
  { value: 2, label: "Disagree" },
  { value: 3, label: "Neutral" },
  { value: 4, label: "Agree" },
  { value: 5, label: "Strongly Agree" },
];

export default function ConfidenceAnxietyItem({ disabled, onResponseChange, feedback }: DiagnosticItemProps) {
  const [ratings, setRatings] = useState<Record<string, number>>({});

  const handleRate = (key: string, value: number) => {
    if (disabled) return;
    const next = { ...ratings, [key]: value };
    setRatings(next);
    const values = RATINGS.map((r) => next[r.key] || r.default);
    onResponseChange({ ratings: values });
  };

  const allRated = RATINGS.every((r) => ratings[r.key] !== undefined);

  return (
    <View>
      <Text style={styles.instruction}>Rate each statement honestly. This helps us understand your learning needs.</Text>
      {RATINGS.map((item) => (
        <View key={item.key} style={styles.ratingBlock}>
          <Text style={styles.question}>{item.question}</Text>
          <View style={styles.optionsRow}>
            {LEVELS.map((level) => {
              const selected = ratings[item.key] === level.value;
              return (
                <TouchableOpacity
                  key={level.value}
                  disabled={disabled}
                  onPress={() => handleRate(item.key, level.value)}
                  style={[styles.option, selected && styles.optionSelected]}
                >
                  <Text style={[styles.optionValue, selected && styles.optionValueSelected]}>{level.value}</Text>
                  <Text style={[styles.optionLabel, selected && styles.optionLabelSelected]}>{level.label.split(" ")[0]}</Text>
                </TouchableOpacity>
              );
            })}
          </View>
        </View>
      ))}
      {allRated && !feedback ? (
        <Text style={styles.readyText}>All rated. Tap Submit to continue.</Text>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  instruction: { fontSize: 14, color: "#555", marginBottom: 20, lineHeight: 20 },
  ratingBlock: { marginBottom: 20 },
  question: { fontSize: 14, fontWeight: "500", color: "#333", marginBottom: 8 },
  optionsRow: { flexDirection: "row", gap: 6 },
  option: { flex: 1, alignItems: "center", paddingVertical: 10, borderRadius: 8, borderWidth: 1, borderColor: "#ddd", backgroundColor: "#fff" },
  optionSelected: { borderColor: "#007AFF", backgroundColor: "#EBF5FF" },
  optionValue: { fontSize: 16, fontWeight: "600", color: "#666" },
  optionValueSelected: { color: "#007AFF" },
  optionLabel: { fontSize: 9, color: "#999", marginTop: 2 },
  optionLabelSelected: { color: "#007AFF" },
  readyText: { fontSize: 13, color: "#007AFF", textAlign: "center", marginTop: 8 },
});
