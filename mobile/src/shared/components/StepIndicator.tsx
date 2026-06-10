import React from "react";
import { StyleSheet, View } from "react-native";

interface Props {
  current: number;
  total: number;
}

export default function StepIndicator({ current, total }: Props) {
  return (
    <View style={styles.container}>
      {Array.from({ length: total }).map((_, index) => (
        <View
          key={index}
          style={[
            styles.dot,
            index < current && styles.activeDot,
            index === current && styles.currentDot,
          ]}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 8,
    paddingVertical: 16,
  },
  dot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: "#ddd",
  },
  activeDot: {
    backgroundColor: "#007AFF",
  },
  currentDot: {
    backgroundColor: "#007AFF",
    width: 12,
    height: 12,
    borderRadius: 6,
  },
});
