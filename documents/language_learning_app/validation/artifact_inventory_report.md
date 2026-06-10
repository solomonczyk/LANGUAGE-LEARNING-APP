# Artifact Inventory Report

**Task:** LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001A  
**Date:** 2026-06-10  
**Status:** COMPLETED

---

## 1. File Counts by Type

| Artifact Type | Count |
|---------------|-------|
| Markdown documents | 105 |
| JSON Schemas | 23 |
| Schema fixtures | 22 |
| End-to-end examples | 5 |
| Diagram files | 1 |
| Validation scripts | 6 |
| Test files | 1 |
| Proof JSON | 1 |
| Artifact index | 1 |
| **Total artifact index entries** | **156** |

## 2. Artifact Index Verification

| Check | Result |
|-------|--------|
| All entries point to existing files | PASS |
| SHA256 matches file content | PASS |
| No missing files | PASS |
| No orphan schema entries | PASS |
| No orphan fixture entries | PASS |

## 3. Correction Applied

- Updated 19 SHA256 values in artifact_index.json (after fixing documents and fixtures)

## 4. Separate Counts

Note: Previous report incorrectly used `example_count: 22` which conflated:
- **Schema fixtures:** 22 (each JSON Schema has one corresponding fixture)
- **End-to-end examples:** 5 (Markdown narrative examples)
- **Total example files:** 27

These are now tracked as separate fields.
