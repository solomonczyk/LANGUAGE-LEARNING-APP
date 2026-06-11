"""
Full alpha session executor — runs the complete learner flow for each synthetic tester.
"""
import httpx
import uuid
import json
import time

BASE = "http://localhost:8000/api/v1"
SEED_LESSON_ID = "00000000-0000-0000-0000-000000000010"
ALL_PASSED = True
RESULTS = {}


def uid():
    return str(uuid.uuid4())[:8]


def log_result(tester_id, step, status, detail=""):
    marker = "PASS" if status else "FAIL"
    print(f"  [{marker}] {tester_id} | {step} | {detail}")
    return {"tester_id": tester_id, "step": step, "status": status, "detail": detail}


def run_tester(tester_id, profile):
    """Run the full learner flow for one synthetic tester."""
    global ALL_PASSED
    user_id = None
    my_results = []

    # 1. Health check
    try:
        r = httpx.get(f"{BASE}/health", timeout=10)
        ok = r.status_code == 200 and r.json().get("status") == "ok"
        my_results.append(log_result(tester_id, "health_check", ok, f"status={r.status_code}"))
        if not ok:
            ALL_PASSED = False
            return my_results
    except Exception as e:
        my_results.append(log_result(tester_id, "health_check", False, str(e)))
        ALL_PASSED = False
        return my_results

    # 2. Register the tester
    uname = f"alpha_{tester_id.lower()}_{uid()}"
    try:
        r = httpx.post(f"{BASE}/identity/register", json={
            "username": uname,
            "display_name": f"Alpha {tester_id}",
            "email": f"{uname}@alpha.test"
        }, timeout=10)
        ok = r.status_code == 200
        if ok:
            user_id = r.json()["id"]
        my_results.append(log_result(tester_id, "register", ok, f"user_id={user_id}"))
    except Exception as e:
        my_results.append(log_result(tester_id, "register", False, str(e)))
        ALL_PASSED = False
        return my_results

    headers = {"X-User-Id": user_id} if user_id else {}

    # 3. Create learner profile
    try:
        r = httpx.post(f"{BASE}/learner-profile", json={
            "target_language": profile["target_language"],
            "native_language": profile["native_language"],
            "learning_goal": profile["learning_goal"],
            "preferred_lesson_duration": profile.get("preferred_duration", 10),
            "self_reported_level": profile["self_reported_level"]
        }, headers=headers, timeout=10)
        ok = r.status_code == 200
        my_results.append(log_result(tester_id, "create_profile", ok,
                                     f"lang={profile['target_language']} level={profile['self_reported_level']}"))
    except Exception as e:
        my_results.append(log_result(tester_id, "create_profile", False, str(e)))
        ALL_PASSED = False
        return my_results

    # 4. Create diagnostic session
    try:
        r = httpx.post(f"{BASE}/diagnostics/sessions", headers=headers, timeout=10)
        ok = r.status_code == 200
        if ok:
            diag_session_id = r.json()["session_id"]
            assert r.json()["status"] == "IN_PROGRESS"
            assert r.json()["total_steps"] == 4
        my_results.append(log_result(tester_id, "diagnostic_create", ok))
    except Exception as e:
        my_results.append(log_result(tester_id, "diagnostic_create", False, str(e)))
        ALL_PASSED = False
        return my_results

    # 5. Submit diagnostic responses
    diag_responses_ok = True
    responses = [
        {"question_key": "grammar_recognition", "response_data": {"is_correct": True}},
        {"question_key": "active_vocabulary", "response_data": {"correct_count": 4, "total_words": 5}},
        {"question_key": "written_production",
         "response_data": {"word_count": 30, "has_structure": True,
                           "text": profile.get("diagnostic_text",
                                               "This morning I woke up early and had breakfast with my family.")}},
        {"question_key": "narrative_coherence", "response_data": {"correct_order": True}},
    ]
    for resp in responses:
        try:
            r = httpx.post(f"{BASE}/diagnostics/sessions/{diag_session_id}/responses",
                           json=resp, headers=headers, timeout=10)
            step_ok = r.status_code == 200
            if not step_ok:
                diag_responses_ok = False
            my_results.append(log_result(tester_id, f"diagnostic_response_{resp['question_key']}", step_ok))
        except Exception as e:
            my_results.append(log_result(tester_id, f"diagnostic_response_{resp['question_key']}", False, str(e)))
            diag_responses_ok = False

    # 6. Complete diagnostic
    try:
        r = httpx.post(f"{BASE}/diagnostics/sessions/{diag_session_id}/complete",
                       headers=headers, timeout=10)
        ok = r.status_code == 200 and r.json()["status"] == "COMPLETED"
        assessments = r.json().get("assessments", [])
        my_results.append(log_result(tester_id, "diagnostic_complete", ok,
                                     f"{len(assessments)} assessments"))
    except Exception as e:
        my_results.append(log_result(tester_id, "diagnostic_complete", False, str(e)))
        ALL_PASSED = False
        return my_results

    if not diag_responses_ok:
        ALL_PASSED = False

    # 7. Learning contract
    try:
        r = httpx.get(f"{BASE}/learning-contract/current", headers=headers, timeout=10)
        if r.status_code == 404:
            # Create it
            r = httpx.post(f"{BASE}/learning-contract/current", headers=headers, timeout=10)
            ok = r.status_code == 200
            if ok:
                contract = r.json()
                assert "target_language" in contract
                my_results.append(log_result(tester_id, "learning_contract_create", True,
                                             f"lang={contract.get('target_language')} version={contract.get('version')}"))
            else:
                my_results.append(log_result(tester_id, "learning_contract_create", False, r.text))
        elif r.status_code == 200:
            contract = r.json()
            my_results.append(log_result(tester_id, "learning_contract_get", True,
                                         f"lang={contract.get('target_language')} version={contract.get('version')}"))
        else:
            my_results.append(log_result(tester_id, "learning_contract_get", False, r.text))
    except Exception as e:
        my_results.append(log_result(tester_id, "learning_contract", False, str(e)))
        ALL_PASSED = False
        return my_results

    # 8. Home / Mastery profile
    try:
        r = httpx.get(f"{BASE}/mastery/profile", headers=headers, timeout=10)
        ok = r.status_code == 200
        my_results.append(log_result(tester_id, "mastery_profile", ok))
    except Exception as e:
        my_results.append(log_result(tester_id, "mastery_profile", False, str(e)))

    # 9. Create lesson session
    try:
        r = httpx.post(f"{BASE}/lesson-sessions", json={
            "lesson_definition_id": SEED_LESSON_ID
        }, headers=headers, timeout=10)
        ok = r.status_code == 200
        if ok:
            session_id = r.json()["session_id"]
        my_results.append(log_result(tester_id, "lesson_create", ok, f"session_id={session_id}"))
    except Exception as e:
        my_results.append(log_result(tester_id, "lesson_create", False, str(e)))
        ALL_PASSED = False
        return my_results

    # 10. Submit text
    text = profile.get("submission_text",
                       "This morning I wake up early and take my dog for a walk. It is a beautiful day.")
    try:
        r = httpx.post(f"{BASE}/lesson-sessions/{session_id}/submissions", json={
            "text": text
        }, headers=headers, timeout=10)
        ok = r.status_code == 200 and r.json()["status"] == "RECEIVED"
        submission_id = r.json().get("submission_id") if ok else None
        my_results.append(log_result(tester_id, "lesson_submit", ok, f"submission_id={submission_id}"))
    except Exception as e:
        my_results.append(log_result(tester_id, "lesson_submit", False, str(e)))
        ALL_PASSED = False
        return my_results

    # 11. Process lesson
    try:
        r = httpx.post(f"{BASE}/lesson-sessions/{session_id}/process",
                       headers=headers, timeout=30)
        ok = r.status_code == 200 and r.json()["status"] == "COMPLETED"
        process_data = r.json()
        has_validation = "validation_results" in process_data or "validations" in process_data
        decision = process_data.get("decision", "N/A")
        my_results.append(log_result(tester_id, "lesson_process", ok,
                                     f"decision={decision} has_validation={has_validation}"))
    except Exception as e:
        my_results.append(log_result(tester_id, "lesson_process", False, str(e)))
        ALL_PASSED = False
        return my_results

    # 12. Get result
    try:
        r = httpx.get(f"{BASE}/lesson-sessions/{session_id}", headers=headers, timeout=10)
        ok = r.status_code == 200 and r.json().get("status") == "COMPLETED"
        my_results.append(log_result(tester_id, "lesson_result", ok))
    except Exception as e:
        my_results.append(log_result(tester_id, "lesson_result", False, str(e)))

    # 13. Verify mastery records exist
    try:
        r = httpx.get(f"{BASE}/mastery/profile", headers=headers, timeout=10)
        ok = r.status_code == 200
        records = r.json().get("records", [])
        my_results.append(log_result(tester_id, "mastery_after_lesson", ok,
                                     f"records={len(records)}"))
    except Exception as e:
        my_results.append(log_result(tester_id, "mastery_after_lesson", False, str(e)))

    # 14. Verify audit events
    try:
        op_headers = {"X-User-Id": "00000000-0000-0000-0000-000000000002"}
        r = httpx.get(f"{BASE}/operator/audit-events", headers=op_headers, timeout=10)
        ok = r.status_code == 200
        if ok:
            events = r.json()
            if isinstance(events, dict):
                events_list = events.get("items", [])
            else:
                events_list = events
            my_results.append(log_result(tester_id, "audit_events", ok,
                                         f"total_events={len(events_list)}"))
        else:
            my_results.append(log_result(tester_id, "audit_events", ok, f"status={r.status_code}"))
    except Exception as e:
        my_results.append(log_result(tester_id, "audit_events", False, str(e)))

    return my_results


# Define tester profiles
TESTERS = [
    {
        "tester_id": "ALPHA-001",
        "profile_type": "returning_learner",
        "target_language": "English",
        "native_language": "Synthetic",
        "learning_goal": "B1 conversational fluency",
        "self_reported_level": "A2",
        "preferred_duration": 15,
        "diagnostic_text": "This morning I woke up, brushed my teeth, had breakfast, and walked my dog in the park. Then I went to work and had meetings.",
        "submission_text": "Yesterday I walked my cat through the garden. The weather was nice and sunny. My cat wanted to play but I was late for work."
    },
    {
        "tester_id": "ALPHA-002",
        "profile_type": "beginner",
        "target_language": "English",
        "native_language": "Synthetic",
        "learning_goal": "Basic conversation",
        "self_reported_level": "A1",
        "preferred_duration": 10,
        "diagnostic_text": "I wake up. I eat breakfast. I go to work.",
        "submission_text": "This morning I wake up and eat breakfast. My cat eat too. Then I go to work."
    },
    {
        "tester_id": "ALPHA-003",
        "profile_type": "work_focused",
        "target_language": "English",
        "native_language": "Synthetic",
        "learning_goal": "Work",
        "self_reported_level": "B1",
        "preferred_duration": 20,
        "diagnostic_text": "Every morning I check my email, plan my tasks, and start working on the most important project first. I use time management to stay productive.",
        "submission_text": "This morning I checked my emails and prepared a presentation for my team. We discussed the quarterly targets and assigned action items."
    },
    {
        "tester_id": "ALPHA-004",
        "profile_type": "low_confidence",
        "target_language": "English",
        "native_language": "Synthetic",
        "learning_goal": "Study",
        "self_reported_level": "A1",
        "preferred_duration": 10,
        "diagnostic_text": "hello my name is test. I like to learn english. It is good for me.",
        "submission_text": "I wake up in morning. My dog is happy. We go to park."
    },
    {
        "tester_id": "ALPHA-005",
        "profile_type": "returning_learner_advanced",
        "target_language": "English",
        "native_language": "Synthetic",
        "learning_goal": "Study",
        "self_reported_level": "B2",
        "preferred_duration": 20,
        "diagnostic_text": "Every morning I follow a consistent routine: I wake up at 6 AM, do a 20-minute meditation session, and then prepare a healthy breakfast. I find that starting the day with structure helps maintain productivity.",
        "submission_text": "This morning I woke up at sunrise and went for a run along the river. The fresh air and quiet atmosphere helped me clear my mind before starting work."
    }
]

# Run all testers
print("=" * 70)
print("ALPHA 005 - CLOSED LEARNER ALPHA EXECUTION")
print("=" * 70)

all_results = {}
all_passed_steps = 0
all_total_steps = 0

for tester in TESTERS:
    tid = tester["tester_id"]
    print(f"\n{'-' * 70}")
    print(f"RUNNING: {tid} ({tester['profile_type']})")
    print(f"{'-' * 70}")

    results = run_tester(tid, tester)
    all_results[tid] = results

    step_ok = sum(1 for r in results if r["status"])
    step_total = len(results)
    all_passed_steps += step_ok
    all_total_steps += step_total

    print(f"\n  {tid} RESULT: {step_ok}/{step_total} steps passed")
    if not all(r["status"] for r in results):
        failed = [r for r in results if not r["status"]]
        print(f"  FAILURES ({len(failed)}):")
        for f in failed:
            print(f"    - {f['step']}: {f['detail']}")

print(f"\n{'=' * 70}")
print(f"OVERALL: {all_passed_steps}/{all_total_steps} steps passed across {len(TESTERS)} testers")
all_tester_ok = all(
    all(r["status"] for r in results)
    for results in all_results.values()
)
print(f"ALL TESTERS COMPLETED: {all_tester_ok}")
print(f"{'=' * 70}")

# Save raw results
out_path = "documents/language_learning_app/implementation/alpha_005/evidence/operator_notes/raw_session_results.json"
with open(out_path, "w") as f:
    json.dump(all_results, f, indent=2, default=str)

print(f"\nRaw results saved to {out_path}")
