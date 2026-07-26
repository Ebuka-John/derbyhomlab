# 3. Folder Structure

## What you will do

Learn where each file belongs. You will create these folders step by step in the
backend and frontend labs.

## Target tree (what you are building)

```
homelab/                          ← your project root
├── .env                          ← secrets (never commit)
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile                    ← backend image (Docker lab)
├── .dockerignore
├── docker-compose.yml            ← runs backend + frontend together
├── src/                          ← FastAPI backend
│   ├── __init__.py
│   ├── app.py                    ← endpoints live here
│   ├── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── address_service.py
│   │   └── geoserver_service.py
│   └── utils/
│       ├── __init__.py
│       ├── coordinates.py
│       └── errors.py
└── frontend/                     ← Next.js frontend
    ├── Dockerfile
    ├── .dockerignore
    ├── package.json
    ├── next.config.ts
    ├── tsconfig.json
    ├── .env.local
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx
    │   ├── globals.css
    │   └── api/nearest-grit-bin/route.ts
    ├── components/
    │   └── SearchForm.tsx
    └── lib/
        └── types.ts
```

## What each area means

| Path | Purpose |
|------|---------|
| `src/app.py` | FastAPI app + `/nearest-grit-bin` endpoint |
| `src/config.py` | Load and validate env vars |
| `src/services/*` | Talk to Address API and GeoServer |
| `src/utils/*` | Coordinates + typed errors |
| `frontend/app/*` | Pages, layout, API route |
| `frontend/components/*` | Interactive UI (`SearchForm`) |
| `frontend/lib/types.ts` | TypeScript shapes matching the API |
| `Dockerfile` / `frontend/Dockerfile` | Image recipes for each service |
| `docker-compose.yml` | Start both containers and wire networking |

> Note: this project keeps the endpoint in `app.py` (no separate `routers/` folder).
> Response shapes use Pydantic in `app.py` and dataclasses inside services — there
> is no `models/gritbin.py`.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Architecture](./02-architecture.md) | [Environment variables](./04-environment-variables.md) → |
