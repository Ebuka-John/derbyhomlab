# Frontend Step 5 — Search form (client component)

## What you will do

1. Create the empty file with PowerShell (`New-Item`) from the project root.
2. Open it and type the code carefully.
3. Run the checkpoint before continuing.

## File to create: `components/SearchForm.tsx`

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path frontend\components\SearchForm.tsx | Out-Null
```

Open `frontend/components/SearchForm.tsx` in your editor and type the contents below yourself.

**Path:** `components/SearchForm.tsx` (relative to `frontend/`)

### Purpose

Interactive form + result/error display. Calls the Next.js proxy (never FastAPI directly from the browser).

### Type this exactly

```tsx
"use client";

import { FormEvent, useId, useState, useTransition } from "react";

import type { LookupResult, NearestGritBinSuccess } from "@/lib/types";

const DEFAULT_POSTCODE = "DE55 5PB";
const DEFAULT_ADDRESS = "HILLBROW";

async function lookupNearest(postcode: string, address: string): Promise<LookupResult> {
  const params = new URLSearchParams({ postcode, address });
  const response = await fetch(`/api/nearest-grit-bin?${params.toString()}`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  const payload = await response.json();

  if (!response.ok) {
    return {
      ok: false,
      status: response.status,
      error: payload?.error ?? {
        code: "unknown_error",
        message: "Unexpected response from the API.",
      },
    };
  }

  return { ok: true, data: payload as NearestGritBinSuccess };
}

export function SearchForm() {
  const formId = useId();
  const postcodeId = `${formId}-postcode`;
  const addressId = `${formId}-address`;
  const statusId = `${formId}-status`;

  const [postcode, setPostcode] = useState(DEFAULT_POSTCODE);
  const [address, setAddress] = useState(DEFAULT_ADDRESS);
  const [result, setResult] = useState<NearestGritBinSuccess | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedPostcode = postcode.trim();
    const trimmedAddress = address.trim();

    if (!trimmedPostcode || !trimmedAddress) {
      setError("Enter both a postcode and an address.");
      setResult(null);
      return;
    }

    startTransition(async () => {
      setError(null);
      setResult(null);

      try {
        const outcome = await lookupNearest(trimmedPostcode, trimmedAddress);
        if (outcome.ok) {
          setResult(outcome.data);
        } else {
          setError(outcome.error.message);
        }
      } catch {
        setError("Something went wrong while contacting the API.");
      }
    });
  }

  return (
    <section className="panel" aria-labelledby={`${formId}-heading`}>
      <header className="panel__intro">
        <h2 id={`${formId}-heading`} className="panel__heading">
          Look up an address
        </h2>
        <p className="panel__lede">
          Resolves the property via the Address API, then finds the nearest grit
          bin within 100 metres on GeoServer WFS.
        </p>
      </header>

      <form className="form" onSubmit={onSubmit} noValidate>
        <div className="field">
          <label htmlFor={postcodeId}>Postcode</label>
          <input
            id={postcodeId}
            name="postcode"
            type="text"
            autoComplete="postal-code"
            inputMode="text"
            spellCheck={false}
            value={postcode}
            onChange={(event) => setPostcode(event.target.value)}
            placeholder="DE55 5PB"
            disabled={isPending}
            required
          />
        </div>

        <div className="field">
          <label htmlFor={addressId}>Address</label>
          <input
            id={addressId}
            name="address"
            type="text"
            autoComplete="street-address"
            spellCheck={false}
            value={address}
            onChange={(event) => setAddress(event.target.value)}
            placeholder="HILLBROW"
            disabled={isPending}
            required
          />
        </div>

        <div className="form__actions">
          <button type="submit" className="button" disabled={isPending}>
            {isPending ? "Searching…" : "Find nearest grit bin"}
          </button>
        </div>
      </form>

      <div
        id={statusId}
        className="status"
        role="status"
        aria-live="polite"
        aria-atomic="true"
      >
        {isPending ? <p className="status__pending">Querying backend…</p> : null}

        {error ? (
          <div className="result result--error">
            <p className="result__label">Could not resolve</p>
            <p className="result__message">{error}</p>
          </div>
        ) : null}

        {result ? (
          <div className="result result--ok">
            <p className="result__label">Nearest grit bin</p>
            <p className="result__title">{result.nearest_grit_bin_title}</p>
            <dl className="result__meta">
              <div>
                <dt>Distance</dt>
                <dd>{result.distance_meters.toFixed(2)} m</dd>
              </div>
              <div>
                <dt>Address</dt>
                <dd>{result.address}</dd>
              </div>
              <div>
                <dt>Postcode</dt>
                <dd>{result.postcode}</dd>
              </div>
            </dl>
          </div>
        ) : null}
      </div>
    </section>
  );
}
```

### How the code works

#### Concepts in this file (React)

| Concept | Where | Plain meaning |
|---------|-------|---------------|
| **`"use client"`** | top of file | This component runs in the **browser** (needs hooks / click handlers). |
| **Component** | `function SearchForm()` | A reusable UI piece that returns JSX (HTML-like markup). |
| **State (`useState`)** | postcode, address, result, error | Values that, when changed, cause React to re-draw the UI. |
| **`useTransition`** | `isPending` | Marks the search as “in progress” so the button can show “Searching…”. |
| **Event handler** | `onSubmit` | Function that runs when the form is submitted. |
| **Conditional render** | `{error ? … : null}` | Only show the error/result blocks when they exist. |
| **`fetch`** | `lookupNearest` | Browser HTTP call to **your** `/api/...` proxy (same origin). |

#### Data flow in the UI

```
User clicks button
   → onSubmit prevents page reload
   → lookupNearest() calls /api/nearest-grit-bin
   → if ok: setResult(data)   → green result card appears
   → if not: setError(message) → error card appears
```

Defaults (`HILLBROW` / `DE55 5PB`) are prefilled so you can test with one click.

## Checkpoint

File should exist under `frontend/components/SearchForm.tsx`.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [API route](./04-api-route.md) | [Layout](./06-layout.md) → |
