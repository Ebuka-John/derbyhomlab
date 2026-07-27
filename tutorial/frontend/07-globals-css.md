# Frontend Step 6b — Global styles

## What you will do

1. Create the empty file in your editor (from the project root).
2. Open it and type the code carefully.
3. Run the checkpoint before continuing.

## File to create: `app/globals.css`

### Create this file in the editor

Create `frontend/app/globals.css` in your editor (from the project root), then type the contents below yourself.

**Path:** `app/globals.css` (relative to `frontend/`)

### Purpose

All visual styling for the shell, form, and result cards.

### Type this exactly

```css
:root {
  --ink: #1c241c;
  --ink-soft: #3d4a3d;
  --paper: #e8efe4;
  --paper-elevated: #f3f7f0;
  --moss: #2f5d3a;
  --moss-deep: #1f3d28;
  --ochre: #c48a2a;
  --ochre-soft: #e2b45a;
  --danger: #8b2e2e;
  --danger-bg: #f6e8e6;
  --ok-bg: #e4efe6;
  --line: rgba(28, 36, 28, 0.14);
  --shadow: 0 18px 40px rgba(20, 32, 22, 0.12);
  --radius: 14px;
  --font-display: "Fraunces", Georgia, serif;
  --font-sans: "Figtree", "Segoe UI", sans-serif;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  min-height: 100%;
}

body {
  color: var(--ink);
  font-family: var(--font-sans);
  background: var(--paper);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

button,
input {
  font: inherit;
}

.shell {
  position: relative;
  isolation: isolate;
  min-height: 100dvh;
  overflow: clip;
}

.atmosphere {
  position: absolute;
  inset: 0;
  z-index: -1;
  background:
    radial-gradient(1200px 600px at 12% -10%, rgba(196, 138, 42, 0.22), transparent 60%),
    radial-gradient(900px 500px at 100% 10%, rgba(47, 93, 58, 0.28), transparent 55%),
    linear-gradient(160deg, #d7e4d4 0%, #eef3ea 42%, #d9e6dc 100%);
}

.atmosphere::after {
  content: "";
  position: absolute;
  inset: 0;
  opacity: 0.35;
  background-image:
    linear-gradient(rgba(28, 36, 28, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(28, 36, 28, 0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.55), transparent 85%);
}

.frame {
  width: min(720px, calc(100% - 2rem));
  margin: 0 auto;
  padding: clamp(2.5rem, 8vw, 5rem) 0 3rem;
  display: grid;
  gap: 2rem;
  animation: rise 520ms ease-out both;
}

.hero {
  display: grid;
  gap: 0.75rem;
}

.hero__brand {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 7vw, 3.6rem);
  font-weight: 650;
  letter-spacing: -0.03em;
  line-height: 0.95;
  color: var(--moss-deep);
}

.hero__title {
  margin: 0;
  max-width: 14ch;
  font-family: var(--font-display);
  font-size: clamp(1.55rem, 4.2vw, 2.15rem);
  font-weight: 560;
  letter-spacing: -0.02em;
  line-height: 1.15;
  color: var(--ink);
}

.hero__support {
  margin: 0;
  max-width: 42ch;
  color: var(--ink-soft);
  font-size: 1.05rem;
}

.panel {
  background: color-mix(in srgb, var(--paper-elevated) 88%, white);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: clamp(1.25rem, 3vw, 1.75rem);
  display: grid;
  gap: 1.25rem;
}

.panel__intro {
  display: grid;
  gap: 0.35rem;
}

.panel__heading {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 650;
}

.panel__lede {
  margin: 0;
  color: var(--ink-soft);
  font-size: 0.98rem;
}

.form {
  display: grid;
  gap: 1rem;
}

.field {
  display: grid;
  gap: 0.4rem;
}

.field label {
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--ink-soft);
}

.field input {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: #fff;
  color: var(--ink);
  padding: 0.85rem 0.95rem;
  transition: border-color 160ms ease, box-shadow 160ms ease;
}

.field input:focus {
  outline: none;
  border-color: color-mix(in srgb, var(--moss) 65%, black);
  box-shadow: 0 0 0 3px rgba(47, 93, 58, 0.18);
}

.field input:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.form__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding-top: 0.25rem;
}

.button {
  appearance: none;
  border: 0;
  border-radius: 10px;
  background: linear-gradient(180deg, var(--moss) 0%, var(--moss-deep) 100%);
  color: #f5faf4;
  font-weight: 650;
  padding: 0.9rem 1.2rem;
  cursor: pointer;
  transition: transform 140ms ease, filter 140ms ease, opacity 140ms ease;
}

.button:hover:not(:disabled) {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

.button:active:not(:disabled) {
  transform: translateY(0);
}

.button:disabled {
  opacity: 0.7;
  cursor: wait;
}

.status {
  min-height: 1.5rem;
}

.status__pending {
  margin: 0;
  color: var(--ink-soft);
  font-size: 0.95rem;
  animation: pulse 1.1s ease-in-out infinite;
}

.result {
  border-radius: 12px;
  padding: 1rem 1.1rem;
  display: grid;
  gap: 0.45rem;
  animation: fade-up 280ms ease-out both;
}

.result--ok {
  background: var(--ok-bg);
  border: 1px solid color-mix(in srgb, var(--moss) 28%, transparent);
}

.result--error {
  background: var(--danger-bg);
  border: 1px solid color-mix(in srgb, var(--danger) 30%, transparent);
}

.result__label {
  margin: 0;
  font-size: 0.8rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-weight: 700;
  color: var(--ink-soft);
}

.result__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 4vw, 2.3rem);
  line-height: 1.05;
  color: var(--moss-deep);
}

.result__message {
  margin: 0;
  color: var(--danger);
  font-weight: 560;
}

.result__meta {
  margin: 0.5rem 0 0;
  display: grid;
  gap: 0.55rem;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
}

.result__meta div {
  display: grid;
  gap: 0.15rem;
}

.result__meta dt {
  margin: 0;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--ink-soft);
  font-weight: 700;
}

.result__meta dd {
  margin: 0;
  font-weight: 600;
}

.foot {
  color: var(--ink-soft);
  font-size: 0.92rem;
}

.foot p {
  margin: 0;
}

.foot span {
  color: var(--ink);
  font-weight: 650;
}

@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.55;
  }
  50% {
    opacity: 1;
  }
}

@media (max-width: 560px) {
  .frame {
    width: min(100% - 1.25rem, 720px);
    gap: 1.5rem;
  }

  .form__actions {
    flex-direction: column;
  }

  .button {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .frame,
  .result,
  .status__pending,
  .button {
    animation: none !important;
    transition: none !important;
  }
}
```

### How the code works

Presentation only — no API logic. Class names must match `page.tsx` and `SearchForm.tsx`.

## Checkpoint

Continue to the home page step.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Layout](./06-layout.md) | [Page](./08-page.md) → |
