import React, { useState } from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import type { DiagnosticItemProps } from "./types";

const MESSAGE = "Your friend wrote: \"I'm feeling nervous about the exam tomorrow. I don't think I studied enough.\"";

const EXPLANATIONS = [
  { key: "worried", text: "Tell them it's normal to feel worried and offer to help study.", has_key_point: true },
  { key: "ignore", text: "Just say \"good luck\" and change the subject.", has_key_point: false },
  { key: "lecture", text: "Explain why they should have studied more.", has_key_point: false },
];

export default function MediationItem({ disabled, onResponseChange, feedback }: DiagnosticItemProps) {
  const [selectedKey, setSelectedKey] = useState<string>("");
  const [hasDetail, setHasDetail] = useState(false);

  const handleSelect = (key: string, hasKeyPoint: boolean) => {
    if (disabled) return;
    setSelectedKey(key);
    setHasDetail(true);
    const wordCount = hasKeyPoint ? 30 : 10;
    onResponseChange({
      has_key_points: hasKeyPoint,
      word_count: wordCount,
      selected_response: key,
    });
  };

  return (
    <View>
      <View style={styles.messageBox}>
        <Text style={styles.messageLabel}>📩 Message from a friend</Text>
        <Text style={styles.messageText}>{MESSAGE}</Text>
      </View>
      <Text style={styles.prompt}>How would you respond? Choose the best approach.</Text>
      {EXPLANATIONS.map((e) => {
        const sel = selectedKey === e.key;
        const showCorrect = feedback && sel && e.has_key_point;
        const showWrong = feedback && sel && !e.has_key_point;
        return (
          <TouchableOpacity
            key={e.key}
            disabled={disabled}
            onPress={() => handleSelect(e.key, e.has_key_point)}
            style={[styles.choice, sel && !feedback && styles.choiceSelected, showCorrect && styles.choiceCorrect, showWrong && styles.choiceWrong]}
          >
            <Text style={[styles.choiceText, sel && styles.choiceTextSelected]}>{e.text}</Text>
          </TouchableOpacity>
        );
      })}
      {selectedKey && !feedback ? (
        <Text style={styles.selectedNote}>You selected an approach. Tap Submit to continue.</Text>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  messageBox: { backgroundColor: "#E3F2FD", borderRadius: 12, padding: 16, marginBottom: 16 },
  messageLabel: { fontSize: 13, fontWeight: "600", color: "#1565C0", marginBottom: 8 },
  messageText: { fontSize: 14, color: "#555", lineHeight: 22, fontStyle: "italic" },
  prompt: { fontSize: 15, fontWeight: "500", color: "#333", marginBottom: 12 },
  choice: { paddingVertical: 12, paddingHorizontal: 14, borderRadius: 8, borderWidth: 1, borderColor: "#ddd", marginBottom: 8, backgroundColor: "#fff" },
  choiceSelected: { borderColor: "#007AFF", backgroundColor: "#EBF5FF" },
  choiceCorrect: { borderColor: "#34C759", backgroundColor: "#E8F5E9" },
  choiceWrong: { borderColor: "#FF3B30", backgroundColor: "#FFF3E0" },
  choiceText: { fontSize: 14, color: "#333" },
  choiceTextSelected: { color: "#007AFF", fontWeight: "500" },
  selectedNote: { fontSize: 13, color: "#007AFF", textAlign: "center", marginTop: 4 },
});
