# Backend Step 1 — Dependencies

## What you will do

1. Create two dependency files at the project root in your editor (type the contents).
2. Create a Python virtual environment.
3. Activate it and install packages.

## File to create: `requirements.txt`

**Path:** `requirements.txt` (project root)

### Create this file in the editor

Create `requirements.txt` in your editor (from the project root), then type the contents below yourself.

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

### Create this file in the editor

Create `requirements-dev.txt` in your editor (from the project root), then type the contents below yourself.

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

Type and run these in PowerShell from the **project root**:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation fails with an execution-policy error:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Then install dependencies (venv must be active — prompt shows `(.venv)`):

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

(Optional later for tests: `pip install -r requirements-dev.txt`)

## Checkpoint

```powershell
# Prompt should show (.venv)
pip show fastapi
```

- Virtualenv is active (prompt shows `(.venv)`)
- `pip show fastapi` prints package info

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Python / FastAPI basics](./00-python-fastapi-basics.md) | [Backend env](./02-env.md) → |
