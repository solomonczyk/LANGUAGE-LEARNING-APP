# Code Quality and Repository Conventions

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Python files | snake_case | `lesson_engine.py` |
| TypeScript files | kebab-case | `lesson-engine.ts` |
| Python functions | snake_case | `get_lesson_session()` |
| Python classes | PascalCase | `LessonSessionService` |
| TypeScript functions | camelCase | `getLessonSession()` |
| TypeScript types/interfaces | PascalCase | `LessonSession` |
| TypeScript components | PascalCase | `LessonScreen` |
| Database columns | snake_case | `created_at` |
| Environment variables | UPPER_SNAKE_CASE | `LL_APP_DATABASE_URL` |
| Git branches | kebab-case | `feature/lesson-session` |

---

## 2. Folder Structure

### Backend (FastAPI)
```
backend/
├── app/
│   ├── modules/{module_name}/
│   │   ├── __init__.py
│   │   ├── public_interface.py    # What other modules may import
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── services.py            # Business logic
│   │   ├── router.py              # FastAPI router (endpoints)
│   │   └── dependencies.py        # Module-specific dependencies
│   └── shared/                    # Shared utilities
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── alembic/versions/
```

### Frontend (React Native)
```
mobile/
├── app/                           # Expo Router routes
├── src/
│   ├── features/{feature_name}/
│   │   ├── components/            # Feature-specific components
│   │   ├── hooks/                 # Feature-specific hooks
│   │   ├── screens/               # Screen components
│   │   └── index.ts               # Public API
│   ├── shared/                    # Shared UI and utilities
│   └── services/                  # Service modules
├── __tests__/
└── e2e/
```

---

## 3. Import Rules

| Rule | Backend | Frontend |
|------|---------|----------|
| Absolute imports preferred | Yes (from app.modules...) | Yes (from @/features/...) |
| Cross-module imports | Only `public_interface.py` | Only `index.ts` |
| No circular imports | CI check (pytest) | CI check (ESLint import) |
| No unused imports | CI check (ruff) | CI check (ESLint) |
| Import ordering | isort (via ruff) | ESLint import/order |

---

## 4. Typing Rules

| Rule | Backend | Frontend |
|------|---------|----------|
| Strict typing | mypy strict mode | TypeScript strict mode |
| No `Any` | Exceptions require inline `# type: ignore` with reason | No `any` except legacy interop |
| Function return types | Required | Required |
| Variable types | Inferred via mypy | Inferred via TypeScript |
| Optional types | `Optional[T]` or `T | None` | `T | undefined` |
| Union types | `Union[T, U]` or `T | U` | `T | U` |

---

## 5. Formatting and Linting

### Backend (Python)
| Tool | Config | Command |
|------|--------|---------|
| ruff (lint) | `pyproject.toml` | `ruff check .` |
| ruff (format) | `pyproject.toml` | `ruff format . --check` |
| mypy (type check) | `pyproject.toml`, strict | `mypy app/` |

### Frontend (TypeScript)
| Tool | Config | Command |
|------|--------|---------|
| ESLint | `eslint.config.js` | `eslint src/` |
| Prettier | `.prettierrc` | `prettier --check src/` |
| TypeScript | `tsconfig.json`, strict | `tsc --noEmit` |

---

## 6. Comments and Documentation

| Item | Requirement |
|------|-------------|
| Public functions/services | Docstring (Python: Google style, TypeScript: JSDoc) |
| Complex logic (>10 lines) | Inline comment explaining intent, not mechanics |
| TODOs | Must reference issue number: `# TODO(ISSUE-42): ...` |
| No commented-out code | CI lint check |
| No broad exception catch without comment | `except Exception: # noqa` with reason |
| Module-level docstring | Required for each module `__init__.py` |

---

## 7. Error Handling

| Rule | Backend | Frontend |
|------|---------|----------|
| Use typed exceptions | `AppException` subclasses | `ApiError` subclasses |
| Catch specific exceptions | Yes (not broad `Exception`) | Yes |
| Log with context | `logger.error(msg, extra={...})` | `console.error(msg, data)` |
| Never swallow silently | Always log or re-raise | Always log or show UI |
| Validation errors | Return canonical error format | Show inline field errors |

---

## 8. Testing Conventions

| Item | Convention |
|------|-----------|
| Test file location | `__tests__/` mirroring source structure |
| Test file naming | `{source_name}.test.ts` or `test_{source_name}.py` |
| Fixture naming | Descriptive: `valid_lesson_session`, `invalid_submission` |
| Test function naming | `test_{scenario}_when_{condition}` |
| One assertion pattern per test | Preferred (or multiple related assertions) |

---

## 9. Dependency Policy

| Rule | Enforcement |
|------|-------------|
| Pin major versions | `pyproject.toml` and `package.json` pin major versions |
| Review new dependencies | Requires rationale in PR description |
| No unused dependencies | CI check (`pip freeze` vs imports, `depcheck`) |
| Security audit | `pip audit` / `npm audit` in CI |
| License check | No GPL/AGPL dependencies (preferred permissive) |

---

## 10. Prohibited Patterns

| Pattern | Reason | CI Check |
|---------|--------|----------|
| `except: pass` | Silent failure | ruff check (`BLE001`) |
| Disabled test without issue | Unknown risk | Code review |
| `TODO` without issue | Untracked work | CI lint (warning) |
| Placeholder code (`pass`, `return None`) | Incomplete implementation | Code review |
| Fake `PASS` in tests | Misleading test result | Code review |
| `console.log` / `print` committed | Debug artifact | CI lint |
| Untracked contract changes | Silent API drift | OpenAPI drift check |
| Secrets in code | Security risk | Secret scan |
