# Database and Migration Canon

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-004, ADR-020  
**Schema:** `schemas/database_convention.schema.json`

---

## 1. Database Technology

| Component | Technology | Version |
|-----------|------------|---------|
| Database | PostgreSQL | 16+ |
| ORM | SQLAlchemy | 2.0+ |
| Migration tool | Alembic | 1.13+ |
| Extension | `pgcrypto` (UUID generation) | — |
| Extension | `pg_trgm` (text search, post-MVP) | — |

---

## 2. Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Table names | snake_case, plural | `lesson_sessions`, `reward_transactions` |
| Column names | snake_case | `created_at`, `learner_profile_id` |
| Primary keys | `id` (UUID) | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` |
| Foreign keys | `{table}_id` | `learner_profile_id UUID REFERENCES learner_profiles(id)` |
| Index names | `idx_{table}_{column}` | `idx_lesson_sessions_status` |
| Unique constraints | `uq_{table}_{columns}` | `uq_submissions_idempotency_key` |
| Check constraints | `ck_{table}_{description}` | `ck_xp_balance_non_negative` |

---

## 3. UUID Policy

- All primary keys: UUID v4 (generated via PostgreSQL `gen_random_uuid()`)
- UUID generated server-side (not client)
- No auto-increment integer primary keys
- Rationale: prevents enumeration, supports distributed systems, survives migration

---

## 4. Timestamp Columns

Every table MUST have:

```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
```

Tables with soft delete MUST have:

```sql
deleted_at TIMESTAMPTZ
```

- All timestamps: `TIMESTAMPTZ` (timestamptz with time zone)
- `updated_at` auto-updated via SQLAlchemy `onupdate=func.now()`
- `deleted_at` NULL = active; non-NULL = soft-deleted

---

## 5. Status Fields

| Convention | Type | Default | Example |
|------------|------|---------|---------|
| Status | `VARCHAR(32)` | `'created'` | `status VARCHAR(32) NOT NULL DEFAULT 'created'` |
| Constraint | CHECK | — | `CHECK (status IN ('created', 'active', 'completed', 'failed'))` |

Status transitions enforced by application logic (state machines), not CHECK constraints alone.

---

## 6. Indexes

| Type | Rule |
|------|------|
| Primary key | Auto-indexed (UUID PK) |
| Foreign keys | Always indexed (explicit `CREATE INDEX`) |
| Status filters | Index on `status` for filtered queries |
| User lookups | Index on `(user_id, created_at DESC)` for timeline queries |
| Unique constraints | Use `UNIQUE` constraint (auto-indexed) |
| Partial indexes | For soft-delete: `CREATE INDEX ... WHERE deleted_at IS NULL` |

---

## 7. Soft Delete vs Hard Delete

| Operation | Method | Audit |
|-----------|--------|-------|
| Lesson session abort | Soft delete (`deleted_at = NOW()`) | `lesson_session.abandoned` event |
| User account deletion | Soft delete + anonymization | `user.deleted` event |
| Audit events | Hard delete FORBIDDEN (append-only) | — |
| Reward transactions | Hard delete FORBIDDEN (append-only) | — |
| Duplicate/resolved integrity signals | Soft delete | `integrity.resolved` event |

---

## 8. Migration Naming

```
{alembic_id}_{description}.py
```

Example: `a1b2c3d4e5f6_add_lesson_sessions_table.py`

---

## 9. Migration Rules

| Rule | Enforcement |
|------|-------------|
| Every migration must have both `upgrade()` and `downgrade()` | CI check |
| `downgrade()` must restore the previous state completely | Code review |
| No data loss in downgrade (truncate/delete may be reversed) | Code review |
| Migration must be idempotent (safe to re-run) | Use `CREATE IF NOT EXISTS` / `ALTER IF EXISTS` |
| Migration must not reference application models (raw SQL or Alembic `op` only) | CI check |
| Migration filenames must not be renamed after commit | Git history check |
| Each migration must be reviewed independently | Code review |
| Migration must not exceed 100 lines (if so, split into multiple) | CI check |

---

## 10. Migration Workflow

1. Developer creates migration: `alembic revision --autogenerate -m "description"`
2. Review auto-generated migration for correctness (autogenerate can miss renames)
3. Test `alembic upgrade head` on local database
4. Test `alembic downgrade -1` (rollback one step)
5. Commit migration with the code change
6. CI runs `alembic upgrade head` on test database
7. CI runs `alembic downgrade -1` to verify rollback

---

## 11. Seed Data

- Seed data: `alembic/seed/` directory with Python scripts
- Seeds are run separately from migrations (`python -m app.seed`)
- Seeds are idempotent (upsert-based)
- Test seed data: pytest fixtures, not database seeds

---

## 12. Source of Truth Rules

PostgreSQL is the **sole source of truth** for:

| Data | Can Be Cached In |
|------|-----------------|
| Lesson completion | PostgreSQL only (NOT Redis, NOT client) |
| Mastery | PostgreSQL only |
| Review state | PostgreSQL only |
| Rewards | PostgreSQL only |
| XP | PostgreSQL only |
| Security events | PostgreSQL only |
| Audit | PostgreSQL only |

Redis may cache but must tolerate data loss (cache-rebuild from PostgreSQL).

---

## 13. Transaction Boundaries

| Scope | Transaction | Notes |
|-------|-------------|-------|
| Single request | One transaction per request | Commit on success, rollback on error |
| Pipeline (submission → validation → mastery) | Single transaction for lesson completion | All-or-nothing |
| Cross-module (reward + audit) | Same transaction | Both commit or both rollback |
| Background job | Transaction per job | Retry on serialization failure |

---

## 14. Concurrency and Duplicate Prevention

| Pattern | Mechanism |
|---------|-----------|
| Duplicate submission | Idempotency key + UNIQUE constraint on `(lesson_session_id, idempotency_key)` |
| Duplicate reward | `(user_id, activity_type, activity_id)` UNIQUE constraint |
| Race condition on mastery | `SELECT ... FOR UPDATE` on MasteryRecord row |
| Concurrent profile update | Optimistic locking with `updated_at` version check |
