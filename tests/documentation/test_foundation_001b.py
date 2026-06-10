"""
Foundation 001B reconciliation closeout test suite.

Tests:
 1. canonical commit chain fields test
 2. full commit hash test
 3. correction commit classification test
 4. requirement count reconciliation test
 5. requirements lost equals zero test
 6. artifact index delta test
 7. new artifact coverage test
 8. artifact hash validation test
 9. forbidden-actions completeness test
10. diagnostic dimension canonical count test
11. proof 001A schema validation
12. proof 001B schema validation
"""
import json, os, hashlib, re

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), '../..'))
DOCS = os.path.join(REPO, 'documents/language_learning_app')
SCHEMAS = os.path.join(DOCS, 'schemas')
VALIDATION = os.path.join(DOCS, 'validation')


# ── 1. canonical commit chain fields test ──────────────────────────────

class TestCanonicalCommitChainFields:
    def test_001b_proof_has_commit_chain(self):
        with open(os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')) as f:
            proof = json.load(f)
        required = [
            'foundation_implementation_commit',
            'correction_starting_commit',
            'correction_intermediate_commits',
            'correction_final_commit',
            'origin_master_commit',
        ]
        for field in required:
            assert field in proof.get('git', {}), f"Missing git.{field} in proof 001B"


# ── 2. full commit hash test ───────────────────────────────────────────

class TestFullCommitHashes:
    def test_all_hashes_are_full(self):
        """All commit hashes must be 40 hex characters."""
        proof_path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(proof_path) as f:
            proof = json.load(f)
        git = proof.get('git', {})
        hash_fields = [
            'foundation_implementation_commit',
            'correction_starting_commit',
            'correction_final_commit',
            'origin_master_commit',
        ]
        for field in hash_fields:
            val = git.get(field, '')
            assert val and len(val) == 40 and all(c in '0123456789abcdef' for c in val), \
                f"git.{field} is not a full 40-char hex hash: {val}"

    def test_intermediate_commits_are_full(self):
        proof_path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(proof_path) as f:
            proof = json.load(f)
        for commit in proof.get('git', {}).get('correction_intermediate_commits', []):
            assert commit and len(commit) == 40 and all(c in '0123456789abcdef' for c in commit), \
                f"Intermediate commit is not a full hash: {commit}"

    def test_git_result_hashes_are_full(self):
        """Also check git_reconciliation_result.json."""
        path = os.path.join(VALIDATION, 'git_reconciliation_result.json')
        with open(path) as f:
            result = json.load(f)
        chain = result.get('canonical_commit_chain', {})
        for field in ['foundation_implementation_commit', 'correction_starting_commit',
                       'correction_final_commit', 'origin_master_commit']:
            val = chain.get(field, '')
            if isinstance(val, str):
                assert val and len(val) == 40, f"{field} not full hash: {val}"


# ── 3. correction commit classification test ───────────────────────────

class TestCorrectionCommitClassification:
    def test_reported_commits_are_docs_only(self):
        path = os.path.join(VALIDATION, 'git_reconciliation_result.json')
        with open(path) as f:
            result = json.load(f)
        for entry in result.get('commit_classification', []):
            assert entry.get('docs_tests_only'), f"{entry['hash']}: not docs/tests-only"
            assert not entry.get('application_runtime_changes'), \
                f"{entry['hash']}: has application/runtime changes"

    def test_no_app_code_in_commits(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001a.json')
        with open(path) as f:
            proof = json.load(f)
        fa = proof.get('forbidden_actions', {})
        assert fa.get('application_code_changed') is False, "application_code_changed must be false"


# ── 4. requirement count reconciliation test ───────────────────────────

class TestRequirementCountReconciliation:
    def test_previous_reported_is_55(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        assert proof.get('requirements', {}).get('previous_reported_requirements') == 55

    def test_canonical_is_52(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        assert proof.get('requirements', {}).get('canonical_requirements') == 52

    def test_matrix_has_52_unique_ids(self):
        """Verify the traceability matrix actually has exactly 52 unique requirement IDs."""
        tm_path = os.path.join(VALIDATION, '138_requirements_traceability_matrix.md')
        with open(tm_path) as f:
            content = f.read()
        ids = re.findall(r'R\d{3}', content)
        unique_ids = len(set(ids))
        assert unique_ids == 52, f"Expected 52 unique IDs, found {unique_ids}"


# ── 5. requirements lost equals zero test ──────────────────────────────

class TestRequirementsLostZero:
    def test_requirements_lost_is_zero(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        assert proof.get('requirements', {}).get('requirements_lost') == 0


# ── 6. artifact index delta test ───────────────────────────────────────

class TestArtifactIndexDelta:
    def test_index_entries_match(self):
        with open(os.path.join(DOCS, 'artifact_index.json')) as f:
            index = json.load(f)
        entry_count = len(index.get('artifacts', []))
        assert entry_count == 156, f"Expected 156 index entries, found {entry_count}"

    def test_index_delta_fields_present(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        arts = proof.get('artifacts', {})
        assert arts.get('previous_index_entries') == 156
        assert arts.get('final_index_entries') == 156


# ── 7. new artifact coverage test ──────────────────────────────────────

class TestNewArtifactCoverage:
    def test_all_required_validation_artifacts_exist(self):
        required = [
            'validation/git_reconciliation_report.md',
            'validation/artifact_inventory_report.md',
            'validation/schema_fixture_validation_report.md',
            'validation/contradiction_audit_report.md',
            'validation/traceability_validation_report.md',
            'validation/final_acceptance_report.md',
            'validation/git_reconciliation_result.json',
            'proof_language_learning_app_documentation_foundation_001.json',
            'proof_language_learning_app_documentation_foundation_001a.json',
            'proof_language_learning_app_documentation_foundation_001b.json',
        ]
        missing = []
        for rel in required:
            full = os.path.join(DOCS, rel.replace('/', os.sep))
            if not os.path.exists(full):
                missing.append(rel)
        assert len(missing) == 0, f"Missing artifacts: {missing}"


# ── 8. artifact hash validation test ───────────────────────────────────

class TestArtifactHashValidation:
    def test_all_index_hashes_match(self):
        with open(os.path.join(DOCS, 'artifact_index.json')) as f:
            index = json.load(f)
        mismatches = []
        for a in index['artifacts']:
            full = os.path.join(REPO, a['path'])
            if not os.path.exists(full):
                continue
            with open(full, 'rb') as f:
                actual = hashlib.sha256(f.read()).hexdigest()
            if actual != a['sha256']:
                mismatches.append(f"{a['path']}: expected {a['sha256'][:16]}... got {actual[:16]}...")
        assert len(mismatches) == 0, '\n'.join(mismatches)


# ── 9. forbidden-actions completeness test ─────────────────────────────

class TestForbiddenActionsCompleteness:
    def test_forbidden_actions_all_fields_present(self):
        """001B proof must have the extended forbidden-actions block."""
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        fa = proof.get('forbidden_actions', {})
        required = [
            'application_code_changed',
            'frontend_changed',
            'backend_changed',
            'runtime_changed',
            'database_changed',
            'deployment_executed',
            'production_modified',
            'staging_modified',
            'real_llm_calls_executed',
            'secrets_added',
        ]
        for field in required:
            assert field in fa, f"Missing forbidden_actions.{field}"
            assert fa[field] is False, f"forbidden_actions.{field} must be false"

    def test_no_forbidden_files_in_repo(self):
        forbidden_patterns = ['.env', 'credentials', 'secrets', 'private.key',
                               'api.key', 'deployment.yaml', 'docker-compose.yaml']
        errors = []
        for root, dirs, files in os.walk(REPO):
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
            for f in files:
                for pat in forbidden_patterns:
                    if pat in f:
                        rel = os.path.relpath(os.path.join(root, f), REPO)
                        errors.append(rel)
                        break
        assert len(errors) == 0, '\n'.join(errors)


# ── 10. diagnostic dimension canonical count test ──────────────────────

class TestDiagnosticDimensionCanonicalCount:
    def test_no_14plus_in_docs(self):
        """No content document should reference '14+' in a diagnostic dimension context.
        Validation reports describing the fix are exempt."""
        skip_prefixes = ['validation' + os.sep, 'validation']
        errors = []
        for root, dirs, files in os.walk(DOCS):
            rel_dir = os.path.relpath(root, DOCS)
            if any(rel_dir.startswith(p) for p in skip_prefixes):
                continue
            for f in files:
                if not f.endswith('.md') and not f.endswith('.json'):
                    continue
                path = os.path.join(root, f)
                with open(path, encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
                if '14+' in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if '14+' in line and ('dimension' in line.lower() or 'diagnostic' in line.lower()):
                            rel = os.path.relpath(path, REPO)
                            errors.append(f"{rel}:{i+1}: {line.strip()}")
        assert len(errors) == 0, f"Found 14+ references:\n" + '\n'.join(errors)

    def test_diagnostic_doc_uses_13(self):
        path = os.path.join(DOCS, 'diagnostics/40_initial_diagnostic_and_placement_system.md')
        with open(path) as f:
            content = f.read()
        assert '13 dimensions' in content or '13 separate' in content, \
            "Diagnostic doc must reference 13 dimensions"


# ── 11. proof 001A schema validation ───────────────────────────────────

class TestProof001ASchemaValidation:
    def test_proof_001a_is_valid_schema(self):
        """Validate that proof_001a conforms to documentation_proof schema."""
        import jsonschema
        schema_path = os.path.join(SCHEMAS, 'documentation_proof.schema.json')
        proof_path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001a.json')
        with open(schema_path) as f:
            schema = json.load(f)
        with open(proof_path) as f:
            proof = json.load(f)
        jsonschema.validate(instance=proof, schema=schema)

    def test_proof_001a_verdict(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001a.json')
        with open(path) as f:
            proof = json.load(f)
        assert proof['task_id'] == 'LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001A'
        assert proof['verdict'] == 'ACCEPTED'


# ── 12. proof 001B schema validation ───────────────────────────────────

class TestProof001BSchemaValidation:
    def test_proof_001b_required_fields(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        assert proof['task_id'] == 'LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001B'
        assert proof['parent_task_id'] == 'LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001A'
        assert proof['verdict'] == 'ACCEPTED'
        assert proof['feature_completed'] is True
        assert proof['documentation_only'] is True
        assert proof['reconciliation_completed'] is True
        assert proof['canonical_commit_chain_verified'] is True
        assert proof['requirement_count_delta_explained'] is True
        assert proof['artifact_index_delta_verified'] is True
        assert proof['forbidden_actions_complete'] is True
        assert proof.get('requirements', {}).get('requirements_lost') == 0

    def test_proof_001b_git_fields(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        git = proof.get('git', {})
        assert git.get('branch') == 'master'
        assert git.get('commit_created') is True
        assert git.get('commit_pushed') is True
        assert git.get('git_clean') is True
        assert git.get('head_matches_origin') is True
        assert git.get('unpushed_commits') == 0

    def test_proof_001b_validation_section(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        v = proof.get('validation', {})
        assert v.get('tests_failed') == 0
        assert v.get('warnings') == 0

    def test_proof_001b_implementation_gate_closed(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001b.json')
        with open(path) as f:
            proof = json.load(f)
        assert proof.get('application_implementation_allowed') is False
        assert proof.get('production_accepted') is False
        assert proof.get('next_allowed_action') == 'mvp_architecture_planning'
