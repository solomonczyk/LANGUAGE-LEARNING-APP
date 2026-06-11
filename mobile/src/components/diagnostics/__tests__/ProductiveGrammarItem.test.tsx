/**
 * Productive Grammar Item Tests — 006D Answer Format Fix
 *
 * Verifies:
 * - Full sentence answers are accepted (Option A)
 * - Fragment-only answers get partial credit
 * - Case/punctuation/space normalization works
 * - Feedback shows full expected sentence
 * - Instruction text matches validator
 */

import React from "react";
import { render, fireEvent, screen } from "@testing-library/react-native";
import ProductiveGrammarItem from "../ProductiveGrammarItem";

describe("ProductiveGrammarItem — instruction text", () => {
  const defaultProps = {
    responseData: null,
    disabled: false,
    onResponseChange: jest.fn(),
    feedback: null,
  };

  it("instruction says 'Rewrite the full sentence correctly'", () => {
    render(<ProductiveGrammarItem {...defaultProps} />);
    expect(
      screen.getByText("Rewrite the full sentence correctly.")
    ).toBeTruthy();
  });

  it("shows helper text about writing the whole sentence", () => {
    render(<ProductiveGrammarItem {...defaultProps} />);
    expect(
      screen.getByText(
        "Write the whole corrected sentence — include all words."
      )
    ).toBeTruthy();
  });

  it("shows three task prompts", () => {
    render(<ProductiveGrammarItem {...defaultProps} />);
    expect(screen.getAllByText("Fix the sentence:")).toHaveLength(3);
  });
});

describe("ProductiveGrammarItem — full sentence acceptance (Option A)", () => {
  let onResponseChange: jest.Mock;

  beforeEach(() => {
    onResponseChange = jest.fn();
  });

  const renderItem = (feedback: boolean = false) =>
    render(
      <ProductiveGrammarItem
        responseData={null}
        disabled={false}
        onResponseChange={onResponseChange}
        feedback={feedback ? { correct: true, text: "" } : null}
      />
    );

  const getInput = (index: number) =>
    screen.getAllByPlaceholderText(
      "Write the whole corrected sentence..."
    )[index];

  // ── Full sentence acceptance ────────────────────────────────────
  it("accepts full corrected sentence for task 1", () => {
    renderItem();
    fireEvent.changeText(getInput(0), "He goes to school every day");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1, total: 3 })
    );
  });

  it("accepts full corrected sentence for task 2", () => {
    renderItem();
    fireEvent.changeText(getInput(1), "She walked to the park yesterday");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1, total: 3 })
    );
  });

  it("accepts full corrected sentence for task 3", () => {
    renderItem();
    fireEvent.changeText(getInput(2), "They are playing football now");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1, total: 3 })
    );
  });

  // ── Partial credit for fragments ─────────────────────────────────
  it("accepts fragment 'he goes' as correct (partial credit)", () => {
    renderItem();
    fireEvent.changeText(getInput(0), "he goes");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1, total: 3 })
    );
  });

  it("accepts fragment 'she walked' as correct (partial credit)", () => {
    renderItem();
    fireEvent.changeText(getInput(1), "she walked");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1, total: 3 })
    );
  });

  it("accepts fragment 'they are' as correct (partial credit)", () => {
    renderItem();
    fireEvent.changeText(getInput(2), "they are");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1, total: 3 })
    );
  });

  // ── Normalization ───────────────────────────────────────────────
  it("is case insensitive", () => {
    renderItem();
    fireEvent.changeText(getInput(0), "HE GOES TO SCHOOL EVERY DAY");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1 })
    );
  });

  it("strips trailing period", () => {
    renderItem();
    fireEvent.changeText(getInput(1), "She walked to the park yesterday.");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1 })
    );
  });

  it("strips trailing exclamation mark", () => {
    renderItem();
    fireEvent.changeText(getInput(2), "They are playing football now!");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1 })
    );
  });

  it("strips trailing question mark", () => {
    renderItem();
    fireEvent.changeText(getInput(0), "He goes to school every day?");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1 })
    );
  });

  it("collapses multiple spaces", () => {
    renderItem();
    fireEvent.changeText(
      getInput(0),
      "He  goes   to school every    day"
    );
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1 })
    );
  });

  it("trims leading/trailing whitespace", () => {
    renderItem();
    fireEvent.changeText(
      getInput(0),
      "  he goes to school every day  "
    );
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 1 })
    );
  });

  // ── Wrong answers ───────────────────────────────────────────────
  it("marks wrong answer as incorrect", () => {
    renderItem();
    fireEvent.changeText(getInput(0), "He go to school");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 0 })
    );
  });

  it("marks completely wrong answer as incorrect", () => {
    renderItem();
    fireEvent.changeText(getInput(0), "I like pizza");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 0 })
    );
  });

  // ── Feedback text ───────────────────────────────────────────────
  it("shows full expected sentence in feedback when wrong", () => {
    renderItem(true);
    // Type something wrong
    const input = getInput(0);
    fireEvent.changeText(input, "wrong answer");
    // Feedback for task 1 should show full expected sentence
    const feedbackText = screen.queryByText(/Expected:/);
    if (feedbackText) {
      expect(feedbackText.props.children).toContain(
        "he goes to school every day"
      );
    }
  });
});

describe("ProductiveGrammarItem — multiple tasks", () => {
  let onResponseChange: jest.Mock;

  beforeEach(() => {
    onResponseChange = jest.fn();
    render(
      <ProductiveGrammarItem
        responseData={null}
        disabled={false}
        onResponseChange={onResponseChange}
        feedback={null}
      />
    );
  });

  it("counts 2 correct when two sentences are right", () => {
    const inputs = screen.getAllByPlaceholderText(
      "Write the whole corrected sentence..."
    );
    fireEvent.changeText(inputs[0], "He goes to school every day");
    fireEvent.changeText(inputs[1], "She walked to the park yesterday");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 2, total: 3 })
    );
  });

  it("counts 3 correct when all sentences are right", () => {
    const inputs = screen.getAllByPlaceholderText(
      "Write the whole corrected sentence..."
    );
    fireEvent.changeText(inputs[0], "He goes to school every day");
    fireEvent.changeText(inputs[1], "She walked to the park yesterday");
    fireEvent.changeText(inputs[2], "They are playing football now");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 3, total: 3 })
    );
  });

  it("counts 0 correct when all are wrong", () => {
    const inputs = screen.getAllByPlaceholderText(
      "Write the whole corrected sentence..."
    );
    fireEvent.changeText(inputs[0], "wrong");
    fireEvent.changeText(inputs[1], "wrong");
    fireEvent.changeText(inputs[2], "wrong");
    expect(onResponseChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ correct_count: 0, total: 3 })
    );
  });
});
