import React from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { useQuery } from "@tanstack/react-query";
import Button from "../src/shared/components/Button";
import LoadingScreen from "../src/shared/components/LoadingScreen";
import { learningContract, mastery } from "../src/services/api";

export default function HomeScreen() {
  const router = useRouter();
  const lessonDefinitionId = "00000000-0000-0000-0000-000000000010";

  const { data: contract, isLoading: contractLoading } = useQuery({
    queryKey: ["learning-contract"],
    queryFn: () => learningContract.getCurrent(),
  });

  const { data: masteryData, isLoading: masteryLoading } = useQuery({
    queryKey: ["mastery-profile"],
    queryFn: () => mastery.getProfile(),
  });

  const isLoading = contractLoading || masteryLoading;

  const handleStartLesson = async () => {
    router.push(`/lesson/${lessonDefinitionId}`);
  };

  if (isLoading) return <LoadingScreen message="Preparing your dashboard..." />;

  const contractData = contract as Record<string, any> | undefined;
  const masteryInfo = masteryData as Record<string, any> | undefined;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.greeting}>Welcome back!</Text>
        <Text style={styles.title}>Your Learning Dashboard</Text>

        {contractData && (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Current Lesson Plan</Text>
            <View style={styles.cardRow}>
              <Text style={styles.cardLabel}>Language</Text>
              <Text style={styles.cardValue}>{contractData.target_language}</Text>
            </View>
            <View style={styles.cardRow}>
              <Text style={styles.cardLabel}>Duration</Text>
              <Text style={styles.cardValue}>{contractData.lesson_duration_minutes} min</Text>
            </View>
            <View style={styles.cardRow}>
              <Text style={styles.cardLabel}>Scaffolding</Text>
              <Text style={styles.cardValue}>{contractData.scaffolding_mode}</Text>
            </View>
          </View>
        )}

        {masteryInfo && (masteryInfo as any).records?.length > 0 && (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Mastery Progress</Text>
            {(masteryInfo as any).records.map((r: any, i: number) => (
              <View key={i} style={styles.cardRow}>
                <Text style={styles.cardLabel}>{r.skill.replace(/_/g, " ")}</Text>
                <Text style={styles.cardValue}>{r.current_state}</Text>
              </View>
            ))}
          </View>
        )}

        <View style={styles.lessonCard}>
          <Text style={styles.lessonTitle}>My Morning with My Pet</Text>
          <Text style={styles.lessonDesc}>
            Write about your morning routine and what you did with your pet.
          </Text>
          <Text style={styles.lessonMeta}>Personal Narrative • ~15 min</Text>
          <Button title="Start Lesson" onPress={handleStartLesson} style={styles.startButton} />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f8f9fa" },
  scroll: { padding: 24 },
  greeting: { fontSize: 14, color: "#007AFF", fontWeight: "500", marginBottom: 4 },
  title: { fontSize: 26, fontWeight: "700", marginBottom: 24, color: "#1a1a1a" },
  card: {
    backgroundColor: "#fff",
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  cardTitle: { fontSize: 16, fontWeight: "600", marginBottom: 12, color: "#333" },
  cardRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  cardLabel: { fontSize: 14, color: "#666", textTransform: "capitalize" },
  cardValue: { fontSize: 14, fontWeight: "600", color: "#333" },
  lessonCard: {
    backgroundColor: "#fff",
    borderRadius: 16,
    padding: 24,
    marginBottom: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  lessonTitle: { fontSize: 20, fontWeight: "700", marginBottom: 8, color: "#1a1a1a" },
  lessonDesc: { fontSize: 14, color: "#666", marginBottom: 8, lineHeight: 20 },
  lessonMeta: { fontSize: 12, color: "#999", marginBottom: 16 },
  startButton: { marginTop: 8 },
});
