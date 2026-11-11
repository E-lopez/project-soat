# Architecture Guidelines

Extends `project-constitution.md`. All rules there remain in force; this document adds depth.

---

## 1. Layer Responsibilities

### `routes/`
- Entry points only: validate the incoming request shape, call one orchestrator or service, return the response.
- No `if/else` business logic. No direct DB or AWS calls.
- Declare response schemas inline or via `schemas/`; never build response dicts by hand inside a route.

### `services/`
- Each service is **either** deterministic **or** LLM-powered — never both.
- A service function takes plain Python values and returns plain Python values (no `Request`, no `Session` objects).
- Side effects (DB writes, S3 puts) are allowed only in deterministic services; LLM services must be pure input → output.
- Maximum one level of private helper (`_helper_name`) inside the same file. If helpers grow, extract to `functions/`.

### `orchestrators/`
- One file per pipeline. Composes services in a fixed, documented sequence.
- Owns retry logic and error recovery for the whole pipeline — services must not retry internally.
- If a stage fails and recovery is impossible, raise a structured exception with enough context for the caller to log and surface to the user.

### `dependencies/`
- Singleton clients only. Initialized once via `lifespan` or `@lru_cache(maxsize=1)`.
- Never call `boto3.client(...)` or `create_async_engine(...)` outside this layer.

### `functions/`
- Pure functions: same input → same output, no I/O, no imports from `services/` or `dependencies/`.
- Acceptable imports: stdlib, third-party parsing libs, `constants/`.

### `constants/`
- All values are module-level constants (UPPER_SNAKE_CASE). No classes, no functions.
- Prompt templates live here as multi-line strings. They may contain `{placeholder}` slots but must not be mutated at runtime.

### `schemas/`
- Pydantic / SQLModel models only. No methods beyond validators (`@field_validator`, `@model_validator`).
- DTOs (request/response shapes) go in `schemas/Dto/`. DB table models go directly in `schemas/`.

---

## 2. Event-Driven Layer

- S3 is the **only** document intake surface. Do not accept raw document bytes over HTTP in production pipelines.
- EventBridge event type names are defined in `constants/` and referenced by name — never hardcoded as strings inline.
- Adding a new event type or S3 trigger requires human approval (HITL trigger #3 in the constitution).

---

## 3. Frontend Layer

- `components/` — presentational only. No `fetch`, no business logic, no direct context mutation.
- `context/` — global state via `useContext` + `useReducer`. Actions are typed discriminated unions (`AppAction`). Reducers are pure functions.
- `services/` — all network calls. Returns typed promises or async generators. No JSX, no hooks.
- `models/` — TypeScript interfaces and `type` aliases. No logic, no classes.
- `pages/` — compose components and wire context. Minimal logic; delegate to services and context.

---

## 4. Testing

### Coverage Requirement
- **Every new feature must ship with unit tests that keep coverage at ≥ 80%.**
- Coverage is measured per-package (`api/` and `ui/` independently).
- A PR that drops coverage below 80% must not be merged until tests are added.

### Backend (Python)
- Use `pytest` + `pytest-asyncio` for async routes and services.
- Mock all I/O boundaries (`boto3`, `AsyncSession`, `httpx`) with `unittest.mock` or `pytest-mock`. Services must be testable without live AWS or DB connections.
- Test files mirror the source tree: `api/tests/services/test_classification_service.py` for `api/app/services/classification_service.py`.
- One test file per source module. Group tests by function/method using classes only when shared fixtures justify it.
- LLM-powered services: test the prompt construction and response parsing logic; mock the actual model call.

### Frontend (TypeScript)
- Use Vitest + React Testing Library.
- Test reducers and pure service functions as unit tests (no DOM needed).
- Component tests assert rendered output and user interactions, not implementation details.
- Mock `fetch` / `api.ts` at the module boundary; never let tests hit a real network.

---

## 5. Error Handling

- **Every** network call, S3 operation, EventBridge publish, and LLM invocation must be wrapped in a try/except (Python) or try/catch (TS).
- Catch specific exceptions first (`BotoCoreError`, `ClientError`), then broad `Exception` as a last resort.
- Re-raise as `HTTPException` with a safe, non-PII message at the route boundary.
- Log the original exception with `logger.exception(...)` (Python) or `console.error(...)` (TS) before re-raising.
- Never swallow errors silently. A bare `except: pass` is forbidden.
- Structured log fields: `service`, `operation`, `error_type`. Never include PII or raw document content.

---

## 6. Design Principles

### Single Responsibility
Each module, class, and function does exactly one thing. If you need to describe a function with "and", split it.

### Simplicity over Cleverness
Prefer a readable `for` loop over a nested list comprehension. Prefer an explicit `if/elif` chain over a dynamic dispatch dict when there are ≤ 4 cases. Code is read far more often than it is written.

### No Premature Abstraction
Do not create a base class, protocol, or factory until there are at least two concrete implementations that share non-trivial logic. Duplication is cheaper than the wrong abstraction.

### Immutability
- Python: prefer returning new dicts/lists over mutating in place. Use `dataclasses(frozen=True)` or Pydantic models for data containers.
- TypeScript: reducers always return new state objects (`{ ...state, ... }`). Never mutate `state` directly.

### Performance
- Avoid O(n²) loops over large document sets. Prefer set lookups over list scans for membership tests.
- DB queries: use indexed columns for filters; avoid `SELECT *` in production queries.
- Embeddings and LLM calls are expensive — never call them inside a loop without explicit justification and a documented cost estimate.

### Maintainability
- If a function exceeds ~40 lines, it is doing too much. Extract.
- If a file exceeds ~200 lines, consider splitting by responsibility.
- Delete dead code immediately. Do not comment it out.
