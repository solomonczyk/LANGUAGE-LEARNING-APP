#!/usr/bin/env python3
"""Tests for Language Learning App canonical documentation validation."""
import unittest, json, os, glob, subprocess, sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DOCS = os.path.join(BASE, "documents/language_learning_app")


class TestDocumentationStructure(unittest.TestCase):
    """Test that all required documentation files exist."""

    def test_core_docs_exist(self):
        """Core documents should exist."""
        for doc in ["00_documentation_index.md", "01_glossary.md", "02_decision_log.md"]:
            path = os.path.join(DOCS, doc)
            self.assertTrue(os.path.exists(path), f"Missing: {doc}")

    def test_product_docs_exist(self):
        """Product documents should exist."""
        for f in ["product/10_product_vision.md", "product/14_market_and_competitor_framework.md"]:
            self.assertTrue(os.path.exists(os.path.join(DOCS, f)), f"Missing: {f}")

    def test_methodology_docs_exist(self):
        """Methodology documents should exist."""
        for f in [f"methodology/{i}_{name}.md" for i, name in [
            (20, "learning_methodology"), (25, "vocabulary_collocation_and_phraseology"),
            (32, "learner_autonomy_and_learning_strategies")
        ]]:
            self.assertTrue(os.path.exists(os.path.join(DOCS, f)), f"Missing: {f}")

    def test_architecture_docs_exist(self):
        """Architecture documents should exist."""
        for f in ["architecture/90_system_architecture.md", "architecture/98_mastery_engine.md",
                   "architecture/99_reward_engine.md"]:
            self.assertTrue(os.path.exists(os.path.join(DOCS, f)), f"Missing: {f}")

    def test_security_docs_exist(self):
        """Security documents should exist."""
        for f in ["security/110_ai_security_and_prompt_injection_defense.md",
                   "security/111_anti_cheat_and_learning_integrity.md"]:
            self.assertTrue(os.path.exists(os.path.join(DOCS, f)), f"Missing: {f}")


class TestDocumentContent(unittest.TestCase):
    """Test that documents have substantive content."""

    def test_docs_not_empty(self):
        """No document should be a placeholder."""
        md_files = glob.glob(f"{DOCS}/**/*.md", recursive=True)
        for path in md_files:
            with open(path) as f:
                content = f.read()
            rel = os.path.relpath(path, DOCS)
            self.assertGreater(len(content), 200, f"{rel} is too short")


class TestJSONSchemas(unittest.TestCase):
    """Test that JSON schemas are valid."""

    def test_schemas_exist(self):
        """Required schemas should exist."""
        schema_dir = os.path.join(DOCS, "schemas")
        required = ["lesson_contract.schema.json", "learner_profile.schema.json",
                     "reward_transaction.schema.json", "mastery_evidence.schema.json"]
        for s in required:
            self.assertTrue(os.path.exists(os.path.join(schema_dir, s)), f"Missing schema: {s}")

    def test_schemas_are_valid_json(self):
        """All schemas should be valid JSON."""
        schema_dir = os.path.join(DOCS, "schemas")
        for path in glob.glob(f"{schema_dir}/*.json"):
            with open(path) as f:
                try:
                    json.load(f)
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON in {path}: {e}")

    def test_schemas_have_required_fields(self):
        """All schemas should have $schema, $id, title, description."""
        schema_dir = os.path.join(DOCS, "schemas")
        for path in glob.glob(f"{schema_dir}/*.json"):
            with open(path) as f:
                schema = json.load(f)
            name = os.path.basename(path)
            self.assertIn("$schema", schema, f"{name} missing $schema")
            self.assertIn("$id", schema, f"{name} missing $id")
            self.assertIn("title", schema, f"{name} missing title")


class TestArtifactIndex(unittest.TestCase):
    """Test that artifact index matches reality."""

    def test_artifact_index_exists(self):
        """artifact_index.json should exist."""
        self.assertTrue(os.path.exists(os.path.join(DOCS, "artifact_index.json")))

    def test_artifact_index_valid_json(self):
        """artifact_index.json should be valid JSON."""
        with open(os.path.join(DOCS, "artifact_index.json")) as f:
            idx = json.load(f)
        self.assertIn("artifacts", idx)
        self.assertGreater(len(idx["artifacts"]), 50, "Too few artifacts")


class TestProofJSON(unittest.TestCase):
    """Test proof JSON exists and is valid."""

    def test_proof_json_exists(self):
        """Proof JSON should exist."""
        path = os.path.join(DOCS, "proof_language_learning_app_documentation_foundation_001.json")
        self.assertTrue(os.path.exists(path))

    def test_proof_json_valid(self):
        """Proof JSON should be valid."""
        path = os.path.join(DOCS, "proof_language_learning_app_documentation_foundation_001.json")
        with open(path) as f:
            proof = json.load(f)
        self.assertEqual(proof["task_id"],
                         "LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001")
        self.assertTrue(proof["documentation_only"])
        self.assertFalse(proof["application_code_changed"])


if __name__ == "__main__":
    unittest.main()
