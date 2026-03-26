---
globs: ["**/migrations/**", "**/db/**", "**/models/**", "**/schema/**"]
---

# Database rules

- One migration file = one logical change
- Down migration (rollback) MANDATORY
- New tables: RLS policies if spec requires them
- Field types: strictly per docs/specs/spec_*.md
- Indexes: on FK and fields in WHERE/ORDER BY
- No CASCADE DELETE without explicit spec mention
- Money/prices: Decimal (NEVER Float)
- Timestamps: created_at + updated_at on every table
- Naming: snake_case, plural table names
