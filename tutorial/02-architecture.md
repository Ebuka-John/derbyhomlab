# 2. Architecture Overview

## What you will do

Understand the data flow. No coding yet.

## Responsibilities

### Backend (FastAPI)

- Accept `postcode` and `address` query params
- Call the Address Lookup API
- Match the address and normalise coordinates to **EPSG:27700** (British National Grid)
- Query GeoServer WFS for the nearest grit bin
- Return JSON success or a typed JSON error

### Frontend (Next.js)

- Render the search form
- Call its **own** `/api/nearest-grit-bin` route (same origin)
- That route (server-side) forwards to FastAPI
- Show the result or a friendly error

## Data flow (text diagram)

```
Browser (user)
   │  GET /api/nearest-grit-bin?postcode=…&address=…
   ▼
Next.js :3000
   │  app/page.tsx + components/SearchForm.tsx
   │  app/api/nearest-grit-bin/route.ts  ← server proxy
   │  GET http://127.0.0.1:8000/nearest-grit-bin?…
   ▼
FastAPI :8000  (src/app.py)
   │
   ├─► Address Lookup API  → resolve property + coordinates
   └─► GeoServer WFS       → nearest grit bin within radius
   │
   ▼
JSON back through Next.js → browser shows result
```

## Why the proxy exists

1. **Secrets stay on the server** (Address API token never reaches the browser)
2. **No CORS pain** — the browser only talks to Next.js on the same origin
3. **Clean separation** — UI talks to `/api/…`; FastAPI talks to Derbyshire systems

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Sources and references](./09-sources-and-references.md) | [Folder structure](./03-folder-structure.md) → |
