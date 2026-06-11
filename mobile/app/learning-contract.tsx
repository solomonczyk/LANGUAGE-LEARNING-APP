import React, { useCallback, useEffect, useState } from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { useQuery } from "@tanstack/react-query";
import Button from "../src/shared/components/Button";
import LoadingScreen from "../src/shared/components/LoadingScreen";
import ErrorScreen from "../src/shared/components/ErrorScreen";
import { learningContract } from "../src/services/api";
import type { DimensionResultResponse } from "../src/components/diagnostics/types";

/** Format a dimension key as a display label. */
function formatSkillName(key: string): string {
  const labels: Record<string, string> = {
    grammar_recognition: "Grammar Recognition",
    productive_grammar: "Productive Grammar",
    passive_vocabulary: "Passive Vocabulary",
    active_vocabulary: "Active Vocabulary",
    reading_comprehension: "Reading Comprehension",
    listening_comprehension: "Listening Comprehension",
    visual_comprehension: "Visual Comprehension",
    written_production: "Written Production",
    narrative_coherence: "Narrative Coherence",
    mediation: "Mediation",
    communication_strategies: "Communication Strategies",
    confidence_and_anxiety: "Confidence & Anxiety",
    spoken_production: "Spoken Production",
    spoken_interaction: "Spoken Interaction",
    pronunciation: "Pronunciation",
  };
  return labels[key] || key.replace(/_/g, " ");
}

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

  if (isLoading || creating || needsContract) {
    return (
      <LoadingScreen
        message={creating || needsContract ? "Creating your learning plan..." : "Loading your learning plan..."}
      />
    );
  }

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <ErrorScreen message={createError || "Could not load learning contract."} onRetry={() => setNeedsContract(true)} />
      </SafeAreaView>
    );
  }

  const contractData = contract as Record<string, any> | undefined;
  const snapshot = contractData?.diagnostic_profile_snapshot as Record<string, any> | undefined;
  const snapshotVersion = snapshot?.version || "1.0.0";

  // Parse dimensions from snapshot (v2.0.0) or fall back to assessments (v1.0.0)
  let measured: [string, any][] = [];
  let uncertain: [string, any][] = [];
  let notMeasured: [string, any][] = [];
  let deferred: [string, any][] = [];

  if (snapshotVersion === "2.0.0" && snapshot?.dimensions) {
    const allDims = Object.entries(snapshot.dimensions) as [string, any][];
    measured = allDims.filter(([_, info]) => info?.status === "measured" || info?.status === "estimated");
    uncertain = allDims.filter(([_, info]) => info?.status === "uncertain" || (info?.needs_follow_up && !info?.deferred && info?.status !== "not_measured_yet"));
    deferred = allDims.filter(([_, info]) => info?.deferred === true);
    notMeasured = allDims.filter(([_, info]) => info?.status === "not_measured_yet" && !info?.deferred);
  } else {
    // Legacy v1.0.0 — use assessments array
    const rawAssessments = snapshot?.assessments || [];
    const seenSkills = new Set<string>();
    const uniqueAssessments = rawAssessments.filter((a: any) => {
      const key = a.skill || "";
      if (!key || seenSkills.has(key)) return false;
      seenSkills.add(key);
      return true;
    });
    measured = uniqueAssessments.map((a: any) => [a.skill, { estimated_level: a.cefr, confidence: a.confidence, status: "measured" }]);
    uncertain = [];
    deferred = [];
    notMeasured = [];
  }

  // Determine if this is an older-format snapshot for A1-friendly wording
  const isLegacySimple = snapshotVersion === "1.0.0" && measured.length > 0 && measured.every(([_, info]) => info?.estimated_level === "A1");

  /** Plain-language explanations for contract terms. */
  function getTermExplanation(label: string): string {
    const explanations: Record<string, string> = {
      "Active Vocabulary Budget": "Number of new vocabulary items introduced per lesson",
      "Grammar Focus Count": "Number of grammar areas covered in each lesson",
      "Max Corrections per Lesson": "Maximum number of primary corrections shown per submission",
      "Scaffolding Level": "Amount of structural support provided during lessons",
      "Lesson Complexity": "Cognitive complexity level of lesson content",
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

  const hasMeasured = measured.length > 0;
  const hasUncertain = uncertain.length > 0;
  const hasNotMeasured = notMeasured.length > 0;
  const hasDeferred = deferred.length > 0;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.badge}>Your Learning Plan</Text>
        <Text style={styles.title}>Learning Entry Contract</Text>
        <Text style={styles.subtitle}>
          Based on your diagnostic results, we've created a personalized learning plan.
          {hasNotMeasured || hasDeferred ? " Some skills weren't assessed yet and will be explored in future lessons." : ""}
        </Text>

        {/* Contract terms card */}
        {contractData && (
          <View style={styles.card}>
            {items.map((item, index) => {
              const explanation = getTermExplanation(item.label);
              return (
                <View key={item.label}>
                  <View style={[styles.row, index < items.length - 1 && styles.borderRow]}>
                    <View style={styles.rowLabelGroup}>
                      <Text style={styles.rowLabel}>{item.label}</Text>
                      {explanation ? <Text style={styles.rowExplanation}>{explanation}</Text> : null}
                    </View>
                    <Text style={styles.rowValue}>{item.value}</Text>
                  </View>
                </View>
              );
            })}
          </View>
        )}

        {/* ===== Measured Skills ===== */}
        {hasMeasured && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>✅ Measured Skills</Text>
            <Text style={styles.sectionSubtitle}>We have enough information about these skills.</Text>
            {measured.map(([key, info]) => (
              <View key={key} style={styles.skillRow}>
                <Text style={styles.skillName}>{formatSkillName(key)}</Text>
                <View style={styles.levelBadge}>
                  <Text style={styles.levelText}>{info.estimated_level || "N/A"}</Text>
                </View>
                <Text style={styles.confidence}>{(info.confidence * 100).toFixed(0)}%</Text>
              </View>
            ))}
          </View>
        )}

        {/* ===== Uncertain Skills ===== */}
        {hasUncertain && (
          <View style={[styles.section, styles.uncertainSection]}>
            <Text style={[styles.sectionTitle, styles.uncertainTitle]}>⚠️ Needs More Information</Text>
            <Text style={styles.sectionSubtitle}>
              We're not entirely sure about your level in these areas. They may be checked in future lessons.
            </Text>
            {uncertain.map(([key, info]) => (
              <View key={key} style={[styles.skillRow, styles.uncertainRow]}>
                <Text style={styles.skillName}>{formatSkillName(key)}</Text>
                <View style={[styles.levelBadge, styles.uncertainBadge]}>
                  <Text style={[styles.levelText, styles.uncertainLevelText]}>{info.estimated_level || "?"}</Text>
                </View>
                <Text style={styles.confidence}>{(info.confidence * 100).toFixed(0)}%</Text>
              </View>
            ))}
          </View>
        )}

        {/* ===== Not Measured Yet ===== */}
        {hasNotMeasured && (
          <View style={[styles.section, styles.notMeasuredSection]}>
            <Text style={[styles.sectionTitle, styles.notMeasuredTitle]}>📋 Not Assessed Yet</Text>
            <Text style={styles.sectionSubtitle}>
              These skills weren't measured in this screening. They may be explored later.
            </Text>
            {notMeasured.map(([key, _]) => (
              <View key={key} style={[styles.skillRow, styles.notMeasuredRow]}>
                <Text style={[styles.skillName, styles.notMeasuredText]}>{formatSkillName(key)}</Text>
                <Text style={styles.notMeasuredLabel}>waiting</Text>
              </View>
            ))}
          </View>
        )}

        {/* ===== Deferred Skills ===== */}
        {hasDeferred && (
          <View style={[styles.section, styles.deferredSection]}>
            <Text style={[styles.sectionTitle, styles.deferredTitle]}>🎤 Speaking Skills</Text>
            <Text style={styles.sectionSubtitle}>
              Speaking and pronunciation require audio recording, which is not available in this version. These will be noted for future expansion.
            </Text>
            {deferred.map(([key, _]) => (
              <View key={key} style={[styles.skillRow, styles.deferredRow]}>
                <Text style={[styles.skillName, styles.deferredText]}>{formatSkillName(key)}</Text>
                <Text style={styles.deferredLabel}>requires audio</Text>
              </View>
            ))}
          </View>
        )}

        {/* Summary for legacy A1 */}
        {isLegacySimple && (
          <View style={styles.summaryBox}>
            <Text style={styles.summaryBoxTitle}>What this means for you</Text>
            <Text style={styles.summaryBoxText}>✓ Lessons will be {contractData?.lesson_duration_minutes || 10} minutes long.</Text>
            <Text style={styles.summaryBoxText}>✓ You'll learn {contractData?.active_vocabulary_budget || 3} new words each lesson.</Text>
            <Text style={styles.summaryBoxText}>✓ Extra support is available whenever you need it.</Text>
            <Text style={styles.summaryBoxText}>✓ You can repeat lessons if you want more practice.</Text>
          </View>
        )}

        {snapshotVersion === "2.0.0" && hasMeasured && (
          <View style={styles.summaryBox}>
            <Text style={styles.summaryBoxTitle}>Your Learning Path</Text>
            <Text style={styles.summaryBoxText}>
              ✓ Lessons are tailored to your current level across {measured.length} measured skill dimensions.
            </Text>
            {hasUncertain && (
              <Text style={styles.summaryBoxText}>
                ⚠️ We'll check {uncertain.length} area{uncertain.length > 1 ? "s" : ""} where we need more information.
              </Text>
            )}
            {hasNotMeasured && (
              <Text style={styles.summaryBoxText}>
                📋 {notMeasured.length} skill{notMeasured.length > 1 ? "s" : ""} {notMeasured.length > 1 ? "were" : "was"} not assessed — they may be added later.
              </Text>
            )}
            <Text style={styles.summaryBoxText}>
              ✓ You can repeat lessons and your profile will update as you progress.
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
  badge: { fontSize: 13, color: "#007AFF", fontWeight: "600", marginBottom: 8, textTransform: "uppercase", letterSpacing: 1 },
  title: { fontSize: 26, fontWeight: "700", marginBottom: 8, color: "#1a1a1a" },
  subtitle: { fontSize: 15, color: "#666", marginBottom: 32, lineHeight: 22 },
  card: { backgroundColor: "#f8f9fa", borderRadius: 16, padding: 4, marginBottom: 24 },
  row: { flexDirection: "row", justifyContent: "space-between", paddingVertical: 14, paddingHorizontal: 16 },
  borderRow: { borderBottomWidth: 1, borderBottomColor: "#e9ecef" },
  rowLabelGroup: { flex: 1, marginRight: 8 },
  rowLabel: { fontSize: 15, color: "#666" },
  rowExplanation: { fontSize: 12, color: "#999", marginTop: 2, lineHeight: 16 },
  rowValue: { fontSize: 15, fontWeight: "600", color: "#1a1a1a" },
  section: { marginBottom: 24 },
  sectionTitle: { fontSize: 18, fontWeight: "600", marginBottom: 4, color: "#333" },
  sectionSubtitle: { fontSize: 13, color: "#888", marginBottom: 12, lineHeight: 18 },
  skillRow: { flexDirection: "row", alignItems: "center", paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: "#f0f0f0" },
  skillName: { flex: 1, fontSize: 14, color: "#333", textTransform: "capitalize" },
  levelBadge: { backgroundColor: "#E8F0FE", paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8, marginRight: 8 },
  levelText: { fontSize: 13, fontWeight: "600", color: "#007AFF" },
  confidence: { fontSize: 12, color: "#999" },
  // Uncertain section
  uncertainSection: { backgroundColor: "#FFF8E1", borderRadius: 16, padding: 16, marginBottom: 24 },
  uncertainTitle: { color: "#E65100" },
  uncertainRow: { borderBottomColor: "#FFE0B2" },
  uncertainBadge: { backgroundColor: "#FFE0B2" },
  uncertainLevelText: { color: "#E65100" },
  // Not measured
  notMeasuredSection: { backgroundColor: "#F5F5F5", borderRadius: 16, padding: 16, marginBottom: 24 },
  notMeasuredTitle: { color: "#757575" },
  notMeasuredRow: { borderBottomColor: "#E0E0E0" },
  notMeasuredText: { color: "#999" },
  notMeasuredLabel: { fontSize: 12, color: "#bbb", fontStyle: "italic" },
  // Deferred
  deferredSection: { backgroundColor: "#ECEFF1", borderRadius: 16, padding: 16, marginBottom: 24 },
  deferredTitle: { color: "#546E7A" },
  deferredRow: { borderBottomColor: "#CFD8DC" },
  deferredText: { color: "#78909C" },
  deferredLabel: { fontSize: 12, color: "#90A4AE", fontStyle: "italic" },
  // Summary
  summaryBox: { backgroundColor: "#E8F5E9", borderRadius: 16, padding: 20, marginBottom: 24 },
  summaryBoxTitle: { fontSize: 16, fontWeight: "600", color: "#2E7D32", marginBottom: 12 },
  summaryBoxText: { fontSize: 14, color: "#33691E", lineHeight: 22, marginBottom: 4 },
  // Footer
  footer: { padding: 24, paddingBottom: 36, borderTopWidth: 1, borderTopColor: "#f0f0f0" },
});
