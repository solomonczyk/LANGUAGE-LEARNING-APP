import React, { useState, useEffect } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import Button from "../src/shared/components/Button";
import StepIndicator from "../src/shared/components/StepIndicator";
import LoadingScreen from "../src/shared/components/LoadingScreen";
import ErrorScreen from "../src/shared/components/ErrorScreen";
import { useDiagnosticStore, useOnboardingStore } from "../src/state/appState";
import { diagnostics, getUserId } from "../src/services/api";

const STEPS = [
  { key: "grammar_recognition", label: "Grammar", prompt: "Which sentence is correct?" },
  { key: "active_vocabulary", label: "Vocabulary", prompt: "Match the words to their meanings" },
  { key: "written_production", label: "Writing", prompt: "Write 2-3 sentences about your morning routine" },
  { key: "narrative_coherence", label: "Coherence", prompt: "Arrange these events in the correct order" },
];

/** Level-specific helper text for diagnostic steps. */
function getLevelHelperText(level: string, stepKey: string): string {
  const l = level.toUpperCase();
  if (stepKey === "grammar_recognition") {
    if (l === "A1") return "This is an example. Just read it — we'll use this as your answer.";
    if (l === "A2") return "This is a sample answer. You don't need to do anything — we'll submit it for you.";
    return "The example below shows a correct answer. It will be submitted as your response.";
  }
  if (stepKey === "active_vocabulary") {
    if (l === "A1") return "Here are some example words and meanings. Just read them — we'll record them.";
    if (l === "A2") return "These are sample vocabulary matches. They'll be used as your response.";
    return "Example vocabulary matches are shown below. These will be submitted as your response.";
  }
  if (stepKey === "narrative_coherence") {
    if (l === "A1") return "The sentences below are in the right order. Just read them — we'll record this.";
    if (l === "A2") return "These events are already in the correct order. Read along — this is your answer.";
    return "The events are arranged in the correct sequence. This sample is your response.";
  }
  return "";
}

export default function DiagnosticScreen() {
  const router = useRouter();
  const store = useDiagnosticStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [textInput, setTextInput] = useState("");

  useEffect(() => {
    initSession();
  }, []);

  const initSession = async () => {
    if (!store.sessionId) {
      setLoading(true);
      setError(null);
      try {
        const session = await diagnostics.createSession();
        store.setSessionId(session.session_id);
      } catch (err: any) {
        setError(err.message || "Failed to start diagnostic");
      } finally {
        setLoading(false);
      }
    }
  };

  const handleResponse = async () => {
    if (!store.sessionId) return;

    setLoading(true);
    setError(null);
    try {
      const step = STEPS[store.currentStep];
      let responseData: Record<string, unknown>;

      switch (step.key) {
        case "grammar_recognition":
          responseData = { is_correct: true };
          break;
        case "active_vocabulary":
          responseData = { correct_count: 4, total_words: 5 };
          break;
        case "written_production":
          responseData = {
            word_count: textInput.split(/\s+/).length,
            has_structure: textInput.length > 30,
            text: textInput,
          };
          break;
        case "narrative_coherence":
          responseData = { correct_order: true };
          break;
        default:
          responseData = {};
      }

      await diagnostics.submitResponse(
        store.sessionId,
        step.key,
        responseData,
      );

      store.setResponse(step.key, responseData);

      if (store.currentStep < STEPS.length - 1) {
        store.nextStep();
        setTextInput("");
      } else {
        // Complete diagnostic
        const result = await diagnostics.complete(store.sessionId);
        store.markComplete();
        router.replace("/learning-contract");
      }
    } catch (err: any) {
      setError(err.message || "Failed to submit response");
    } finally {
      setLoading(false);
    }
  };

  if (loading && !store.sessionId) return <LoadingScreen message="Starting diagnostic..." />;
  if (error && !store.sessionId) return <ErrorScreen message={error} onRetry={initSession} />;

  const currentStep = STEPS[store.currentStep];
  const learnerLevel = useOnboardingStore.getState().selfReportedLevel || "A1";

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.flex}
      >
        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
          <StepIndicator current={store.currentStep} total={STEPS.length} />

          <Text style={styles.stepLabel}>{currentStep.label}</Text>
          <Text style={styles.title}>{currentStep.prompt}</Text>

          {currentStep.key === "grammar_recognition" && (
            <View style={styles.options}>
              <View style={styles.demoBadge}>
                <Text style={styles.demoBadgeText}>Example only</Text>
              </View>
              {[
                { id: "a", text: "He go to school every day." },
                { id: "b", text: "He goes to school every day." },
                { id: "c", text: "He going to school every day." },
              ].map((opt) => (
                <View key={opt.id} style={styles.optionItem}>
                  <Text style={styles.optionText}>{opt.text}</Text>
                </View>
              ))}
              <Text style={styles.correctLabel}>✓ Sentence B is correct</Text>
              <Text style={styles.hint}>{getLevelHelperText(learnerLevel, "grammar_recognition")}</Text>
            </View>
          )}

          {currentStep.key === "active_vocabulary" && (
            <View style={styles.options}>
              <View style={styles.demoBadge}>
                <Text style={styles.demoBadgeText}>Example only</Text>
              </View>
              <Text style={styles.hint}>Here are some example word matches:</Text>
              <Text style={styles.demoText}>• "Morning" → the start of the day</Text>
              <Text style={styles.demoText}>• "Breakfast" → first meal of the day</Text>
              <Text style={styles.demoText}>• "Pet" → a domestic animal</Text>
              <Text style={styles.demoText}>• "Walk" → to move on foot</Text>
              <Text style={styles.correctLabel}>✓ Vocabulary check complete</Text>
              <Text style={styles.hint}>{getLevelHelperText(learnerLevel, "active_vocabulary")}</Text>
            </View>
          )}

          {currentStep.key === "written_production" && (
            <View style={styles.options}>
              <TextInput
                style={styles.textArea}
                placeholder="Write 2-3 sentences about your morning..."
                value={textInput}
                onChangeText={setTextInput}
                multiline
                numberOfLines={5}
                textAlignVertical="top"
              />
              <Text style={styles.hint}>
                Write at least 20 characters. Current: {textInput.length} chars
              </Text>
            </View>
          )}

          {currentStep.key === "narrative_coherence" && (
            <View style={styles.options}>
              <View style={styles.demoBadge}>
                <Text style={styles.demoBadgeText}>Example only</Text>
              </View>
              <Text style={styles.hint}>The events are already in the right order:</Text>
              <Text style={styles.demoText}>1. Wake up</Text>
              <Text style={styles.demoText}>2. Get out of bed</Text>
              <Text style={styles.demoText}>3. Have breakfast</Text>
              <Text style={styles.demoText}>4. Brush teeth</Text>
              <Text style={styles.demoText}>5. Leave home</Text>
              <Text style={styles.correctLabel}>✓ Correct order selected</Text>
              <Text style={styles.hint}>{getLevelHelperText(learnerLevel, "narrative_coherence")}</Text>
            </View>
          )}

          {error && <Text style={styles.error}>{error}</Text>}
        </ScrollView>

        <View style={styles.footer}>
          <Button
            title={
              store.currentStep < STEPS.length - 1
                ? "Next"
                : "Complete Diagnostic"
            }
            onPress={handleResponse}
            disabled={
              loading ||
              (currentStep.key === "written_production" && textInput.length < 10)
            }
            loading={loading}
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
  stepLabel: { fontSize: 14, color: "#007AFF", fontWeight: "500", marginBottom: 8, textAlign: "center" },
  title: { fontSize: 22, fontWeight: "700", marginBottom: 24, color: "#1a1a1a", textAlign: "center" },
  options: { gap: 12 },
  optionItem: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: "#f8f9fa",
    borderWidth: 1,
    borderColor: "#e9ecef",
  },
  optionText: { fontSize: 16, color: "#333" },
  textArea: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 12,
    padding: 14,
    fontSize: 16,
    minHeight: 120,
    backgroundColor: "#fafafa",
  },
  hint: { fontSize: 14, color: "#666", marginTop: 8, fontStyle: "italic", lineHeight: 20 },
  demoBadge: {
    alignSelf: "flex-start",
    backgroundColor: "#E8F0FE",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
    marginBottom: 8,
  },
  demoBadgeText: { fontSize: 12, fontWeight: "600", color: "#007AFF" },
  correctLabel: {
    fontSize: 14,
    color: "#34C759",
    fontWeight: "600",
    marginTop: 8,
    paddingVertical: 4,
  },
  demoText: { fontSize: 15, color: "#555", paddingVertical: 4, paddingLeft: 8 },
  error: { color: "#dc3545", fontSize: 14, textAlign: "center", marginTop: 8 },
  footer: {
    padding: 24,
    paddingBottom: Platform.OS === "ios" ? 36 : 24,
    borderTopWidth: 1,
    borderTopColor: "#f0f0f0",
  },
});
