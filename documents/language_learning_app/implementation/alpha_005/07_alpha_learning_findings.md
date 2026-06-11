# Alpha Learning Findings

## Overview

This document captures findings related to learning clarity, pedagogical flow, and educational effectiveness observed during the closed alpha execution.

## Positive Findings

### 1. Communicative Goal Clarity
The "Communicative Goal" section clearly explains the broader learning objective before presenting the specific task. This layered approach helps learners understand *why* they are doing the task.

**Source**: Lesson screen
**Evidence**: All 5 testers understood the task from the goal + task structure

### 2. Scaffolding Information
Grammar focus and key vocabulary chips provide useful contextual support without being overwhelming. Learners can reference them while writing.

**Source**: Lesson screen support box
**Evidence**: All testers completed submissions with appropriate context

### 3. Constructive Feedback Structure
The result screen orders information as: strengths → corrections → improved phrasing → validation results. This strengths-first approach reduces the punitive feel of corrections.

**Source**: Result screen
**Evidence**: Mock corrections are shown with severity badges and improvement suggestions, not just errors

### 4. Processing Pipeline Transparency
The lesson session screen shows 7 processing steps with progress animation. This helps learners understand that their submission is being analyzed through multiple stages.

**Source**: Lesson session screen
**Evidence**: Clear progress indicator and meaningful step labels

## Areas for Improvement

### 1. Level-Appropriate Content
The most significant finding is that the current MVP does not differentiate lesson content by learner level. A1 beginners and B2 advanced learners see the same lesson title, task, and grammar focus. While the learning contract parameters differ, the actual learning experience is identical.

**Impact**: Advanced learners may feel unchallenged; beginners may feel overwhelmed
**Recommendation**: Implement level-adaptive lesson content loading as a higher priority

### 2. Diagnostic-to-Contract Connection
The diagnostic results flow into the learning contract parameters, but this connection is not explicitly shown to the learner. Showing a "Based on your diagnostic, we recommend..." narrative would strengthen the perceived value.

**Impact**: The contract may feel like a generic template rather than personalized
**Recommendation**: Add a brief narrative connecting diagnostic results to contract parameters

### 3. Mock AI Feedback Scope
The mock AI provides deterministic feedback that, while structurally correct, does not adapt to the specific content of the learner's submission beyond keyword matching. This limits the pedagogical value for alpha participants.

**Impact**: Feedback quality is limited until real AI integration
**Recommendation**: Accept as known limitation of the mock AI gateway

## Learner Engagement Observations

- The step-by-step flow (onboarding → diagnostic → contract → home → lesson) creates a logical learning arc
- The learning contract serves as a "commitment device" that reinforces the learning plan
- The processing pipeline animation creates anticipation for results
- The result screen provides closure and a clear path back to home for continued learning
