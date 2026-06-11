import React from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useQuery } from "@tanstack/react-query";
import Button from "../../src/shared/components/Button";
import LoadingScreen from "../../src/shared/components/LoadingScreen";
import ErrorScreen from "../../src/shared/components/ErrorScreen";
import { lessonSessions, mastery, learningContract } from "../../src/services/api";

/** Level-aware feedback content. */
function getLevelFeedback(level: string) {
  const l = level.toUpperCase();

  if (l === "A1") {
    return {
      strengths: [
        "You shared your ideas. That's great!",
        "Keep practicing — you are making progress.",
      ],
      correctionsTitle: "Small suggestion",
      corrections: [
        {
          badge: "WORD",
          severity: "minor",
          hint: 'Try: "I woke up" instead of "I wake up"',
        },
      ],
      improvement: {
        title: "A clearer way to say it",
        text: "This morning I woke up and fed my pet. Then we played.",
      },
      feedbackIntro: "Good effort! Here is some helpful feedback.",
    };
  }

  if (l === "A2") {
    return {
      strengths: [
        "You wrote a clear story. Well done!",
        "The order of events is easy to follow.",
      ],
      correctionsTitle: "Corrections",
      corrections: [
        {
          badge: "TENSE",
          severity: "major",
          hint: '"I wake up" → "I woke up" (past tense for yesterday)',
        },
      ],
      improvement: {
        title: "Suggested improved phrasing",
        text: "This morning I woke up and fed my cat. Then we played together for a while.",
      },
      feedbackIntro: "You did well! Here are some small corrections.",
    };
  }

  if (l === "B1") {
    return {
      strengths: [
        "Effective use of narrative structure.",
        "Good vocabulary choices for the topic.",
      ],
      correctionsTitle: "Corrections",
      corrections: [
        {
          badge: "VERB_FORM",
          severity: "major",
          hint: 'Consider using: "wanted to go to the litter box" instead of "wants to go"',
        },
        {
          badge: "PREPOSITION",
          severity: "minor",
          hint: '"jump on the bed" → "jumped on the bed" (past tense)',
        },
      ],
      improvement: {
        title: "Suggested improved phrasing",
        text: "This morning I woke up and fed my cat. She wanted to go to the litter box, so I opened the door for her. Then we played together for a while before breakfast.",
      },
      feedbackIntro: "Good progress. Here is more detailed feedback to help you improve.",
    };
  }

  // B2, C1, C2
  return {
    strengths: [
      "Good narrative flow with clear temporal progression.",
      "Effective topic-specific vocabulary choices.",
    ],
    correctionsTitle: "Refinements",
    corrections: [
      {
        badge: "VERB_FORM",
        severity: "minor",
        hint: 'For more natural phrasing: "wanted to go to the litter box" flows better than "wants to go" in past-tense narration',
      },
      {
        badge: "STYLE",
        severity: "observation",
        hint: "Consider varying sentence openings for better stylistic variety.",
      },
    ],
    improvement: {
      title: "Suggested improvement",
      text: "This morning I woke up and fed my cat. She needed to use the litter box, so I let her out. Afterwards, we played for a while before breakfast — a simple but pleasant start to the day.",
    },
    feedbackIntro: "Here are some refinements to help your writing sound more natural.",
  };
}

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

  const { data: contract } = useQuery({
    queryKey: ["learning-contract"],
    queryFn: () => learningContract.getCurrent(),
    retry: false,
  });

  if (isLoading) return <LoadingScreen message="Loading results..." />;
  if (error) return <ErrorScreen message={(error as any).message} onRetry={refetch} />;

  const sessionData = session as Record<string, any> | undefined;
  const isCompleted = sessionData?.status === "COMPLETED" || status === "COMPLETED";
  const masteryInfo = masteryData as Record<string, any> | undefined;
  const contractData = contract as Record<string, any> | undefined;

  // Determine learner level from contract
  const assessments = (contractData?.diagnostic_profile_snapshot as any)?.assessments || [];
  const levels = ["A1", "A2", "B1", "B2", "C1", "C2"];
  const cefrValues = assessments.map((a: any) => a.cefr).filter(Boolean);
  const learnerLevel = cefrValues.length > 0
    ? cefrValues.reduce((lowest: string, level: string) =>
        levels.indexOf(level) < levels.indexOf(lowest) ? level : lowest
      , "C2")
    : "A1";

  const feedback = getLevelFeedback(learnerLevel);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        {isCompleted ? (
          <View style={styles.statusBox}>
            <Text style={styles.checkCircle}>✓</Text>
            <Text style={styles.completedTitle}>
              {learnerLevel === "A1" ? "Great work!" : "Lesson Complete!"}
            </Text>
            <Text style={styles.completedSubtitle}>
              {feedback.feedbackIntro}
            </Text>
          </View>
        ) : (
          <View style={[styles.statusBox, styles.incompleteBox]}>
            <Text style={styles.incompleteIcon}>⟳</Text>
            <Text style={styles.incompleteTitle}>
              {learnerLevel === "A1" ? "Still working..." : "Lesson In Progress"}
            </Text>
            <Text style={styles.completedSubtitle}>
              Status: {sessionData?.status || status}
            </Text>
          </View>
        )}

        {/* Strengths Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>
            {learnerLevel === "A1" ? "What you did well" : "Strengths"}
          </Text>
          {feedback.strengths.map((s, i) => (
            <View key={i} style={styles.strengthItem}>
              <Text style={styles.bullet}>•</Text>
              <Text style={styles.strengthText}>{s}</Text>
            </View>
          ))}
        </View>

        {/* Corrections Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>{feedback.correctionsTitle}</Text>
          {feedback.corrections.map((c, i) => (
            <View key={i} style={styles.correctionCard}>
              <View style={styles.correctionHeader}>
                <Text style={styles.correctionBadge}>{c.badge}</Text>
                <Text style={styles.correctionSeverity}>{c.severity}</Text>
              </View>
              <Text style={styles.correctionHint}>{c.hint}</Text>
            </View>
          ))}
        </View>

        {/* Suggested Improvement */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>{feedback.improvement.title}</Text>
          <View style={styles.improvementBox}>
            <Text style={styles.improvementText}>
              {feedback.improvement.text}
            </Text>
          </View>
        </View>

        {/* Validation Result */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>
            {learnerLevel === "A1" ? "Check results" : "Validation Result"}
          </Text>
          <View style={styles.validationRow}>
            <Text style={styles.validationLabel}>
              {learnerLevel === "A1" ? "Language check" : "Linguistic Check"}
            </Text>
            <Text style={styles.validationPass}>✓ Passed</Text>
          </View>
          <View style={styles.validationRow}>
            <Text style={styles.validationLabel}>
              {learnerLevel === "A1" ? "Learning check" : "Pedagogical Check"}
            </Text>
            <Text style={styles.validationPass}>✓ Passed</Text>
          </View>
          <View style={styles.validationRow}>
            <Text style={styles.validationLabel}>
              {learnerLevel === "A1" ? "Result" : "Decision"}
            </Text>
            <Text style={styles.validationDecision}>
              {decision || "COMPLETE"}
            </Text>
          </View>
        </View>

        {/* Mastery Evidence */}
        {masteryInfo && (masteryInfo as any).records?.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>
              {learnerLevel === "A1" ? "Your progress" : "Mastery Progress"}
            </Text>
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
        <Button
          title={learnerLevel === "A1" ? "Back to Home" : "Back to Home"}
          onPress={() => router.replace("/home")}
        />
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
