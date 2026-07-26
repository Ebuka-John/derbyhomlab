"use client";

import { FormEvent, useId, useState, useTransition } from "react";

import type {
  ApiErrorBody,
  GritBinsSuccess,
  LookupResult,
  NearestGritBinsSuccess,
} from "@/lib/types";

const DEFAULT_POSTCODE = "DE55 5PB";
const DEFAULT_ADDRESS = "HILLBROW";
const DEFAULT_LIMIT = 5;

async function parseLookup<T>(response: Response): Promise<LookupResult<T>> {
  const payload = await response.json();

  if (!response.ok) {
    return {
      ok: false,
      status: response.status,
      error: (payload as ApiErrorBody)?.error ?? {
        code: "unknown_error",
        message: "Unexpected response from the API.",
      },
    };
  }

  return { ok: true, data: payload as T };
}

async function lookupNearestN(
  postcode: string,
  address: string,
  limit: number,
): Promise<LookupResult<NearestGritBinsSuccess>> {
  const params = new URLSearchParams({
    postcode,
    address,
    limit: String(limit),
  });
  const response = await fetch(`/api/nearest-grit-bins?${params.toString()}`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  return parseLookup<NearestGritBinsSuccess>(response);
}

async function lookupAllBins(): Promise<LookupResult<GritBinsSuccess>> {
  const response = await fetch("/api/grit-bins", {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  return parseLookup<GritBinsSuccess>(response);
}

export function SearchForm() {
  const formId = useId();
  const postcodeId = `${formId}-postcode`;
  const addressId = `${formId}-address`;
  const limitId = `${formId}-limit`;
  const statusId = `${formId}-status`;

  const [postcode, setPostcode] = useState(DEFAULT_POSTCODE);
  const [address, setAddress] = useState(DEFAULT_ADDRESS);
  const [limit, setLimit] = useState(DEFAULT_LIMIT);
  const [nearest, setNearest] = useState<NearestGritBinsSuccess | null>(null);
  const [allBins, setAllBins] = useState<GritBinsSuccess | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();
  const [pendingAction, setPendingAction] = useState<"nearest" | "all" | null>(
    null,
  );

  function clearResults() {
    setError(null);
    setNearest(null);
    setAllBins(null);
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedPostcode = postcode.trim();
    const trimmedAddress = address.trim();
    const safeLimit = Math.min(50, Math.max(1, Math.trunc(limit) || 1));

    if (!trimmedPostcode || !trimmedAddress) {
      setError("Enter both a postcode and an address.");
      setNearest(null);
      setAllBins(null);
      return;
    }

    setPendingAction("nearest");
    startTransition(async () => {
      clearResults();

      try {
        const outcome = await lookupNearestN(
          trimmedPostcode,
          trimmedAddress,
          safeLimit,
        );
        if (outcome.ok) {
          setNearest(outcome.data);
        } else {
          setError(outcome.error.message);
        }
      } catch {
        setError("Something went wrong while contacting the API.");
      } finally {
        setPendingAction(null);
      }
    });
  }

  function onListAll() {
    setPendingAction("all");
    startTransition(async () => {
      clearResults();

      try {
        const outcome = await lookupAllBins();
        if (outcome.ok) {
          setAllBins(outcome.data);
        } else {
          setError(outcome.error.message);
        }
      } catch {
        setError("Something went wrong while contacting the API.");
      } finally {
        setPendingAction(null);
      }
    });
  }

  return (
    <section className="panel" aria-labelledby={`${formId}-heading`}>
      <header className="panel__intro">
        <h2 id={`${formId}-heading`} className="panel__heading">
          Look up grit bins
        </h2>
        <p className="panel__lede">
          Resolve an address, then rank the closest grit bins by distance across
          the layer — or list every Derbyshire WFS feature.
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

        <div className="field field--narrow">
          <label htmlFor={limitId}>How many nearest</label>
          <input
            id={limitId}
            name="limit"
            type="number"
            min={1}
            max={50}
            step={1}
            value={limit}
            onChange={(event) => setLimit(Number(event.target.value))}
            disabled={isPending}
          />
        </div>

        <div className="form__actions">
          <button type="submit" className="button" disabled={isPending}>
            {pendingAction === "nearest"
              ? "Searching…"
              : "Find nearest grit bins"}
          </button>
          <button
            type="button"
            className="button button--secondary"
            disabled={isPending}
            onClick={onListAll}
          >
            {pendingAction === "all" ? "Loading…" : "List all grit bins"}
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

        {nearest ? (
          <div className="result result--ok">
            <p className="result__label">Nearest grit bins</p>
            <p className="result__context">
              {nearest.address}, {nearest.postcode}
            </p>
            <ol className="rank-list">
              {nearest.nearest_grit_bins.map((bin, index) => (
                <li key={`${bin.title}-${index}`} className="rank-list__item">
                  <span className="rank-list__index">{index + 1}</span>
                  <span className="rank-list__title">{bin.title}</span>
                  <span className="rank-list__distance">
                    {bin.distance_meters.toFixed(2)} m
                  </span>
                </li>
              ))}
            </ol>
          </div>
        ) : null}

        {allBins ? (
          <div className="result result--ok">
            <p className="result__label">All grit bins</p>
            <p className="result__context">{allBins.count} features from WFS</p>
            <div className="bin-scroll" tabIndex={0}>
              <table className="bin-table">
                <thead>
                  <tr>
                    <th scope="col">Title</th>
                    <th scope="col">Easting</th>
                    <th scope="col">Northing</th>
                  </tr>
                </thead>
                <tbody>
                  {allBins.grit_bins.map((bin, index) => (
                    <tr key={`${bin.title}-${bin.easting}-${index}`}>
                      <td>{bin.title}</td>
                      <td>{bin.easting.toFixed(1)}</td>
                      <td>{bin.northing.toFixed(1)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ) : null}
      </div>
    </section>
  );
}
