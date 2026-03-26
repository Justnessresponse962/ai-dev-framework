# PROJECT_IDEA — Project Idea Document
# Version: 1.0 | Date: 2026-03-22

---

## Purpose

The first and most important project document. Written FOR AI, not for investors
and not for marketers. AI analyzes this document and generates architecture,
specification, and implementation plan.

The more specific the problem, audience, and solution are described —
the more autonomously Claude Code operates.

**Specificity rule:** instead of "advanced analytics" write
"dashboard with retention charts by cohort, free→pro conversion, WAU/MAU".
AI does not work with abstractions.

Order: this document first (analytical foundation),
then 02_project_brief_template.md (technical framework).

---

## 1. Problem

Specific description of the pain point. Not "people find it inconvenient", but "a developer spends
3-5 hours on setup instead of 5 minutes".

- Numbers, examples, current workarounds
- Who suffers and how much
- What happens if the problem is not solved

---

## 2. Solution

Step-by-step product description. Each step = a specific action.
This is the foundation for specification modules.

- Step 1: [what the user does → what the system does]
- Step 2: [...]
- ...

---

## 3. Why Now

Market timing: what technologies have emerged, what niches have opened,
what has changed in user behavior.

AI uses this section for positioning and prioritization.

---

## 4. Target Audience

Primary and secondary. For each segment:
- Who: [role, age, context]
- Task: [what they want to solve]
- Current tools: [what they use now]
- Willingness to pay: [yes/no/how much]

---

## 5. Architecture

System layers with a text diagram. Stack with justification for choices.
Modules with inputs/outputs.

```
[User] → [Frontend] → [API] → [Backend] → [DB]
                                         → [External API]
```

- Stack: [language, framework, DB — with justification]
- Key modules: [list with brief descriptions]

---

## 6. Monetization

Plans, pricing, feature gating.

| Plan | Price | What's Included |
|------|-------|-----------------|
| Free | $0 | [limited functionality] |
| Pro | $X/mo | [full functionality] |

AI uses this section to generate subscription tables
and payment integrations.

---

## 7. Competitors

| Competitor | What It Does | What It Lacks | Our Advantage |
|------------|-------------|---------------|---------------|
| [name] | [description] | [weakness] | [how we're better] |
| ... | ... | ... | ... |

Helps prioritize features.

---

## 8. Launch Plan

Phases with goals and metrics. MVP highlighted separately.

| Phase | Goal | Success Metric | Timeline |
|-------|------|----------------|----------|
| MVP | [minimum to validate hypothesis] | [what we measure] | [when] |
| v1.0 | [full product] | [what we measure] | [when] |

---

## 9. Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [description] | High/Medium/Low | [what breaks] | [how to reduce] |
| ... | ... | ... | ... |

Helps AI build modularity and fallbacks into the architecture.

---

## 10. Technical Details

Repository structure, key DB tables, AI pipeline.
The more detail — the more accurate the specification.

- File structure: [if there's already an understanding]
- Key tables: [if there's a DB]
- External APIs: [list with purpose]
- Special requirements: [performance, security, scale]

---
