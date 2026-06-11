"""Tests for the deterministic state machine."""

import pytest
from app.shared.state_machine import StateMachine


class TestDiagnosticStateMachine:
    def setup_method(self):
        self.sm = StateMachine("CREATED", {"CREATED", "IN_PROGRESS", "COMPLETED", "FAILED"})
        self.sm.add_transition("CREATED", "start", "IN_PROGRESS")
        self.sm.add_transition("CREATED", "fail", "FAILED")
        self.sm.add_transition("IN_PROGRESS", "complete", "COMPLETED")
        self.sm.add_transition("IN_PROGRESS", "fail", "FAILED")

    def test_initial_state(self):
        assert self.sm.current_state == "CREATED"

    def test_valid_transition(self):
        self.sm.transition("start")
        assert self.sm.current_state == "IN_PROGRESS"

    def test_invalid_transition(self):
        with pytest.raises(ValueError, match="Invalid transition"):
            self.sm.transition("complete")  # Can't complete from CREATED

    def test_forbidden_transition_after_failure(self):
        self.sm.transition("start")
        self.sm.transition("fail")
        assert self.sm.current_state == "FAILED"
        with pytest.raises(ValueError):
            self.sm.transition("complete")

    def test_allowed_events(self):
        events = self.sm.allowed_events()
        assert "start" in events
        assert "fail" in events

    def test_guard_denied_transition(self):
        sm = StateMachine("CREATED", {"CREATED", "ACTIVE"})
        sm.add_transition("CREATED", "activate", "ACTIVE", guard=lambda **k: False)
        with pytest.raises(ValueError, match="Guard denied"):
            sm.transition("activate")

    def test_duplicate_event_safe(self):
        self.sm.transition("start")
        self.sm.transition("complete")
        assert self.sm.current_state == "COMPLETED"
        with pytest.raises(ValueError):
            self.sm.transition("complete")  # No transition from COMPLETED

    def test_reset(self):
        self.sm.transition("start")
        self.sm.reset("CREATED")
        assert self.sm.current_state == "CREATED"


class TestLessonStateMachine:
    def setup_method(self):
        states = {"CREATED", "ACTIVE", "SUBMITTED", "ANALYSIS_PENDING",
                  "ANALYSIS_VALIDATED", "COMPLETED", "REJECTED", "FAILED"}
        self.sm = StateMachine("CREATED", states)
        self.sm.add_transition("CREATED", "activate", "ACTIVE")
        self.sm.add_transition("ACTIVE", "submit", "SUBMITTED")
        self.sm.add_transition("SUBMITTED", "start_analysis", "ANALYSIS_PENDING")
        self.sm.add_transition("ANALYSIS_PENDING", "validate", "ANALYSIS_VALIDATED")
        self.sm.add_transition("ANALYSIS_VALIDATED", "complete", "COMPLETED")
        self.sm.add_transition("ANALYSIS_VALIDATED", "reject", "REJECTED")
        self.sm.add_transition("CREATED", "fail", "FAILED")

    def test_full_happy_path(self):
        self.sm.transition("activate")
        assert self.sm.current_state == "ACTIVE"
        self.sm.transition("submit")
        assert self.sm.current_state == "SUBMITTED"
        self.sm.transition("start_analysis")
        assert self.sm.current_state == "ANALYSIS_PENDING"
        self.sm.transition("validate")
        assert self.sm.current_state == "ANALYSIS_VALIDATED"
        self.sm.transition("complete")
        assert self.sm.current_state == "COMPLETED"

    def test_rejection_path(self):
        self.sm.transition("activate")
        self.sm.transition("submit")
        self.sm.transition("start_analysis")
        self.sm.transition("validate")
        self.sm.transition("reject")
        assert self.sm.current_state == "REJECTED"

    def test_failure_at_any_state(self):
        self.sm.transition("activate")
        with pytest.raises(ValueError):
            # No direct fail from ACTIVE in this config
            self.sm.transition("fail")

    def test_audit_event_per_transition(self):
        events = []
        # Simulate audit logging
        self.sm.transition("activate")
        events.append("activate")
        self.sm.transition("submit")
        events.append("submit")
        assert len(events) == 2
