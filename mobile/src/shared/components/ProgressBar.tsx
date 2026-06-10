import React from "react";
import { StyleSheet, View, ViewStyle } from "react-native";

interface Props {
  progress: number; // 0.0 to 1.0
  style?: ViewStyle;
}

export default function ProgressBar({ progress, style }: Props) {
  const clamped = Math.min(1, Math.max(0, progress));

  return (
    <View style={[styles.container, style]}>
      <View style={[styles.fill, { width: `${clamped * 100}%` }]} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    height: 6,
    backgroundColor: "#e0e0e0",
    borderRadius: 3,
    overflow: "hidden",
  },
  fill: {
    height: "100%",
    backgroundColor: "#007AFF",
    borderRadius: 3,
  },
});
