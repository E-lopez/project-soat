---
name: spec-clarification
description: Review a spec file, identify ambiguities and missing requirements, and ask exactly 5 clarifying questions.
argument-hint: "[spec-file]"
allowed-tools:
  - read
  - grep
  - glob
triggers:
  - user
  - model
---

Use this skill when the user wants discovery-oriented clarification questions for a product or feature spec.

Before you begin:
- Ask the user which spec file to review if they did not already provide one
- Treat the provided value as a project-relative path, for example `.devin/spec.md` or `.devin/specs/refactor-deep-linking.md`

Read:
1. `.devin/core/constitution.md` (project constraints)
2. Every other file under `.devin/core`
3. The user-provided spec file

Task:
- Identify ambiguities, edge cases, and missing requirements
- Ask exactly 5 clarifying questions across these categories:
  1. Data validation/integrity (2 questions)
  2. User experience/error handling (1 question)
  3. Performance/scalability (1 question)
  4. Security/privacy (1 question)
- Format each question as:
  - **Question:** [Your question]
  - **Why it matters:** [Impact of not addressing this]
  - **Example scenario:** [Concrete case where this becomes an issue]
- Do NOT suggest solutions. Only ask questions.

Output:
- A clarification review containing exactly 5 questions in the required format
- A reminder that the human should:
  - Answer each question thoughtfully
  - Update the chosen spec file with the decisions
  - Add entries to the Decision Log section
  - Run the clarification loop again if new questions emerge
- After clarification is complete, run the `spec-review` skill against the same spec file
