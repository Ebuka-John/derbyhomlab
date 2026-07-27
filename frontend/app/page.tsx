import { SearchForm } from "@/components/SearchForm";

export default function HomePage() {
  return (
    <main className="shell">
      <div className="atmosphere" aria-hidden="true" />

      <div className="frame">
        <header className="hero">
          <p className="hero__brand">Gritfinder</p>
        </header>

        <SearchForm />

        <footer className="foot">
          <p>
            Example: <span>Example Building</span>, <span>AB12 3CD</span> →
            nearest grit bin within 100&nbsp;m.
          </p>
        </footer>
      </div>
    </main>
  );
}
