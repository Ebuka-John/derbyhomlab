# The 8-Hour Study Plan — Nearest Grit Bin Lab

This is your timetable for completing the entire lab in **8 focused hours**
(one long day, two half-days, or four evenings of 2 hours). Every hour has:

- a **goal** — what exists at the end of the hour that didn't at the start
- the **pages to work through**, in order, with time budgets
- an **exit checkpoint** — do not start the next hour until it passes
- a **transition** — one sentence connecting what you just did to what's next

If you fall behind, use the [catch-up rules](#if-you-fall-behind) rather than
skipping checkpoints. If you only have 6 hours, use the
[fast track](#fast-track-6-hours).

---

## The day at a glance

| Hour | Theme | You finish with |
|------|-------|-----------------|
| 1 | Orient & set up | Mental model + working Python/Node environment |
| 2 | Backend foundations | Config, env, and error system importable |
| 3 | The geospatial core | Coordinates + Address API service passing checkpoints |
| 4 | Spatial queries & the API | Full backend answering `/nearest-grit-bin` |
| 5 | Frontend plumbing | Next.js scaffold + server proxy talking to the backend |
| 6 | Frontend UI & full-stack run | Complete flow: form → proxy → backend → result |
| 7 | Containerise | Whole stack running under `docker compose up` |
| 8 | Consolidate for the interview | Spatial concepts explained *by you*, out loud |

The dependency chain is strict: hours 2–4 build the backend the frontend calls
in hours 5–6, which Docker packages in hour 7. Hour 1 and hour 8 are the
bookends — context in, mastery out.

---

## Hour 1 — Orient & set up (the map before the territory)

**Goal:** you know *what* you are building, *why* each piece exists, and your
machine can build it.

| Time | Do this |
|------|---------|
| 0:00–0:10 | [README.md](./README.md) + [01-introduction.md](./01-introduction.md) — the what and the how of the lab |
| 0:10–0:25 | [09-sources-and-references.md](./09-sources-and-references.md) **§1–2 only** — grit bins, postcodes, British National Grid. Skim the rest; you'll return in hour 8 |
| 0:25–0:35 | [02-architecture.md](./02-architecture.md) + [03-folder-structure.md](./03-folder-structure.md) — how backend and frontend talk, where files live |
| 0:35–0:40 | [04-environment-variables.md](./04-environment-variables.md) — secrets strategy |
| 0:40–0:55 | Environment setup in **PowerShell**: `python --version` (3.11+), `node --version` (20+), create the project folder with `New-Item`, then follow [backend/01-requirements.md](./backend/01-requirements.md) for `python -m venv .venv` and `.\.venv\Scripts\Activate.ps1` |
| 0:55–1:00 | Skim [backend/00-python-fastapi-basics.md](./backend/00-python-fastapi-basics.md) — bookmark it; you will consult it *as needed*, not read it linearly |

**Exit checkpoint:** you can sketch the request path from memory —
*browser → Next.js proxy → FastAPI → Address API + GeoServer → back* — and
`python` + `node` both run in your terminal.

**Transition:** you now know the backend is the heart of the system, so that's
where the typing starts.

---

## Hour 2 — Backend foundations (everything the services lean on)

**Goal:** the project skeleton exists and the three support layers — settings,
environment, errors — import cleanly.

| Time | Do this |
|------|---------|
| 0:00–0:05 | [backend/README.md](./backend/README.md) + [backend/00-backend-design.md](./backend/00-backend-design.md) — layered design (Mermaid) |
| 0:05–0:15 | [backend/01-requirements.md](./backend/01-requirements.md) — type both requirements files, `pip install` |
| 0:15–0:25 | [backend/02-env.md](./backend/02-env.md) — create `.env` / `.env.example` |
| 0:25–0:35 | [backend/03-init-packages.md](./backend/03-init-packages.md) — full layered `src/` tree |
| 0:35–0:50 | [backend/04-config.md](./backend/04-config.md) — `core/settings` + logging |
| 0:50–1:00 | [backend/05-errors.md](./backend/05-errors.md) — `utils/exceptions.py` |

**Exit checkpoint:** the checkpoints in steps 04 and 05 both pass (settings
load from `.env`; error classes import and carry status codes).

**Transition:** with config and errors in place, you can now write the code
that actually *thinks* — coordinates and API clients — without stopping to
invent infrastructure.

---

## Hour 3 — The geospatial core (the interview-differentiating hour)

**Goal:** you can convert any coordinate to British National Grid and fetch a
matching address from the Address API.

| Time | Do this |
|------|---------|
| 0:00–0:20 | [backend/06-coordinates.md](./backend/06-coordinates.md) — domain points + `utils/geospatial.py`. **Type slowly here** |
| 0:20–0:25 | Pause and read [10-spatial-querying.md](./10-spatial-querying.md) **§1 only** (EPSG:27700) |
| 0:25–0:55 | [backend/07-address-service.md](./backend/07-address-service.md) — address **repository** + **service** |
| 0:55–1:00 | Run both checkpoints; take a 5-minute break if ahead |

**Exit checkpoint:** `euclidean_distance_meters(P(0,0), P(3,4))` prints `5.0`,
and the address-service checkpoint passes.

**Transition:** you can now turn a postcode into a point in metres — next you
ask GeoServer what's *near* that point.

---

## Hour 4 — Spatial queries & the API (the backend comes alive)

**Goal:** a complete FastAPI backend that answers
`GET /nearest-grit-bin?postcode=...&address=...`.

| Time | Do this |
|------|---------|
| 0:00–0:30 | [backend/08-geoserver-service.md](./backend/08-geoserver-service.md) — gritbin repository + service (DWITHIN + fallback) |
| 0:30–0:35 | Pause and read [10-spatial-querying.md](./10-spatial-querying.md) **§2–3** (WFS vs WMS, DWITHIN) |
| 0:35–0:50 | [backend/09-app.md](./backend/09-app.md) — dependencies, routers, `app.py`, `main.py` |
| 0:50–1:00 | [backend/10-run-and-test.md](./backend/10-run-and-test.md) — `uvicorn` up, `/docs` open, tests green |

**Exit checkpoint:** the interview example works — `HILLBROW` + `DE55 5PB`
returns grit bin `GB0199` at roughly 49 m (or the mocked tests pass if you
have no live credentials).

**Transition:** the backend is done and proven. Everything from here on is
about *reaching* it — first from a browser via a proxy, then from containers.

---

## Hour 5 — Frontend plumbing (the proxy before the pixels)

**Goal:** a Next.js app whose server-side route can call your backend — the
CORS-safe pattern the exercise brief demands.

| Time | Do this |
|------|---------|
| 0:00–0:05 | [frontend/README.md](./frontend/README.md) — frontend build order |
| 0:05–0:25 | [frontend/01-scaffold.md](./frontend/01-scaffold.md) — scaffold the app, prune to a clean base |
| 0:25–0:30 | [frontend/02-env.md](./frontend/02-env.md) — `BACKEND_URL` in `.env.local` |
| 0:30–0:40 | [frontend/03-types.md](./frontend/03-types.md) — shared TypeScript types mirroring the backend response |
| 0:40–1:00 | [frontend/04-api-route.md](./frontend/04-api-route.md) — the proxy route handler; test it with the backend running |

**Exit checkpoint:** with the backend up, requesting
`http://localhost:3000/api/nearest-grit-bin?...` returns backend JSON — the
browser never touches Derbyshire directly.

**Transition:** the data path works end to end; now give it a face.

---

## Hour 6 — Frontend UI & the full-stack run (make it visible)

**Goal:** a person can type a postcode into a page and see the nearest grit
bin with its distance.

| Time | Do this |
|------|---------|
| 0:00–0:25 | [frontend/05-search-form.md](./frontend/05-search-form.md) — the form component with loading and error states |
| 0:25–0:35 | [frontend/06-layout.md](./frontend/06-layout.md) + [frontend/08-page.md](./frontend/08-page.md) — layout and page shell |
| 0:35–0:45 | [frontend/07-globals-css.md](./frontend/07-globals-css.md) — paste-friendly; do not hand-type 300 lines of CSS under time pressure |
| 0:45–0:55 | [frontend/09-run-and-test.md](./frontend/09-run-and-test.md) + [05-running-fullstack.md](./05-running-fullstack.md) — both servers, full flow |
| 0:55–1:00 | Buffer: fix anything the full-stack run revealed |

**Exit checkpoint:** postcode + address in the browser → grit bin title and
distance on screen, and a wrong postcode shows a friendly error, not a crash.

**Transition:** it works on your machine — hour 7 makes it work on *any*
machine.

---

## Hour 7 — Containerise (repeatable anywhere)

**Goal:** `docker compose up --build` starts the whole stack with no local
Python or Node required.

| Time | Do this |
|------|---------|
| 0:00–0:05 | [docker/README.md](./docker/README.md) — what gets containerised and why |
| 0:05–0:20 | [docker/01-backend-dockerfile.md](./docker/01-backend-dockerfile.md) + [docker/02-backend-dockerignore.md](./docker/02-backend-dockerignore.md) |
| 0:20–0:40 | [docker/03-frontend-dockerfile.md](./docker/03-frontend-dockerfile.md) + [docker/04-frontend-dockerignore.md](./docker/04-frontend-dockerignore.md) — multi-stage build; the trickiest Docker file, budget accordingly |
| 0:40–0:50 | [docker/05-compose.md](./docker/05-compose.md) — wire both services together |
| 0:50–1:00 | [docker/06-run-and-test.md](./docker/06-run-and-test.md) — build, run, verify in the browser |

**Exit checkpoint:** the browser flow from hour 6 works identically at the
composed URLs, served entirely from containers.

**Transition:** you have built everything; the final hour converts *built it*
into *can explain and extend it* — which is what the interview measures.

---

## Hour 8 — Consolidate for the interview (own the material)

**Goal:** you can explain every spatial decision without notes and modify the
project on request.

| Time | Do this |
|------|---------|
| 0:00–0:25 | [10-spatial-querying.md](./10-spatial-querying.md) in full — you read §1–3 in hours 3–4; now read §4–5 and the "how it fits together" diagram, then attempt the **self-check questions at the end, out loud** |
| 0:25–0:35 | [06-common-mistakes.md](./06-common-mistakes.md) — recognise the failure modes before an interviewer shows you one |
| 0:35–0:50 | [07-derbyshire-exercise.md](./07-derbyshire-exercise.md) — do one modification for real (custom radius is the best time-boxed choice: query param → service → UI field) |
| 0:50–1:00 | [08-next-steps.md](./08-next-steps.md) + revisit [09-sources-and-references.md](./09-sources-and-references.md) §6 — the investigation trail is a ready-made "how I approached it" interview answer |

**Exit checkpoint:** you answer all five self-check questions in
[10-spatial-querying.md](./10-spatial-querying.md) without opening the page,
and your custom-radius change works in the browser.

**You are done.** The lab is complete and, more importantly, defensible.

---

## Fast track (6 hours)

Same order, tighter scope — for when the deadline is closer than the plan:

| Cut | How |
|-----|-----|
| Hour 1 → 30 min | Read only README, 01-introduction, and 02-architecture; set up tooling; skip §1–2 background reading (return to it only if a concept blocks you) |
| Hour 6 CSS | Copy-paste `globals.css` wholesale (already recommended) and skip visual polish |
| Hour 7 → optional | Docker is the safest whole hour to drop — it is packaging, not spatial reasoning. Read the compose file (10 min) instead of typing it |
| Hour 8 → 45 min | Keep the spatial-querying self-check and one modification; drop next-steps reading |

Do **not** cut hours 3–4. The coordinates, address service, and GeoServer
service are the exercise; everything else is delivery.

---

## If you fall behind

1. **Never skip an exit checkpoint** — a failing checkpoint compounds; ten
   minutes of debugging now saves forty later.
2. **Overrun by more than 15 minutes?** Stop typing and copy-paste the rest of
   the current file, then read it line by line. Understanding is the goal;
   typing is the method, not the deliverable.
3. **Stuck on an error?** Give [06-common-mistakes.md](./06-common-mistakes.md)
   two minutes before deep debugging — most lab errors are catalogued there.
4. **No live API credentials?** The tests use mocks (`respx`); every checkpoint
   except the live end-to-end call still works. Note it and move on.

## Breaks

Take 5–10 minutes between hours, and a longer break after hour 4 — it is the
natural halfway point: the backend is finished and verified, and the frontend
is a fresh context. Do not break mid-hour; each hour is designed as one
uninterrupted arc from goal to checkpoint.


---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Lab home](./README.md) | [Introduction](./01-introduction.md) → |
