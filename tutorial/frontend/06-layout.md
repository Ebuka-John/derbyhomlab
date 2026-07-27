# Frontend Step 6a — Root layout

## What you will do

1. Create the empty file in your editor (from the project root).
2. Open it and type the code carefully.
3. Run the checkpoint before continuing.

## File to create: `app/layout.tsx`

### Create this file in the editor

Create `frontend/app/layout.tsx` in your editor (from the project root), then type the contents below yourself.

**Path:** `app/layout.tsx` (relative to `frontend/`)

### Purpose

Root HTML shell, fonts, metadata, and global CSS import.

### Type this exactly

```tsx
import type { Metadata } from "next";
import { Fraunces, Figtree } from "next/font/google";

import "./globals.css";

const display = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
});

const sans = Figtree({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Gritfinder — nearest grit bin",
  description:
    "Test console for the nearest grit bin API. Enter a postcode and address to locate the closest Derbyshire grit bin within 100 metres.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${display.variable} ${sans.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

### How the code works

#### Concepts in this file

| Concept | Where | Plain meaning |
|---------|-------|---------------|
| **Layout** | `RootLayout` | Wraps **every** page. Shared shell for `<html>`, fonts, and CSS. |
| **`{children}`** | prop | Slot where the current page (`page.tsx`) is inserted. |
| **Server component** | default (no `"use client"`) | Runs on the server; no browser hooks needed here. |
| **Metadata** | `export const metadata` | Sets the browser tab title and description. |

Fonts are loaded once here and exposed as CSS variables used by `globals.css`.

## Checkpoint

Continue to the CSS step.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Search form](./05-search-form.md) | [Globals CSS](./07-globals-css.md) → |
