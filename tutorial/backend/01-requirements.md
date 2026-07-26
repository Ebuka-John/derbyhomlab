# Backend Step 1 — Dependencies

## What you will do

1. Create two dependency files by hand at the project root.
2. Create a Python virtual environment.
3. Install packages.

> Create every file in this lab **manually** in your editor: create a new file in
> the correct folder, type the exact filename, then type the contents. Do not
> generate them with scripts.

## File to create: `requirements.txt`

**Path:** `requirements.txt` (project root)

**Type this exactly:**

```text
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
httpx>=0.27.0
python-dotenv>=1.0.1
pyproj>=3.6.1
pydantic>=2.9.0
pydantic-settings>=2.5.0
```

### Why this file

`pip` reads it to install everything FastAPI needs: the web framework, the ASGI
server, HTTP client, env loading, coordinate conversion, and settings validation.

---

## File to create: `requirements-dev.txt`

**Path:** `requirements-dev.txt` (project root)

**Type this exactly:**

```text
-r requirements.txt

pytest>=8.3.0
pytest-asyncio>=0.24.0
respx>=0.21.1
```

### Why this file

Adds test tools. `-r requirements.txt` includes the runtime deps too.

---

## Commands to run now

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

(Optional later for tests: `pip install -r requirements-dev.txt`)

## Checkpoint

- Virtualenv is active (prompt shows `.venv`)
- `pip show fastapi` prints package info

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Python / FastAPI basics](./00-python-fastapi-basics.md) | [Backend env](./02-env.md) → |
