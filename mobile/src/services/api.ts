/**
 * API client for backend communication.
 * Uses fetch with auth headers and idempotency support.
 */

const API_BASE = "http://localhost:8000/api/v1";

let userId: string | null = null;

export function setUserId(id: string) {
  userId = id;
}

export function getUserId(): string | null {
  return userId;
}

async function request<T>(
  method: string,
  path: string,
  body?: Record<string, unknown>,
  idempotencyKey?: string,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (userId) {
    headers["X-User-Id"] = userId;
  }

  if (idempotencyKey) {
    headers["X-Idempotency-Key"] = idempotencyKey;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      error: { code: "UNKNOWN", message: response.statusText },
    }));
    throw new ApiError(
      errorData.error?.code || "UNKNOWN",
      errorData.error?.message || response.statusText,
      response.status,
      errorData.error?.details,
    );
  }

  return response.json();
}

export class ApiError extends Error {
  code: string;
  status: number;
  details?: Record<string, unknown>;

  constructor(code: string, message: string, status: number, details?: Record<string, unknown>) {
    super(message);
    this.code = code;
    this.status = status;
    this.details = details;
    this.name = "ApiError";
  }
}

// === Identity ===
export const identity = {
  register: (username: string, displayName: string) =>
    request<{ id: string; username: string; display_name: string }>("POST", "/identity/register", {
      username,
      display_name: displayName,
    }),
  login: (username: string) =>
    request<{ id: string; username: string; display_name: string }>("POST", "/identity/login", {
      username,
    }),
};

// === Learner Profile ===
export const learnerProfile = {
  create: (data: {
    target_language: string;
    native_language: string;
    learning_goal?: string;
    preferred_lesson_duration: number;
    self_reported_level: string;
  }) => request<Record<string, unknown>>("POST", "/learner-profile", data),
  getMe: () => request<Record<string, unknown>>("GET", "/learner-profile/me"),
};

// === Diagnostics ===
export const diagnostics = {
  createSession: () =>
    request<{ session_id: string; status: string; current_step: number; total_steps: number }>(
      "POST",
      "/diagnostics/sessions",
    ),
  submitResponse: (sessionId: string, questionKey: string, responseData: Record<string, unknown>) =>
    request<{ session_id: string; status: string; step: number; total_steps: number }>(
      "POST",
      `/diagnostics/sessions/${sessionId}/responses`,
      { question_key: questionKey, response_data: responseData },
    ),
  complete: (sessionId: string) =>
    request<{ session_id: string; status: string; assessments: Record<string, unknown>[] }>(
      "POST",
      `/diagnostics/sessions/${sessionId}/complete`,
    ),
  getSession: (sessionId: string) =>
    request<Record<string, unknown>>("GET", `/diagnostics/sessions/${sessionId}`),
};

// === Learning Contract ===
export const learningContract = {
  getCurrent: () => request<Record<string, unknown>>("GET", "/learning-contract/current"),
  create: () => request<Record<string, unknown>>("POST", "/learning-contract/current"),
};

// === Lesson Sessions ===
export const lessonSessions = {
  create: (lessonDefinitionId: string) =>
    request<{ session_id: string; status: string; lesson_definition_id: string }>(
      "POST",
      "/lesson-sessions",
      { lesson_definition_id: lessonDefinitionId },
    ),
  get: (sessionId: string) =>
    request<Record<string, unknown>>("GET", `/lesson-sessions/${sessionId}`),
  submitText: (sessionId: string, text: string) =>
    request<{ submission_id: string; session_id: string; status: string }>(
      "POST",
      `/lesson-sessions/${sessionId}/submissions`,
      { text },
    ),
  process: (sessionId: string) =>
    request<{ session_id: string; status: string; decision?: string; validation_results?: Record<string, unknown> }>(
      "POST",
      `/lesson-sessions/${sessionId}/process`,
    ),
};

// === Mastery ===
export const mastery = {
  getProfile: () => request<Record<string, unknown>>("GET", "/mastery/profile"),
};

// === Health ===
export const health = {
  check: () => request<{ status: string; version: string }>("GET", "/health"),
};
