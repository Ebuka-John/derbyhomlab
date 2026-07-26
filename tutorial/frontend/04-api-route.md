# Frontend Step 4 — API proxy route

## What you will do

1. Create the file at the path below (inside `frontend/`).
2. Type the code carefully.
3. Run the checkpoint before continuing.

## File to create: `app/api/nearest-grit-bin/route.ts`

**Path:** `app/api/nearest-grit-bin/route.ts` (relative to `frontend/`)

### Purpose

Next.js Route Handler that runs on the server and forwards requests to FastAPI.

### Type this exactly

```typescript
import { NextRequest, NextResponse } from "next/server";

import type { ApiErrorBody, NearestGritBinSuccess } from "@/lib/types";

/**
 * Server-side proxy to FastAPI.
 *
 * The browser never calls Derbyshire upstreams (CORS constraint) and never
 * talks to FastAPI cross-origin either — this Route Handler keeps BACKEND_URL
 * on the server and forwards the typed JSON contract.
 */
export async function GET(request: NextRequest) {
  const postcode = request.nextUrl.searchParams.get("postcode")?.trim() ?? "";
  const address = request.nextUrl.searchParams.get("address")?.trim() ?? "";

  if (!postcode || !address) {
    const body: ApiErrorBody = {
      error: {
        code: "missing_parameter",
        message: "Both postcode and address are required.",
      },
    };
    return NextResponse.json(body, { status: 400 });
  }

  const backend = process.env.BACKEND_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";
  const url = new URL("/nearest-grit-bin", backend);
  url.searchParams.set("postcode", postcode);
  url.searchParams.set("address", address);

  try {
    const upstream = await fetch(url, {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store",
    });

    const payload = (await upstream.json()) as NearestGritBinSuccess | ApiErrorBody;
    return NextResponse.json(payload, { status: upstream.status });
  } catch {
    const body: ApiErrorBody = {
      error: {
        code: "backend_unreachable",
        message: "Could not reach the FastAPI backend. Is it running on port 8000?",
      },
    };
    return NextResponse.json(body, { status: 502 });
  }
}
```

### How the code works

#### Concepts in this file (Next.js)

| Concept | Where | Plain meaning |
|---------|-------|---------------|
| **Route Handler** | `app/api/.../route.ts` + `export async function GET` | File path **is** the URL. Exporting `GET` handles GET requests. |
| **Server-only code** | this whole file | Runs on the Next.js **server**, not in the browser. Safe place for `BACKEND_URL`. |
| **Proxy pattern** | fetch FastAPI, return its JSON | Browser → Next.js → FastAPI. Browser never sees the Python URL or secrets. |
| **`process.env`** | `BACKEND_URL` | Environment variable available to server code. |

This is the frontend twin of FastAPI’s “keep secrets on the server” idea.

## Checkpoint

You will test this after the UI exists. For now ensure the folder path is exactly `app/api/nearest-grit-bin/route.ts`.

## Next

→ [05-search-form.md](./05-search-form.md)
