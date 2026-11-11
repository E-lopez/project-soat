---
name: task-generation
description: Generate `.devin/tasks.md` from `.devin/plan.md` as a set of atomic implementation tasks.
argument-hint: "[spec-file]"
allowed-tools:
  - read
  - grep
  - glob
  - edit
  - write
triggers:
  - user
  - model
---

Use this skill when the user wants an execution task list generated from an approved implementation plan.

Before you begin:
- Confirm that `.devin/plan.md` exists
- If it does not, ask the user which spec file should be used to generate the plan first

Read:
1. `.devin/core/constitution.md`
2. Every other file under `.devin/core`
3. `.devin/plan.md`

Task:
- Create `.devin/tasks.md` with 10-15 atomic tasks
- Ensure each task includes:
  - **Description:** 1-2 sentences
  - **Files Created/Modified:** specific paths
  - **Acceptance Criteria:** 3-5 testable checkboxes
  - **Time Estimate:** 15-45 minutes
  - **Dependencies:** task numbers or `None`
- Keep tasks:
  - Independent enough to be worked on without waiting on unrelated unfinished tasks
  - Small enough to usually modify fewer than 5 files
  - Testable with clear pass/fail criteria
  - Estimated at roughly 15-45 minutes each
- Organize tasks in a practical implementation order
- Prefer vertical slices when possible so each feature area can move toward completion end-to-end
- Use phases such as `Setup`, `Core Features`, and `Polish` when helpful

Output:
- `.devin/tasks.md`
- Tasks ordered in a practical sequence such as infrastructure/setup, models/validation, services/business logic, controllers or UI entrypoints, tests, and documentation or polish
