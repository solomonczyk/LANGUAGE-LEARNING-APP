import React from "react";
import { StyleSheet, Text, View } from "react-native";
import type { FeedbackData } from "./types";

interface Props {
  feedback: FeedbackData;
}

export default function FeedbackDisplay({ feedback }: Props) {
  return (
    <View style={[styles.container, feedback.correct ? styles.correct : styles.incorrect]}>
      <Text style={styles.icon}>{feedback.correct ? "✓" : "✗"}</Text>
      <View style={styles.textGroup}>
        <Text style={styles.title}>{feedback.correct ? "Correct!" : "Not quite"}</Text>
        <Text style={styles.text}>{feedback.text}</Text>
        {feedback.details ? (
          <Text style={styles.details}>{feedback.details}</Text>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    alignItems: "flex-start",
  },
  correct: { backgroundColor: "#E8F5E9" },
  incorrect: { backgroundColor: "#FFF3E0" },
  icon: { fontSize: 24, marginRight: 12, marginTop: 2 },
  textGroup: { flex: 1 },
  title: { fontSize: 16, fontWeight: "600", marginBottom: 4, color: "#333" },
  text: { fontSize: 14, color: "#555", lineHeight: 20 },
  details: { fontSize: 13, color: "#777", marginTop: 6, fontStyle: "italic" },
});
