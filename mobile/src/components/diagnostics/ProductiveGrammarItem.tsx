import React, { useState } from "react";
import { StyleSheet, Text, TextInput, View } from "react-native";
import type { DiagnosticItemProps } from "./types";

const TASKS = [
  { id: "t1", prompt: "Fix the sentence:", text: "he go to school every day", hint: "Use the correct form of 'go'" },
  { id: "t2", prompt: "Fix the sentence:", text: "she walk to the park yesterday", hint: "Use the correct past tense" },
  { id: "t3", prompt: "Fix the sentence:", text: "they is playing football now", hint: "Use the correct form of 'be'" },
];

/** Full corrected sentences (Option A: full sentence rewrite). */
const FULL_EXPECTED = [
  "he goes to school every day",
  "she walked to the park yesterday",
  "they are playing football now",
];

/** Fragments accepted as partial credit (the old expected values). */
const FRAGMENT_EXPECTED = ["he goes", "she walked", "they are"];

/**
 * Normalize a user answer for comparison:
 * - Trim whitespace
 * - Lowercase
 * - Collapse multiple spaces
 * - Strip trailing punctuation (. ! ?)
 */
function normalize(s: string): string {
  return s
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ")
    .replace(/[.!?]+$/, "");
}

export default function ProductiveGrammarItem({ disabled, onResponseChange, feedback }: DiagnosticItemProps) {
  const [inputs, setInputs] = useState<Record<string, string>>({});

  const handleChange = (id: string, value: string) => {
    if (disabled) return;
    const next = { ...inputs, [id]: value };
    setInputs(next);
    const correctCount = Object.keys(next).filter((k) => {
      const idx = TASKS.findIndex((t) => t.id === k);
      if (idx < 0) return false;
      const normalized = normalize(next[k]);
      return normalized === FULL_EXPECTED[idx] || normalized === FRAGMENT_EXPECTED[idx];
    }).length;
    onResponseChange({ correct_count: correctCount, total: TASKS.length, responses: next });
  };

  const getFeedbackText = (userAnswer: string | undefined, idx: number): { text: string; isCorrect: boolean } => {
    if (!userAnswer) return { text: "", isCorrect: false };
    const normalized = normalize(userAnswer);
    if (normalized === FULL_EXPECTED[idx]) {
      return { text: "✓ Correct!", isCorrect: true };
    }
    if (normalized === FRAGMENT_EXPECTED[idx]) {
      return { text: `✓ Correct (full sentence: "${FULL_EXPECTED[idx]}.")`, isCorrect: true };
    }
    return { text: `✗ Expected: "${FULL_EXPECTED[idx]}."`, isCorrect: false };
  };

  return (
    <View>
      <Text style={styles.instruction}>Rewrite the full sentence correctly.</Text>
      <Text style={styles.subInstruction}>Write the whole corrected sentence — include all words.</Text>
      {TASKS.map((task, idx) => (
        <View key={task.id} style={styles.taskBlock}>
          <Text style={styles.taskPrompt}>{task.prompt}</Text>
          <Text style={styles.taskText}>{task.text}</Text>
          <TextInput
            style={styles.input}
            value={inputs[task.id] || ""}
            onChangeText={(v) => handleChange(task.id, v)}
            placeholder="Write the whole corrected sentence..."
            placeholderTextColor="#bbb"
            editable={!disabled}
            autoCapitalize="sentences"
          />
          {!disabled && !inputs[task.id] ? (
            <Text style={styles.hint}>{task.hint}</Text>
          ) : null}
          {feedback ? (
            <Text style={[styles.feedback, getFeedbackText(inputs[task.id], idx).isCorrect ? styles.feedbackCorrect : styles.feedbackWrong]}>
              {getFeedbackText(inputs[task.id], idx).text}
            </Text>
          ) : null}
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  instruction: { fontSize: 15, color: "#555", marginBottom: 4 },
  subInstruction: { fontSize: 13, color: "#888", marginBottom: 16, fontStyle: "italic" },
  taskBlock: { marginBottom: 20, padding: 14, backgroundColor: "#f8f9fa", borderRadius: 12 },
  taskPrompt: { fontSize: 13, fontWeight: "600", color: "#666", marginBottom: 4 },
  taskText: { fontSize: 14, color: "#999", fontStyle: "italic", marginBottom: 10, textDecorationLine: "line-through" },
  input: { borderWidth: 1, borderColor: "#ddd", borderRadius: 8, padding: 10, fontSize: 14, backgroundColor: "#fff", color: "#333" },
  hint: { fontSize: 12, color: "#999", marginTop: 4 },
  feedback: { fontSize: 13, marginTop: 6, fontWeight: "500" },
  feedbackCorrect: { color: "#34C759" },
  feedbackWrong: { color: "#FF3B30" },
});
