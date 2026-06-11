import React, { useState } from "react";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
import type { DiagnosticItemProps } from "./types";

const TRANSCRIPT =
  "Anna: Hi Tom, how was your weekend?\nTom: It was great! I went hiking with my friends.\nAnna: That sounds fun! Where did you go?\nTom: We went to Green Mountain. The view was amazing.\nAnna: I'd love to go there sometime.";

const QUESTIONS = [
  { id: "q1", question: "What did Tom do on the weekend?", options: ["He went swimming", "He went hiking", "He visited family", "He stayed home"], correct: 1 },
  { id: "q2", question: "Where did Tom go?", options: ["Blue Lake", "Green Mountain", "Red Valley", "Silver Beach"], correct: 1 },
];

export default function ListeningFallbackItem({ disabled, onResponseChange, feedback }: DiagnosticItemProps) {
  const [answers, setAnswers] = useState<Record<string, number>>({});

  const handleSelect = (qId: string, optIdx: number) => {
    if (disabled) return;
    const next = { ...answers, [qId]: optIdx };
    setAnswers(next);
    onResponseChange({
      q1_correct: next.q1 === 1,
      q2_correct: next.q2 === 1,
      transcript_shown: true,
    });
  };

  const allAnswered = Object.keys(answers).length === QUESTIONS.length;

  return (
    <View>
      <View style={styles.transcriptBox}>
        <Text style={styles.transcriptLabel}>📖 Conversation</Text>
        <Text style={styles.transcriptText}>{TRANSCRIPT}</Text>
        <Text style={styles.fallbackNote}>This is a reading-based listening task — no audio is played.</Text>
      </View>
      {QUESTIONS.map((q) => (
        <View key={q.id} style={styles.questionBlock}>
          <Text style={styles.questionText}>{q.question}</Text>
          {q.options.map((opt, idx) => {
            const selected = answers[q.id] === idx;
            const showCorrect = feedback && q.correct === idx;
            const showWrong = feedback && selected && q.correct !== idx;
            return (
              <TouchableOpacity
                key={idx}
                disabled={disabled}
                onPress={() => handleSelect(q.id, idx)}
                style={[styles.option, selected && !feedback && styles.optionSelected, showCorrect && styles.optionCorrect, showWrong && styles.optionWrong]}
              >
                <Text style={[styles.optionText, selected && styles.optionTextSelected]}>{opt}</Text>
              </TouchableOpacity>
            );
          })}
        </View>
      ))}
      {allAnswered && !feedback ? (
        <Text style={styles.readyText}>You have answered all questions. Tap Submit when ready.</Text>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  transcriptBox: { backgroundColor: "#FFF8E1", borderRadius: 12, padding: 16, marginBottom: 20 },
  transcriptLabel: { fontSize: 14, fontWeight: "600", color: "#F57F17", marginBottom: 8 },
  transcriptText: { fontSize: 14, color: "#555", lineHeight: 22, fontStyle: "italic" },
  fallbackNote: { fontSize: 12, color: "#999", marginTop: 8, fontStyle: "italic" },
  questionBlock: { marginBottom: 20 },
  questionText: { fontSize: 15, fontWeight: "500", color: "#333", marginBottom: 8 },
  option: { paddingVertical: 10, paddingHorizontal: 14, borderRadius: 8, borderWidth: 1, borderColor: "#ddd", marginBottom: 6, backgroundColor: "#fff" },
  optionSelected: { borderColor: "#007AFF", backgroundColor: "#EBF5FF" },
  optionCorrect: { borderColor: "#34C759", backgroundColor: "#E8F5E9" },
  optionWrong: { borderColor: "#FF3B30", backgroundColor: "#FFF3E0" },
  optionText: { fontSize: 14, color: "#333" },
  optionTextSelected: { color: "#007AFF", fontWeight: "500" },
  readyText: { fontSize: 13, color: "#007AFF", textAlign: "center", marginTop: 4 },
});
