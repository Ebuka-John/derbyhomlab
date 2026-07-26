"use client";

import { FormEvent, useId, useState, useTransition } from "react";

import type { LookupResult, NearestGritBinSuccess } from "@/lib/types";

const DEFAULT_POSTCODE = "DE55 5PB";
const DEFAULT_ADDRESS = "HILLBROW";

async function lookupNearest(postcode: string, address: string): Promise<LookupResult> {
  const params = new URLSearchParams({ postcode, address });
  const response = await fetch(`/api/nearest-grit-bin?${params.toString()}`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  const payload = await response.json();

  if (!response.ok) {
    return {
      ok: false,
      status: response.status,
      error: payload?.error ?? {
        code: "unknown_error",
        message: "Unexpected response from the API.",
      },
    };
  }

  return { ok: true, data: payload as NearestGritBinSuccess };
}

export function SearchForm() {
  const formId = useId();
  const postcodeId = `${formId}-postcode`;
  const addressId = `${formId}-address`;
  const statusId = `${formId}-status`;

  const [postcode, setPostcode] = useState(DEFAULT_POSTCODE);
  const [address, setAddress] = useState(DEFAULT_ADDRESS);
  const [result, setResult] = useState<NearestGritBinSuccess | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedPostcode = postcode.trim();
    const trimmedAddress = address.trim();

    if (!trimmedPostcode || !trimmedAddress) {
      setError("Enter both a postcode and an address.");
      setResult(null);
      return;
    }

    startTransition(async () => {
      setError(null);
      setResult(null);

      try {
        const outcome = await lookupNearest(trimmedPostcode, trimmedAddress);
        if (outcome.ok) {
          setResult(outcome.data);
        } else {
          setError(outcome.error.message);
        }
      } catch {
        setError("Something went wrong while contacting the API.");
      }
    });
  }

  return (
    <section className="panel" aria-labelledby={`${formId}-heading`}>
      <header className="panel__intro">
        <h2 id={`${formId}-heading`} className="panel__heading">
          Look up an address
        </h2>
        <p className="panel__lede">
          Resolves the property via the Address API, then finds the nearest grit
          bin within 100 metres on GeoServer WFS.
        </p>
      </header>

      <form className="form" onSubmit={onSubmit} noValidate>
        <div className="field">
          <label htmlFor={postcodeId}>Postcode</label>
          <input
            id={postcodeId}
            name="postcode"
            type="text"
            autoComplete="postal-code"
            inputMode="text"
            spellCheck={false}
            value={postcode}
            onChange={(event) => setPostcode(event.target.value)}
            placeholder="DE55 5PB"
            disabled={isPending}
            required
          />
        </div>

        <div className="field">
          <label htmlFor={addressId}>Address</label>
          <input
            id={addressId}
            name="address"
            type="text"
            autoComplete="street-address"
            spellCheck={false}
            value={address}
            onChange={(event) => setAddress(event.target.value)}
            placeholder="HILLBROW"
            disabled={isPending}
            required
          />
        </div>

        <div className="form__actions">
          <button type="submit" className="button" disabled={isPending}>
            {isPending ? "Searching…" : "Find nearest grit bin"}
          </button>
        </div>
      </form>

      <div
        id={statusId}
        className="status"
        role="status"
        aria-live="polite"
        aria-atomic="true"
      >
        {isPending ? <p className="status__pending">Querying backend…</p> : null}

        {error ? (
          <div className="result result--error">
            <p className="result__label">Could not resolve</p>
            <p className="result__message">{error}</p>
          </div>
        ) : null}

        {result ? (
          <div className="result result--ok">
            <p className="result__label">Nearest grit bin</p>
            <p className="result__title">{result.nearest_grit_bin_title}</p>
            <dl className="result__meta">
              <div>
                <dt>Distance</dt>
                <dd>{result.distance_meters.toFixed(2)} m</dd>
              </div>
              <div>
                <dt>Address</dt>
                <dd>{result.address}</dd>
              </div>
              <div>
                <dt>Postcode</dt>
                <dd>{result.postcode}</dd>
              </div>
            </dl>
          </div>
        ) : null}
      </div>
    </section>
  );
}
