# Handoff Protocol

## What is a handoff
A handoff is a structured artifact that one subagent creates for the next subagent.
It contains EXACTLY what the next agent needs — no more, no less.

## Why handoffs
Without handoffs, the next agent must read and reverse-engineer all previous work.
This wastes tokens and loses context. A handoff is a contract:
"here is what I did, here is what you need to know."

## Rules
1. Every subagent MUST create a handoff before completion
2. Every subagent MUST read previous handoffs before starting
3. Handoff format is defined in the subagent's prompt (.claude/agents/*.md)
4. Handoffs live in: docs/handoffs/[module]/

## Naming convention
```
docs/handoffs/[module]/
  01_schema_done.md       ← database-architect output
  02_api_ready.md         ← backend-engineer output
  03_frontend_done.md     ← frontend-developer output
  04_review_report.md     ← qa-reviewer output
  05_fixes_applied.md     ← post-review fixes (if any)
  06_review_report_v2.md  ← re-review after fixes (if any)
```

## Numbering
Sequential. If a module requires re-review after fixes:
```
  04_review_report.md     ← first review
  05_fixes_applied.md     ← what was fixed
  06_review_report_v2.md  ← second review
```

## Priority rule
**Spec is the source of truth. Handoff is supplementary.**
If handoff contradicts spec — follow spec, note the discrepancy in handoff.

## What a handoff contains
- What was done (facts, not opinions)
- What the next agent needs to know (types, formats, constraints)
- Known limitations or deviations from spec
- NOT: reasoning, alternatives considered, or general advice
