---
name: plan-generation
description: Generate `.devin/plan.md` from a spec file and project constraints.
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

Use this skill when the user wants an implementation plan generated from a product or feature spec.

Before you begin:
- Ask the user which spec file to review if they did not already provide one
- Treat the provided value as a project-relative path, for example `.devin/spec.md` or `.devin/specs/refactor-deep-linking.md`

Read:
1. `.devin/core/constitution.md`
2. Every other file under `.devin/core`
3. `.devin/spec.md`
4. The user-provided spec file

Task:
- Create `.devin/plan.md` using only the sections justified by the chosen spec file
- Prefer a right-sized plan: a refactor may need fewer or different sections than a net-new feature
- Include sections such as these when they are justified:
  1. **Architecture Overview**
     - High-level architecture diagram in Mermaid syntax
     - Layered structure explanation
     - Rationale for architectural choices
  2. **Technology Stack Justification**
     - Frameworks and libraries needed
     - Alignment with `constitution.md`
     - Dependencies that require human approval
  3. **Folder Structure**
     - Expected directory tree
     - Purpose of major folders
     - Naming conventions applied
  4. **Data Models**
     - Mapping from spec entities to technical structures
     - Field types, validations, and constraints
     - Persistence implications when applicable
  5. **API Implementation Plan**
     - Endpoints required by the spec
     - Request and response shapes
     - Error-handling approach
  6. **Testing Strategy**
     - Unit test scope
     - Integration test scope
     - Test-data approach
  7. **Assumptions Made**
     - Decisions not explicit in the spec
     - Items that require human validation

Output:
- `.devin/plan.md`
- Markdown headers and code blocks where appropriate
- Mermaid diagrams only when they clarify the plan
- A concise implementation plan rather than a long design document
- No implementation code yet
