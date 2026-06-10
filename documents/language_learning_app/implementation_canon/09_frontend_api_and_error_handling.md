# Frontend API and Error Handling

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. API Client Architecture

```
src/services/api/
├── client.ts              # Base fetch wrapper with auth, timeout, trace ID
├── types.ts               # ApiResponse<T>, ApiError, PaginatedResponse
├── interceptors.ts        # Request/response interceptors (auth, trace, error mapping)
├── api-config.ts          # Base URL, timeouts, retry config
└── query-client.ts        # TanStack QueryClient configuration
```

---

## 2. Base URL Configuration

| Environment | Base URL | Source |
|-------------|----------|--------|
| Local development | `http://localhost:8000/api/v1` | `.env.development` |
| Test | `http://localhost:8000/api/v1` | Test config |
| Staging | `https://api-staging.llapp.com/api/v1` | `.env.staging` |
| Production | `https://api.llapp.com/api/v1` | `.env.production` (locked) |

---

## 3. Request Pipeline

```
Client code
  → useQuery / useMutation
    → queryClient
      → apiClient.request(method, path, options)
        → interceptors.request (add auth, trace ID, content-type)
          → fetch(url, options)
            → interceptors.response (parse JSON, map errors)
              → validate with Zod schema
                → return typed data / throw typed ApiError
```

---

## 4. Auth Token Injection

- Access token retrieved from `expo-secure-store` in request interceptor
- Header: `Authorization: Bearer <access_token>`
- On 401: attempt token refresh via `/auth/refresh`
  - If refresh succeeds: retry original request with new token
  - If refresh fails: clear auth state, redirect to login
- Token refresh race condition: queue concurrent 401s and refresh once

---

## 5. Trace ID

- Generated on each request: `crypto.randomUUID()` (or `uuid.v4()` polyfill)
- Header: `X-Trace-Id: <uuid>`
- Logged in console and telemetry for request correlation
- Shown in error responses for support debugging

---

## 6. API Response Types

```typescript
// Successful response
interface ApiResponse<T> {
  data: T;
}

// Paginated response
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    limit: number;
    offset: number;
    total: number;
    has_more: boolean;
  };
}

// Error response (maps to backend canon error contract)
interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    trace_id: string;
    retryable: boolean;
  };
}
```

---

## 7. Error Handling Hierarchy

```
ApiError (typed, thrown by API client)
├── AuthError (401 — token expired, invalid)
├── PermissionError (403 — forbidden)
├── NotFoundError (404)
├── ValidationError (422 — field-level errors in details)
├── RateLimitError (429 — retryable with Retry-After header)
├── ServerError (5xx — retryable)
└── NetworkError (fetch failed — retryable)
```

---

## 8. Frontend Error Display Mapping

| Error | User Message | Action |
|-------|-------------|--------|
| AuthError | "Session expired. Please log in again." | Redirect to login |
| PermissionError | "You don't have access to this feature." | Back to home |
| NotFoundError | "This content could not be found." | Back to previous |
| ValidationError | Per-field messages from `details` | Scroll to field, show inline |
| RateLimitError | "Too many requests. Please wait a moment." | Auto-retry after header delay |
| ServerError | "Something went wrong. Please try again." | Show retry button |
| NetworkError | "No internet connection." | Offline banner; retry on reconnect |

---

## 9. TanStack Query Client Defaults

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,        // 5 minutes
      gcTime: 30 * 60 * 1000,           // 30 minutes (formerly cacheTime)
      retry: 3,
      retryDelay: (attempt) => Math.min(1000 * 2 ** attempt, 10000),
      refetchOnWindowFocus: true,
      refetchOnReconnect: true,
      networkMode: 'offlineFirst',
    },
    mutations: {
      retry: 0,
      networkMode: 'offlineFirst',
    },
  },
});
```

---

## 10. Mutation Error Handling Pattern

```typescript
const mutation = useMutation({
  mutationFn: (data) => apiClient.post('/lessons/sessions', data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['lessons'] });
  },
  onError: (error: ApiError) => {
    if (error instanceof AuthError) {
      // redirect to login
    } else if (error instanceof ValidationError) {
      // set field errors on form
    } else if (error instanceof ServerError && error.retryable) {
      // show toast with retry
    } else {
      // show generic error screen/toast
    }
  },
});
```

---

## 11. Forbidden Patterns

| Pattern | Reason |
|---------|--------|
| `try/catch` around fetch without mapping to `ApiError` | Unhandled error types leak to UI |
| Displaying raw API error message to user | May contain internal details |
| Ignoring non-2xx responses | Silent failures |
| Using `any` or `unknown` for API response types | Bypasses validation |
| Mutating TanStack Query cache directly without invalidation | Stale data |
| Using `axios` instead of `fetch` | Unnecessary dependency |
