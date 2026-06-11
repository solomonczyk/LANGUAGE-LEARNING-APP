# Issue Register

## Issue Summary

| Category | Critical | Major | Minor | Observation | Total |
|----------|----------|-------|-------|-------------|-------|
| Runtime | 0 | 0 | 0 | 0 | 0 |
| UX | 0 | 0 | 3 | 2 | 5 |
| Learning Clarity | 0 | 0 | 1 | 1 | 2 |
| Accessibility | 0 | 0 | 0 | 0 | 0 |
| Trust/Safety | 0 | 0 | 0 | 0 | 0 |
| Content | 0 | 0 | 0 | 1 | 1 |
| Technical Debt | 0 | 0 | 0 | 2 | 2 |
| **Total** | **0** | **0** | **4** | **6** | **10** |

Blocking next stage: **0**

## Detailed Issue Register

### UX Issues

---

**ISSUE-001: Diagnostic step shows demo responses without clear interactivity indication**
- **Source**: operator
- **Category**: ux
- **Severity**: minor
- **Screen/Step**: Diagnostic (all steps)
- **Description**: The diagnostic screen displays pre-filled responses (e.g., "✓ Sentence B is correct") that look like they should be interactive but are actually demo/informational placeholders. This could confuse learners into thinking they can select different options when the actual behavior is auto-advancing.
- **Evidence**: Code review of diagnostic.tsx lines 126-136 — the grammar_recognition step shows options but only the hint text indicates which is correct
- **Recommended action**: Either make the diagnostic truly interactive (tappable options) or replace demo options with clearer non-interactive design
- **Required before next stage**: false (minor UX improvement)

---

**ISSUE-002: Lesson duration preference not reflected in lesson cards**
- **Source**: operator
- **Profile**: ALPHA-003
- **Severity**: minor
- **Screen/Step**: Home lesson card
- **Description**: The home screen lesson card shows "~15 min" for all learners, regardless of the preferred lesson duration set during onboarding. Learners who chose 10 or 20 minutes see the same estimate.
- **Evidence**: home.tsx line 76 hardcodes "~15 min" instead of reading from the learning contract
- **Recommended action**: Dynamically calculate duration estimate from the learning contract or lesson definition
- **Required before next stage**: false (minor UX improvement)

---

**ISSUE-003: Level selection labels could be more encouraging for beginners**
- **Source**: operator
- **Profile**: ALPHA-004
- **Severity**: observation
- **Screen/Step**: Onboarding step 3 (level selection)
- **Description**: The A1 level is labeled as "Beginner" which is clear but could be more encouraging ("Starting Out", "New to the language") to reduce anxiety for low-confidence learners.
- **Evidence**: onboarding.tsx getLevelDescription function line 280
- **Recommended action**: Consider more encouraging level labels or descriptions
- **Required before next stage**: false (observation)

---

**ISSUE-004: No visible UI differentiation between learner levels**
- **Source**: operator
- **Profile**: ALPHA-005
- **Severity**: observation
- **Screen/Step**: Home, Lesson
- **Description**: A1 and B2 learners see identical lesson content (same title, same task, same lesson card). The only differentiation is in the learning contract parameters. This reduces perceived value for advanced learners.
- **Evidence**: home.tsx and lesson/[id].tsx use static LESSON_INFO — no dynamic level-based content
- **Recommended action**: Implement level-adaptive lesson content loading
- **Required before next stage**: false (product finding, not a defect)

---

### Learning Clarity Issues

---

**ISSUE-005: Learning contract terms may be technical for beginners**
- **Source**: operator
- **Profile**: ALPHA-002, ALPHA-004
- **Severity**: minor
- **Screen/Step**: Learning Contract screen
- **Description**: Terms like "scaffolding mode", "active vocabulary budget", "max primary corrections", "lesson complexity" are displayed in the contract but may not be intuitive for A1 learners. The contract is functionally correct but the UX assumes some domain knowledge.
- **Evidence**: learning-contract.tsx lines 86-99 map these terms directly from the backend
- **Recommended action**: Add brief plain-language explanations next to technical terms, or use more learner-friendly labels
- **Required before next stage**: false (minor improvement)

---

**ISSUE-006: Communicative goal and task distinction could be clearer**
- **Source**: operator
- **Severity**: observation
- **Screen/Step**: Lesson screen
- **Description**: The lesson screen shows both "Communicative Goal" and "Your Task" sections. While clearly labeled, some learners might benefit from an explicit connection between the goal (the broader skill) and the task (the specific action).
- **Evidence**: lesson/[id].tsx lines 93-101
- **Recommended action**: Consider adding a bridging sentence like "To achieve this goal, we'd like you to..."
- **Required before next stage**: false (observation)

---

### Content Issues

---

**ISSUE-007: Only one lesson definition available for testing**
- **Source**: operator
- **Severity**: observation
- **Screen/Step**: Lesson creation
- **Description**: The alpha uses a single seed lesson definition (ID: 00000000-0000-0000-0000-000000000010). While sufficient for flow testing, real alpha participants would need multiple lesson types.
- **Evidence**: Lesson session creation always uses the same lesson definition ID
- **Recommended action**: Seed additional lesson definitions for broader testing
- **Required before next stage**: false (scope-limited alpha)

---

### Technical Debt Issues

---

**ISSUE-008: Mock AI fixtures are deterministic and do not adapt to learner level**
- **Source**: operator
- **Severity**: observation
- **Screen/Step**: AI Analysis pipeline
- **Description**: The mock AI analysis returns the same fixture structure regardless of learner level or submission quality. Text keyword matching selects the fixture, not CEFR-level-aware analysis. This is sufficient for mock mode but limits level-adaptive feedback.
- **Evidence**: Mock AI service uses keyword-based fixture selection
- **Recommended action**: Document as known limitation; real AI integration will resolve this
- **Required before next stage**: false (accepted limitation of mock mode)

---

**ISSUE-009: Operator audit access control not enforced**
- **Source**: operator (confirmed by integration tests)
- **Severity**: observation (filed as known limitation)
- **Screen/Step**: Operator audit endpoint
- **Description**: The integration test confirms that non-operator users can access the audit events endpoint. This is a known limitation of the current operator authorization implementation.
- **Evidence**: Integration test test_audit_access_blocked_for_non_operator accepts both 200 and 403
- **Recommended action**: Implement proper operator authorization middleware before staging
- **Required before next stage**: false (alpha scope; needed before staging)

---

**ISSUE-010: No forbidden actions detected during alpha**
- **Source**: operator (automated check)
- **Severity**: observation
- **Category**: runtime
- **Description**: Forbidden action scan confirmed no real AI calls, no staging/production deployment, no public access, no real personal data.
- **Evidence**: Verified by code review and session logs
- **Recommended action**: Continue monitoring
- **Required before next stage**: false (all clean)
