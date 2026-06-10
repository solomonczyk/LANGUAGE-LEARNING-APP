# Git Delivery and Feature Closeout

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Feature Closeout Checklist

Every future feature-layer task MUST complete the following sequence:

```
preflight
→ implementation
→ tests
→ artifacts
→ documentation update
→ proof JSON
→ diff inspection
→ commit
→ push
→ fetch
→ clean git
→ HEAD == origin
```

---

## 2. Preflight

Before starting any implementation:

```bash
git fetch origin
git status --short       # Must be clean
git rev-parse HEAD       # Record starting commit
git rev-parse origin/master  # Record origin state
```

---

## 3. Implementation + Tests

- All code changes must include corresponding tests
- All existing tests must continue to pass
- No TODO, placeholder, or incomplete implementation
- No secrets or credentials

---

## 4. Artifacts

- Update artifact index (`implementation_artifact_index.json`) with new files
- Update traceability matrix if new requirements are added
- Generate or update proof JSON

---

## 5. Documentation Update

- Update any affected documentation
- Ensure document index reflects new documents
- Ensure all cross-references are valid

---

## 6. Proof JSON

Each feature layer creates a proof JSON with:

```json
{
  "task_id": "TASK-ID",
  "verdict": "ACCEPTED",
  "feature_completed": true,
  "tests": {
    "tests_passed": 42
  },
  "traceability": {
    "requirements_traced": 15,
    "requirements_untraced": 0
  },
  "git": {
    "branch": "master",
    "starting_commit": "FULL_HASH",
    "final_commit": "FULL_HASH",
    "commit_created": true,
    "commit_pushed": true,
    "git_clean": true,
    "head_matches_origin": true,
    "unpushed_commits": 0,
    "uncommitted_changes": 0
  }
}
```

Proof JSON must pass its own JSON Schema validation.

---

## 7. Diff Inspection

```bash
git status --short            # Confirm only expected files changed
git diff                      # Review all uncommitted changes
git diff --cached             # Review staged changes (if any)
```

Verification:

| Check | Pass/Fail |
|-------|-----------|
| No mobile runtime code excluded? | Must pass |
| No backend runtime code excluded? | Must pass |
| No migrations added? | Must pass (unless migration task) |
| No secrets added? | Must pass |
| No deployment files that activate deployment? | Must pass |
| Only expected files changed? | Must pass |

---

## 8. Commit

```bash
git add <files>
git commit -m "type: description"
```

**Commit message format:**
```
<type>: <description>

<optional body>
```

**Types:** `docs`, `feat`, `fix`, `test`, `refactor`, `chore`

**Example:**
```
docs: add implementation canon and vertical slice readiness
```

---

## 9. Push

```bash
git push origin master
```

---

## 10. Final Verification

```bash
git fetch origin
git status --porcelain
git rev-parse HEAD
git rev-parse origin/master
git diff HEAD origin/master
```

### Required Final State

```json
{
  "git_clean": true,
  "head_matches_origin": true,
  "unpushed_commits": 0,
  "uncommitted_changes": 0
}
```

---

## 11. Closeout Summary

Each feature closeout generates a summary in the task output:

```json
{
  "branch": "master",
  "starting_commit": "FULL_HASH",
  "final_commit": "FULL_HASH",
  "commit_created": true,
  "commit_pushed": true,
  "git_clean": true,
  "head_matches_origin": true,
  "unpushed_commits": 0,
  "uncommitted_changes": 0
}
```
