# 02 — Root Cause Analysis

## Methodology

Static code analysis of the onboarding screen (`mobile/app/onboarding.tsx`), state model (`mobile/src/state/appState.ts`), and comparison with the diagnostic screen (`mobile/app/diagnostic.tsx`) which handles the same chip-selection pattern correctly.

## Root Cause: Primary

### #1: TouchableChip uses `<Text onPress>` instead of `<Pressable>`

**File:** `mobile/app/onboarding.tsx` (original, lines 224-244)

```typescript
function TouchableChip({ label, selected, onPress, wide }) {
  return (
    <View style={wide ? styles.chipWide : undefined}>
      <Text style={[styles.chip, selected && styles.chipSelected]} onPress={onPress}>
        {label}
      </Text>
    </View>
  );
}
```

The `TouchableChip` component relied on `<Text onPress={onPress}>` for touch handling. In React Native, while `<Text onPress>` is documented, it has known reliability issues:

1. **Touch event propagation**: The wrapping `<View>` (even with no explicit touch handler) can interfere with touch event propagation on certain React Native versions and platforms. Taps may not reach the `<Text>` element reliably.

2. **No press feedback**: `<Text onPress>` does not provide any visual press feedback (no highlight, no opacity change, no ripple on Android). The user cannot tell if their tap was registered.

3. **ScrollView interference**: The `keyboardShouldPersistTaps="handled"` prop on the ScrollView interacts poorly with nested `<Text onPress>` inside `<View>` wrappers in some configurations.

### Evidence: Diagnostic Screen Uses Pressable

The diagnostic screen (`mobile/app/diagnostic.tsx`) uses `<Pressable>` for all interactive chip/option elements:

```tsx
<Pressable key={opt.id} style={optStyle} onPress={() => ...}>
  ...
</Pressable>
```

This pattern works correctly in the same codebase. The inconsistency between onboarding (using `<Text onPress>`) and diagnostic (using `<Pressable>`) confirms `<Pressable>` is the correct, reliable approach.

## Root Cause: Secondary

### #2: No visible selected state feedback

The selected chip style only changes color subtly:

```typescript
chipSelected: {
  backgroundColor: "#E8F0FE",
  color: "#007AFF",
  borderColor: "#007AFF",
}
```

When the state doesn't update due to the touch issue, there's no visual feedback to tell the user whether their selection registered.

### #4: No validation feedback

When the Continue button is disabled, there is no UI text explaining what fields are required. The user sees a disabled button with no context.

## Root Cause Conclusion

**Primary root cause #1** — TouchableChip using `<Text onPress>` instead of `<Pressable>` — is the direct cause of Continue remaining disabled. Touch events on the learning goal chips do not reliably propagate, so the Zustand store's `learningGoal` field is never updated, and `canProceed()` correctly returns `false`.

**Secondary issues #2 and #4** exacerbate the problem by providing no visual feedback, making it impossible for the user to diagnose what's happening.

## Candidate Analysis

| Candidate | Relevant? | Verdict |
|-----------|-----------|---------|
| #1: learning goal card click not updating state | ✅ Yes | Primary cause — `<Text onPress>` unreliable |
| #2: selected goal not visually highlighted | ✅ Yes | Compounding — no feedback when selection fails |
| #3: custom goal field required incorrectly | ❌ No | Custom field is optional |
| #4: duration selected but not persisted | ❌ No | Duration defaults to 10, always truthy |
| #5: validation checks wrong field name | ❌ No | Field name `learningGoal` matches store |
| #6: onboarding step index/state mismatch | ❌ No | Step 3 = index 2, correctly mapped |
| #7: stale Zustand/local state | ❌ No | Zustand correctly triggers re-render on update |
| #8: form schema mismatch with backend payload | ❌ No | Payload fields match backend expectations |
