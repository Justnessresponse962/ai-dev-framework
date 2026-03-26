# Specification: [MODULE NAME]

## Description
[What this module does, for whom, why. 2-3 sentences.]

---

## User Stories

- As [role], I want [action], so that [result]
- As [role], I want [action], so that [result]
- As [role], I want [action], so that [result]

---

## Data Model

```sql
CREATE TABLE [name] (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    [field] [type] [constraints],
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);
```

RLS policies (if applicable):
```sql
-- SELECT: [condition]
-- UPDATE: [condition]
```

---

## API

| Method | Path | Request body | Response | Error codes |
|--------|------|-------------|----------|-------------|
| POST | /api/[resource] | `{field: type}` | `{result}` | 201, 400, 409 |
| GET | /api/[resource]/:id | — | `{object}` | 200, 404 |

---

## Screens and Components

### Screen: [name]
- **Path:** /[path]
- **Components:**
  - [Component] — [what it shows]
- **States:**
  - Loading: [what to show]
  - Error: [what to show]
  - Empty: [what to show]
  - Success: [what to show]
- **Actions:**
  - Click [element] → [what happens]
  - Input [field] → [validation, behavior]

---

## Business Logic

### Validations
- [field]: [concrete rule] (example: email — regex + unique + max 254 chars)

### Constraints
- [constraint] (example: max 10 items on free plan)

### State transitions
```
[state_1] → [action] → [state_2]
```

---

## Edge Cases

| Situation | Expected behavior |
|-----------|------------------|
| No data | [what to show/do] |
| API not responding | [retry? fallback? message?] |
| Concurrent editing | [who wins? lock?] |
| Invalid input | [error message, format] |
| Boundary values (0, negative, max) | [behavior] |

---

## Priority and Dependencies

- **Priority:** [high / medium / low]
- **Depends on:** [module X — must be ready first]
- **Blocks:** [module Y — cannot start without this]

---

## Deviations from spec (filled AFTER implementation)

| What changed | Why | Impact |
|-------------|-----|--------|
| — | — | — |
