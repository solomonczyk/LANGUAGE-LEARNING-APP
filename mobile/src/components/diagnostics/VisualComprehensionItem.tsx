import React, { useState } from "react";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
import type { DiagnosticItemProps } from "./types";

const SCENE_DESCRIPTION = "A sunny park with children playing on swings, a dog running after a ball, and people sitting on benches reading books.";

const CHOICES = [
  { key: "playground", text: "Children are playing while adults watch nearby." },
  { key: "park_scene", text: "A sunny park where children play, a dog runs, and people read." },
  { key: "sports", text: "People are playing sports and exercising in a field." },
  { key: "empty", text: "A quiet park with no one around." },
];

const CORRECT_KEY = "park_scene";

export default function VisualComprehensionItem({ disabled, onResponseChange, feedback }: DiagnosticItemProps) {
  const [selected, setSelected] = useState<string>("");

  const handleSelect = (key: string) => {
    if (disabled) return;
    setSelected(key);
    const correct = key === CORRECT_KEY;
    const hasDetail = key === "park_scene" || key === "playground";
    onResponseChange({ selected_description: key, expected_key: CORRECT_KEY, has_detail: hasDetail });
  };

  return (
    <View>
      <View style={styles.sceneBox}>
        <Text style={styles.sceneIcon}>🖼️</Text>
        <Text style={styles.sceneLabel}>Scene Description</Text>
        <Text style={styles.sceneText}>{SCENE_DESCRIPTION}</Text>
      </View>
      <Text style={styles.prompt}>Which description best matches the scene?</Text>
      {CHOICES.map((c) => {
        const sel = selected === c.key;
        const showCorrect = feedback && sel && c.key === CORRECT_KEY;
        const showWrong = feedback && sel && c.key !== CORRECT_KEY;
        return (
          <TouchableOpacity
            key={c.key}
            disabled={disabled}
            onPress={() => handleSelect(c.key)}
            style={[styles.choice, sel && !feedback && styles.choiceSelected, showCorrect && styles.choiceCorrect, showWrong && styles.choiceWrong]}
          >
            <Text style={[styles.choiceText, sel && styles.choiceTextSelected]}>{c.text}</Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  sceneBox: { backgroundColor: "#F3E5F5", borderRadius: 12, padding: 16, marginBottom: 16, alignItems: "center" },
  sceneIcon: { fontSize: 32, marginBottom: 8 },
  sceneLabel: { fontSize: 14, fontWeight: "600", color: "#7B1FA2", marginBottom: 8 },
  sceneText: { fontSize: 14, color: "#555", lineHeight: 22, textAlign: "center", fontStyle: "italic" },
  prompt: { fontSize: 15, fontWeight: "500", color: "#333", marginBottom: 12 },
  choice: { paddingVertical: 12, paddingHorizontal: 14, borderRadius: 8, borderWidth: 1, borderColor: "#ddd", marginBottom: 8, backgroundColor: "#fff" },
  choiceSelected: { borderColor: "#007AFF", backgroundColor: "#EBF5FF" },
  choiceCorrect: { borderColor: "#34C759", backgroundColor: "#E8F5E9" },
  choiceWrong: { borderColor: "#FF3B30", backgroundColor: "#FFF3E0" },
  choiceText: { fontSize: 14, color: "#333" },
  choiceTextSelected: { color: "#007AFF", fontWeight: "500" },
});
