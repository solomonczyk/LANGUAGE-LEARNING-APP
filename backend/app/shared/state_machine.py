"""Deterministic state machine implementation."""

from __future__ import annotations

from typing import Any


class StateMachine:
    """A deterministic, auditable state machine.

    Each transition is defined with:
    - current state
    - event name
    - guard predicate (callable returning bool)
    - next state
    - side effect description
    """

    def __init__(self, initial_state: str, states: set[str]) -> None:
        self._current_state = initial_state
        self._states = states
        self._transitions: dict[tuple[str, str], dict[str, Any]] = {}

    def add_transition(
        self,
        from_state: str,
        event: str,
        to_state: str,
        guard: callable | None = None,
    ) -> None:
        key = (from_state, event)
        self._transitions[key] = {
            "to": to_state,
            "guard": guard or (lambda **kwargs: True),
        }

    def transition(self, event: str, **kwargs: Any) -> str:
        key = (self._current_state, event)
        if key not in self._transitions:
            raise ValueError(
                f"Invalid transition: {self._current_state} -> {event}. "
                f"Allowed events: {[e for (s, e) in self._transitions if s == self._current_state]}"
            )

        t = self._transitions[key]
        guard_pass = t["guard"](**kwargs)
        if not guard_pass:
            raise ValueError(f"Guard denied transition: {self._current_state} -> {event}")

        self._current_state = t["to"]
        return self._current_state

    @property
    def current_state(self) -> str:
        return self._current_state

    def can_transition(self, event: str, **kwargs: Any) -> bool:
        key = (self._current_state, event)
        if key not in self._transitions:
            return False
        return self._transitions[key]["guard"](**kwargs)

    def allowed_events(self) -> list[str]:
        return [e for (s, e) in self._transitions if s == self._current_state]

    def reset(self, state: str) -> None:
        if state not in self._states:
            raise ValueError(f"Invalid state: {state}")
        self._current_state = state
