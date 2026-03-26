# Workflow — Design and Implementation Stages
# Version: 3.0 | Date: 2026-03-26

---

## 1. Overview

Every product goes through 9 stages. The order is MANDATORY.

```
Stage 1: Concept                            ← you + Claude
    ↓
Stage 2: Architecture                       ← Claude + .claude/agents/skeptic.md
    ↓
Stage 3: Working Design                     ← Claude
    ↓
Stage 4: Module Specifications              ← Claude + .claude/agents/spec-reviewer.md
    ↓
Stage 4.5: Module Preparation               ← python scripts/prepare_module.py (TDD)
    ↓
Stage 5: Implementation (Subagent Pipeline) ← .claude/agents/ + docs/handoffs/
    ↓
Stage 5.5: Automated Acceptance             ← python scripts/quality_gate.py
    ↓
Stage 6: Manual Acceptance (Operator)       ← you verify functionality
    ↓
Stage 7: Executive Documentation            ← Claude updates CLAUDE.md
```

**Exception:** bugfix / minor fix → stage 5 → 5.5 → 6 → 7.

### Operational Tools by Stage

| Stage | Tool | File |
|-------|------|------|
| 2 | Stack verification | .claude/agents/skeptic.md |
| 4 | Spec completeness check | .claude/agents/spec-reviewer.md |
| 4.5 | Preparation: folders + TDD tests | scripts/prepare_module.py |
| 5 | Subagent pipeline | .claude/agents/*.md + docs/handoffs/PROTOCOL.md |
| 5.5 | Quality gate (GO/CONDITIONAL/NO-GO) | scripts/quality_gate.py |
| 5 (pipeline) | QA review by checklist | .claude/agents/qa-reviewer.md |

---

## 2. Stage 1: Concept

**Who:** you (the client) + Claude.
**Input:** product idea.
**Output:** 04_project_idea_template.md + 02_project_brief_template.md (sections A-C).
**Criterion:** you can explain in 2-3 sentences what the product is and how to verify it works.

---

## 3. Stage 2: Architecture

**Who:** Claude (architect) + skeptic.md for verification.
**Input:** concept.
**Output:** module list, dependency diagram, stack choice, implementation stages.
**Criterion:** you understand what blocks the product consists of.

**Stack selection rule:**
1. MANDATORY: 2-3 options with comparison table
2. MANDATORY: recommendation with justification
3. MANDATORY: product-level question to operator (not technical)
4. FORBIDDEN: single option without alternatives
5. After selection: run .claude/agents/skeptic.md

---

## 4. Stage 3: Working Design

**Who:** Claude. You verify compliance with technical requirements (01).
**Input:** architecture.
**Output:** file tree, API contracts, DB schema, project CLAUDE.md, module CLAUDE.md files.
**Criterion:** structure is created, CLAUDE.md files are filled in, ready to start coding.

---

## 5. Stage 4: Module Specifications

**Who:** Claude (architect). You verify the product aspects.
**Input:** working design.
**Output:** docs/specs/spec_[module].md for each module.

**6 mandatory blocks:** User Stories, Data Model, API, Screens, Business Logic, Edge Cases.
**Template:** docs/specs/TEMPLATE.md

**Control:** .claude/agents/spec-reviewer.md checks against a checklist.
A specification with TODO stubs = automatic NEEDS WORK.
**Criterion:** Claude in a new session implements the module without clarifying questions.

---

## 6. Stage 4.5: Module Preparation

**Who:** script `python scripts/prepare_module.py [module] --lang=py|ts|both`.
**Creates:** folders, module CLAUDE.md, handoffs folder, **red TDD tests**.
**--lang:** explicitly specifies test language. Without flag — auto-detect with warning for mixed-stack.
**Tests:** `raise NotImplementedError("Implement from spec: ...")` — the agent MUST make them green.
**Criterion:** tests exist and fail (red).

---

## 7. Stage 5: Implementation (Subagent Pipeline)

**Who:** subagents from .claude/agents/ following the pipeline.
**Protocol:** docs/handoffs/PROTOCOL.md

```
database-architect  → handoff: 01_schema_done.md
        ↓ quality_gate.py --tier=1
backend-engineer    → handoff: 02_api_ready.md
        ↓ quality_gate.py --tier=2
frontend-developer  → handoff: 03_frontend_done.md
        ↓ quality_gate.py --tier=2
qa-reviewer         → handoff: 04_review_report.md
```

**Rules:**
1. Each subagent MUST read previous handoffs before starting
2. Each subagent MUST create their handoff before finishing
3. After each subagent: `python scripts/quality_gate.py --tier=1` or `--tier=2`
4. On NO-GO → STOP, fix, repeat
5. On deviation from spec → update the "Deviations" section in spec

**Skipping steps:** no DB → skip database-architect. No UI → skip frontend-developer.

---

## 8. Stage 5.5: Automated Acceptance (Quality Gate)

**Who:** script `python scripts/quality_gate.py --tier=all --module=[module]`.

```
Tier 1 (Stability): syntax, compilation → PASS/FAIL
Tier 2 (Balance): file/function sizes, secrets, empty catch, tests, .gitignore
    → Hard veto: secrets = automatic NO-GO
    → Majority vote for remaining checks
Tier 3 (Regression): comparison with baseline → WARN if degradation
```

**Verdict:** GO → stage 6. CONDITIONAL → stage 6 with notes. NO-GO → STOP.

---

## 9. Stage 6: Manual Acceptance (Operator)

**Who:** you. Check ONLY functionality.
**Process:** success criteria from the brief (section E.3) → verify each point manually.
**You do NOT check:** security, file sizes, typing, secrets — that was done at stages 5 and 5.5.

**When a gap is found:**
Defect → update spec (Edge Cases) → write test (red) → agent fixes → test green → quality_gate → other tests not broken.

---

## 10. Stage 7: Executive Documentation

**Who:** Claude updates, you verify.
**Output:** updated CLAUDE.md (project + module), README.md, .env.example.
**Criterion:** a new Claude in a clean session reads CLAUDE.md and immediately understands the project.

---

## Feedback Loops

The pipeline is not linear. When problems occur, the process returns to the appropriate stage.

### Spec rejected by spec-reviewer
→ Return to stage 4 (specification)
→ Fix specific points from the report
→ Re-run spec-reviewer (only on fixed points)

### QA-reviewer found CRITICAL issues
→ Identify the source of the problem:
  - DB schema issue → return to database-architect
  - API logic issue → return to backend-engineer
  - UI issue → return to frontend-developer
→ The implementer fixes ONLY the points from the review (does not "improve" code)
→ Re-run QA only on fixed points

### Quality gate NO-GO
→ Tier 1 fail (won't run) → return to last implementer
→ Tier 2 fail (lint/types/sizes) → implementer fixes specific files
→ Tier 2 fail (secrets) → HARD STOP. Remove secrets. Re-run gate
→ Tier 3 fail (regression) → compare with baseline, identify what broke

### Operator rejects at control point
→ Operator explains what's wrong
→ Lead-agent returns to the appropriate stage
→ Re-run with feedback taken into account

### Maximum iterations
→ If the same stage fails 3 times in a row — STOP
→ Lead-agent reports to operator: "Stage [X] failed 3 times. Possible causes: [list]. Manual intervention needed."

---

## 11. Cycles and Iterations

```
New feature   → stage 2 → 3 → 4 → 4.5 → 5 → 5.5 → 6 → 7
Bug           → stage 5 → 5.5 → 6 → 7
Refactoring   → stage 3 → 4 → 4.5 → 5 → 5.5 → 6 → 7
```

Stage 1 is not repeated — the product is already defined.

---

## Quality Gate Integration

### Manual Run
```bash
python scripts/quality_gate.py --tier=all --module=[name]
```

### Automatic Run (Recommended)

Add a pre-commit hook in .claude/settings.json:

```json
{
  "hooks": {
    "pre-commit": [
      {
        "command": "python scripts/quality_gate.py --tier=1-2",
        "description": "Quality gate: stability + code balance check",
        "on_failure": "block"
      }
    ]
  }
}
```

When using Claude Code — add to project settings:
- Pre-commit hook blocks commit on NO-GO
- CONDITIONAL allows commit with a warning
- GO — commit passes without notes

### When to Run Quality Gate
| Moment | Tier | Automatic? |
|--------|------|------------|
| After each subagent | 1-2 | Recommended |
| Before handoff | 2 | Mandatory |
| Final module check | all | Mandatory |
| Pre-commit hook | 1-2 | Automatic |
