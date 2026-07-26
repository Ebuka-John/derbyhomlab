# 4. Environment Variables

## What you will do

Learn which variables the app needs. You will create the files in the backend and
frontend steps — do not invent values yet unless you already have credentials.

## Backend (root `.env`)

| Variable | Purpose |
|----------|---------|
| `ADDRESS_API_BASE_URL` | Base URL; code appends `/{postcode}` |
| `ADDRESS_API_ALIAS` | Sent as header `x-alias` |
| `ADDRESS_API_AUTH_TOKEN` | Sent as header `x-auth-token` (secret) |
| `GEOSERVER_BASE_URL` | GeoServer root; WFS URL becomes `{base}/DCC/ows` |
| `GEOSERVER_LAYER` | WFS typeName, e.g. `DCC:Gritbins` |
| `NEAREST_SEARCH_RADIUS_METERS` | Optional (default `100`) |
| `HTTP_TIMEOUT_SECONDS` | Optional (default `30`) |

These are loaded by `src/config.py` via pydantic-settings.

## Frontend (`frontend/.env.local`)

| Variable | Purpose |
|----------|---------|
| `BACKEND_URL` | Where the Next.js **server** proxy sends requests (e.g. `http://127.0.0.1:8000`) |

Not prefixed with `NEXT_PUBLIC_`, so it stays **server-only**.

## Golden rule

Secrets and upstream URLs stay on the **server** (FastAPI + Next.js route handler).
The browser only ever calls `/api/nearest-grit-bin`.

## Your action now

Start coding: open **[backend/README.md](./backend/README.md)**.
