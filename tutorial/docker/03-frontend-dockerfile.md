# Docker Step 3 — Frontend Dockerfile

## What you will do

Create a **multi-stage** Dockerfile for Next.js. Stage 1 installs deps, stage 2
builds the app, stage 3 runs a tiny production server.

## Prerequisite

`frontend/package-lock.json` must exist. If you followed the frontend lab and ran
`npm install`, it is already there. If not, create it once:

```powershell
cd frontend
npm install
```

(`npm ci` in the Dockerfile requires the lockfile.)

Also confirm `frontend/next.config.ts` still has `output: "standalone"` — that
setting produces the `.next/standalone` folder the runner stage copies.

## File to create: `frontend/Dockerfile`

**Path:** `frontend/Dockerfile`

### Purpose

Build a production Next.js image that serves the UI on port 3000 and can call the
backend over the Compose network via `BACKEND_URL`.

### Type this exactly

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:22-alpine AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0

RUN addgroup --system --gid 1001 nodejs \
  && adduser --system --uid 1001 nextjs

# public/ is optional; keep an empty dir so the COPY always succeeds
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000

CMD ["node", "server.js"]
```

### How the code works

**Stage `deps`**
- Copies only the lockfiles and runs `npm ci` (clean, reproducible install)
- Cached until `package.json` / `package-lock.json` change

**Stage `builder`**
- Reuses `node_modules` from `deps`
- Copies the full frontend source and runs `npm run build`
- With `output: "standalone"`, Next emits a minimal Node server under `.next/standalone`

**Stage `runner`**
- Starts from a fresh Alpine Node image (no build tools, no source tree)
- Copies only `public`, the standalone server, and static assets
- Runs as user `nextjs` (non-root)
- `CMD ["node", "server.js"]` starts the standalone server

`BACKEND_URL` is **not** baked into the image. Compose injects it at runtime so the
proxy route can reach `http://backend:8000`.

## Checkpoint

Confirm `frontend/Dockerfile` exists and `frontend/package-lock.json` exists.

## Next

→ [04-frontend-dockerignore.md](./04-frontend-dockerignore.md)
