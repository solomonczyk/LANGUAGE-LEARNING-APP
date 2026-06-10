import React, { useState, useEffect } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import {
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Button from "../../src/shared/components/Button";
import LoadingScreen from "../../src/shared/components/LoadingScreen";
import ErrorScreen from "../../src/shared/components/ErrorScreen";
import { useLessonDraftStore } from "../../src/state/appState";
import { lessonSessions } from "../../src/services/api";

const LESSON_INFO = {
  title: "My Morning with My Pet",
  goal: "Describe a personal daily routine with a focus on sequence of events and interaction with your pet.",
  task: "Write 3-5 sentences about how your morning started and what happened with your pet.",
  grammarFocus: ["Past tense", "Subject-verb agreement"],
  vocabularyFocus: ["morning", "pet", "breakfast", "walk"],
};

export default function LessonScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const draft = useLessonDraftStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionCreated, setSessionCreated] = useState(false);

  useEffect(() => {
    createSession();
  }, []);

  const createSession = async () => {
    if (sessionCreated) return;
    setLoading(true);
    setError(null);
    try {
      const session = await lessonSessions.create(id!);
      draft.setSessionId(session.session_id);
      setSessionCreated(true);
    } catch (err: any) {
      setError(err.message || "Failed to create lesson session");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!draft.sessionId || draft.currentText.trim().length < 10) return;

    draft.setSubmitting(true);
    draft.setError(null);
    try {
      const submission = await lessonSessions.submitText(
        draft.sessionId,
        draft.currentText,
      );
      router.push(`/lesson-session/${draft.sessionId}`);
    } catch (err: any) {
      draft.setError(err.message || "Failed to submit");
    } finally {
      draft.setSubmitting(false);
    }
  };

  if (loading && !sessionCreated) {
    return <LoadingScreen message="Setting up your lesson..." />;
  }

  if (error && !sessionCreated) {
    return <ErrorScreen message={error} onRetry={createSession} />;
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.flex}
      >
        <ScrollView
          contentContainerStyle={styles.scroll}
          keyboardShouldPersistTaps="handled"
        >
          <Text style={styles.badge}>Personal Narrative</Text>
          <Text style={styles.title}>{LESSON_INFO.title}</Text>

          <View style={styles.goalBox}>
            <Text style={styles.goalLabel}>Communicative Goal</Text>
            <Text style={styles.goalText}>{LESSON_INFO.goal}</Text>
          </View>

          <View style={styles.taskBox}>
            <Text style={styles.taskLabel}>Your Task</Text>
            <Text style={styles.taskText}>{LESSON_INFO.task}</Text>
          </View>

          <View style={styles.supportBox}>
            <Text style={styles.supportTitle}>Grammar Focus</Text>
            <View style={styles.chipRow}>
              {LESSON_INFO.grammarFocus.map((g) => (
                <View key={g} style={styles.chip}>
                  <Text style={styles.chipText}>{g}</Text>
                </View>
              ))}
            </View>
            <Text style={styles.supportTitle}>Key Vocabulary</Text>
            <View style={styles.chipRow}>
              {LESSON_INFO.vocabularyFocus.map((v) => (
                <View key={v} style={styles.chip}>
                  <Text style={styles.chipText}>{v}</Text>
                </View>
              ))}
            </View>
          </View>

          <View style={styles.inputSection}>
            <Text style={styles.inputLabel}>Your Response</Text>
            <TextInput
              style={styles.textInput}
              placeholder="Write your response here... (at least 10 characters)"
              value={draft.currentText}
              onChangeText={draft.setText}
              multiline
              numberOfLines={6}
              textAlignVertical="top"
              editable={!draft.isSubmitting}
            />
            {draft.currentText.length > 0 && draft.currentText.length < 10 && (
              <Text style={styles.minLength}>
                Minimum 10 characters ({draft.currentText.length}/10)
              </Text>
            )}
            {draft.submitError && (
              <Text style={styles.error}>{draft.submitError}</Text>
            )}
          </View>
        </ScrollView>

        <View style={styles.footer}>
          <Button
            title="Submit"
            onPress={handleSubmit}
            disabled={
              draft.isSubmitting ||
              draft.currentText.trim().length < 10
            }
            loading={draft.isSubmitting}
          />
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fff" },
  flex: { flex: 1 },
  scroll: { padding: 24, paddingBottom: 100 },
  badge: {
    fontSize: 13,
    color: "#007AFF",
    fontWeight: "600",
    marginBottom: 8,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  title: { fontSize: 24, fontWeight: "700", marginBottom: 20, color: "#1a1a1a" },
  goalBox: {
    backgroundColor: "#E8F0FE",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  goalLabel: {
    fontSize: 12,
    fontWeight: "600",
    color: "#007AFF",
    textTransform: "uppercase",
    marginBottom: 4,
  },
  goalText: { fontSize: 15, color: "#333", lineHeight: 22 },
  taskBox: {
    backgroundColor: "#FFF3E0",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  taskLabel: {
    fontSize: 12,
    fontWeight: "600",
    color: "#E65100",
    textTransform: "uppercase",
    marginBottom: 4,
  },
  taskText: { fontSize: 16, color: "#333", lineHeight: 22 },
  supportBox: {
    backgroundColor: "#f8f9fa",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  supportTitle: {
    fontSize: 13,
    fontWeight: "600",
    color: "#666",
    marginBottom: 8,
    marginTop: 8,
  },
  chipRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 8 },
  chip: {
    backgroundColor: "#e9ecef",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  chipText: { fontSize: 13, color: "#555" },
  inputSection: { marginBottom: 24 },
  inputLabel: { fontSize: 16, fontWeight: "600", marginBottom: 8, color: "#333" },
  textInput: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 12,
    padding: 14,
    fontSize: 16,
    minHeight: 140,
    backgroundColor: "#fafafa",
  },
  minLength: { fontSize: 12, color: "#E65100", marginTop: 4 },
  error: { color: "#dc3545", fontSize: 14, marginTop: 8 },
  footer: {
    padding: 24,
    paddingBottom: Platform.OS === "ios" ? 36 : 24,
    borderTopWidth: 1,
    borderTopColor: "#f0f0f0",
  },
});
