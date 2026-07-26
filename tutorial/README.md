# Nearest Grit Bin — Hands-On Fullstack Lab

Welcome. In this lab you rebuild the **FastAPI + Next.js** grit-bin project by
**typing each file yourself**, in order, until the full stack works end to end.

You are not copying a finished app blindly. Each step tells you:

1. **What to do** (create a folder, install deps, open a file…)
2. **Which file to create** (exact path)
3. **What to type** (the full code)
4. **How to check** it worked before moving on

---

## How to follow this lab

1. Create an empty project folder (or work in a clean clone and delete `src/` /
   `frontend/` first if you want a true type-from-scratch experience).
2. Start at **[01-introduction.md](./01-introduction.md)** and read the overview docs
   (including **[09-sources-and-references.md](./09-sources-and-references.md)** if
   Derbyshire / postcodes / maps are new).
3. Complete every file under **`backend/`** in numbered order.
4. Complete every file under **`frontend/`** in numbered order.
5. Finish local run with **[05-running-fullstack.md](./05-running-fullstack.md)**.
6. Optionally containerise with **[docker/](./docker/README.md)**.

Work **one step at a time**. Do not skip ahead until the checkpoint passes.

### Create everything by hand

All folders and files are created **manually in your editor** (new folder / new
file, type the exact name, then type the code). That is the whole point of the
lab — the typing is what builds the mental model.

Terminal commands appear only for real actions: installing packages, starting the
servers, and verifying results.

---

## Lab map

| Order | Path | What you learn |
|------:|------|----------------|
| 1 | [01-introduction.md](./01-introduction.md) | What you are building |
| 2 | [09-sources-and-references.md](./09-sources-and-references.md) | Domain background + real docs/websites used |
| 3 | [02-architecture.md](./02-architecture.md) | How backend + frontend talk |
| 4 | [03-folder-structure.md](./03-folder-structure.md) | Where files live |
| 5 | [04-environment-variables.md](./04-environment-variables.md) | Secrets and config |
| 6 | [backend/](./backend/README.md) | FastAPI (+ Python/OOP primer) |
| 7 | [frontend/](./frontend/README.md) | Next.js UI + proxy |
| 8 | [05-running-fullstack.md](./05-running-fullstack.md) | Run both sides together locally |
| 9 | [docker/](./docker/README.md) | Containerise with Docker Compose |
| 10 | [06-common-mistakes.md](./06-common-mistakes.md) | Fix typical errors |
| 11 | [10-spatial-querying.md](./10-spatial-querying.md) | Geospatial deep dive: EPSG:27700, WFS vs WMS, DWITHIN, fallback, SP_GEOMETRY |
| 12 | [07-derbyshire-exercise.md](./07-derbyshire-exercise.md) | Apply skills to the interview exercise |
| 13 | [08-next-steps.md](./08-next-steps.md) | Auth, scale, further ideas |

---

## What you will have when finished

- FastAPI on port **8000** with `GET /nearest-grit-bin`
- Next.js on port **3000** with a search form
- A Next.js **server proxy** so the browser never calls Derbyshire APIs directly
- A working flow: postcode + address → nearest grit bin + distance in metres

---

## Prerequisites

- Python **3.11+**
- Node.js **20+** (18+ usually fine)
- A code editor of your choice
- Docker Desktop (or Docker Engine + Compose) if you follow the Docker lab
- Real Address API credentials in `.env` when you want live calls

---

## Start here

Open **[01-introduction.md](./01-introduction.md)** → then follow the numbered docs.
