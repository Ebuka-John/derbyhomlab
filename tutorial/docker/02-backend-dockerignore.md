# Docker Step 2 — Backend .dockerignore

## What you will do

Create `.dockerignore` with PowerShell (`New-Item`), then type its contents so
the backend image build does not send secrets, virtualenvs, or the frontend tree
into the Docker build context.

## File to create: `.dockerignore`

**Path:** `.dockerignore` (project root)

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path .dockerignore | Out-Null
```

Open `.dockerignore` in your editor and type the contents below yourself.

### Purpose

Same idea as `.gitignore`, but for `docker build`. Smaller context = faster builds
and less risk of baking secrets into layers.

### Type this exactly

```text
.git
.venv
venv
__pycache__
*.py[cod]
.pytest_cache
.mypy_cache
.ruff_cache
.coverage
htmlcov
.env
.env.*
!.env.example
*.md
tests
.vscode
.idea
.DS_Store
Dockerfile
docker-compose*.yml
.dockerignore
frontend
docs
```

### How the code works

- `.env` / `.env.*` are excluded — credentials never enter the image
- `.venv`, caches, and tests are excluded — not needed at runtime
- `frontend` is excluded — the backend image only needs Python code
- `!.env.example` keeps the safe template allowed if you ever need it (secrets still stay out)

## Checkpoint

Confirm `.dockerignore` sits next to `Dockerfile` at the project root.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Backend Dockerfile](./01-backend-dockerfile.md) | [Frontend Dockerfile](./03-frontend-dockerfile.md) → |
