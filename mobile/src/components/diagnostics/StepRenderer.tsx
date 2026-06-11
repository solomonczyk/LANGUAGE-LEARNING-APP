import React from "react";
import { Text, View } from "react-native";
import type { DiagnosticItemProps } from "./types";
import ReadingComprehensionItem from "./ReadingComprehensionItem";
import ListeningFallbackItem from "./ListeningFallbackItem";
import VisualComprehensionItem from "./VisualComprehensionItem";
import ProductiveGrammarItem from "./ProductiveGrammarItem";
import MediationItem from "./MediationItem";
import ConfidenceAnxietyItem from "./ConfidenceAnxietyItem";

interface StepRendererProps extends DiagnosticItemProps {
  stepKey: string;
}

export default function StepRenderer({ stepKey, ...props }: StepRendererProps) {
  switch (stepKey) {
    case "reading_comprehension":
      return <ReadingComprehensionItem {...props} />;
    case "listening_fallback":
      return <ListeningFallbackItem {...props} />;
    case "visual_comprehension":
      return <VisualComprehensionItem {...props} />;
    case "productive_grammar":
      return <ProductiveGrammarItem {...props} />;
    case "mediation":
      return <MediationItem {...props} />;
    case "confidence_anxiety":
      return <ConfidenceAnxietyItem {...props} />;
    default:
      // For existing items (grammar, vocab, writing, narrative), return null
      // as they are rendered inline in diagnostic.tsx
      return <View />;
  }
}
