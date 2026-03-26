# Project Brief — TEMPLATE
# Version: 1.0 | Date: 2026-03-21

---

## How to Use This Template

Copy this file into a new project. Fill in each section BEFORE starting development.
This document is the technical framework of the project: WHAT we're building, for WHOM, within what CONSTRAINTS.
Filled in AFTER 04_project_idea_template.md (analytical foundation).
Both documents together form the basis for design. Without them, development DOES NOT START.

---


## Section A: Concept (Idea)

### A.1. Product Name
[Product Name]

### A.2. One Sentence — What Is It
[Example: "A system for automating the management of multiple browser profiles"]

### A.3. Problem Being Solved
[Describe the problem in plain language. Not technical. As if explaining to a friend.
Example: "I have 200 social media accounts and can't manage them manually"]

### A.4. Who Is the User
[Myself / my team / external users / ...]

### A.5. What the Product MUST Do (Required)
1. [Feature 1]
2. [Feature 2]
3. [...]

### A.6. What the Product MAY Do (Nice to Have)
1. [Feature 1]
2. [...]

### A.7. What the Product MUST NOT Do (Boundaries)
1. [Example: "Does not store passwords in plain text"]
2. [Example: "Does not work on mobile devices"]
3. [...]


---


## Section B: Technical Constraints

### B.1. Platform
- [ ] Web application
- [ ] Desktop application
- [ ] Script / CLI
- [ ] Telegram bot
- [ ] Other: ___

### B.2. Language and Framework
[If you know — specify. If you don't — write "at Claude's discretion"
with preferences: "I want it simple" / "I want it fast" / ...]

### B.3. Database
- [ ] Needed (data persists between sessions)
- [ ] Not needed (everything in memory / files)
- [ ] Don't know

### B.4. External Services and APIs
[List everything the product will interact with:
APIs, websites, other programs, databases, file systems...]

### B.5. Where It Will Run
- [ ] On my computer (Windows / Mac / Linux)
- [ ] On a server
- [ ] In the cloud
- [ ] Don't know

### B.6. Expected Size
- [ ] Small (up to 2,000 lines, 1-3 modules)
- [ ] Medium (2,000-10,000 lines, 5-10 modules)
- [ ] Large (10,000+ lines, 10+ modules)
- [ ] Don't know


---


## Section C: Architectural Requirements

### C.1. Reference to Technical Requirements
The project is developed in accordance with:
- 01_technical_requirements.md (all standards are mandatory)

### C.2. Additional Project Constraints
[If this specific project has constraints beyond the general technical requirements — specify.
Example: "files no larger than 300 lines" (stricter than the general 500 limit)]

### C.3. Security Requirements
- [ ] Working with passwords / tokens (encryption needed)
- [ ] Working with personal data
- [ ] Working with finances / crypto
- [ ] No special requirements

### C.4. Reliability Requirements
- [ ] Critical — must not crash (retry, graceful shutdown needed)
- [ ] Important — must log errors and continue
- [ ] Not critical — crashes are acceptable


---


## Section D: Implementation Stages

### D.1. Breakdown into Stages
[Claude fills in this section based on sections A-C.
Each stage is a self-contained working part of the product.]

Stage 1: [Name] — [What will work after this stage]
Stage 2: [Name] — [What will work after this stage]
...

### D.2. Module Specifications
Before implementing each stage, module specifications are created (docs/specs/spec_[module].md).
Specification format — 6 mandatory blocks:
1. User Stories — usage scenarios
2. Data Model — tables, fields, types, relationships
3. API — endpoints, methods, request/response body, error codes
4. Screens and Components — UI, states, actions
5. Business Logic — validations, constraints, state transitions
6. Edge Cases — no data, API errors, concurrent scenarios

Without a module specification, code IS NOT WRITTEN (see 03_workflow.md, stage 4).

### D.3. Priorities
[What functionality is needed FIRST? What can wait?]

### D.4. Definition of "Done" for Each Stage
[How will you (not Claude, but YOU) verify that a stage is complete?
Example: "I open the dashboard, see a list of profiles, can add a new one"]


---


## Section E: Acceptance and Quality Control

### E.1. How I Will Verify the Work
[Describe how you check the result. You don't know the code — so you check behavior.
Example: "I run it, open in browser, click a button, look at the result"]

### E.2. What Counts as a Bug
[Example: "system doesn't start", "I click a button — nothing happens",
"shows an error on screen"]

### E.3. What Counts as Success
[Example: "I can add 10 profiles, launch a task for each,
see the result on the dashboard"]


---
