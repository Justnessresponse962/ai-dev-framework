---
globs: ["**/components/**", "**/pages/**", "**/views/**", "**/screens/**", "**/templates/**"]
---

# Frontend rules

- Every screen: 4 states (loading, error, empty, success)
- Every form: client-side validation + server-side validation
- No hardcoded text strings (prepare for i18n)
- Responsive layout (mobile-first if applicable)
- Accessibility: labels, alt text, keyboard navigation
- Component = single responsibility
- Component < 300 lines
