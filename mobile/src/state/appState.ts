/**
 * Zustand stores for temporary local UI/session state.
 * Server state is managed by TanStack Query.
 */

import { create } from "zustand";

// === Onboarding Draft Store ===
interface OnboardingState {
  targetLanguage: string;
  nativeLanguage: string;
  learningGoal: string;
  preferredDuration: number;
  selfReportedLevel: string;
  isComplete: boolean;
  setField: (field: string, value: string | number) => void;
  reset: () => void;
  markComplete: () => void;
}

export const useOnboardingStore = create<OnboardingState>((set) => ({
  targetLanguage: "",
  nativeLanguage: "",
  learningGoal: "",
  preferredDuration: 10,
  selfReportedLevel: "A1",
  isComplete: false,

  setField: (field, value) => set((state) => ({ ...state, [field]: value })),
  reset: () =>
    set({
      targetLanguage: "",
      nativeLanguage: "",
      learningGoal: "",
      preferredDuration: 10,
      selfReportedLevel: "A1",
      isComplete: false,
    }),
  markComplete: () => set({ isComplete: true }),
}));

// === Diagnostic Draft Store ===
interface DiagnosticState {
  currentStep: number;
  sessionId: string | null;
  responses: Record<string, Record<string, unknown>>;
  isComplete: boolean;
  setSessionId: (id: string) => void;
  setResponse: (key: string, data: Record<string, unknown>) => void;
  nextStep: () => void;
  reset: () => void;
  markComplete: () => void;
}

export const useDiagnosticStore = create<DiagnosticState>((set) => ({
  currentStep: 0,
  sessionId: null,
  responses: {},
  isComplete: false,

  setSessionId: (id) => set({ sessionId: id }),
  setResponse: (key, data) =>
    set((state) => ({
      responses: { ...state.responses, [key]: data },
    })),
  nextStep: () => set((state) => ({ currentStep: state.currentStep + 1 })),
  reset: () =>
    set({
      currentStep: 0,
      sessionId: null,
      responses: {},
      isComplete: false,
    }),
  markComplete: () => set({ isComplete: true }),
}));

// === Lesson Text Draft Store ===
interface LessonDraftState {
  currentText: string;
  sessionId: string | null;
  isSubmitting: boolean;
  submitError: string | null;
  setText: (text: string) => void;
  setSessionId: (id: string) => void;
  setSubmitting: (v: boolean) => void;
  setError: (err: string | null) => void;
  reset: () => void;
}

export const useLessonDraftStore = create<LessonDraftState>((set) => ({
  currentText: "",
  sessionId: null,
  isSubmitting: false,
  submitError: null,
  setText: (text) => set({ currentText: text }),
  setSessionId: (id) => set({ sessionId: id }),
  setSubmitting: (v) => set({ isSubmitting: v }),
  setError: (err) => set({ submitError: err }),
  reset: () =>
    set({
      currentText: "",
      sessionId: null,
      isSubmitting: false,
      submitError: null,
    }),
}));

// === Route Intent Store (for recovery) ===
interface RouteIntentState {
  currentRoute: string;
  routeParams: Record<string, string>;
  setRoute: (route: string, params?: Record<string, string>) => void;
  clear: () => void;
}

export const useRouteIntentStore = create<RouteIntentState>((set) => ({
  currentRoute: "/onboarding",
  routeParams: {},
  setRoute: (route, params) => set({ currentRoute: route, routeParams: params || {} }),
  clear: () => set({ currentRoute: "/onboarding", routeParams: {} }),
}));
