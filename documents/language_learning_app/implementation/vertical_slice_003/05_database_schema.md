# 05 — Database Schema (Vertical Slice 003)

## PostgreSQL 16.14

All 17 tables verified via `\dt`:
1. users
2. learner_profiles
3. diagnostic_sessions
4. diagnostic_responses
5. skill_assessments
6. learning_entry_contracts
7. lesson_definitions
8. lesson_sessions
9. lesson_attempts
10. submissions
11. ai_analysis_requests
12. ai_analysis_results
13. validation_results
14. mastery_records
15. mastery_evidence
16. audit_events
17. alembic_version

## Key Constraints
- 20 foreign key constraints (all ON DELETE CASCADE)
- 5 unique constraints (username, email, user+contract_version, session+attempt, user+skill+cefr)
- 46 indexes (PKs, FKs, lookup columns)

## Migration
- Single migration: `001_initial_schema.py`
- Upgrade: `alembic upgrade head` → 001
- Downgrade: `alembic downgrade base` → clean
- Re-upgrade: verified clean → head
- Current: `001 (head)`

## Verified
- All tables: PASSED
- All indexes: PASSED
- All foreign keys: PASSED
- All unique constraints: PASSED
- Upgrade/downgrade/reupgrade cycle: PASSED
