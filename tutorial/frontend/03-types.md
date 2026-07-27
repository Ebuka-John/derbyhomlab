# Frontend Step 3 — Shared types

## What you will do

1. Create the empty file in your editor (from the project root).
2. Open it and type the code carefully.
3. Run the checkpoint before continuing.

## File to create: `lib/types.ts`

### Create this file in the editor

Create `frontend/lib/types.ts` in your editor (from the project root), then type the contents below yourself.

**Path:** `lib/types.ts` (relative to `frontend/`)

### Purpose

TypeScript types that mirror the FastAPI JSON success and error contracts.

### Type this exactly

```typescript
export type NearestGritBinSuccess = {
  address: string;
  postcode: string;
  nearest_grit_bin_title: string;
  distance_meters: number;
};

export type ApiErrorBody = {
  error: {
    code: string;
    message: string;
  };
};

export type LookupResult =
  | { ok: true; data: NearestGritBinSuccess }
  | { ok: false; status: number; error: ApiErrorBody["error"] };
```

### How the code works

#### Concepts in this file (TypeScript)

| Concept | Where | Plain meaning |
|---------|-------|---------------|
| **`type`** | `NearestGritBinSuccess` | A named shape for an object — like a Pydantic model, but for TypeScript. |
| **Union type** | `LookupResult` | “Either success **or** failure” — written with `\|`. |
| **Discriminated union** | `ok: true` / `ok: false` | Check `ok` first; TypeScript then knows which fields exist. |

Why bother? So the UI cannot accidentally read `data` on an error, or `error` on
success — the compiler catches that mistake.

## Checkpoint

No runtime check yet — continue once the file exists with no TypeScript red squiggles when later files import it.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Frontend env](./02-env.md) | [API route](./04-api-route.md) → |
