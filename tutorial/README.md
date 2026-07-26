# Nearest Grit Bin — Hands-On Fullstack Lab

Welcome. In this lab you rebuild the **FastAPI + Next.js** grit-bin project by
**typing each file yourself**, in order, until the full stack works end to end.

You are not copying a finished app blindly. Each step tells you:

1. **What to do** (create a folder, install deps, open a file…)
2. **Which file to create** (exact path)
3. **What to type** (the full code)
4. **How to check** it worked before moving on

---

## On a deadline?

Follow **[00-study-plan.md](./00-study-plan.md)** — the full lab organised into
**8 timed hours** (with a 6-hour fast track), each with a goal, time-boxed
steps, and an exit checkpoint. Recommended even without a deadline: the pacing
and transitions are designed for retention.

---

## How to follow this lab

1. Open **PowerShell** and create an empty project folder (or work in a clean
   clone and delete `src/` / `frontend/` first if you want a true type-from-scratch
   experience).
2. Start at **[01-introduction.md](./01-introduction.md)** and read the overview docs
   (including **[09-sources-and-references.md](./09-sources-and-references.md)** if
   Derbyshire / postcodes / maps are new).
3. Complete every file under **`backend/`** in numbered order.
4. Complete every file under **`frontend/`** in numbered order.
5. Finish local run with **[05-running-fullstack.md](./05-running-fullstack.md)**.
6. Optionally containerise with **[docker/](./docker/README.md)**.

Work **one step at a time**. Do not skip ahead until the checkpoint passes.

### Type-along + PowerShell (how every step works)

This is a **type-along** lab on **Windows PowerShell**. You run every command
yourself. The pattern never changes:

1. **PowerShell creates** the empty file or folder (`New-Item …`).
2. **You open the file** in your editor and **type** the contents yourself.
3. **PowerShell runs** installs, servers, and checkpoints.

Do not paste a finished source tree from elsewhere — typing the code builds the
mental model. Every command is in a `powershell` block: copy it into your
terminal and run it.

#### PowerShell conventions used throughout

```powershell
# Create folders / empty files (from the project root)
New-Item -ItemType Directory -Force -Path src\utils | Out-Null
New-Item -ItemType File -Force -Path src\utils\geospatial.py | Out-Null

# Activate the Python virtual environment (every new terminal)
.\.venv\Scripts\Activate.ps1

# If Activate.ps1 is blocked by execution policy, run this once in that terminal:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

## Lab map

| Order | Path | What you learn |
|------:|------|----------------|
| 0 | [00-study-plan.md](./00-study-plan.md) | The 8-hour timetable (start here if time-boxed) |
| 1 | [01-introduction.md](./01-introduction.md) | What you are building |
| 2 | [09-sources-and-references.md](./09-sources-and-references.md) | Domain background + real docs/websites used |
| 3 | [02-architecture.md](./02-architecture.md) | How backend + frontend talk |
| 4 | [03-folder-structure.md](./03-folder-structure.md) | Where files live |
| 5 | [04-environment-variables.md](./04-environment-variables.md) | Secrets and config |
| 6 | [backend/](./backend/README.md) | FastAPI layered design (+ Mermaid) + type-along |
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
- **Windows PowerShell** (this lab’s command language)
- A code editor of your choice
- Docker Desktop (or Docker Engine + Compose) if you follow the Docker lab
- Real Address API credentials in `.env` when you want live calls


---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← *Start of lab* | [8-hour study plan](./00-study-plan.md) → |
