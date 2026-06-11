import React, { useState } from "react";
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
import { useOnboardingStore } from "../src/state/appState";
import { identity, learnerProfile, setUserId } from "../src/services/api";

const LANGUAGES = ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Korean", "Chinese"];
const LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"];

export default function OnboardingScreen() {
  const router = useRouter();
  const store = useOnboardingStore();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const totalSteps = 4;

  const handleNext = () => {
    if (step < totalSteps - 1) {
      setStep(step + 1);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      // Register/login the local learner
      const user = await identity.login("local_learner");
      setUserId(user.id);

      // Create learner profile
      await learnerProfile.create({
        target_language: store.targetLanguage,
        native_language: store.nativeLanguage,
        learning_goal: store.learningGoal,
        preferred_lesson_duration: store.preferredDuration,
        self_reported_level: store.selfReportedLevel,
      });

      store.markComplete();
      router.replace("/diagnostic");
    } catch (err: any) {
      if (err.code === "NOT_FOUND") {
        // User doesn't exist, register first
        try {
          const user = await identity.register("local_learner", "Local Learner");
          setUserId(user.id);

          await learnerProfile.create({
            target_language: store.targetLanguage,
            native_language: store.nativeLanguage,
            learning_goal: store.learningGoal,
            preferred_lesson_duration: store.preferredDuration,
            self_reported_level: store.selfReportedLevel,
          });

          store.markComplete();
          router.replace("/diagnostic");
        } catch (regErr: any) {
          setError(regErr.message || "Registration failed");
        }
      } else {
        setError(err.message || "Something went wrong");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.flex}
      >
        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
          <Text style={styles.step}>Step {step + 1} of {totalSteps}</Text>
          <Text style={styles.title}>{getStepTitle(step)}</Text>
          <Text style={styles.subtitle}>{getStepSubtitle(step)}</Text>

          {step === 0 && (
            <View style={styles.field}>
              <Text style={styles.label}>Target Language</Text>
              <View style={styles.optionsGrid}>
                {LANGUAGES.slice(0, 6).map((lang) => (
                  <TouchableChip
                    key={lang}
                    label={lang}
                    selected={store.targetLanguage === lang}
                    onPress={() => store.setField("targetLanguage", lang)}
                  />
                ))}
              </View>
              {!store.targetLanguage && (
                <TextInput
                  style={styles.input}
                  placeholder="Or type another language..."
                  value={
                    LANGUAGES.slice(0, 6).includes(store.targetLanguage)
                      ? ""
                      : store.targetLanguage
                  }
                  onChangeText={(t) => store.setField("targetLanguage", t)}
                />
              )}
            </View>
          )}

          {step === 1 && (
            <View style={styles.field}>
              <Text style={styles.label}>Native Language</Text>
              <View style={styles.optionsGrid}>
                {LANGUAGES.map((lang) => (
                  <TouchableChip
                    key={lang}
                    label={lang}
                    selected={store.nativeLanguage === lang}
                    onPress={() => store.setField("nativeLanguage", lang)}
                  />
                ))}
              </View>
              <TextInput
                style={styles.input}
                placeholder="Or type your language..."
                value={
                  LANGUAGES.includes(store.nativeLanguage) ? "" : store.nativeLanguage
                }
                onChangeText={(t) => store.setField("nativeLanguage", t)}
              />
            </View>
          )}

          {step === 2 && (
            <View style={styles.field}>
              <Text style={styles.label}>What's your learning goal?</Text>
              {["Basic conversation", "Travel", "Work", "Study", "Cultural interest"].map(
                (goal) => (
                  <TouchableChip
                    key={goal}
                    label={goal}
                    selected={store.learningGoal === goal}
                    onPress={() => store.setField("learningGoal", goal)}
                    wide
                  />
                ),
              )}
              <TextInput
                style={[styles.input, { marginTop: 12 }]}
                placeholder="Or describe your goal..."
                value={
                  ["Basic conversation", "Travel", "Work", "Study", "Cultural interest"].includes(
                    store.learningGoal,
                  )
                    ? ""
                    : store.learningGoal
                }
                onChangeText={(t) => store.setField("learningGoal", t)}
              />
              <Text style={styles.label}>Preferred lesson duration (minutes)</Text>
              <View style={styles.optionsGrid}>
                {[5, 10, 15, 20, 30].map((d) => (
                  <TouchableChip
                    key={d}
                    label={`${d} min`}
                    selected={store.preferredDuration === d}
                    onPress={() => store.setField("preferredDuration", d)}
                  />
                ))}
              </View>
            </View>
          )}

          {step === 3 && (
            <View style={styles.field}>
              <Text style={styles.label}>Your current level</Text>
              <Text style={styles.hint}>
                Be honest — this helps us start at the right place.
              </Text>
              <View style={styles.optionsGrid}>
                {LEVELS.map((level) => (
                  <View key={level} style={styles.levelItem}>
                    <TouchableChip
                      label={level}
                      selected={store.selfReportedLevel === level}
                      onPress={() => store.setField("selfReportedLevel", level)}
                    />
                    <Text style={styles.levelDesc}>{getLevelDescription(level)}</Text>
                  </View>
                ))}
              </View>
            </View>
          )}

          {error && <Text style={styles.error}>{error}</Text>}
        </ScrollView>

        <View style={styles.footer}>
          <Button
            title={step < totalSteps - 1 ? "Continue" : "Start Learning!"}
            onPress={handleNext}
            disabled={!canProceed(step, store)}
            loading={loading}
          />
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

function TouchableChip({
  label,
  selected,
  onPress,
  wide,
}: {
  label: string;
  selected: boolean;
  onPress: () => void;
  wide?: boolean;
}) {
  return (
    <View style={wide ? styles.chipWide : undefined}>
      <Text
        style={[styles.chip, selected && styles.chipSelected]}
        onPress={onPress}
      >
        {label}
      </Text>
    </View>
  );
}

function getStepTitle(step: number): string {
  switch (step) {
    case 0:
      return "What language do you want to learn?";
    case 1:
      return "What's your native language?";
    case 2:
      return "Set your learning preferences";
    case 3:
      return "What's your current level?";
    default:
      return "";
  }
}

function getStepSubtitle(step: number): string {
  switch (step) {
    case 0:
      return "Choose the language you'd like to start learning.";
    case 1:
      return "We'll use this for explanations and support.";
    case 2:
      return "Tell us about your goals and preferred pace.";
    case 3:
      return "This helps us find the right starting level for you.";
    default:
      return "";
  }
}

function getLevelDescription(level: string): string {
  switch (level) {
    case "A1":
      return "Starting Out";
    case "A2":
      return "Building Confidence";
    case "B1":
      return "Getting Comfortable";
    case "B2":
      return "Growing Independent";
    case "C1":
      return "Advanced";
    case "C2":
      return "Mastery";
    default:
      return "";
  }
}

function canProceed(step: number, store: { targetLanguage: string; nativeLanguage: string; learningGoal: string; selfReportedLevel: string }): boolean {
  switch (step) {
    case 0:
      return !!store.targetLanguage;
    case 1:
      return !!store.nativeLanguage;
    case 2:
      return !!store.learningGoal;
    case 3:
      return !!store.selfReportedLevel;
    default:
      return false;
  }
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fff" },
  flex: { flex: 1 },
  scroll: { padding: 24, paddingBottom: 100 },
  step: { fontSize: 14, color: "#007AFF", marginBottom: 8, fontWeight: "500" },
  title: { fontSize: 24, fontWeight: "700", marginBottom: 8, color: "#1a1a1a" },
  subtitle: { fontSize: 15, color: "#666", marginBottom: 32, lineHeight: 22 },
  field: { marginBottom: 24 },
  label: { fontSize: 16, fontWeight: "600", marginBottom: 12, color: "#333", marginTop: 8 },
  hint: { fontSize: 13, color: "#999", marginBottom: 16 },
  optionsGrid: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  chip: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 24,
    backgroundColor: "#f5f5f5",
    color: "#333",
    fontSize: 14,
    fontWeight: "500",
    overflow: "hidden",
    borderWidth: 2,
    borderColor: "transparent",
  },
  chipSelected: {
    backgroundColor: "#E8F0FE",
    color: "#007AFF",
    borderColor: "#007AFF",
  },
  chipWide: { width: "100%", marginBottom: 4 },
  levelItem: { width: "30%", alignItems: "center", marginBottom: 16 },
  levelDesc: { fontSize: 11, color: "#999", marginTop: 4 },
  input: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 12,
    padding: 14,
    fontSize: 16,
    marginTop: 8,
    backgroundColor: "#fafafa",
  },
  error: { color: "#dc3545", fontSize: 14, textAlign: "center", marginTop: 8 },
  footer: {
    padding: 24,
    paddingBottom: Platform.OS === "ios" ? 36 : 24,
    borderTopWidth: 1,
    borderTopColor: "#f0f0f0",
  },
});
