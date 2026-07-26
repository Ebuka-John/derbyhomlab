# Frontend Step 7 — Home page

## What you will do

1. Create the file at the path below (inside `frontend/`).
2. Type the code carefully.
3. Run the checkpoint before continuing.

## File to create: `app/page.tsx`

**Path:** `app/page.tsx` (relative to `frontend/`)

### Purpose

The `/` page: hero copy plus the SearchForm.

### Type this exactly

```tsx
import { SearchForm } from "@/components/SearchForm";

export default function HomePage() {
  return (
    <main className="shell">
      <div className="atmosphere" aria-hidden="true" />

      <div className="frame">
        <header className="hero">
          <p className="hero__brand">Gritfinder</p>
          <h1 className="hero__title">Find the nearest grit bin</h1>
          <p className="hero__support">
            Integration test UI for the Derbyshire nearest-grit-bin service.
            Calls the FastAPI backend through a Next.js proxy — never the
            upstream APIs from the browser.
          </p>
        </header>

        <SearchForm />

        <footer className="foot">
          <p>
            Example: <span>HILLBROW</span>, <span>DE55 5PB</span> → expected grit
            bin nearby within 100&nbsp;m.
          </p>
        </footer>
      </div>
    </main>
  );
}
```

### How the code works

#### Concepts in this file

| Concept | Where | Plain meaning |
|---------|-------|---------------|
| **Page = route** | `app/page.tsx` | This file is the `/` URL. |
| **Composition** | `<SearchForm />` | Build UIs by nesting components — page owns layout, form owns interactivity. |
| **Server + client mix** | page (server) + SearchForm (client) | Static shell on the server; interactive bits in the browser. |

The page stays thin on purpose: branding and structure here, behaviour in `SearchForm`.

## Checkpoint

Once the app runs, open http://127.0.0.1:3000 and confirm the form appears.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Globals CSS](./07-globals-css.md) | [Frontend run and test](./09-run-and-test.md) → |
