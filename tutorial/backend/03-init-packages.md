# Backend Step 3 — Python packages

## What you will do

Create the `src` package folders and the `__init__.py` marker files **by hand** in
your editor, so imports like `from src.config import …` work.

## Folders to create

In your editor's file explorer, right-click the **project root** and create these
folders one at a time:

1. `src`
2. `src/services` (create `services` **inside** `src`)
3. `src/utils` (create `utils` **inside** `src`)

When you are done the tree looks like this:

```
your-project/
├── requirements.txt
├── .env
└── src/
    ├── services/
    └── utils/
```

> Hover the project root in your editor's file tree, create a new folder, type
> the name, and confirm. Repeat for each folder.

## Files to create

Create each file by adding a new file in the folder and typing the filename.

### 1. `src/__init__.py`

Create the file, then type this single line:

```python
"""Package marker for src."""
```

### 2. `src/services/__init__.py`

Create the file and **leave it empty**. Nothing to type — just save it.

### 3. `src/utils/__init__.py`

Create the file and **leave it empty**. Save it.

Your tree should now be:

```
src/
├── __init__.py
├── services/
│   └── __init__.py
└── utils/
    └── __init__.py
```

## Why these files

### Concept: packages and imports

Python needs a marker to treat a folder as a **package** (a group of importable
modules). That marker is `__init__.py`.

Without it, this later line fails:

```python
from src.utils.errors import AppError
```

With the three `__init__.py` files in place, Python can walk:

`src` → `utils` → `errors.py` and find `AppError`.

> Primer: [00-python-fastapi-basics.md](./00-python-fastapi-basics.md) §1.

## Checkpoint

Run this from the project root:

```powershell
python -c "import src; print('ok')"
```

Should print `ok`. If you get `ModuleNotFoundError`, check that you are in the
project root and that `src/__init__.py` exists.

## Next

→ [04-config.md](./04-config.md)
