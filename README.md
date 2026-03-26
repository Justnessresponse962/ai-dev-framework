# AI Dev Framework

> A spec-first, quality-gated development framework for AI-assisted software production with Claude Code.

## The Problem

AI coding assistants generate code fast, but quality is inconsistent. Without structure, you get:
- Code that "works" but is full of holes
- No tests, no error handling, no edge cases
- AI reviewers that rubber-stamp AI-written code
- The "vibe coding" loop: generate &rarr; patch &rarr; pray

## The Solution

This framework turns AI-assisted development from ad-hoc prompting into a **structured production pipeline**:

1. **Spec First** — Write detailed specifications before any code
2. **TDD** — Tests are created as failing stubs before implementation
3. **Specialized Sub-agents** — Separate roles for coding, reviewing, and challenging
4. **Quality Gates** — Automated checks at every stage (GO / CONDITIONAL / NO-GO)
5. **Handoff Protocol** — Structured context transfer between agents

## Architecture

```
your-project/
├── CLAUDE.md                    # Project router (what's where)
├── .claude/
│   ├── agents/                  # Sub-agent prompts
│   │   ├── lead.md              # Pipeline orchestrator
│   │   ├── database-architect.md
│   │   ├── backend-engineer.md
│   │   ├── frontend-developer.md
│   │   ├── qa-reviewer.md       # Read-only code review
│   │   ├── spec-reviewer.md     # Specification completeness check
│   │   └── skeptic.md           # Challenges tech decisions
│   └── rules/                   # Auto-loaded by file pattern
│       ├── database.md
│       ├── api-routes.md
│       ├── frontend.md
│       ├── security.md
│       └── tests.md
├── scripts/
│   ├── quality_gate.py          # 3-tier quality check (Python, cross-platform)
│   └── prepare_module.py        # TDD stub generator
├── standards/                   # Development standards & templates
│   ├── 00_table_of_contents.md
│   ├── 01_technical_requirements.md
│   ├── 02_project_brief_template.md
│   ├── 03_workflow.md           # 9-stage development process
│   ├── 04_project_idea_template.md
│   └── 05_subagent_roles.md
└── docs/
    ├── specs/
    │   └── TEMPLATE.md          # Module specification template
    └── handoffs/
        └── PROTOCOL.md          # Agent-to-agent handoff protocol
```

## How It Works

### The Pipeline

```
You: "Build auth module"
        │
        ▼
┌─────────────────┐
│ Specification    │ ← You + Claude write spec
│ + Spec Review    │ ← spec-reviewer validates completeness
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Preparation      │ ← prepare_module.py creates failing test stubs (TDD)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Implementation   │ ← Sub-agents work sequentially:
│                  │   database-architect → backend-engineer → frontend-developer
│                  │   Each creates a handoff artifact for the next
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ QA Review        │ ← qa-reviewer checks against 29-point checklist
│                  │   Fix issues → re-review → repeat until clean
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Quality Gate     │ ← quality_gate.py: GO / CONDITIONAL / NO-GO
└────────┬────────┘
         │
         ▼
    ✅ Done
```

### Key Principles

- **Deterministic > Probabilistic**: Scripts and hooks enforce rules, not prompts
- **Isolation of concerns**: Builders never review their own work
- **Spec is the contract**: If it's not in the spec, the agent decides (badly)
- **Every found bug becomes a test**: Bugs are closed permanently, not patched temporarily

## Quick Start

1. **Use this template** &rarr; Create a new repo from this template
2. **Fill in CLAUDE.md** &rarr; Your project name, stack, modules
3. **Write your first spec** &rarr; Copy `docs/specs/TEMPLATE.md`, fill it in
4. **Run the pipeline**:
   ```bash
   # Prepare module with TDD stubs
   python scripts/prepare_module.py my_module --lang=py

   # After implementation, run quality gate
   python scripts/quality_gate.py --tier=all --module=my_module
   ```

## Quality Gate

Three-tier automated quality check:

| Tier | What it checks | Failure = |
|------|---------------|-----------|
| **1: Stability** | App starts, syntax OK, no crashes | NO-GO |
| **2: Code Balance** | Lint, types, file sizes, no secrets, tests pass | NO-GO on secrets, CONDITIONAL on others |
| **3: Regression** | Compare with baseline metrics | Warning |

Secrets in code = **automatic hard NO-GO**. No exceptions.

## Sub-agents

| Agent | Role | Access |
|-------|------|--------|
| **lead** | Pipeline orchestrator, guides through stages | Full |
| **database-architect** | Schema, migrations, indexes | Write |
| **backend-engineer** | API, business logic, tests | Write |
| **frontend-developer** | UI components, forms, states | Write |
| **qa-reviewer** | Code review against checklist | **Read-only** |
| **spec-reviewer** | Specification completeness check | **Read-only** |
| **skeptic** | Challenges technology decisions | Read + WebSearch |

## Requirements

- Python 3.8+ (for quality_gate.py and prepare_module.py)
- Claude Code (or compatible AI coding assistant)
- Git

## License

MIT

## Contributing

Issues and PRs welcome. Please read the existing standards before proposing changes.
