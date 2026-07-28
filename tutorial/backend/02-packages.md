# Backend 2 — Package tree

## Concept

Python needs packages (`__init__.py`) so imports like
`from src.services.address_service import AddressService` work.

Layers map to folders:

| Folder | Job |
|--------|-----|
| `core/` | Settings, logging |
| `utils/` | Errors, CRS, postcode |
| `models/domain` | Internal shapes |
| `models/dto` | API request/response models |
| `repositories/` | Upstream HTTP |
| `services/` | Business rules |
| `api/` | FastAPI routers + Depends |

## Create folders (lab)

Right-click project root → `New → Directory` / `Python Package` as needed:

```text
src/
  core/
  api/
    routers/
    dependencies/
  services/
  repositories/
  models/
    dto/
    domain/
  utils/
```

## Type these `__init__.py` files (from reference)

Open each path in the reference window and type the same content into the lab
(many are empty or a one-line docstring):

| Create in lab | Type from reference |
|---------------|---------------------|
| `src/__init__.py` | `src/__init__.py` |
| `src/core/__init__.py` | `src/core/__init__.py` |
| `src/api/__init__.py` | `src/api/__init__.py` |
| `src/api/routers/__init__.py` | `src/api/routers/__init__.py` |
| `src/api/dependencies/__init__.py` | create empty file for now — full content in step 8 |
| `src/services/__init__.py` | `src/services/__init__.py` |
| `src/repositories/__init__.py` | `src/repositories/__init__.py` |
| `src/models/__init__.py` | `src/models/__init__.py` |
| `src/models/dto/__init__.py` | `src/models/dto/__init__.py` |
| `src/models/domain/__init__.py` | `src/models/domain/__init__.py` |
| `src/utils/__init__.py` | `src/utils/__init__.py` |

> Leave `src/api/dependencies/__init__.py` empty until step 8 (providers need services).

## Checkpoint

Do **not** continue to the next lesson until this passes.


```powershell
.\.venv\Scripts\Activate.ps1
python -c "import src; print('ok')"
```

## Deeper reading

- `main`: `tutorial/backend/03-init-packages.md`, `tutorial/03-folder-structure.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Requirements](./01-requirements-env.md) | [Config](./03-config.md) → |
