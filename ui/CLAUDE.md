# UI Package (Vite / React / TypeScript)

## Module Commands
Run these commands from inside this subdirectory:
- **Run Local UI:** `pnpm run dev`
- **Build UI:** `pnpm run build`
- **Lint UI:** `pnpm run lint`

## Domain Standards
- **Schemas:** Rely strictly on explicit TypeScript interfaces or types for incoming and outgoing data payloads.
- **API Operations:** Modularize network calls inside specialized service classes or functions. Use `async/await` syntax exclusively and `try/catch` blocks.

## Coding Guidelines
- **Naming Conventions:** Use `camelCase` for functions, variables, and hooks. Use `PascalCase` for React components and TypeScript interfaces.
- **Utility Extraction:** Abstract any structural calculations, data wrangling, formatting, or shared mathematical operations into the `src/functions/` directory. Organize into logical files (e.g., `dateUtils.ts`, `financialMathUtils.ts`).
- **Component Design:** Keep components short, self-contained, and highly presentation-focused. Abstract reusable elements early.
- **State Management:** Use React Context combined with `useReducer` hooks for local or module-level global state. Write explicitly typed initial states and action mutations. Avoid deep prop-drilling beyond 1 level deep.

## Custom Commands
- `/test-ui`: `npm test`
- `/test-cov`: `vitest run --reporter verbose --coverage`
