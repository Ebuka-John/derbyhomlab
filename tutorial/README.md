# Nearest Grit Bin — Simplified Type-Along (PyCharm)

Rebuild the **FastAPI + Next.js** grit-bin app by **typing each file yourself**,
one at a time, in **PyCharm**.

This lab is a **trimmed** version of the full tutorial on `main`.

| This branch (`readytosubmit`) | `main` branch |
|-------------------------------|---------------|
| **Source of truth for code** — type every file from here | Deeper explanations, study plan, primers, spatial FAQ |
| Short concept notes + checkpoints | Full embedded walkthrough under `tutorial/` |

---

## How to work (two PyCharm windows)

1. **Reference window** — open this repo on branch `readytosubmit`.  
   You only **read** files here; do not edit them for the lab.
2. **Lab window** — `File → New Project…` → empty project (e.g. `grit-bin-lab`).  
   You **create and type** every file here.

For each step:

1. In the **reference** window, open the listed path.
2. In the **lab** window, create the same path (`Alt+Insert` → File / Package).
3. **Type** the file (do not copy-paste if you want the learning benefit).
4. **Run that lesson’s Checkpoint immediately** — do **not** type the whole
   backend/frontend and only test at the end.
5. Only then open the next lesson.

Catching a typo after one file is cheap; catching it after twenty is not.

Early checkpoints are usually `import` / install checks. The live API and UI
smoke tests come once those layers exist (`backend/09-run.md`,
`frontend/04-run.md`). That is still “test as you go” — each layer must pass
before you build on it.

> Tip: arrange both windows side by side, or use PyCharm’s split editor with
> the reference file on the left and your new file on the right.

---

## Lab map

| Order | Path | What you do |
|------:|------|-------------|
| 1 | [01-pycharm-setup.md](./01-pycharm-setup.md) | Two windows, interpreter, terminals |
| 2 | [02-overview.md](./02-overview.md) | What you are building (brief) |
| 3 | [backend/](./backend/README.md) | Type the FastAPI backend |
| 4 | [frontend/](./frontend/README.md) | Type the Next.js UI + proxy |
| 5 | [docker/](./docker/README.md) | Optional: Docker Compose |

---

## Deeper reading (on `main`)

Check out or browse `main` when you want more detail:

- [00-study-plan.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/00-study-plan.md) — timed 8-hour plan
- [00-backend-design.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/backend/00-backend-design.md) — layered design + Mermaid
- [00-python-fastapi-basics.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/backend/00-python-fastapi-basics.md) — Python/FastAPI primer
- [10-spatial-querying.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/10-spatial-querying.md) — EPSG:27700, WFS, `DWITHIN`
- [09-sources-and-references.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/09-sources-and-references.md) — domain background
- [lfdocs/](../lfdocs/) on this branch — interview notes (submission / panel)

Also useful on this branch: root [README.md](../README.md).

---

## Prerequisites

- Python **3.11+** (3.12 fine)
- Node.js **20+**
- JetBrains **PyCharm** (Professional or Community)
- Address API credentials in `.env` for live calls
- Docker Desktop (only for the optional Docker section)

---

## Finished product

- FastAPI on **:8000** — `/nearest-grit-bin`, `/nearest-grit-bins`, `/grit-bins`, `/health`
- Next.js on **:3000** — form → server proxy → FastAPI (browser never hits Derbyshire APIs)

Start → [01-pycharm-setup.md](./01-pycharm-setup.md)
