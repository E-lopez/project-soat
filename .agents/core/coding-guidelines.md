# Coding Guidelines

Conventions derived from the existing codebase. Follow them in all new code.

---

## 1. Naming

### Python (`api/`)
| Construct | Convention | Example |
|---|---|---|
| Module / file | `snake_case` | `classification_service.py` |
| Function | `snake_case` | `classify_definitions`, `hybrid_search` |
| Private helper | `_snake_case` | `_fetch_definitions` |
| Class | `PascalCase` | `MainIndex`, `TelemetryBedrockClient` |
| Constant (module-level) | `UPPER_SNAKE_CASE` | `SYNTHESIS_MODEL_ID`, `PROMPT_TEMPLATE` |
| Variable / parameter | `snake_case` | `query_embedding`, `doc_name` |
| Type alias | `snake_case` or inline | `DbSession` (via `Annotated`) |

### TypeScript (`ui/`)
| Construct | Convention | Example |
|---|---|---|
| File (component) | `PascalCase` | `AppStateContext.tsx` |
| File (service/model) | `camelCase` | `api.ts` |
| Interface | `PascalCase` | `AppState`, `QueryResponseChunk` |
| Type alias | `camelCase` + `T` suffix | `scoresT`, `AppAction` |
| Function / hook | `camelCase` | `sendQuery`, `useAppState` |
| React component | `PascalCase` | `AppStateProvider` |
| Constant | `UPPER_SNAKE_CASE` | `BASE_URL` |
| Enum-like discriminant | string literal union | `'answer_chunk' | 'metrics' | 'sources'` |

---

## 2. Folder Structure

```
api/app/
  constants/     # UPPER_SNAKE_CASE values only
  dependencies/  # singleton clients, @lru_cache or lifespan-initialized, databses, ai gateways or similar
  functions/     # pure helpers, no I/O
  orchestrators/ # one file per pipeline (not yet present, add here)
  api/        # APIRouter per domain, prefix declared at router level
  schemas/
    Dto/         # request/response shapes
  tasks/      # one concern per file, deterministic OR llm-powered
  tools/  # functions accessible to agents
  workflows/ # Holds the agent workflows
  main.py        # app factory + lifespan only

ui/src/
  components/    # one folder per component, PascalCase folder name
  context/       # useContext + useReducer providers
  models/
    AppState/    # state shape + action union
    interfaces/  # shared TS interfaces
  pages/         # route-level components
  services/      # fetch wrappers, no JSX
```

---

## 3. Imports

### Python
- Standard library → third-party → internal (`app.*`), separated by blank lines.
- Import specific names, not modules, when the usage is clear: `from fastapi import HTTPException` not `import fastapi`.
- Avoid circular imports: `functions/` and `constants/` must never import from `services/` or `routes/`.

### TypeScript
- Named imports preferred over default imports for models and utilities.
- Default imports only for React components and pages.
- `import.meta.env` for environment variables; never `process.env` in the UI.

---

## 4. Immutability

### Python
- Return new collections instead of mutating: `[*existing, new_item]` or `{**existing, key: value}`.
- Pydantic / SQLModel models are the canonical data containers — do not attach ad-hoc attributes to them.
- `constants/` values must never be reassigned at runtime.

### TypeScript
- Reducers: always spread state — `{ ...state, field: newValue }`. Never `state.field = newValue`.
- Interfaces and types are readonly by convention; add `readonly` modifier to fields that must not change after construction.
- Prefer `const` everywhere; `let` only when reassignment is unavoidable.

---

## 5. Async Patterns

### Python
- All DB operations use `async/await` with `AsyncSession`.
- CPU-bound or sync third-party calls (e.g., `pymupdf4llm`) stay synchronous; do not wrap them in `asyncio.run_in_executor` unless profiling shows a bottleneck.
- `@lru_cache(maxsize=1)` for singleton clients that are safe to cache (stateless boto3 clients).

### TypeScript
- `async function` for service calls; `AsyncGenerator` for streaming responses.
- Always `finally { reader.releaseLock() }` after consuming a `ReadableStream`.
- Never `await` inside a `forEach`; use `for...of` or `Promise.all`.

---

## 6. Error Handling Style

### Python
```python
try:
    result = client.invoke_model(...)
except (BotoCoreError, ClientError) as e:
    raise HTTPException(status_code=502, detail="Upstream model call failed.") from e
```
- Catch the narrowest exception type first.
- Always chain with `from e` to preserve the traceback.
- Log before raising at service boundaries; routes surface the `HTTPException`.

### TypeScript
```typescript
if (!res.ok) {
  const body = await res.json().catch(() => ({})) as { detail?: string }
  throw new Error(body.detail ?? 'Request failed.')
}
```
- Provide a safe fallback message; never expose raw server error strings to the UI.
- Errors propagate to the context via `dispatch({ type: 'SET_ERROR', payload: message })`.

---

## 7. Comments & Documentation

- Write code that reads like prose; comments explain *why*, not *what*.
- Docstrings on public functions that have non-obvious parameters or return shapes (Google style).
- Inline comments only for regex patterns, bit manipulation, or non-obvious algorithmic choices.
- Do not leave `TODO` comments in merged code; open a task instead.

---

## 8. Configuration & Secrets

- All secrets in `.env` / `.env.{env}` files, loaded via `dotenv` or Doppler.
- Access via `get_doppler_secret(key, fallback)` — never `os.environ[key]` directly (no fallback safety).
- `import.meta.env.DEV` / `import.meta.env.VITE_*` in the UI; never hardcode URLs.

---

## 9. Commit & Branch Convention

```
[ui|api] [feature|bugfix|test|refactor]: short imperative description
```
- Branch names: `feature/`, `bugfix/`, `test/`, `refactor/` prefixes.
- One logical change per commit. Do not bundle unrelated fixes.
