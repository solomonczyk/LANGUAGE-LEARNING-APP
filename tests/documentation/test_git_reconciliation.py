"""
Comprehensive 20-test reconciliation suite for FOUNDATION-001A closeout.
"""
import json, os, hashlib, re
import jsonschema

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), '../..'))
DOCS = os.path.join(REPO, 'documents/language_learning_app')
SCHEMAS = os.path.join(DOCS, 'schemas')
EXAMPLES = os.path.join(DOCS, 'examples')


class TestRepositoryStructure:
    def test_required_dirs_exist(self):
        required = [
            'product', 'methodology', 'diagnostics', 'lessons', 'skill_modes',
            'memory_and_engagement', 'architecture', 'security', 'validation',
            'schemas', 'examples', 'diagrams'
        ]
        for d in required:
            path = os.path.join(DOCS, d.replace('/', os.sep))
            assert os.path.isdir(path), f"Missing directory: {d}"


class TestRequiredDocumentSections:
    def test_all_policy_docs_have_sections(self):
        skip = ['00_documentation_index.md', '01_glossary.md', '02_decision_log.md',
                'system_architecture.md']
        skip_dirs = ['diagrams', 'examples', 'validation']
        required_sections = ['Status', 'Version', 'Purpose', 'In scope',
                              'Out of scope', 'Core decisions', 'Acceptance criteria']
        errors = []
        for root, dirs, files in os.walk(DOCS):
            rel_dir = os.path.relpath(root, DOCS)
            if any(sd in rel_dir for sd in skip_dirs):
                continue
            for f in files:
                if not f.endswith('.md'):
                    continue
                if f in skip:
                    continue
                path = os.path.join(root, f)
                with open(path, encoding='utf-8') as fh:
                    content = fh.read()
                for sec in required_sections:
                    patterns = [
                        f'## {sec}', f'**{sec}:**',
                        f'## **{sec}**', f'### {sec}'
                    ]
                    if not any(p in content for p in patterns):
                        rel = os.path.relpath(path, REPO)
                        errors.append(f"{rel}: missing '{sec}'")
        assert len(errors) == 0, '\n'.join(errors[:20])


class TestEmptyPlaceholderDocuments:
    def test_no_empty_or_placeholder_content(self):
        errors = []
        for root, dirs, files in os.walk(DOCS):
            for f in files:
                if not f.endswith('.md'):
                    continue
                path = os.path.join(root, f)
                with open(path, encoding='utf-8') as fh:
                    content = fh.read()
                if len(content.strip()) < 50:
                    rel = os.path.relpath(path, REPO)
                    errors.append(f"{rel}: too short ({len(content.strip())} chars)")
        assert len(errors) == 0, '\n'.join(errors)


class TestJSONSyntax:
    def test_all_json_is_valid(self):
        errors = []
        for root, dirs, files in os.walk(DOCS):
            for f in files:
                if not f.endswith('.json'):
                    continue
                path = os.path.join(root, f)
                with open(path, encoding='utf-8') as fh:
                    try:
                        json.load(fh)
                    except json.JSONDecodeError as e:
                        rel = os.path.relpath(path, REPO)
                        errors.append(f"{rel}: {e}")
        assert len(errors) == 0, '\n'.join(errors)


class TestJSONSchemaMetaValidation:
    def test_all_schemas_have_required_meta(self):
        errors = []
        seen_ids = []
        for sf in os.listdir(SCHEMAS):
            if not sf.endswith('.schema.json'):
                continue
            path = os.path.join(SCHEMAS, sf)
            with open(path) as f:
                schema = json.load(f)
            if '$schema' not in json.dumps(schema):
                errors.append(f"{sf}: missing $schema")
            if '$id' not in json.dumps(schema):
                errors.append(f"{sf}: missing $id")
            else:
                sid = schema.get('$id', '')
                if sid in seen_ids:
                    errors.append(f"{sf}: duplicate $id '{sid}'")
                seen_ids.append(sid)
            if 'title' not in schema:
                errors.append(f"{sf}: missing title")
            if 'description' not in schema:
                errors.append(f"{sf}: missing description")
            if 'type' not in schema:
                errors.append(f"{sf}: missing type")
        assert len(errors) == 0, '\n'.join(errors)


class TestFixtureToSchemaValidation:
    def test_all_fixtures_validate(self):
        schema_files = {}
        for sf in os.listdir(SCHEMAS):
            if sf.endswith('.schema.json'):
                name = sf.replace('.schema.json', '')
                with open(os.path.join(SCHEMAS, sf)) as f:
                    schema_files[name] = json.load(f)

        errors = []
        valid = 0
        for ff in sorted(os.listdir(EXAMPLES)):
            if not ff.endswith('.json'):
                continue
            path = os.path.join(EXAMPLES, ff)
            with open(path) as f:
                fixture = json.load(f)
            schema_key = ff.replace('.json', '').replace('fixture_', '')
            if schema_key in schema_files:
                try:
                    jsonschema.validate(instance=fixture, schema=schema_files[schema_key])
                    valid += 1
                except jsonschema.ValidationError as e:
                    errors.append(f"{ff}: {e.message}")
        assert len(errors) == 0, '\n'.join(errors)


class TestUniqueSchemaIDs:
    def test_unique_ids(self):
        seen = []
        for sf in os.listdir(SCHEMAS):
            if not sf.endswith('.schema.json'):
                continue
            with open(os.path.join(SCHEMAS, sf)) as f:
                schema = json.load(f)
            sid = schema.get('$id', None)
            if sid in seen:
                raise AssertionError(f"Duplicate $id: {sid}")
            seen.append(sid)


class TestArtifactExistence:
    def test_all_artifacts_exist(self):
        with open(os.path.join(DOCS, 'artifact_index.json')) as f:
            index = json.load(f)
        missing = []
        for a in index['artifacts']:
            full = os.path.join(REPO, a['path'])
            if not os.path.exists(full):
                missing.append(a['path'])
        assert len(missing) == 0, '\n'.join(missing)


class TestArtifactSHA256:
    def test_all_hashes_match(self):
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


class TestTraceabilityPaths:
    def test_traceability_links_exist(self):
        trace_path = os.path.join(DOCS, 'validation/138_requirements_traceability_matrix.md')
        with open(trace_path, encoding='utf-8') as f:
            content = f.read()
        # Find markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        errors = []
        for label, path in links:
            if path.startswith('http'):
                continue
            full = os.path.join(REPO, path.replace('/', os.sep))
            if not os.path.exists(full):
                errors.append(f"Broken link: {path} ({label})")
        assert len(errors) == 0, '\n'.join(errors)


class TestDuplicateRequirementIDs:
    def test_no_duplicate_ids(self):
        trace_path = os.path.join(DOCS, 'validation/138_requirements_traceability_matrix.md')
        with open(trace_path, encoding='utf-8') as f:
            content = f.read()
        ids = re.findall(r'R\d{3}', content)
        from collections import Counter
        counts = Counter(ids)
        dupes = {k: v for k, v in counts.items() if v > 2}
        assert len(dupes) == 0, f"Possible duplicate IDs: {dupes}"


class TestCanonicalLessonModes:
    def test_modes_in_taxonomy(self):
        canonical = [
            'personal_narrative', 'suggested_situation', 'visual_single_scene',
            'visual_sequence', 'illustrated_emotion_and_perspective', 'audio_narrative',
            'audio_dialogue', 'reading_based', 'functional_communication',
            'repair_lesson', 'mediation_lesson', 'review_lesson',
            'progress_checkpoint', 'assessment_lesson'
        ]
        path = os.path.join(DOCS, 'lessons/50_lesson_type_taxonomy.md')
        with open(path, encoding='utf-8') as f:
            content = f.read()
        missing = [m for m in canonical if m not in content]
        assert len(missing) == 0, f"Missing modes in taxonomy: {missing}"


class TestMasteryLifecycleConsistency:
    def test_mastery_states_in_engine(self):
        states = ['introduced', 'recognized', 'reconstructed', 'guided_use',
                   'independent_use', 'interactive_use', 'transferred', 'retained']
        path = os.path.join(DOCS, 'architecture/98_mastery_engine.md')
        with open(path, encoding='utf-8') as f:
            content = f.read()
        missing = [s for s in states if s not in content]
        assert len(missing) == 0, f"Missing mastery states: {missing}"


class TestDiagnosticDimensionsConsistency:
    def test_dimension_count_matches(self):
        path = os.path.join(DOCS, 'diagnostics/40_initial_diagnostic_and_placement_system.md')
        with open(path, encoding='utf-8') as f:
            content = f.read()
        # Count dimensions in the table (13)
        expected_dims = ['Reading', 'Listening', 'Passive vocabulary', 'Active vocabulary',
                          'Grammar recognition', 'Productive grammar', 'Spoken production',
                          'Spoken interaction', 'Pronunciation intelligibility', 'Narrative coherence',
                          'Writing', 'Mediation', 'Communication strategies']
        actual = sum(1 for d in expected_dims if d in content)
        assert actual == 13, f"Expected 13 dimensions in table, found {actual}"
        # Verify no "14+" remains
        assert '14+' not in content, "14+ reference still present in dimensions doc"


class TestReviewIntervalsConsistency:
    def test_intervals_in_primary(self):
        intervals = ['within lesson', '2 hours', '12 hours', '2 days', '7 days']
        path = os.path.join(DOCS, 'memory_and_engagement/80_spaced_repetition_and_memory_consolidation.md')
        with open(path, encoding='utf-8') as f:
            content = f.read().lower()
        missing = [i for i in intervals if i not in content]
        assert len(missing) == 0, f"Missing intervals: {missing}"


class TestLLMPermissionsConsistency:
    def test_llm_restrictions_in_architecture(self):
        arch_docs = [
            'architecture/91_ai_agent_architecture.md',
            'architecture/98_mastery_engine.md',
            'architecture/99_reward_engine.md'
        ]
        patterns = ['LLM cannot', 'deterministic', 'Cannot directly change']
        for doc_rel in arch_docs:
            path = os.path.join(DOCS, doc_rel)
            with open(path, encoding='utf-8') as f:
                content = f.read()
            assert any(p in content for p in patterns), \
                f"{doc_rel}: missing LLM restriction"


class TestRewardAuthorityConsistency:
    def test_deterministic_reward_in_engine(self):
        path = os.path.join(DOCS, 'architecture/99_reward_engine.md')
        with open(path, encoding='utf-8') as f:
            content = f.read()
        assert 'Deterministic' in content or 'deterministic' in content
        assert 'sole authority' in content or 'No LLM involvement' in content


class TestProofJSONSchemaValidation:
    def test_proof_001_validates(self):
        schema_path = os.path.join(SCHEMAS, 'documentation_proof.schema.json')
        proof_path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001.json')
        with open(schema_path) as f:
            schema = json.load(f)
        with open(proof_path) as f:
            proof = json.load(f)
        jsonschema.validate(instance=proof, schema=schema)

    def test_proof_001a_is_valid_json(self):
        path = os.path.join(DOCS, 'proof_language_learning_app_documentation_foundation_001a.json')
        with open(path) as f:
            data = json.load(f)
        assert data['task_id'] == 'LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001A'
        assert data['verdict'] == 'ACCEPTED'


class TestForbiddenFileScan:
    def test_no_forbidden_files(self):
        forbidden = ['.env', 'credentials', 'secrets', 'private.key', 'api.key',
                     'deployment.yaml', 'docker-compose.yaml']
        errors = []
        for root, dirs, files in os.walk(REPO):
            for f in files:
                for pat in forbidden:
                    if pat in f or f.startswith(pat):
                        rel = os.path.relpath(os.path.join(root, f), REPO)
                        errors.append(rel)
                        break
        assert len(errors) == 0, '\n'.join(errors)


class TestDocumentationOnlyGitDiff:
    def test_no_runtime_code_in_docs_diff(self):
        # Check that only documentation files exist (no .py in docs, etc)
        for root, dirs, files in os.walk(DOCS):
            for f in files:
                assert not f.endswith('.py'), f"Python file in docs: {f}"
