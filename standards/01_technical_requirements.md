# Technical Requirements for Designing Software Products with Claude
# Version: 1.0 | Date: 2026-03-21

---

## 1. Purpose

Describes immutable environment constraints (Claude AI) that MUST be followed
when designing and implementing any software product.

Violating technical requirements leads to:
- Context loss (Claude forgets what it was doing)
- Vibe coding loop (writes → breaks → fixes → breaks again)
- Inability to debug and maintain
- Quality degradation as the project grows


---

## 2. Environment Constraints (Stable Principles)

### 2.1. Context Window
- Context is limited → CLAUDE.md must be compact, code must be modular
- Context includes: system prompt + CLAUDE.md + conversation history + code
- During long sessions: the system automatically compresses old messages (compaction)

### 2.2. No Memory Between Sessions
- Every new conversation with Claude starts from scratch
- Claude does NOT remember what it did yesterday unless there is documentation
- The only "memory" is project files (CLAUDE.md, code, comments)

### 2.3. Sequential Reading
- Claude reads files one at a time, on request
- Cannot see the "big picture" of a project until it reads navigation files
- Navigates by file names, function names, folder structure

### 2.4. Probabilistic Nature
- Claude is a language model, not a deterministic compiler
- May solve the same task differently on different days
- Prompts are intentions, not commands
- For critical rules, enforcement mechanisms are needed (hooks, scripts)

### 2.5. Tools
- Claude Code: terminal tool, works with code directly
- Cowork: desktop application, files + browser + documents
- Both read CLAUDE.md automatically

---

## Appendix A: Current Model Parameters
**Revision date: 2026-03-21**

| Parameter | Value |
|-----------|-------|
| Model | Claude Opus 4.6 / Sonnet 4.6 |
| Context window | ~1,000,000 tokens (GA since March 2026) |
| Prompt reliability | ~70-85% (empirical estimate) |

*This section is updated when the model changes or parameters are modified.*


---

## 3. Code Structure Standards

### 3.1. File Sizes
| Parameter | Recommended | Acceptable Maximum | Critical (Forbidden) |
|-----------|-------------|--------------------|-----------------------|
| Lines per file | 200-300 | 500 | >500 |
| Functions per file | 5-10 | 15 | >20 |
| Lines per function | 20-40 | 80 | >100 |
| Parameters per function | 2-4 | 6 | >8 |

Rationale: a 500-line file takes ~5% of context. A 3000-line file takes ~30%.
Working with two large files simultaneously exhausts the context.

### 3.2. Nesting Depth
- Backend: recommended up to 4 levels, acceptable 5
- Frontend: acceptable 5-6 levels (components/features/auth/forms/fields/ is normal)
- Avoid: 7+ levels — hinders navigation regardless of stack

### 3.3. Naming
- Files: descriptive names reflecting purpose (NOT utils, helpers, misc)
- Functions/methods: verb + object (send_tweet, getProfileRiskScore)
- Classes/types: PascalCase (ProfileManager, TaskExecutor)
- Constants: UPPER_SNAKE_CASE (MAX_RETRY_COUNT, DEFAULT_TIMEOUT)
- Casing conventions: determined by project language (snake_case for Python, camelCase for JS/TS)
- Forbidden: single-letter names (except i, j in loops), names like temp, data, stuff

### 3.4. One File — One Responsibility
- A file does ONE thing and does it well
- If the file description contains "and" — it needs to be split
- Example: "reads from DB AND sends to API" → two files

### 3.5. Explicit Dependencies
- All imports at the top of the file
- Forbidden: dynamic imports, global variables for data passing
- Forbidden: magic strings for function calls
- Every module must have an explicitly defined public API (approach depends on language)


---

## 4. Documentation Standards

### 4.1. CLAUDE.md Hierarchy
```
~/.claude/CLAUDE.md                    ← Global (tech requirements, general rules)
  └── project/CLAUDE.md                ← Project (module map, status, context)
       └── project/app/module/CLAUDE.md ← Module (files, connections, module tasks)
```

### 4.2. CLAUDE.md Sizes
| Level | Max Lines | Content |
|-------|-----------|---------|
| Global | 100 | Tech requirements, code standards, workflow |
| Project | 150 | Module map, current status, routing |
| Module | 50 | File list, connections, typical tasks |

Rationale: CLAUDE.md is read EVERY time on entry. An overloaded CLAUDE.md
consumes context itself and reduces effectiveness.

### 4.3. Required Code Documentation
- Every public function: brief purpose description (docstring / JSDoc / comment — depends on language)
- Every class/type: purpose description
- Type annotations on public functions (type hints / TypeScript types / annotations — depends on language)
- Comments only for "WHY", not for "WHAT" (code should speak for itself)

### 4.4. Executive Documentation
- CLAUDE.md reflects ACTUAL state, not plans
- After every significant change — update CLAUDE.md
- "Known Issues" section — mandatory
- "Not Implemented" section — mandatory


---

## 5. Development Process Standards

### 5.1. Iterative Approach
- Recommended: one task per session (conversation with Claude)
- Target: 3-5 files, 200-400 lines per session
- Exception: migrations, cross-cutting refactors, infrastructure changes may touch more files
- After every change: verification (test, run, screenshot)
- Avoid: "write me a 2000-line module in one go"

### 5.2. Git Discipline
- One commit = one logical change
- Commit message: type + what + why
- Types: feat (new), fix (bugfix), refactor (restructure), docs (documentation)
- Commit BEFORE starting a new task (save point)
- Forbidden: commits like "fix stuff", "update", "changes"

### 5.3. Configuration
- All settings in .env file
- .env.example with comments for each variable
- Forbidden: hardcoded URLs, keys, timeouts, limits in code
- Single configuration reading point (config.py / config.ts / etc.)

### 5.4. Error Handling
- Structured messages: WHERE + WHAT + CONTEXT
- Example: "ActionEngine.execute: timeout 30s waiting for #tweet-btn, profile=42, url=twitter.com"
- Forbidden: empty except/catch, "something went wrong", console.log/print instead of structured logging

### 5.5. Tests as Contracts
- Tests describe EXPECTED behavior
- Minimum test surface:
  - Unit: domain logic, pure functions
  - Integration: interaction with DB, external APIs
  - Smoke/e2e: critical user path (launch → main action → result)
- Before refactoring — ensure tests pass
- After refactoring — tests must still pass


---

## 6. Data and Infrastructure Standards

### 6.1. Monetary and Financial Values
- All money, price, amount fields — type `Decimal` (NOT Float/Double)
- Reason: Float produces rounding errors (0.1 + 0.2 = 0.30000...04). Over thousands of operations, discrepancies accumulate
- Prisma: `Decimal`, PostgreSQL: `NUMERIC(12,2)`, JS: work through strings or library (decimal.js)
- Forbidden: Float/Double for money, JS number arithmetic on prices without Decimal

### 6.2. Monitoring
- At MVP stage: structured logging (winston/pino) + health endpoint
- On deploy: Prometheus for metrics collection (requests/sec, latency, errors, DB connections)
- Caching decisions — only based on monitoring data, not blindly

### 6.3. Caching
- Apply only when monitoring shows the need
- Pattern: Cache-Aside (simplest and most reliable)
- Implementation: Redis
- Forbidden: cache without invalidation strategy, cache "just in case"

### 6.4. Database Backups
- Mandatory before production deploy
- Minimum: daily pg_dump + 30-day rotation
- Recommended: copy to cloud storage (S3/GCS) + alert if backup not created within 25 hours
- Test restore from backup at least once before launch


---

## 7. Forbidden Practices (Red Lines)

The following practices are FORBIDDEN under any circumstances:

1. Hardcoded secrets, keys, passwords in code
2. Deleting files without a commit (save point)
3. Empty except/catch blocks (swallowing errors)
4. Float/Double for storing monetary amounts and prices

The following practices are strong recommendations (violation requires justification):

5. File larger than 500 lines
6. Function larger than 100 lines
7. More than 20 functions in one file
8. CLAUDE.md larger than 150 lines (project level)
9. Changing more than 5 files per session without intermediate verification


---

## 8. Application

This document is the FOUNDATION for:
- Design brief (02_project_brief_template.md)
- Workflow (03_workflow.md)
- Global CLAUDE.md (~/.claude/CLAUDE.md)

Changes to technical requirements are only possible when environment
constraints change (new version of Claude with different context window, etc.).

---
