import React, { useState, useEffect } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Button from "../../src/shared/components/Button";
import ProgressBar from "../../src/shared/components/ProgressBar";
import ErrorScreen from "../../src/shared/components/ErrorScreen";
import { lessonSessions } from "../../src/services/api";

const PROCESSING_STEPS = [
  { label: "Submitting text", key: "submitting" },
  { label: "Validating input", key: "validating" },
  { label: "Running analysis", key: "analysis" },
  { label: "Linguistic check", key: "linguistic" },
  { label: "Pedagogical check", key: "pedagogical" },
  { label: "Making decision", key: "decision" },
  { label: "Finalizing", key: "finalizing" },
];

export default function LessonSessionScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [processing, setProcessing] = useState(true);
  const [result, setResult] = useState<Record<string, any> | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    runProcessing();
  }, []);

  const runProcessing = async () => {
    // Simulate processing steps with progress
    for (let i = 1; i <= PROCESSING_STEPS.length; i++) {
      setStep(i);
      await new Promise((r) => setTimeout(r, 400));
    }

    try {
      const processResult = await lessonSessions.process(id!);
      setResult(processResult);

      if (processResult.status === "COMPLETED") {
        // Navigate to result after brief pause
        setTimeout(() => {
          router.replace(
            `/result/${id}?status=${processResult.status}&decision=${processResult.decision || ""}`,
          );
        }, 1500);
      }
    } catch (err: any) {
      setError(err.message || "Processing failed");
    } finally {
      setProcessing(false);
    }
  };

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <ErrorScreen message={error} onRetry={runProcessing} />
      </SafeAreaView>
    );
  }

  const progress = step / PROCESSING_STEPS.length;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Analyzing Your Response</Text>
        <Text style={styles.subtitle}>
          We're reviewing your text through our validation pipeline.
        </Text>

        <ProgressBar progress={progress} style={styles.progress} />

        <View style={styles.stepsContainer}>
          {PROCESSING_STEPS.map((s, i) => (
            <View key={s.key} style={styles.stepRow}>
              <View
                style={[
                  styles.stepDot,
                  i < step && styles.stepDotCompleted,
                  i === step && styles.stepDotActive,
                ]}
              >
                {i < step && <Text style={styles.checkmark}>✓</Text>}
              </View>
              <Text
                style={[
                  styles.stepLabel,
                  i < step && styles.stepLabelCompleted,
                  i === step && styles.stepLabelActive,
                ]}
              >
                {s.label}
              </Text>
            </View>
          ))}
        </View>

        {!processing && result && (
          <View style={styles.resultBox}>
            <Text style={styles.resultText}>
              {result.status === "COMPLETED"
                ? "✓ Lesson completed successfully!"
                : `Status: ${result.status}`}
            </Text>
          </View>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fff" },
  content: { flex: 1, padding: 24, justifyContent: "center" },
  title: {
    fontSize: 24,
    fontWeight: "700",
    marginBottom: 8,
    color: "#1a1a1a",
    textAlign: "center",
  },
  subtitle: {
    fontSize: 15,
    color: "#666",
    marginBottom: 32,
    textAlign: "center",
    lineHeight: 22,
  },
  progress: { marginBottom: 32 },
  stepsContainer: { gap: 4, marginBottom: 32 },
  stepRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    gap: 12,
  },
  stepDot: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: "#f0f0f0",
    justifyContent: "center",
    alignItems: "center",
  },
  stepDotCompleted: { backgroundColor: "#34C759" },
  stepDotActive: { backgroundColor: "#007AFF" },
  checkmark: { color: "#fff", fontSize: 12, fontWeight: "700" },
  stepLabel: { fontSize: 15, color: "#999" },
  stepLabelCompleted: { color: "#34C759" },
  stepLabelActive: { color: "#007AFF", fontWeight: "600" },
  resultBox: {
    backgroundColor: "#E8F5E9",
    borderRadius: 12,
    padding: 16,
    alignItems: "center",
  },
  resultText: { fontSize: 16, color: "#2E7D32", fontWeight: "600" },
});
