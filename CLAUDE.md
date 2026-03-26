# [Product Name]
# Status: [stage] | Updated: [date]

## What is this
[1-2 sentences. What the product does, for whom.]

## Stack
- Language: [...]
- Framework: [...]
- Database: [...]

## Module Map
| Module | Path | Status |
|--------|------|--------|
| — | — | — |

## Specifications
- docs/specs/spec_[module].md

## System Navigation
- **Development standards** → standards/
- **Workflow (9 stages)** → standards/03_workflow.md
- **Sub-agents** → .claude/agents/ (lead, database-architect, backend-engineer, frontend-developer, qa-reviewer, spec-reviewer, skeptic)
- **Code rules** → .claude/rules/ (database, api-routes, frontend, security, tests)
- **Quality gate** → python scripts/quality_gate.py --tier=all
- **Module preparation** → python scripts/prepare_module.py [name] --lang=[py|ts]
- **Handoffs** → docs/handoffs/[module]/
- **Spec template** → docs/specs/TEMPLATE.md

## Orchestration
For the full pipeline use the lead agent: .claude/agents/lead.md
It guides through all stages with control points.

## Imperatives
- File: 200-300 lines, max 500
- Function: 20-40 lines, max 100
- One file = one responsibility
- Secrets NEVER in code
- Ask the operator, don't guess

## Problem Routing
- "Won't start" → config, main entry point
- "DB error" → migrations, models, .claude/rules/database.md
- "API not responding" → routes, middleware, .claude/rules/api-routes.md
- "Tests failing" → tests/, fixtures, .claude/rules/tests.md
- "Security issue" → .claude/rules/security.md

## Entry Point
- Run: [command]
- Tests: [command]
- Quality gate: python scripts/quality_gate.py --tier=all

## Current Status
- Working: [list]
- Known issues: [list]

## Recent Changes
- [date]: [what changed]
