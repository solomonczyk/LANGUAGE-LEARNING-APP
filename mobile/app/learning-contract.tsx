import React, { useCallback, useEffect, useState } from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { useQuery } from "@tanstack/react-query";
import Button from "../src/shared/components/Button";
import LoadingScreen from "../src/shared/components/LoadingScreen";
import ErrorScreen from "../src/shared/components/ErrorScreen";
import { learningContract } from "../src/services/api";

export default function LearningContractScreen() {
  const router = useRouter();
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState<string | null>(null);
  const [needsContract, setNeedsContract] = useState(false);

  const {
    data: contract,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["learning-contract"],
    queryFn: () => learningContract.getCurrent(),
    retry: false,
  });

  // Detect when contract doesn't exist yet and auto-create
  useEffect(() => {
    if (error && !needsContract && !creating) {
      const apiError = error as { status?: number; code?: string };
      if (apiError?.status === 404 || apiError?.code === "NOT_FOUND") {
        setNeedsContract(true);
      }
    }
  }, [error, needsContract, creating]);

  const handleCreate = useCallback(async () => {
    if (creating) return;
    setCreating(true);
    setCreateError(null);
    try {
      await learningContract.create();
      await refetch();
    } catch (err: any) {
      setCreateError(err?.message || "Failed to create learning plan");
    } finally {
      setCreating(false);
    }
  }, [creating, refetch]);

  // Auto-create triggered when needed
  useEffect(() => {
    if (needsContract && !creating && !contract) {
      handleCreate();
    }
  }, [needsContract, creating, contract, handleCreate]);

  // Show loading while fetching or creating contract
  if (isLoading || creating || needsContract) {
    return (
      <LoadingScreen
        message={
          creating || needsContract
            ? "Creating your learning plan..."
            : "Loading your learning plan..."
        }
      />
    );
  }

  // Show error for non-404 failures
  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <ErrorScreen
          message={createError || "Could not load learning contract."}
          onRetry={() => {
            setNeedsContract(true);
          }}
        />
      </SafeAreaView>
    );
  }

  const contractData = contract as Record<string, any> | undefined;

  // Determine learner level from contract data
  const assessments = (contractData?.diagnostic_profile_snapshot as any)?.assessments || [];
  const levels = ["A1", "A2", "B1", "B2", "C1", "C2"];
  const cefrValues = assessments.map((a: any) => a.cefr).filter(Boolean);
  const learnerLevel = cefrValues.length > 0
    ? cefrValues.reduce((lowest: string, level: string) =>
        levels.indexOf(level) < levels.indexOf(lowest) ? level : lowest
      , "C2")
    : "A1";
  const isA1 = learnerLevel === "A1";

  /** Plain-language explanations for contract terms. */
  function getTermExplanation(label: string): string {
    const explanations: Record<string, string> = {
      "Active Vocabulary Budget": isA1
        ? "New words you will learn in each lesson"
        : "Number of new vocabulary items introduced per lesson",
      "Grammar Focus Count": isA1
        ? "Grammar topics we will practice"
        : "Number of grammar areas covered in each lesson",
      "Max Corrections per Lesson": isA1
        ? "How many small fixes we suggest (gentle feedback)"
        : "Maximum number of primary corrections shown per submission",
      "Scaffolding Level": isA1
        ? "How much help and support you get"
          : "Amount of structural support provided during lessons",
      "Lesson Complexity": isA1
        ? "How challenging the lesson will be"
        : "Cognitive complexity level of lesson content",
      "Lesson Duration": "How long each lesson is designed to take",
      "Target Language": "The language you are learning",
      "Support Language": "Your native language — used for explanations",
      "Contract Version": "Plan version number",
    };
    return explanations[label] || "";
  }

  const items = contractData
    ? [
        { label: "Target Language", value: contractData.target_language },
        { label: "Support Language", value: contractData.support_language },
        { label: "Lesson Duration", value: `${contractData.lesson_duration_minutes} min` },
        { label: "Active Vocabulary Budget", value: `${contractData.active_vocabulary_budget} words` },
        { label: "Grammar Focus Count", value: `${contractData.grammar_focus_count} areas` },
        { label: "Max Corrections per Lesson", value: `${contractData.max_primary_corrections}` },
        { label: "Scaffolding Level", value: contractData.scaffolding_mode },
        { label: "Lesson Complexity", value: contractData.lesson_complexity },
        { label: "Contract Version", value: contractData.version },
      ]
    : [];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.badge}>{isA1 ? "Your Learning Plan" : "Learning Entry Contract"}</Text>
        <Text style={styles.title}>
          {isA1 ? "Your Personal Learning Plan" : "Learning Entry Contract"}
        </Text>
        <Text style={styles.subtitle}>
          {isA1
            ? "Based on your answers, we made a plan just for you. Here's what you can expect."
            : "Based on your diagnostic results, we've created a personalized learning plan for you."
          }
        </Text>

        {contractData && (
          <View style={styles.card}>
            {items.map((item, index) => {
              const explanation = getTermExplanation(item.label);
              return (
                <View key={item.label}>
                  <View
                    style={[styles.row, index < items.length - 1 && styles.borderRow]}
                  >
                    <View style={styles.rowLabelGroup}>
                      <Text style={styles.rowLabel}>{item.label}</Text>
                      {isA1 && explanation ? (
                        <Text style={styles.rowExplanation}>{explanation}</Text>
                      ) : null}
                    </View>
                    <Text style={styles.rowValue}>{item.value}</Text>
                  </View>
                  {!isA1 && explanation && index < items.length - 1 ? (
                    <Text style={styles.hintText}>{explanation}</Text>
                  ) : null}
                </View>
              );
            })}
          </View>
        )}

        {assessments.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>
              {isA1 ? "Your Skills" : "Skill Profile"}
            </Text>
            {assessments.map((a: any, i: number) => (
              <View key={i} style={styles.skillRow}>
                <Text style={styles.skillName}>
                  {a.skill?.replace(/_/g, " ") || "Skill"}
                </Text>
                <View style={styles.levelBadge}>
                  <Text style={styles.levelText}>{a.cefr || "N/A"}</Text>
                </View>
                <Text style={styles.confidence}>
                  {(a.confidence * 100).toFixed(0)}% confidence
                </Text>
              </View>
            ))}
          </View>
        )}

        {/* Summary explanation for A1 */}
        {isA1 && (
          <View style={styles.summaryBox}>
            <Text style={styles.summaryBoxTitle}>What this means for you</Text>
            <Text style={styles.summaryBoxText}>
              ✓ Lessons will be {contractData?.lesson_duration_minutes || 10} minutes long.
            </Text>
            <Text style={styles.summaryBoxText}>
              ✓ You'll learn {contractData?.active_vocabulary_budget || 3} new words each lesson.
            </Text>
            <Text style={styles.summaryBoxText}>
              ✓ Extra support is available whenever you need it.
            </Text>
            <Text style={styles.summaryBoxText}>
              ✓ You can repeat lessons if you want more practice.
            </Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.footer}>
        <Button title="Start Your First Lesson!" onPress={() => router.replace("/home")} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fff" },
  scroll: { padding: 24 },
  badge: {
    fontSize: 13,
    color: "#007AFF",
    fontWeight: "600",
    marginBottom: 8,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  title: { fontSize: 26, fontWeight: "700", marginBottom: 8, color: "#1a1a1a" },
  subtitle: { fontSize: 15, color: "#666", marginBottom: 32, lineHeight: 22 },
  card: {
    backgroundColor: "#f8f9fa",
    borderRadius: 16,
    padding: 4,
    marginBottom: 24,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 14,
    paddingHorizontal: 16,
  },
  borderRow: { borderBottomWidth: 1, borderBottomColor: "#e9ecef" },
  rowLabelGroup: { flex: 1, marginRight: 8 },
  rowLabel: { fontSize: 15, color: "#666" },
  rowExplanation: { fontSize: 12, color: "#999", marginTop: 2, lineHeight: 16 },
  rowValue: { fontSize: 15, fontWeight: "600", color: "#1a1a1a" },
  hintText: { fontSize: 12, color: "#999", paddingHorizontal: 16, paddingBottom: 8, lineHeight: 16 },
  section: { marginBottom: 24 },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 12,
    color: "#333",
  },
  skillRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  skillName: { flex: 1, fontSize: 14, color: "#333", textTransform: "capitalize" },
  levelBadge: {
    backgroundColor: "#E8F0FE",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
    marginRight: 8,
  },
  levelText: { fontSize: 13, fontWeight: "600", color: "#007AFF" },
  confidence: { fontSize: 12, color: "#999" },
  summaryBox: {
    backgroundColor: "#E8F5E9",
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  summaryBoxTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#2E7D32",
    marginBottom: 12,
  },
  summaryBoxText: {
    fontSize: 14,
    color: "#33691E",
    lineHeight: 22,
    marginBottom: 4,
  },
  footer: {
    padding: 24,
    paddingBottom: 36,
    borderTopWidth: 1,
    borderTopColor: "#f0f0f0",
  },
});
