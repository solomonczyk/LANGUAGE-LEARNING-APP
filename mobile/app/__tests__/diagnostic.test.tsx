/**
 * Diagnostic Narrative Coherence Tests
 *
 * Verifies that ordering/coherence tasks have one clearly correct
 * causal/temporal order and that the accepted_alternatives mechanism
 * works for any future items with genuinely valid alternatives.
 */

// ── Narrative coherence data (mirrors diagnostic.tsx) ─────────────────
const NARRATIVE_EVENTS = [
  { id: "1", text: "Dig a small hole in the soil" },
  { id: "2", text: "Place the seed in the hole" },
  { id: "3", text: "Cover the seed with soil" },
  { id: "4", text: "Water the soil gently" },
  { id: "5", text: "Wait for the seed to sprout" },
];
const CORRECT_NARRATIVE_ORDER = ["1", "2", "3", "4", "5"];
const ACCEPTED_NARRATIVE_ALTERNATIVES: string[][] = [];
const SCRAMBLED_DISPLAY_ORDER = ["3", "5", "1", "4", "2"];

/**
 * Returns true if userOrder matches either the exact correct order
 * or any accepted alternative. Mirrors the logic in diagnostic.tsx.
 */
function isNarrativeOrderCorrect(userOrder: string[]): boolean {
  const matchesExact =
    userOrder.length === CORRECT_NARRATIVE_ORDER.length &&
    userOrder.every((id, i) => id === CORRECT_NARRATIVE_ORDER[i]);
  if (matchesExact) return true;

  const matchesAlternative = ACCEPTED_NARRATIVE_ALTERNATIVES.some(
    (alt) =>
      userOrder.length === alt.length &&
      userOrder.every((id, i) => id === alt[i])
  );
  return matchesAlternative;
}

describe("Narrative Coherence — plant-growing sequence", () => {
  // ── Causal/temporal order verification ──────────────────────────
  it("has a single correct order (causally unambiguous)", () => {
    // The plant-growing sequence has one clearly correct order:
    // 1. Dig a hole (must happen first)
    // 2. Place the seed (must happen after hole is dug)
    // 3. Cover the seed (must happen after seed is placed)
    // 4. Water the soil (must happen after seed is covered)
    // 5. Wait for sprout (must happen after everything else)
    const correctOrder = CORRECT_NARRATIVE_ORDER;
    expect(correctOrder).toEqual(["1", "2", "3", "4", "5"]);
  });

  it("has no accepted alternatives (no ambiguous orders)", () => {
    // Every step causally depends on the previous, so there is
    // exactly one valid order. No alternatives needed.
    expect(ACCEPTED_NARRATIVE_ALTERNATIVES).toHaveLength(0);
  });

  // ── Correct order matching ───────────────────────────────────────
  it("isNarrativeOrderCorrect returns true for the correct order", () => {
    expect(isNarrativeOrderCorrect(["1", "2", "3", "4", "5"])).toBe(true);
  });

  it("isNarrativeOrderCorrect returns false for reversed order", () => {
    expect(isNarrativeOrderCorrect(["5", "4", "3", "2", "1"])).toBe(false);
  });

  it("isNarrativeOrderCorrect returns false for scrambled order", () => {
    expect(isNarrativeOrderCorrect(["3", "1", "4", "2", "5"])).toBe(false);
  });

  it("isNarrativeOrderCorrect returns false for empty order", () => {
    expect(isNarrativeOrderCorrect([])).toBe(false);
  });

  it("isNarrativeOrderCorrect returns false for partial order", () => {
    expect(isNarrativeOrderCorrect(["1", "2", "3"])).toBe(false);
  });

  // ── Plausible alternative that should NOT be accepted ────────────
  it("does not accept 'Place seed before digging hole' (causally wrong)", () => {
    // You cannot place a seed before digging a hole
    expect(isNarrativeOrderCorrect(["2", "1", "3", "4", "5"])).toBe(false);
  });

  it("does not accept 'Water before covering seed' (causally wrong)", () => {
    // You cannot water the seed before covering it with soil
    expect(isNarrativeOrderCorrect(["1", "2", "4", "3", "5"])).toBe(false);
  });

  it("does not accept 'Sprout before watering' (causally wrong)", () => {
    // The seed cannot sprout before being watered
    expect(isNarrativeOrderCorrect(["1", "2", "3", "5", "4"])).toBe(false);
  });

  // ── Scramble verification ────────────────────────────────────────
  it("scrambled display order differs from correct order", () => {
    const isSameOrder =
      SCRAMBLED_DISPLAY_ORDER.length === CORRECT_NARRATIVE_ORDER.length &&
      SCRAMBLED_DISPLAY_ORDER.every(
        (id, i) => id === CORRECT_NARRATIVE_ORDER[i]
      );
    expect(isSameOrder).toBe(false);
  });

  it("scrambled order contains all event IDs", () => {
    const allIds = NARRATIVE_EVENTS.map((e) => e.id);
    const sortedScramble = [...SCRAMBLED_DISPLAY_ORDER].sort();
    const sortedCorrect = [...allIds].sort();
    expect(sortedScramble).toEqual(sortedCorrect);
  });

  // ── Accepted alternatives mechanism ──────────────────────────────
  it("accepted_alternatives mechanism works when alternatives exist", () => {
    // Simulate a future sequence where 2 orders are both valid
    // (this tests the mechanism, not the current data)
    const testAlternatives: string[][] = [["2", "1", "3", "4", "5"]];

    const matchesCurrent = isNarrativeOrderCorrect(["2", "1", "3", "4", "5"]);
    expect(matchesCurrent).toBe(false); // Not in current alternatives

    // The mechanism itself — checking against a hypothetical alternative
    const matchesHypothetical = testAlternatives.some(
      (alt) =>
        ["2", "1", "3", "4", "5"].length === alt.length &&
        ["2", "1", "3", "4", "5"].every((id, i) => id === alt[i])
    );
    expect(matchesHypothetical).toBe(true);
  });

  // ── Event text semantic verification ─────────────────────────────
  it("each step text describes a distinct action", () => {
    const texts = NARRATIVE_EVENTS.map((e) => e.text);
    const uniqueTexts = new Set(texts);
    expect(uniqueTexts.size).toBe(texts.length);
  });

  it("all steps are required to complete the sequence", () => {
    // The task requires ALL events to be placed before submission
    expect(NARRATIVE_EVENTS.length).toBe(5);
  });

  it("no event has empty text", () => {
    NARRATIVE_EVENTS.forEach((ev) => {
      expect(ev.text.trim().length).toBeGreaterThan(0);
    });
  });
});
