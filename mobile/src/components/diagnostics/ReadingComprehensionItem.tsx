import React, { useState } from "react";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
import type { DiagnosticItemProps } from "./types";

const PASSAGE = {
  title: "A Busy Morning",
  text: "Maria woke up at 6:30 AM. She made coffee and toast for breakfast. After eating, she walked to the bus stop and took the bus to work. She arrived at 8:45 AM, just in time for her meeting.",
};

const QUESTIONS = [
  { id: "q1", question: "What time did Maria wake up?", options: ["5:30 AM", "6:30 AM", "7:30 AM", "8:00 AM"], correct: 1 },
  { id: "q2", question: "How did Maria get to work?", options: ["She drove", "She walked", "She took the bus", "She took a taxi"], correct: 2 },
  { id: "q3", question: "What did Maria have for breakfast?", options: ["Cereal and milk", "Coffee and toast", "Eggs and bacon", "Nothing"], correct: 1 },
];

export default function ReadingComprehensionItem({ disabled, onResponseChange, feedback }: DiagnosticItemProps) {
  const [answers, setAnswers] = useState<Record<string, number>>({});

  const handleSelect = (qId: string, optIdx: number) => {
    if (disabled) return;
    const next = { ...answers, [qId]: optIdx };
    setAnswers(next);
    const mc_correct = QUESTIONS.filter((q) => next[q.id] === q.correct).length;
    onResponseChange({ mc_correct, mc_total: QUESTIONS.length, mc_responses: next });
  };

  return (
    <View>
      <View style={styles.passage}>
        <Text style={styles.passageTitle}>{PASSAGE.title}</Text>
        <Text style={styles.passageText}>{PASSAGE.text}</Text>
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
                style={[
                  styles.option,
                  selected && !feedback && styles.optionSelected,
                  showCorrect && styles.optionCorrect,
                  showWrong && styles.optionWrong,
                ]}
              >
                <Text style={[styles.optionText, selected && styles.optionTextSelected]}>
                  {opt}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  passage: { backgroundColor: "#F0F4FF", borderRadius: 12, padding: 16, marginBottom: 20 },
  passageTitle: { fontSize: 16, fontWeight: "600", color: "#333", marginBottom: 8 },
  passageText: { fontSize: 14, color: "#555", lineHeight: 22 },
  questionBlock: { marginBottom: 20 },
  questionText: { fontSize: 15, fontWeight: "500", color: "#333", marginBottom: 8 },
  option: { paddingVertical: 10, paddingHorizontal: 14, borderRadius: 8, borderWidth: 1, borderColor: "#ddd", marginBottom: 6, backgroundColor: "#fff" },
  optionSelected: { borderColor: "#007AFF", backgroundColor: "#EBF5FF" },
  optionCorrect: { borderColor: "#34C759", backgroundColor: "#E8F5E9" },
  optionWrong: { borderColor: "#FF3B30", backgroundColor: "#FFF3E0" },
  optionText: { fontSize: 14, color: "#333" },
  optionTextSelected: { color: "#007AFF", fontWeight: "500" },
});
