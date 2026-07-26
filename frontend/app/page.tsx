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
