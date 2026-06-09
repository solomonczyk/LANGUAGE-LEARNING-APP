#!/usr/bin/env python3
"""Generate methodology documents from doc_data.json."""
import json, os

BASE = "f:/Dev/Projects/LANGUAGE-LEARNING-APP/documents/language_learning_app"

with open("scripts/doc_data.json", encoding="utf-8") as f:
    data = json.load(f)

TMPL = """# {title}

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

{purpose}

## In scope

- Pedagogical framework definition and theoretical foundations
- Curriculum structure and progression design
- Assessment and competence model specifications
- Learning strategy and learner autonomy frameworks

## Out of scope

- Detailed lesson plans
- Specific curriculum item specifications
- Assessment rubric details
- Tutor training materials

## Core decisions

1. Methodology is grounded in established SLA research (Krashen, Swain, Long, Ellis, Vygotsky)
2. Task-Based Language Teaching is the core instructional approach
3. Personal narrative is the primary content source
4. CEFR 2020 is the reference framework including mediation and plurilingualism

## Acceptance criteria

1. Methodology is clearly articulated and internally consistent
2. Research foundations are cited appropriately
3. Methodology directly informs product design decisions
4. All recommendations are actionable for implementation

---

{content}
"""

for filename, doc in data["methodology"].items():
    path = os.path.join(BASE, "methodology", filename)
    text = TMPL.format(title=doc["title"], purpose=doc["purpose"], content=doc["content"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Created: methodology/{filename}")

print("Methodology documents complete!")
