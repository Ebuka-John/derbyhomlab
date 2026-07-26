# Backend — Python & FastAPI basics (read first)

You do **not** need to be a professional engineer to follow this lab. This page
explains the building blocks you will see in the Python files, in plain language.

Skim it once. When a later step says “see the primer”, come back here.

---

## 1. Files and imports

A `.py` file is a **module**. A folder of modules with `__init__.py` is a
**package**.

```python
from src.config import Settings
from src.utils.exceptions import MissingParameterError
from src.models.domain.geometry import Point27700
from src.utils.geospatial import euclidean_distance_meters
```

Each line imports from a layer in the codebase (`config`, `utils/exceptions`,
`models/domain`, `utils/geospatial`). That is how pieces of the app talk to
each other without pasting all the code into one giant file.

---

## 2. Functions

A **function** is a named recipe. You define it once, call it many times.

```python
def add(a: int, b: int) -> int:
    return a + b

add(2, 3)  # → 5
```

- `a: int` is a **type hint** — a note for humans and tools saying “expect an int”
- `-> int` means “this function returns an int”
- Type hints do **not** change how Python runs (unless a library uses them, like
  Pydantic / FastAPI)

---

## 3. Classes and objects (OOP)

**OOP** = Object-Oriented Programming. The idea: group related data + behaviour
into a **class** (the blueprint). When you create one, you get an **object**
(also called an **instance**).

```python
class Dog:
    def __init__(self, name: str) -> None:
        self.name = name          # data stored on this object

    def bark(self) -> str:        # behaviour (a method)
        return f"{self.name} says woof"
```

| Word | Meaning |
|------|---------|
| `class Dog` | Blueprint named Dog |
| `__init__` | Constructor — runs when you create a Dog |
| `self` | “This particular Dog” (the current instance) |
| `self.name` | Data belonging to this Dog |
| `bark` | A **method** — a function that lives on the class |
| `Dog("Rex")` | Create one object |

```python
rex = Dog("Rex")
rex.bark()   # → "Rex says woof"
```

### Inheritance

A class can **extend** another class and reuse its behaviour.

```python
class AppError(Exception):
    ...

class MissingParameterError(AppError):
    ...
```

`MissingParameterError` **is an** `AppError`. Anything that handles `AppError`
also handles the specific ones. That is how our error system works.

### `super()`

Inside a child class, `super().__init__(...)` means “run the parent’s constructor
first, then add our own bits.”

---

## 4. Dataclasses

Writing `__init__` just to store fields gets boring. `@dataclass` auto-builds
that for you:

```python
from src.models.domain.geometry import Point27700

Point27700(easting=440000, northing=355000)
```

In our codebase, `Point27700` is a **domain value object** in
`src/models/domain/geometry.py` — a `@dataclass(frozen=True, slots=True)` that
documents British National Grid coordinates. `frozen=True` means fields cannot
be changed after creation (safer).

Still OOP — just less boilerplate.

---

## 5. Decorators (`@something`)

A **decorator** is a sticker that wraps a function or method and changes how it
behaves.

```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

`@app.get("/health")` tells FastAPI: “when someone GETs `/health`, run this
function.” You did not write the web-server wiring yourself — the decorator did.

Other decorators you will see:

| Decorator | Rough meaning |
|-----------|----------------|
| `@lru_cache` | Remember the return value; don’t recompute every time |
| `@property` | Call like `obj.thing` instead of `obj.thing()` |
| `@classmethod` | Method that receives the **class**, not an instance (`cls`) |
| `@dataclass` | Auto-generate `__init__` and friends |

---

## 6. Async / await (why FastAPI feels “async”)

Calling an external API takes time. If the server waits with a normal function,
it sits idle. **Async** lets it start other work while waiting.

```python
async def lookup_postcode(self, postcode: str):
    response = await self._client.get(url)
```

- `async def` — this function can pause
- `await` — “pause here until this network call finishes”
- FastAPI endpoints are usually `async def` so they can await HTTP clients like
  `httpx`

You do not need to master concurrency. Rule of thumb: if you call the network,
use `async`/`await`.

---

## 7. Exceptions (`raise` / `try` / `except`)

When something goes wrong, Python can **raise** an error:

```python
from src.utils.exceptions import MissingParameterError

raise MissingParameterError("postcode")
```

Later, FastAPI catches that error and turns it into a JSON response. That is
cleaner than returning random error strings from every function.

```python
try:
    features = await repo.query_dwithin(...)
except GeoServerUnreachableError:
    features = await repo.fetch_all()  # fallback plan
```

---

## 8. Pydantic (data shapes)

**Pydantic** checks that data matches a shape you declare. FastAPI uses it for:

- Request / response bodies
- Settings from environment variables (`pydantic-settings`)

```python
class NearestGritBinResponse(BaseModel):
    address: str
    postcode: str
    nearest_grit_bin_title: str
    distance_meters: float
```

If something is missing or the wrong type, Pydantic complains early — before bad
data spreads through the app.

---

## 9. FastAPI in one minute

FastAPI is a library that turns Python functions into HTTP endpoints.

```python
app = FastAPI(...)

@app.get("/nearest-grit-bin")
async def nearest_grit_bin(postcode: str, address: str):
    ...
```

- `app` is the web application object
- `@app.get(...)` registers a route
- Query params become function arguments
- Return a Pydantic model (or dict) → FastAPI turns it into JSON
- Open `/docs` → interactive API documentation, generated for free

---

## 10. Glossary cheat sheet

| Term | Plain meaning |
|------|----------------|
| Module | One `.py` file |
| Package | Folder of modules |
| Class | Blueprint |
| Instance / object | One concrete thing made from a class |
| Method | Function on a class |
| Attribute | Data on an object (`self.x`) |
| Inheritance | Child class reuses parent class |
| Type hint | Optional note about types |
| Decorator | `@` wrapper that changes a function |
| Async | Pause-friendly function for I/O |
| Exception | Structured “something went wrong” |
| Endpoint / route | A URL + HTTP method your API handles |


---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Backend design](./00-backend-design.md) | [Requirements](./01-requirements.md) → |
