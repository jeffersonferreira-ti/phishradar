"use client";

import { FormEvent, useState } from "react";
import { analyzeContent } from "@/lib/phishradar-api";
import type { AnalyzeResponse } from "@/types/analysis";

const SAMPLE_CONTENT =
  "Urgent: confirm your password at https://login-secure-account-update.example.com now.";

export default function Home() {
  const [content, setContent] = useState("");
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setResult(null);

    if (!content.trim()) {
      setError("Enter content before running analysis.");
      return;
    }

    setIsLoading(true);

    try {
      const analysis = await analyzeContent({ content });
      setResult(analysis);
    } catch (error) {
      const developmentDetail =
        process.env.NODE_ENV === "development" && error instanceof Error
          ? ` (${error.message})`
          : "";

      setError(
        `Could not analyze the content. Please try again.${developmentDetail}`,
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main>
      <section className="header">
        <h1>PhishRadar</h1>
        <p>
          Paste a message, URL, or raw e-mail content to analyze phishing and
          fraud risk signals.
        </p>
      </section>

      <section className="workspace" aria-label="Analysis workspace">
        <form className="panel form" onSubmit={handleSubmit}>
          <label className="field-label" htmlFor="content">
            Content
          </label>
          <textarea
            id="content"
            name="content"
            value={content}
            onChange={(event) => setContent(event.target.value)}
            placeholder={SAMPLE_CONTENT}
          />

          <div className="actions">
            <button type="submit" disabled={isLoading}>
              {isLoading ? "Analyzing..." : "Analyze"}
            </button>
            {isLoading ? (
              <span className="status-text">Request in progress</span>
            ) : null}
          </div>

          {error ? <p className="error">{error}</p> : null}
        </form>

        <aside className="panel result" aria-live="polite">
          <h2>Result</h2>

          {result ? (
            <>
              <div className="metrics">
                <div className="metric">
                  <span>Score</span>
                  <strong>{result.score}</strong>
                </div>
                <div className="metric">
                  <span>Label</span>
                  <strong>{result.label}</strong>
                </div>
              </div>

              {result.reasons.length > 0 ? (
                <ul className="reasons">
                  {result.reasons.map((reason) => (
                    <li key={reason}>{reason}</li>
                  ))}
                </ul>
              ) : (
                <p className="empty-state">No risk signals detected.</p>
              )}
            </>
          ) : (
            <p className="empty-state">Analysis results will appear here.</p>
          )}
        </aside>
      </section>
    </main>
  );
}
