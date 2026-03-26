# Subagent Model — Roles, Pipeline, Handoffs
# Version: 3.0 | Date: 2026-03-26

---

## Team

### Implementers (Write/Edit)

| Subagent | Model | Responsibility | Prompt |
|----------|-------|----------------|--------|
| database-architect | opus | DB schema, migrations, indexes, RLS | .claude/agents/database-architect.md |
| backend-engineer | opus | API, server logic, tests | .claude/agents/backend-engineer.md |
| frontend-developer | sonnet | UI, forms, navigation | .claude/agents/frontend-developer.md |

### Reviewers (Read-only, do NOT write code)

| Subagent | Model | Responsibility | Prompt |
|----------|-------|----------------|--------|
| qa-reviewer | opus | Review by checklist (security, spec, code, tests) | .claude/agents/qa-reviewer.md |
| spec-reviewer | opus | Specification completeness check | .claude/agents/spec-reviewer.md |
| skeptic | opus | Architecture decision verification | .claude/agents/skeptic.md |

**Model selection criterion:** mistake is expensive → Opus. Fixable in a minute → Sonnet.

---

## Module Implementation Pipeline

```
spec_[module].md
      │
      ▼
database-architect → 01_schema_done.md → quality_gate --tier=1
      │
      ▼
backend-engineer   → 02_api_ready.md   → quality_gate --tier=2
      │
      ▼
frontend-developer → 03_frontend_done.md → quality_gate --tier=2
      │
      ▼
qa-reviewer        → 04_review_report.md → GO / CONDITIONAL / NO-GO
      │
      ▼ (if there are issues)
Fixes              → 05_fixes_applied.md → re-run qa-review
```

**Skipping steps:** no DB → skip database-architect. No UI → skip frontend-developer.

---

## Handoff Protocol

Each subagent MUST:
1. Read previous handoffs before starting
2. Create their own handoff before finishing

Handoff format is defined in each subagent's prompt.
Full protocol: docs/handoffs/PROTOCOL.md

**Priority on conflict:** spec is the source of truth. Handoff is supplementary. On discrepancy — follow spec, note in handoff.

---

## Reviewers at Design Stages

**Stage 2 (stack):** Claude MUST provide 2-3 options with a comparison table. After selection — skeptic.md verifies.

**Stage 4 (specification):** spec-reviewer.md checks against a checklist. A specification with TODOs = NEEDS WORK.

---

## Critical Rule

Reviewers NEVER get Write/Edit access. Reviewer describes the problem → implementer fixes → reviewer re-checks.

---

## When to Add Subagents

| Situation | Action |
|-----------|--------|
| First project | No subagents |
| Project > 10 files | + qa-reviewer |
| Complex DB | + database-architect |
| Frontend + Backend | + frontend-developer + backend-engineer |
| Critical architecture | + skeptic |
| Full pipeline | Entire team + spec-reviewer |
