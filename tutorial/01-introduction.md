# 1. Introduction

## What you will do

Read this page. Do not write code yet.

## What this project does

You enter a UK **postcode** (e.g. `AB12 3CD`) and an **address** hint
(e.g. `Example Building`). The app:

1. Looks up addresses for that postcode (Derbyshire Address Lookup API)
2. Finds the matching property and its map coordinates
3. Asks GeoServer for grit bins near that point (within 100 metres)
4. Returns the nearest grit bin title and distance in metres

## Why FastAPI + Next.js

| Layer | Tool | Job |
|-------|------|-----|
| Backend | **FastAPI** | Validate input, call external APIs, do coordinate maths, return JSON |
| Frontend | **Next.js** | Show a form/UI, and proxy browser requests to FastAPI safely |

They fit well because:

- FastAPI is strong at integrations and typed APIs
- Next.js is strong at UI **and** can run server-side routes (our proxy)
- The browser never needs Address API tokens or GeoServer URLs

## What you will build

A fullstack app matching this repository:

- Python package under `src/`
- Next.js App Router under `frontend/`
- Shared JSON contract for success and errors

## New to coding or FastAPI?

You do not need to be a professional engineer. The backend lab starts with a plain-language
primer on Python classes, async, and FastAPI:

→ [backend/00-python-fastapi-basics.md](./backend/00-python-fastapi-basics.md)

Each step also explains concepts **inline** where they appear (inheritance, decorators,
`async`/`await`, React state, and so on).

## New to Derbyshire / postcodes / maps?

If grit bins, UK postcodes, GeoServer, or EPSG:27700 are unfamiliar, read the
sources guide before or alongside the lab. It lists the real websites, standards
docs, and investigation trail used to build this project:

→ [09-sources-and-references.md](./09-sources-and-references.md)

For a plain-language CRS / BNG / DWITHIN / Euclidean FAQ tied to this codebase:

→ [10-spatial-querying.md — Beginner FAQ](./10-spatial-querying.md#beginner-faq--crs-bng-and-this-codebase)

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [8-hour study plan](./00-study-plan.md) | [Sources and references](./09-sources-and-references.md) → |
