# Backend Step 2 — Environment files

## What you will do

1. Create a safe template `.env.example` (PowerShell + type contents).
2. Copy it to `.env` and fill real values.
3. Make sure `.env` is gitignored.

## File to create: `.env.example`

**Path:** `.env.example` (project root)

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path .env.example | Out-Null
```

Open `.env.example` in your editor and **type this exactly:**

```text
# Address Lookup API
ADDRESS_API_BASE_URL=https://example.com/DerbyshireApplicationsWebService/api/Address
ADDRESS_API_ALIAS=example
ADDRESS_API_AUTH_TOKEN=exampletoken

# GeoServer WFS
GEOSERVER_BASE_URL=https://wms.derbyshire.gov.uk/geoserver
GEOSERVER_LAYER=DCC:Gritbins

# Optional tuning
NEAREST_SEARCH_RADIUS_METERS=100
HTTP_TIMEOUT_SECONDS=30
```

### Why this file

Documents which variables exist without committing real secrets.

---

## File to create: `.env`

**Path:** `.env` (project root)

### Create it in PowerShell (project root)

```powershell
Copy-Item .env.example .env
```

Open `.env` in your editor and replace the Address API values with your real
credentials:

- `ADDRESS_API_BASE_URL` — the real base URL you were given
- `ADDRESS_API_ALIAS` — your alias
- `ADDRESS_API_AUTH_TOKEN` — your token

Leave the GeoServer and tuning values as they are.

Confirm the file is visible (dotfiles can be hidden):

```powershell
Get-ChildItem -Force .env, .env.example
```

> Some editors hide dotfiles. If `.env` disappears from the file tree, it still
> exists — use `Get-ChildItem -Force` or your editor's "show hidden files"
> setting.

### Why this file

`src/config.py` (next steps) loads these at startup. Without them the API will not
start correctly.

---

## Also do this — `.gitignore`

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path .gitignore | Out-Null
```

Open `.gitignore` and type at least:

```text
.env
.venv/
__pycache__/
```

(If you already have a fuller `.gitignore` from the finished repo, keep that.)

## Checkpoint

```powershell
Test-Path .env
Get-Item .env | Select-Object Name, Length
```

- `.env` exists next to `requirements.txt`
- File is named `.env` (not `.env.txt`)
- You have filled `ADDRESS_API_*` if you want live lookups

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Requirements](./01-requirements.md) | [Init packages](./03-init-packages.md) → |
