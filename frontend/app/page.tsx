import { SearchForm } from "@/components/SearchForm";

export default function HomePage() {
  return (
    <main className="shell">
      <div className="atmosphere" aria-hidden="true" />

      <div className="frame">
        <header className="hero">
          <p className="hero__brand">Gritfinder</p>
          <h1 className="hero__title">Find nearby grit bins</h1>
          <p className="hero__support">
            Integration test UI for the Derbyshire grit-bin service. Rank the
            nearest N bins for an address, or list the full WFS layer — always
            through a Next.js proxy, never the upstream APIs from the browser.
          </p>
        </header>

        <SearchForm />

        <footer className="foot">
          <p>
            Example: <span>HILLBROW</span>, <span>DE55 5PB</span> → nearest
            bins within 100&nbsp;m, or the full layer via List all.
          </p>
        </footer>
      </div>
    </main>
  );
}
