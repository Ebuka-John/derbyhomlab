# Backend 1 — Requirements & environment

## Concept

- **`requirements.txt`** — runtime deps (FastAPI, httpx, pyproj, pydantic-settings).
- **`requirements-dev.txt`** — test tools (pytest, …).
- **`.env.example`** — safe template; **`.env`** — real secrets (never commit).

Pydantic Settings will load `.env` at startup and fail fast if required keys are missing.

## Type these files (from reference)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `requirements.txt` | `requirements.txt` |
| 2 | `requirements-dev.txt` | `requirements-dev.txt` |
| 3 | `.env.example` | `.env.example` |
| 4 | `.env` | Copy `.env.example`, then fill real Address API values |

In PyCharm lab: project root → `New → File` for each.

## Install (lab Terminal)

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
```

## Checkpoint

Do **not** continue to the next lesson until this passes.


```powershell
python -c "import fastapi, httpx, pyproj, pydantic_settings; print('deps ok')"
```

Confirm `.env` exists and is **not** the same as committed secrets (use your real token).

## Deeper reading

- `main`: `tutorial/backend/01-requirements.md`, `tutorial/backend/02-env.md`, `tutorial/04-environment-variables.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Backend README](./README.md) | [Packages](./02-packages.md) → |
