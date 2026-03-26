---
globs: ["**/tests/**", "**/*test*", "**/*spec*"]
---

# Test rules

- Test name describes WHAT it verifies, not HOW
- One test = one assertion
- No dependency on execution order
- Mock only external services, not internal modules
- Test data: factories/fixtures, no hardcoded values
- Before refactor: tests pass. After refactor: tests still pass
