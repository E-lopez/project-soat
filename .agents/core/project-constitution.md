# Project Constitution & Agent Boundaries

This document defines the absolute operational boundaries, ethical constraints, and behavioral contracts for all AI agents operating within this repository. Adherence is non-negotiable.

---

## Core Mission & System Goal

This system is a **legal intake and automation platform**. It ingests legal and medical documents, identifies actionable legal claims, and drives a downstream pipeline that:

1. **Qualifies leads** — classifies documents to determine eligibility for specific legal services and creates sales pipelines.
2. **Generates personalized outreach** — produces tailored messages for email and WhatsApp communication with prospective clients.
3. **Initiates legal actions** — fills proprietary legal formats with extracted case data and user information to produce ready-to-file documents.
4. **Processes source documents** — parses, normalizes, and stores legal and medical documents to make them consumable by all other services.

The system has some **event-driven** features: AWS S3 triggers document intake events via EventBridge, which fan out to the appropriate processing pipelines. Human intent drives what pipelines exist; agent execution drives their implementation.

Also, the system has some **AI-Orchestrated** features: langGraph orchestrating.

---

## Repository Structure & Context Boundaries

Monorepo with two isolated packages. Never apply frontend conventions to backend files or vice versa.

| Package | Path | Detailed Rules |
|---|---|---|
| Backend | `api/` | `api/CLAUDE.md` |
| Frontend | `ui/` | `ui/CLAUDE.md` |

Shared governance (git workflow, secrets, architecture principles) lives in the root `CLAUDE.md`.

Detailed guidance for agents lives in this directory:

| Document | Scope |
|---|---|
| `architecture-guidelines.md` | Layer contracts, testing requirements (≥ 80% coverage), error handling, and design principles |
| `coding-guidelines.md` | Naming conventions, folder structure, immutability patterns, async style, and commit format |

---

## Architecture Conventions (Stable Across Rewrites)

- Full layer-by-layer rules, testing constraints, error handling patterns, and design principles are in `architecture-guidelines.md`.
- Preserve clear boundaries between presentation, application, domain, and infrastructure concerns
- Prefer simple designs that support the current requirements without introducing speculative abstractions

### Backend — FastAPI (Python 3.11+)

The backend is a **monolith** structured as a collection of endpoints and services. Separation of concerns is strict:

- `routes/` — HTTP and event entry points only. No business logic. Delegates immediately to the orchestrator or a service.
- `services/` — Atomic business logic units. Each service is either **deterministic** (document parsing, DB writes, template filling, format validation) or **LLM-powered** (classification, extraction, message generation). A service must never be both.
- `orchestrators/` — One orchestrator per pipeline. Composes deterministic and LLM-powered services in sequence. The only place where services are wired together. Owns the pipeline's error recovery strategy.
- `dependencies/` — Singleton clients (DB, S3, EventBridge, Bedrock). Initialized once at startup via FastAPI's `lifespan`. Never instantiated inside services.
- `functions/` — Pure utility helpers. No side effects, no I/O, no external calls.
- `constants/` — Immutable configuration: model IDs, prompt templates, SQL statements, EventBridge event type names.
- `schemas/` — Pydantic/SQLModel data contracts. No logic.

### Event-Driven Layer — AWS
- **S3** is the document intake surface. All document processing pipelines are triggered by S3 events.
- **EventBridge** routes events to the correct pipeline. Event type names are defined in `constants/` and must not be hardcoded inline.
- New event types require human approval before being added to the EventBridge rule set.

### Frontend — React + TypeScript (Vite + pnpm)
- `components/` — Presentational, self-contained React components.
- `context/` — Global state via `useContext` + `useReducer`. No deep prop-drilling.
- `services/` — All network calls. Isolated from components.
- `models/` — TypeScript interfaces and types. No logic.

> Naming conventions, folder structure, immutability rules, and async patterns are in `coding-guidelines.md`.

---

## Domain Constraints

These rules exist because the system handles **legal and medical documents and initiates legal actions**. Violations here carry real-world consequences.

- **No data fabrication:** LLM-powered services must never invent case facts, legal citations, personal data, or document content. If extraction confidence is low, the output must be flagged for human review — not filled with a plausible guess.
- **No autonomous legal action:** No service may submit, file, or send a finalized legal document or outreach message without an explicit human approval step in the pipeline.
- **PII isolation:** Personal data (names, medical records, case identifiers) must never appear in logs, error messages, or LLM prompts beyond what is strictly required for the task. Mask or tokenize before logging.
- **Document immutability:** Source documents stored in S3 are read-only. Processing pipelines write to separate output prefixes. Never overwrite an ingested source file.
- **Prompt integrity:** Prompts that drive legal classification, document filling, or outreach generation are `constants/`. They may not be modified inline by a service or route at runtime.

---

## Operational Boundaries

### Always Do
- **HITL for Deep Changes:** Pause and request explicit human approval before modifying database schemas, orchestrator pipelines, EventBridge rules, or deleting existing modules.
- **Idempotent Scripts:** All scripts (build, migration, seed, event replay) must be safe to run multiple times without duplicating data or side effects.
- **Explicit Error Handling:** Every network request, S3 operation, EventBridge publish, or LLM call must have a graceful failure state and structured logging.
- **Verify against package rules:** Before marking a task complete, verify output against the relevant `CLAUDE.md` for that package.
- **Commit convention:** `[ui|api] [feature|bugfix|test|refactor]: description`

### Never Do
- **No Silent Overwrites:** Never overwrite `.env` files, config files, or structural modules without prompting the user first.
- **No Phantom Dependencies:** Never introduce a new pip or pnpm package without explicit human sign-off.
- **No Hardcoded Secrets:** API keys, tokens, and credentials go in `.env` files exclusively. Never in source code or config files.
- **No Cross-Boundary Edits:** A task scoped to `ui/` must not touch `api/`, and vice versa.
- **No Logic in Routes or Schemas:** Routes delegate; schemas describe. Business logic belongs in services or orchestrators.
- **No Fabricated Implementations:** If an API contract, model behavior, or AWS service behavior is ambiguous, ask before implementing.

---

## Human-in-the-Loop (HITL) Triggers

Halt and yield to the human when encountering:

1. **Destructive Operations:** `rm -rf`, `DROP TABLE`, hard git resets, S3 object deletion, or any irreversible data operation.
2. **Pipeline Changes:** Modifying the service composition order inside an orchestrator, or adding/removing a stage from an existing pipeline.
3. **New Event Types:** Adding a new EventBridge event type or S3 trigger that fans out to a new pipeline.
4. **Legal Output Changes:** Any modification to document-filling templates, legal format schemas, or outreach message prompts.
5. **Refactoring Cascades:** A single change that requires modifying more than three unrelated files.
6. **Conflicting Requirements:** When a user prompt contradicts the rules in this document or a `CLAUDE.md`.

---

## Communication & Output Style
- **Solution first:** Provide the code or architectural decision before any explanation.
- **Impact summary:** For complex changes, add a 2-line note on *what* changes and *what it might affect*.
- **Concise over verbose:** No filler, no repetition.
