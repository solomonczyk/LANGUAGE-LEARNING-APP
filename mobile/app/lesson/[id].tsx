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
import { useQuery } from "@tanstack/react-query";
import Button from "../../src/shared/components/Button";
import LoadingScreen from "../../src/shared/components/LoadingScreen";
import ErrorScreen from "../../src/shared/components/ErrorScreen";
import { useLessonDraftStore } from "../../src/state/appState";
import { lessonSessions, learningContract } from "../../src/services/api";

/** Level-aware lesson content variants for A1 / A2 / B1 / B2. */
interface LevelLessonInfo {
  title: string;
  goal: string;
  task: string;
  grammarFocus: string[];
  vocabularyFocus: string[];
  exampleSentence?: string;
  supportHint?: string;
}

const LEVEL_LESSON_INFO: Record<string, LevelLessonInfo> = {
  A1: {
    title: "My Morning with My Pet",
    goal: "Tell a short story about your morning with your pet.",
    task: "Write 2-3 short sentences. What did you do? What did your pet do? You can use simple words.",
    grammarFocus: ["Past tense — use 'I played', 'I ate'", "Subject-verb agreement — 'He runs', 'She eats'"],
    vocabularyFocus: ["morning", "pet", "breakfast", "walk"],
    exampleSentence: "This morning I walked my dog. He was happy.",
    supportHint: "Use your own language if you need to check a word. Just do your best!",
  },
  A2: {
    title: "My Morning with My Pet",
    goal: "Write about your morning routine with your pet. Use simple sentences.",
    task: "Write 3-4 sentences about what happened this morning. Include your pet if you have one.",
    grammarFocus: ["Past tense", "Subject-verb agreement"],
    vocabularyFocus: ["morning", "pet", "breakfast", "walk"],
    supportHint: "Try using 'first', 'then', 'after' to connect your ideas.",
  },
  B1: {
    title: "My Morning with My Pet",
    goal: "Describe a personal daily routine with a focus on sequence of events and interaction with your pet.",
    task: "Write 3-5 sentences about how your morning started and what happened with your pet. Use time markers to show the order of events.",
    grammarFocus: ["Past tense — narrative consistency", "Subject-verb agreement"],
    vocabularyFocus: ["morning", "pet", "breakfast", "walk"],
  },
  B2: {
    title: "My Morning with My Pet",
    goal: "Craft a concise narrative about your morning, focusing on temporal flow and natural interaction with your pet.",
    task: "Write 4-6 sentences describing your morning routine and your pet's involvement. Use a variety of past tense forms and sequence markers for a natural narrative flow.",
    grammarFocus: ["Past tense variation — simple past, past continuous", "Subject-verb agreement in complex sentences"],
    vocabularyFocus: ["morning", "pet", "breakfast", "walk"],
  },
};

function getLessonInfo(level: string): LevelLessonInfo {
  const l = level.toUpperCase();
  if (l in LEVEL_LESSON_INFO) return LEVEL_LESSON_INFO[l];
  if (l === "C1" || l === "C2") return LEVEL_LESSON_INFO.B2;
  return LEVEL_LESSON_INFO.A2; // default
}

export default function LessonScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const draft = useLessonDraftStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionCreated, setSessionCreated] = useState(false);

  // Fetch contract to get learner level
  const { data: contract } = useQuery({
    queryKey: ["learning-contract"],
    queryFn: () => learningContract.getCurrent(),
    retry: false,
  });

  const contractData = contract as Record<string, any> | undefined;
  const assessments = (contractData?.diagnostic_profile_snapshot as any)?.assessments || [];
  const levels = ["A1", "A2", "B1", "B2", "C1", "C2"];
  const cefrValues = assessments.map((a: any) => a.cefr).filter(Boolean);
  const learnerLevel = cefrValues.length > 0
    ? cefrValues.reduce((lowest: string, level: string) =>
        levels.indexOf(level) < levels.indexOf(lowest) ? level : lowest
      , "C2")
    : "A1";
  const lessonInfo = getLessonInfo(learnerLevel);

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
          <View style={styles.headerRow}>
            <Text style={styles.badge}>Personal Narrative</Text>
            <Text style={styles.levelBadge}>{learnerLevel}</Text>
          </View>
          <Text style={styles.title}>{lessonInfo.title}</Text>

          <View style={styles.goalBox}>
            <Text style={styles.goalLabel}>
              {learnerLevel === "A1" ? "Goal" : "Communicative Goal"}
            </Text>
            <Text style={styles.goalText}>{lessonInfo.goal}</Text>
          </View>

          {learnerLevel === "A1" || learnerLevel === "A2" ? (
            <>
              <View style={styles.goalBox}>
                <Text style={styles.goalLabel}>Your Task</Text>
                <Text style={styles.goalText}>{lessonInfo.task}</Text>
              </View>
              {lessonInfo.exampleSentence && (
                <View style={styles.exampleBox}>
                  <Text style={styles.exampleLabel}>Example sentence</Text>
                  <Text style={styles.exampleText}>{lessonInfo.exampleSentence}</Text>
                </View>
              )}
            </>
          ) : (
            <View style={styles.taskBox}>
              <Text style={styles.taskLabel}>Your Task</Text>
              <Text style={styles.taskText}>{lessonInfo.task}</Text>
            </View>
          )}

          <View style={styles.supportBox}>
            <Text style={styles.supportTitle}>
              {learnerLevel === "A1" ? "What to practice" : "Grammar Focus"}
            </Text>
            <View style={styles.chipRow}>
              {lessonInfo.grammarFocus.map((g) => (
                <View key={g} style={styles.chip}>
                  <Text style={styles.chipText}>{g}</Text>
                </View>
              ))}
            </View>
            <Text style={styles.supportTitle}>
              {learnerLevel === "A1" ? "Useful words" : "Key Vocabulary"}
            </Text>
            <View style={styles.chipRow}>
              {lessonInfo.vocabularyFocus.map((v) => (
                <View key={v} style={styles.chip}>
                  <Text style={styles.chipText}>{v}</Text>
                </View>
              ))}
            </View>
          </View>

          {lessonInfo.supportHint && (
            <View style={styles.hintBox}>
              <Text style={styles.hintIcon}>💡</Text>
              <Text style={styles.hintText}>{lessonInfo.supportHint}</Text>
            </View>
          )}

          <View style={styles.inputSection}>
            <Text style={styles.inputLabel}>
              {learnerLevel === "A1" ? "Write here" : "Your Response"}
            </Text>
            <TextInput
              style={styles.textInput}
              placeholder={
                learnerLevel === "A1"
                  ? "Write 2-3 sentences..."
                  : "Write your response here... (at least 10 characters)"
              }
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
            title={
              learnerLevel === "A1" ? "Send my answer" : "Submit"
            }
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
  headerRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  badge: {
    fontSize: 13,
    color: "#007AFF",
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  levelBadge: {
    fontSize: 12,
    fontWeight: "600",
    color: "#007AFF",
    backgroundColor: "#E8F0FE",
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderRadius: 8,
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
  exampleBox: {
    backgroundColor: "#F3E8FF",
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  exampleLabel: {
    fontSize: 12,
    fontWeight: "600",
    color: "#7C3AED",
    textTransform: "uppercase",
    marginBottom: 4,
  },
  exampleText: { fontSize: 14, color: "#555", lineHeight: 20, fontStyle: "italic" },
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
  hintBox: {
    flexDirection: "row",
    backgroundColor: "#FFF8E1",
    borderRadius: 12,
    padding: 14,
    marginBottom: 16,
    gap: 8,
  },
  hintIcon: { fontSize: 16 },
  hintText: { fontSize: 13, color: "#795548", flex: 1, lineHeight: 18 },
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
