import React, { useState } from "react";
import { StyleSheet, Text, TextInput, View } from "react-native";
import type { DiagnosticItemProps } from "./types";

const TASKS = [
  { id: "t1", prompt: "Fix the sentence:", text: "he go to school every day", hint: "Use the correct form of 'go'" },
  { id: "t2", prompt: "Fix the sentence:", text: "she walk to the park yesterday", hint: "Use the correct past tense" },
  { id: "t3", prompt: "Fix the sentence:", text: "they is playing football now", hint: "Use the correct form of 'be'" },
];

const EXPECTED = ["he goes", "she walked", "they are"];

export default function ProductiveGrammarItem({ disabled, onResponseChange, feedback }: DiagnosticItemProps) {
  const [inputs, setInputs] = useState<Record<string, string>>({});

  const handleChange = (id: string, value: string) => {
    if (disabled) return;
    const next = { ...inputs, [id]: value };
    setInputs(next);
    const correctCount = Object.keys(next).filter((k) => {
      const idx = TASKS.findIndex((t) => t.id === k);
      return idx >= 0 && next[k].toLowerCase().trim() === EXPECTED[idx];
    }).length;
    onResponseChange({ correct_count: correctCount, total: TASKS.length, responses: next });
  };

  return (
    <View>
      <Text style={styles.instruction}>Rewrite each sentence correctly.</Text>
      {TASKS.map((task, idx) => (
        <View key={task.id} style={styles.taskBlock}>
          <Text style={styles.taskPrompt}>{task.prompt}</Text>
          <Text style={styles.taskText}>{task.text}</Text>
          <TextInput
            style={styles.input}
            value={inputs[task.id] || ""}
            onChangeText={(v) => handleChange(task.id, v)}
            placeholder={`Write the correct sentence...`}
            placeholderTextColor="#bbb"
            editable={!disabled}
            autoCapitalize="none"
          />
          {!disabled && !inputs[task.id] ? (
            <Text style={styles.hint}>{task.hint}</Text>
          ) : null}
          {feedback ? (
            <Text style={[styles.feedback, (inputs[task.id]?.toLowerCase().trim() === EXPECTED[idx]) ? styles.feedbackCorrect : styles.feedbackWrong]}>
              {(inputs[task.id]?.toLowerCase().trim() === EXPECTED[idx]) ? "✓ Correct" : `✗ Expected: "${EXPECTED[idx]}"`}
            </Text>
          ) : null}
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  instruction: { fontSize: 15, color: "#555", marginBottom: 16 },
  taskBlock: { marginBottom: 20, padding: 14, backgroundColor: "#f8f9fa", borderRadius: 12 },
  taskPrompt: { fontSize: 13, fontWeight: "600", color: "#666", marginBottom: 4 },
  taskText: { fontSize: 14, color: "#999", fontStyle: "italic", marginBottom: 10, textDecorationLine: "line-through" },
  input: { borderWidth: 1, borderColor: "#ddd", borderRadius: 8, padding: 10, fontSize: 14, backgroundColor: "#fff", color: "#333" },
  hint: { fontSize: 12, color: "#999", marginTop: 4 },
  feedback: { fontSize: 13, marginTop: 6, fontWeight: "500" },
  feedbackCorrect: { color: "#34C759" },
  feedbackWrong: { color: "#FF3B30" },
});
