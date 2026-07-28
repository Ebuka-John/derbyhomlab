# 1 — PyCharm setup

## Concept

You learn by **recreating** the app, not by reading a finished tree. Keep a
**reference** project open (this branch) and type into a **fresh lab** project.

## Steps

### 1. Reference project (read-only for the lab)

1. Open this `homelab` folder in PyCharm.
2. Confirm the Git branch is `readytosubmit` (bottom-right / Git tool window).
3. Leave it open — you will open files under `src/`, `frontend/`, etc. from here.

### 2. Lab project (where you type)

1. `File → New Project…`
2. Choose **Pure Python** (or Empty) — not “from existing sources”, and **not** the FastAPI wizard.
3. Location example: `C:\Users\<you>\Cursor_AI_projects\grit-bin-lab`
4. Create the project and open it in a **new window**.

Why not the FastAPI project type? That wizard generates its own starter tree
(`main.py`, sample routes, often a different layout). This lab teaches *our*
layered `src/` layout by typing every file from the reference — a blank project
avoids fighting or deleting scaffold you did not ask for. You still use FastAPI;
you just install it yourself in the next backend step.

### 3. Python interpreter (lab window)

1. `File → Settings → Project → Python Interpreter`
2. Add a **Virtualenv** interpreter with base Python 3.11+.
3. Location: `<lab-root>\.venv` (PyCharm can create this for you).

Or in the lab’s Terminal tool window:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Mark sources (after `src/` exists)

Later, once you have typed `src/`:

1. Right-click the **lab project root** (not only `src`) — we import as `src.…`
2. You do **not** need to mark `src` as Sources Root if you always run from the
   project root with `uvicorn src.app:app`. Running from the root is enough.

### 5. Terminals

Use PyCharm’s **Terminal** tab in the **lab** window for all checkpoints
(`pip`, `uvicorn`, `npm`, `curl`). Keep the working directory at the **lab root**.

## Checkpoint

Do **not** continue to the next lesson until this passes.


In the lab terminal:

```powershell
python --version
node --version
```

Python ≥ 3.11 and Node ≥ 20.

---

| Previous | Next |
|:---------|-----:|
| ← [README](./README.md) | [Overview](./02-overview.md) → |
