# Standard for Designing and Building Software Products with Claude
# Version: 3.0 | Date: 2026-03-26

---

## Architecture: Two Layers

**Layer 1 — Standards (standards/):** building codes. HOW to design and build.
**Layer 2 — Operational Tools:** implement the standards. Copied into each project.

```
project/
├── CLAUDE.md                       ← Operational file (agent reads ALWAYS)
│
├── standards/                      ← LAYER 1: Standards (6 documents)
│   ├── 00_table_of_contents.md     ← Navigator (this file)
│   ├── 01_technical_requirements   ← Environment constraints, code standards
│   ├── 02_project_brief_template   ← Project brief template
│   ├── 03_workflow                 ← 9 stages of design and implementation
│   ├── 04_project_idea_template    ← Project analytical document
│   └── 05_subagent_roles           ← Roles, pipeline, handoffs
│
├── .claude/                        ← LAYER 2: Operational Tools
│   ├── agents/                     ← Prompts for 6 subagents (implements 05)
│   └── rules/                      ← Context rules by glob patterns
│
├── scripts/                        ← Python scripts (cross-platform)
│   ├── quality_gate.py             ← GO / CONDITIONAL / NO-GO
│   └── prepare_module.py           ← Module preparation + TDD tests
│
└── docs/
    ├── specs/TEMPLATE.md           ← Module specification template
    └── handoffs/PROTOCOL.md        ← Handoff protocol between agents
```

---

## Dependency Map

| Standard | Declares | Implemented By |
|----------|----------|----------------|
| 01 Technical Requirements | Code standards, sizes, naming | CLAUDE.md + quality_gate.py |
| 02 Project Brief | New project brief template | Manual (stage 1) |
| 03 Workflow | 9 stages from idea to documentation | scripts/*.py + .claude/agents/*.md |
| 04 Project Idea | Project analytical document | Manual (stage 1) |
| 05 Subagent Roles | Roles, pipeline, handoff protocol | .claude/agents/*.md + docs/handoffs/ |

**What was removed (10 → 6):**
- 03 Reliability Hierarchy → implemented in quality_gate.py + .claude/rules/
- 05 CLAUDE.md Templates → implemented in CLAUDE.md + prepare_module.py
- 07 Spec Template → lives as docs/specs/TEMPLATE.md
- 09 Rules Glob Patterns → lives as .claude/rules/*.md

Principle: if a standard describes something already implemented in an operational file — the standard is removed.

---

## Usage Order

**New project:**
1. Copy: CLAUDE.md, .gitignore, .claude/, scripts/, docs/
2. Fill in 04 (idea) → 02 (brief)
3. Claude designs architecture → skeptic.md verifies
4. Specifications per docs/specs/TEMPLATE.md → spec-reviewer.md reviews
5. Pipeline: prepare_module.py → agents with handoffs → quality_gate.py
6. Manual acceptance → documentation update

**Reading order:**
- First time: **00_table_of_contents.md** → 03_workflow → 05_subagent_roles
- New project: 04_project_idea → 02_project_brief
- Understand subagents: 05_subagent_roles → .claude/agents/
