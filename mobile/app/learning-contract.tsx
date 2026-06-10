import React, { useState } from "react";
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

  const { data: contract, isLoading, error, refetch } = useQuery({
    queryKey: ["learning-contract"],
    queryFn: () => learningContract.getCurrent(),
    retry: false,
  });

  const handleCreate = async () => {
    setCreating(true);
    try {
      await learningContract.create();
      await refetch();
    } catch (err) {
      // Will show error state
    } finally {
      setCreating(false);
    }
  };

  if (isLoading) return <LoadingScreen message="Loading your learning plan..." />;

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <ErrorScreen
          message="No learning contract found yet. Complete your diagnostic first."
          onRetry={refetch}
        />
      </SafeAreaView>
    );
  }

  const contractData = contract as Record<string, any> | undefined;

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
        <Text style={styles.badge}>Your Learning Plan</Text>
        <Text style={styles.title}>Learning Entry Contract</Text>
        <Text style={styles.subtitle}>
          Based on your diagnostic results, we've created a personalized learning plan for you.
        </Text>

        {contractData && (
          <View style={styles.card}>
            {items.map((item, index) => (
              <View
                key={item.label}
                style={[styles.row, index < items.length - 1 && styles.borderRow]}
              >
                <Text style={styles.rowLabel}>{item.label}</Text>
                <Text style={styles.rowValue}>{item.value}</Text>
              </View>
            ))}
          </View>
        )}

        {contractData?.diagnostic_profile_snapshot && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Skill Profile</Text>
            {(contractData.diagnostic_profile_snapshot as any)?.assessments?.map(
              (a: any, i: number) => (
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
              ),
            )}
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
  rowLabel: { fontSize: 15, color: "#666" },
  rowValue: { fontSize: 15, fontWeight: "600", color: "#1a1a1a" },
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
  footer: {
    padding: 24,
    paddingBottom: 36,
    borderTopWidth: 1,
    borderTopColor: "#f0f0f0",
  },
});
