---
globs: ["**/auth/**", "**/*.env*", "**/config/**", "**/middleware/**"]
---

# Security rules

- .env files: NEVER commit
- Tokens/keys: only through environment variables
- Passwords: bcrypt or argon2 only
- SQL: parameterized queries only
- CORS: explicit whitelist, no wildcard
- JWT secret: >= 64 chars, random, from .env
- Refresh token: httpOnly cookie
- Access token: in memory (not localStorage)
- Rate limit on login: <= 10 attempts / 15 min
- File upload: check extension AND mime, whitelist, size limit
