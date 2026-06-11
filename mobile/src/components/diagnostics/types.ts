/** Shared types for diagnostic item components. */

export interface FeedbackData {
  correct: boolean;
  text: string;
  details?: string;
}

export interface DiagnosticItemProps {
  responseData: Record<string, unknown> | null;
  disabled: boolean;
  onResponseChange: (data: Record<string, unknown>) => void;
  feedback: FeedbackData | null;
}

export interface StepConfig {
  key: string;
  type: string;
  label: string;
  prompt: string;
  estimated_seconds: number;
}

export interface DimensionResultResponse {
  raw_score: number | null;
  estimated_level: string;
  confidence: number;
  evidence_count: number;
  contradictions: string[];
  needs_follow_up: boolean;
  status: string;
  deferred?: boolean;
}
