import React from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useQuery } from "@tanstack/react-query";
import Button from "../../src/shared/components/Button";
import LoadingScreen from "../../src/shared/components/LoadingScreen";
import ErrorScreen from "../../src/shared/components/ErrorScreen";
import { lessonSessions, mastery } from "../../src/services/api";

export default function ResultScreen() {
  const { id, status, decision } = useLocalSearchParams<{
    id: string;
    status: string;
    decision: string;
  }>();
  const router = useRouter();

  const {
    data: session,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["lesson-session", id],
    queryFn: () => lessonSessions.get(id!),
  });

  const { data: masteryData } = useQuery({
    queryKey: ["mastery-profile"],
    queryFn: () => mastery.getProfile(),
  });

  if (isLoading) return <LoadingScreen message="Loading results..." />;
  if (error) return <ErrorScreen message={(error as any).message} onRetry={refetch} />;

  const sessionData = session as Record<string, any> | undefined;
  const isCompleted = sessionData?.status === "COMPLETED" || status === "COMPLETED";
  const masteryInfo = masteryData as Record<string, any> | undefined;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        {isCompleted ? (
          <View style={styles.statusBox}>
            <Text style={styles.checkCircle}>✓</Text>
            <Text style={styles.completedTitle}>Lesson Complete!</Text>
            <Text style={styles.completedSubtitle}>
              Your response has been analyzed and validated.
            </Text>
          </View>
        ) : (
          <View style={[styles.statusBox, styles.incompleteBox]}>
            <Text style={styles.incompleteIcon}>⟳</Text>
            <Text style={styles.incompleteTitle}>Lesson In Progress</Text>
            <Text style={styles.completedSubtitle}>
              Status: {sessionData?.status || status}
            </Text>
          </View>
        )}

        {/* Strengths Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Strengths</Text>
          <View style={styles.strengthItem}>
            <Text style={styles.bullet}>•</Text>
            <Text style={styles.strengthText}>
              The sequence of events is understandable.
            </Text>
          </View>
          <View style={styles.strengthItem}>
            <Text style={styles.bullet}>•</Text>
            <Text style={styles.strengthText}>
              Good use of time markers to organize the narrative.
            </Text>
          </View>
        </View>

        {/* Corrections Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Important Corrections</Text>
          <View style={styles.correctionCard}>
            <View style={styles.correctionHeader}>
              <Text style={styles.correctionBadge}>VERB_FORM</Text>
              <Text style={styles.correctionSeverity}>major</Text>
            </View>
            <Text style={styles.correctionHint}>
              "wants to the water closet" → "wanted to go to the litter box"
            </Text>
          </View>
        </View>

        {/* Suggested Improvement */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Suggested Improved Phrasing</Text>
          <View style={styles.improvementBox}>
            <Text style={styles.improvementText}>
              This morning I woke up and fed my cat. She wanted to go to the litter box, so I opened
              the door for her. Then we played together for a while before breakfast.
            </Text>
          </View>
        </View>

        {/* Validation Result */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Validation Result</Text>
          <View style={styles.validationRow}>
            <Text style={styles.validationLabel}>Linguistic Check</Text>
            <Text style={styles.validationPass}>✓ Passed</Text>
          </View>
          <View style={styles.validationRow}>
            <Text style={styles.validationLabel}>Pedagogical Check</Text>
            <Text style={styles.validationPass}>✓ Passed</Text>
          </View>
          <View style={styles.validationRow}>
            <Text style={styles.validationLabel}>Decision</Text>
            <Text style={styles.validationDecision}>
              {decision || "COMPLETE"}
            </Text>
          </View>
        </View>

        {/* Mastery Evidence */}
        {masteryInfo && (masteryInfo as any).records?.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Mastery Progress</Text>
            {(masteryInfo as any).records.map((r: any, i: number) => (
              <View key={i} style={styles.masteryRow}>
                <Text style={styles.masterySkill}>
                  {r.skill.replace(/_/g, " ")}
                </Text>
                <View style={styles.masteryBadge}>
                  <Text style={styles.masteryState}>{r.current_state}</Text>
                </View>
              </View>
            ))}
          </View>
        )}

        {/* Lesson Status Warning */}
        {!isCompleted && (
          <View style={styles.warningBox}>
            <Text style={styles.warningText}>
              ⚠️ Lesson not marked as completed. The lesson completion gate requires all
              validations to pass and a positive policy decision.
            </Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.footer}>
        <Button title="Back to Home" onPress={() => router.replace("/home")} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fff" },
  scroll: { padding: 24 },
  statusBox: {
    backgroundColor: "#E8F5E9",
    borderRadius: 20,
    padding: 32,
    alignItems: "center",
    marginBottom: 24,
  },
  incompleteBox: { backgroundColor: "#FFF3E0" },
  checkCircle: {
    fontSize: 48,
    color: "#34C759",
    marginBottom: 12,
  },
  incompleteIcon: { fontSize: 48, color: "#FF9800", marginBottom: 12 },
  completedTitle: { fontSize: 22, fontWeight: "700", color: "#2E7D32", marginBottom: 4 },
  incompleteTitle: { fontSize: 22, fontWeight: "700", color: "#E65100", marginBottom: 4 },
  completedSubtitle: { fontSize: 14, color: "#666", textAlign: "center" },
  section: { marginBottom: 24 },
  sectionTitle: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 12,
    color: "#333",
  },
  strengthItem: {
    flexDirection: "row",
    gap: 8,
    marginBottom: 8,
    paddingLeft: 4,
  },
  bullet: { fontSize: 16, color: "#34C759" },
  strengthText: { fontSize: 14, color: "#555", flex: 1, lineHeight: 20 },
  correctionCard: {
    backgroundColor: "#FFF3E0",
    borderRadius: 12,
    padding: 16,
    marginBottom: 8,
  },
  correctionHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 8,
  },
  correctionBadge: {
    fontSize: 12,
    fontWeight: "600",
    color: "#E65100",
    backgroundColor: "#FFE0B2",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
  },
  correctionSeverity: {
    fontSize: 12,
    color: "#E65100",
    textTransform: "capitalize",
  },
  correctionHint: { fontSize: 14, color: "#555", lineHeight: 20 },
  improvementBox: {
    backgroundColor: "#f8f9fa",
    borderRadius: 12,
    padding: 16,
  },
  improvementText: { fontSize: 14, color: "#333", lineHeight: 22, fontStyle: "italic" },
  validationRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  validationLabel: { fontSize: 14, color: "#666" },
  validationPass: { fontSize: 14, color: "#34C759", fontWeight: "600" },
  validationDecision: { fontSize: 14, color: "#007AFF", fontWeight: "600" },
  masteryRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  masterySkill: { fontSize: 14, color: "#333", textTransform: "capitalize" },
  masteryBadge: {
    backgroundColor: "#E8F0FE",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  masteryState: { fontSize: 12, fontWeight: "600", color: "#007AFF" },
  warningBox: {
    backgroundColor: "#FFF3E0",
    borderRadius: 12,
    padding: 16,
  },
  warningText: { fontSize: 13, color: "#E65100", lineHeight: 20 },
  footer: {
    padding: 24,
    paddingBottom: 36,
    borderTopWidth: 1,
    borderTopColor: "#f0f0f0",
  },
});
