---
name: spec-review
description: Review a spec file for completeness and identify remaining implementation gaps.
argument-hint: "[spec-file]"
allowed-tools:
  - read
  - grep
  - glob
triggers:
  - user
  - model
---

Use this skill when the user wants a completeness review of a product or feature spec.

Before you begin:
- Ask the user which spec file to review if they did not already provide one
- Treat the provided value as a project-relative path, for example `.devin/spec.md` or `.devin/specs/refactor-deep-linking.md`

Read:
1. `.devin/core/constitution.md`
2. Every other file under `.devin/core`
3. The user-provided spec file

Task:
- Review the chosen spec file for completeness
- Answer these five questions:
  1. Are all user stories testable?
  2. Are business rules unambiguous?
  3. Does API contract cover all user stories?
  4. Are there conflicts with `constitution.md`?
  5. Can you implement this without making assumptions?
- If NO to any question, identify the gap

Output:
- A direct review organized by the five questions above
