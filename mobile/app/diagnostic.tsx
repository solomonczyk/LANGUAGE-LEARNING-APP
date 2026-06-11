import React, { useCallback, useState, useEffect } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  Pressable,
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
import StepRenderer from "../src/components/diagnostics/StepRenderer";
import type { FeedbackData } from "../src/components/diagnostics/types";

const STEPS = [
  { key: "grammar_recognition",   type: "multiple_choice",   label: "Grammar",      prompt: "Which sentence is correct?" },
  { key: "active_vocabulary",     type: "matching",          label: "Vocabulary",   prompt: "Select the correct meaning for each word" },
  { key: "written_production",    type: "writing",           label: "Writing",       prompt: "Write 2-3 sentences about your morning routine" },
  { key: "narrative_coherence",   type: "ordering",          label: "Coherence",     prompt: "Tap each event in the correct order" },
  { key: "reading_comprehension", type: "passage",           label: "Reading",       prompt: "Read the passage and answer the questions." },
  { key: "listening_fallback",    type: "transcript",        label: "Listening",     prompt: "Read the conversation and answer the questions." },
  { key: "visual_comprehension",  type: "visual",            label: "Visual",        prompt: "Read the scene description and choose the best answer." },
  { key: "productive_grammar",    type: "sentence_rewrite",  label: "Grammar (Write)", prompt: "Rewrite each sentence correctly." },
  { key: "mediation",             type: "mediation",         label: "Explain",       prompt: "Read the message and explain it simply." },
  { key: "confidence_anxiety",   type: "self_assessment",   label: "Confidence",    prompt: "Rate your confidence in these language situations." },
];

// ── Grammar Recognition ──────────────────────────────────────────────
const GRAMMAR_OPTIONS = [
  { id: "a", text: "He go to school every day." },
  { id: "b", text: "He goes to school every day." },
  { id: "c", text: "He going to school every day." },
];
const GRAMMAR_CORRECT_ID = "b";

// ── Active Vocabulary ────────────────────────────────────────────────
interface VocabQuestion { word: string; options: { id: string; text: string }[]; correctId: string; }

const VOCABULARY_QUESTIONS: VocabQuestion[] = [
  { word: "Morning",  options: [{ id: "a", text: "the first meal of the day" }, { id: "b", text: "the start of the day" }, { id: "c", text: "a domestic animal" }, { id: "d", text: "to move on foot" }], correctId: "b" },
  { word: "Breakfast", options: [{ id: "a", text: "the first meal of the day" }, { id: "b", text: "the start of the day" }, { id: "c", text: "a period of rest" }, { id: "d", text: "the end of the day" }], correctId: "a" },
  { word: "Pet",      options: [{ id: "a", text: "a type of food" }, { id: "b", text: "a kind of vehicle" }, { id: "c", text: "a domestic animal" }, { id: "d", text: "a building" }], correctId: "c" },
  { word: "Walk",     options: [{ id: "a", text: "to move on foot" }, { id: "b", text: "to sit still" }, { id: "c", text: "to sleep" }, { id: "d", text: "to eat quickly" }], correctId: "a" },
];

// ── Narrative Coherence ──────────────────────────────────────────────
const NARRATIVE_EVENTS = [
  { id: "1", text: "Wake up" },
  { id: "2", text: "Get out of bed" },
  { id: "3", text: "Have breakfast" },
  { id: "4", text: "Brush teeth" },
  { id: "5", text: "Leave home" },
];
const CORRECT_NARRATIVE_ORDER = ["1", "2", "3", "4", "5"];
const SCRAMBLED_DISPLAY_ORDER = ["3", "5", "1", "4", "2"];

// ── Feedback helpers ─────────────────────────────────────────────────
function getGrammarFeedback(selectedId: string | null): FeedbackData {
  if (selectedId === GRAMMAR_CORRECT_ID) {
    return { correct: true, text: '"He goes to school every day." is correct!' };
  }
  return { correct: false, text: 'The correct sentence is "He goes to school every day."' };
}

function getVocabularyFeedback(correctCount: number, total: number): FeedbackData {
  return correctCount === total
    ? { correct: true, text: `Perfect! You matched all ${total} words correctly.` }
    : { correct: false, text: `You matched ${correctCount} of ${total} words.` };
}

function getNarrativeFeedback(correctOrder: boolean): FeedbackData {
  return correctOrder
    ? { correct: true, text: "Correct order!" }
    : { correct: false, text: "Correct order: Wake up → Get out of bed → Have breakfast → Brush teeth → Leave home" };
}

function isNewStep(key: string): boolean {
  return ["reading_comprehension", "listening_fallback", "visual_comprehension", "productive_grammar", "mediation", "confidence_anxiety"].includes(key);
}

export default function DiagnosticScreen() {
  const router = useRouter();
  const store = useDiagnosticStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [textInput, setTextInput] = useState("");

  // Interaction state per step (existing inline items)
  const [selectedGrammarOption, setSelectedGrammarOption] = useState<string | null>(null);
  const [vocabularyAnswers, setVocabularyAnswers] = useState<Record<number, string>>({});
  const [narrativeOrder, setNarrativeOrder] = useState<string[]>([]);

  // Response data from StepRenderer-based items
  const [stepResponse, setStepResponse] = useState<Record<string, unknown> | null>(null);

  // Submission / feedback state
  const [lastFeedback, setLastFeedback] = useState<FeedbackData | null>(null);

  useEffect(() => { initSession(); }, []);

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

  const handleSubmit = async () => {
    if (!store.sessionId || loading || lastFeedback !== null) return;
    setLoading(true);
    setError(null);
    try {
      const step = STEPS[store.currentStep];
      let responseData: Record<string, unknown>;
      let feedback: FeedbackData;

      if (isNewStep(step.key)) {
        // New StepRenderer-based items
        responseData = stepResponse || {};
        feedback = { correct: true, text: "Response recorded." };
      } else {
        switch (step.key) {
          case "grammar_recognition": {
            const selected = selectedGrammarOption;
            const isCorrect = selected === GRAMMAR_CORRECT_ID;
            responseData = { is_correct: isCorrect, selected_option: selected };
            feedback = getGrammarFeedback(selected);
            break;
          }
          case "active_vocabulary": {
            let correctCount = 0;
            const total = VOCABULARY_QUESTIONS.length;
            const selections: Record<string, string> = {};
            VOCABULARY_QUESTIONS.forEach((q, i) => {
              const ans = vocabularyAnswers[i] || "";
              selections[q.word] = ans;
              if (ans === q.correctId) correctCount++;
            });
            responseData = { correct_count: correctCount, total_words: total, selections };
            feedback = getVocabularyFeedback(correctCount, total);
            break;
          }
          case "written_production": {
            const wordCount = textInput.split(/\s+/).filter(Boolean).length;
            responseData = { word_count: wordCount, has_structure: textInput.length > 30, text: textInput };
            feedback = { correct: textInput.length >= 30, text: `${textInput.length} characters recorded.` };
            break;
          }
          case "narrative_coherence": {
            const isCorrectOrder = narrativeOrder.length === CORRECT_NARRATIVE_ORDER.length && narrativeOrder.every((id, i) => id === CORRECT_NARRATIVE_ORDER[i]);
            responseData = { correct_order: isCorrectOrder, user_order: [...narrativeOrder] };
            feedback = getNarrativeFeedback(isCorrectOrder);
            break;
          }
          default:
            responseData = {};
            feedback = { correct: false, text: "" };
        }
      }

      await diagnostics.submitResponse(store.sessionId, step.key, responseData);
      store.setResponse(step.key, responseData);
      setLastFeedback(feedback);
    } catch (err: any) {
      setError(err.message || "Failed to submit response");
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = () => {
    if (!lastFeedback) return;
    setLastFeedback(null);
    setStepResponse(null);

    if (store.currentStep < STEPS.length - 1) {
      setTextInput("");
      setSelectedGrammarOption(null);
      setVocabularyAnswers({});
      setNarrativeOrder([]);
      store.nextStep();
    } else {
      (async () => {
        setLoading(true);
        setError(null);
        try {
          await diagnostics.complete(store.sessionId);
          store.markComplete();
          router.replace("/learning-contract");
        } catch (err: any) {
          setError(err.message || "Failed to complete diagnostic");
        } finally {
          setLoading(false);
        }
      })();
    }
  };

  const currentStep = STEPS[store.currentStep];
  const showingFeedback = lastFeedback !== null;

  // ── Derived: can we submit? ──────────────────────────────────────
  const canSubmit = (() => {
    if (loading || showingFeedback) return false;
    if (isNewStep(currentStep.key)) return stepResponse !== null && Object.keys(stepResponse).length > 0;
    switch (currentStep.key) {
      case "grammar_recognition": return selectedGrammarOption !== null;
      case "active_vocabulary": return Object.keys(vocabularyAnswers).length >= VOCABULARY_QUESTIONS.length;
      case "written_production": return textInput.trim().length >= 10;
      case "narrative_coherence": return narrativeOrder.length === NARRATIVE_EVENTS.length;
      default: return false;
    }
  })();

  // ── Loading / error guards ────────────────────────────────────────
  if (loading && !store.sessionId) return <LoadingScreen message="Starting diagnostic..." />;
  if (error && !store.sessionId) return <ErrorScreen message={error} onRetry={initSession} />;

  // ── Render ────────────────────────────────────────────────────────
  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={styles.flex}>
        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
          <StepIndicator current={store.currentStep} total={STEPS.length} />
          <Text style={styles.stepLabel}>{currentStep.label}</Text>
          <Text style={styles.title}>{currentStep.prompt}</Text>

          {currentStep.key === "grammar_recognition" && (
            <View style={styles.options}>
              {GRAMMAR_OPTIONS.map((opt) => {
                const isSelected = selectedGrammarOption === opt.id;
                const isCorrectOption = opt.id === GRAMMAR_CORRECT_ID;
                let optStyle = [styles.optionItem];
                if (showingFeedback && isCorrectOption) optStyle.push(styles.optionCorrect);
                else if (showingFeedback && isSelected && !isCorrectOption) optStyle.push(styles.optionIncorrect);
                else if (isSelected) optStyle.push(styles.optionSelected);
                return (
                  <Pressable key={opt.id} style={optStyle} onPress={() => !showingFeedback && setSelectedGrammarOption(opt.id)} disabled={showingFeedback}>
                    <Text style={styles.optionText}>{isSelected ? "● " : "○ "}{opt.text}</Text>
                  </Pressable>
                );
              })}
              {showingFeedback && <Text style={[styles.feedback, lastFeedback.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}>{lastFeedback.text}</Text>}
            </View>
          )}

          {currentStep.key === "active_vocabulary" && (
            <View style={styles.options}>
              {VOCABULARY_QUESTIONS.map((q, qIdx) => {
                const selectedId = vocabularyAnswers[qIdx];
                return (
                  <View key={qIdx} style={styles.vocabBlock}>
                    <Text style={styles.vocabWord}>{q.word}</Text>
                    <View style={styles.vocabOptions}>
                      {q.options.map((opt) => {
                        const isSelected = selectedId === opt.id;
                        const isCorrectOpt = opt.id === q.correctId;
                        let optStyle = [styles.vocabOptItem];
                        if (showingFeedback && isCorrectOpt) optStyle.push(styles.vocabOptCorrect);
                        else if (showingFeedback && isSelected && !isCorrectOpt) optStyle.push(styles.vocabOptIncorrect);
                        else if (isSelected) optStyle.push(styles.vocabOptSelected);
                        return (
                          <Pressable key={opt.id} style={optStyle} onPress={() => { if (!showingFeedback) setVocabularyAnswers((prev) => ({ ...prev, [qIdx]: opt.id })); }} disabled={showingFeedback}>
                            <Text style={styles.vocabOptText}>{isSelected ? "● " : "○ "}{opt.text}</Text>
                          </Pressable>
                        );
                      })}
                    </View>
                  </View>
                );
              })}
              {showingFeedback && <Text style={[styles.feedback, lastFeedback.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}>{lastFeedback.text}</Text>}
            </View>
          )}

          {currentStep.key === "written_production" && (
            <View style={styles.options}>
              <TextInput style={styles.textArea} placeholder="Write 2-3 sentences about your morning..." value={textInput} onChangeText={setTextInput} multiline numberOfLines={5} textAlignVertical="top" editable={!showingFeedback} />
              <Text style={styles.hint}>Write at least 10 characters. Current: {textInput.length} chars</Text>
              {showingFeedback && <Text style={[styles.feedback, lastFeedback.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}>{lastFeedback.text}</Text>}
            </View>
          )}

          {currentStep.key === "narrative_coherence" && (
            <View style={styles.options}>
              {(() => {
                const availableEvents = NARRATIVE_EVENTS.filter((e) => !narrativeOrder.includes(e.id));
                const orderedEvents = narrativeOrder.map((id) => NARRATIVE_EVENTS.find((e) => e.id === id)).filter(Boolean);
                return (
                  <>
                    {availableEvents.length > 0 && (
                      <>
                        <Text style={styles.narrativeLabel}>Tap each event in the correct order:</Text>
                        {SCRAMBLED_DISPLAY_ORDER.filter((scrambledId) => availableEvents.some((e) => e.id === scrambledId)).map((scrambledId) => {
                          const ev = NARRATIVE_EVENTS.find((e) => e.id === scrambledId)!;
                          return (
                            <Pressable key={ev.id} style={styles.narrativeItem} onPress={() => { if (!showingFeedback) setNarrativeOrder((prev) => [...prev, ev.id]); }} disabled={showingFeedback}>
                              <Text style={styles.narrativeItemText}>+ {ev.text}</Text>
                            </Pressable>
                          );
                        })}
                      </>
                    )}
                    {orderedEvents.length > 0 && (
                      <>
                        <Text style={[styles.narrativeLabel, styles.narrativeYourOrderLabel]}>Your order (tap to undo):</Text>
                        {orderedEvents.map((ev, idx) => ev ? (
                          <Pressable key={ev.id} style={styles.narrativeOrderedItem} onPress={() => { if (!showingFeedback) setNarrativeOrder((prev) => prev.filter((id) => id !== ev.id)); }} disabled={showingFeedback}>
                            <Text style={styles.narrativeOrderNum}>{idx + 1}.</Text>
                            <Text style={styles.narrativeItemText}>{ev.text}</Text>
                          </Pressable>
                        ) : null)}
                      </>
                    )}
                    <Text style={styles.hint}>{narrativeOrder.length} of {NARRATIVE_EVENTS.length} placed</Text>
                    {showingFeedback && <Text style={[styles.feedback, lastFeedback.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}>{lastFeedback.text}</Text>}
                  </>
                );
              })()}
            </View>
          )}

          {isNewStep(currentStep.key) && (
            <View style={styles.options}>
              <StepRenderer
                stepKey={currentStep.key}
                responseData={stepResponse}
                disabled={showingFeedback}
                onResponseChange={setStepResponse}
                feedback={showingFeedback ? lastFeedback : null}
              />
              {showingFeedback && (
                <Text style={[styles.feedback, lastFeedback.correct ? styles.feedbackCorrect : styles.feedbackIncorrect]}>
                  {lastFeedback.text}
                </Text>
              )}
            </View>
          )}

          {error && <Text style={styles.error}>{error}</Text>}
        </ScrollView>

        <View style={styles.footer}>
          <Button
            title={showingFeedback ? "Continue →" : store.currentStep < STEPS.length - 1 ? "Submit" : "Complete Diagnostic"}
            onPress={showingFeedback ? handleContinue : handleSubmit}
            disabled={showingFeedback ? false : !canSubmit}
            loading={loading}
          />
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

// ── Styles ───────────────────────────────────────────────────────────
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fff" },
  flex: { flex: 1 },
  scroll: { padding: 24, paddingBottom: 100 },
  stepLabel: { fontSize: 14, color: "#007AFF", fontWeight: "500", marginBottom: 8, textAlign: "center" },
  title: { fontSize: 22, fontWeight: "700", marginBottom: 24, color: "#1a1a1a", textAlign: "center" },
  options: { gap: 12 },
  optionItem: { padding: 16, borderRadius: 12, backgroundColor: "#f8f9fa", borderWidth: 1.5, borderColor: "#e9ecef" },
  optionSelected: { padding: 16, borderRadius: 12, backgroundColor: "#E8F0FE", borderWidth: 1.5, borderColor: "#007AFF" },
  optionCorrect: { padding: 16, borderRadius: 12, backgroundColor: "#E8F5E9", borderWidth: 1.5, borderColor: "#34C759" },
  optionIncorrect: { padding: 16, borderRadius: 12, backgroundColor: "#FFEBEE", borderWidth: 1.5, borderColor: "#FF3B30" },
  optionText: { fontSize: 16, color: "#333" },
  vocabBlock: { marginBottom: 8, padding: 12, borderRadius: 12, backgroundColor: "#f8f9fa", borderWidth: 1, borderColor: "#e9ecef" },
  vocabWord: { fontSize: 17, fontWeight: "700", color: "#1a1a1a", marginBottom: 8 },
  vocabOptions: { gap: 6 },
  vocabOptItem: { padding: 10, borderRadius: 8, backgroundColor: "#fff", borderWidth: 1, borderColor: "#e9ecef" },
  vocabOptSelected: { padding: 10, borderRadius: 8, backgroundColor: "#E8F0FE", borderWidth: 1, borderColor: "#007AFF" },
  vocabOptCorrect: { padding: 10, borderRadius: 8, backgroundColor: "#E8F5E9", borderWidth: 1, borderColor: "#34C759" },
  vocabOptIncorrect: { padding: 10, borderRadius: 8, backgroundColor: "#FFEBEE", borderWidth: 1, borderColor: "#FF3B30" },
  vocabOptText: { fontSize: 14, color: "#444" },
  textArea: { borderWidth: 1, borderColor: "#ddd", borderRadius: 12, padding: 14, fontSize: 16, minHeight: 120, backgroundColor: "#fafafa" },
  narrativeLabel: { fontSize: 14, fontWeight: "600", color: "#555", marginBottom: 4 },
  narrativeYourOrderLabel: { marginTop: 16, color: "#007AFF" },
  narrativeItem: { padding: 14, borderRadius: 10, backgroundColor: "#f0f4ff", borderWidth: 1, borderColor: "#d0d8f0", borderStyle: "dashed" },
  narrativeOrderedItem: { padding: 14, borderRadius: 10, backgroundColor: "#E8F0FE", borderWidth: 1, borderColor: "#007AFF", flexDirection: "row", alignItems: "center" },
  narrativeOrderNum: { fontSize: 15, fontWeight: "700", color: "#007AFF", marginRight: 8, width: 24 },
  narrativeItemText: { fontSize: 15, color: "#333" },
  feedback: { fontSize: 15, fontWeight: "600", marginTop: 8, padding: 12, borderRadius: 8, textAlign: "center", lineHeight: 22 },
  feedbackCorrect: { color: "#1B5E20", backgroundColor: "#E8F5E9" },
  feedbackIncorrect: { color: "#B71C1C", backgroundColor: "#FFEBEE" },
  hint: { fontSize: 14, color: "#666", marginTop: 8, fontStyle: "italic", lineHeight: 20 },
  error: { color: "#dc3545", fontSize: 14, textAlign: "center", marginTop: 8 },
  footer: { padding: 24, paddingBottom: Platform.OS === "ios" ? 36 : 24, borderTopWidth: 1, borderTopColor: "#f0f0f0" },
});
