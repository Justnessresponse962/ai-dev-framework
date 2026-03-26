---
globs: ["**/routers/**", "**/api/**", "**/routes/**", "**/endpoints/**"]
---

# API rules

- Every endpoint: validate input
- Structured responses: {data, error, status}
- Error codes: per docs/specs/spec_*.md
- Auth check on every protected route
- Logging: request + response + execution time
- Error format: WHERE + WHAT + CONTEXT
- No raw SQL with string concatenation
