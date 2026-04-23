# PhishRadar Roadmap

PhishRadar has moved from an initial heuristic prototype to a more structured and explainable phishing detection engine. This roadmap tracks what is already shipped, what is currently being refined, and where the product should evolve next.

---

## Completed

### Platform Foundations

- FastAPI backend for phishing analysis
- Next.js web application for manual inspection
- Chrome extension with page analysis and badge feedback
- automated test coverage for the risk engine

---

### Risk Engine v1

- deterministic rule-based scoring
- URL and domain extraction
- urgency and credential/payment signal detection
- suspicious URL keyword and structure analysis
- brand lookalike detection

---

### Risk Engine v2

Status: `Complete`

Recent improvements shipped in v2:

- improved score calibration with predictable thresholds
- new `MODERATE` risk level between `LOW_RISK` and `SUSPICIOUS`
- additive correlation rules for combined signals:
  - urgency + sensitive action
  - shortener + sensitive action
  - suspicious domain + sensitive action
- brand mismatch detection between message content and linked domains
- Brazilian scam pattern detection for delivery, fee, customs, PIX, and account-update narratives
- score breakdown system with:
  - `content_score`
  - `url_score`
  - `domain_score`
  - `brand_score`
  - `correlation_score`
- stronger explainability through reasons plus category-level attribution

---

## In Progress

### Product Maturity

- refining portfolio presentation assets and screenshots
- improving documentation consistency across README, roadmap, and demo materials
- expanding regression-style tests around real-world phishing scenarios

---

### Detection Quality

- reviewing additional false-negative cases for mixed content and URL scams
- identifying the next set of high-signal heuristics that improve recall without making the engine noisy

---

## Next Steps

### Detection Enhancements

- redirect analysis to inspect multi-hop destination chains
- domain reputation enrichment for stronger contextual scoring
- sender and email-header oriented signals for mailbox-focused scenarios
- broader brand coverage and regional scam narratives beyond the current Brazil-focused set

---

### Performance and Reliability

- shared caching strategy across API and client surfaces
- TTL-based analysis caching and invalidation policies
- response telemetry for calibration and rule tuning
- better handling for repeated analysis of popular URLs

---

### Product and Visibility

- dashboard for aggregated analysis results and trend visibility
- visual score breakdown components in the web app
- analyst-oriented history view for recent scans
- richer extension UX for manual review and drill-down explanations

---

## Strategic Direction

PhishRadar should continue evolving as an explainable phishing detection product rather than a black-box classifier. The next phase should prioritize:

- better real-world signal coverage
- stronger contextual enrichment
- faster repeated analysis through caching
- clearer presentation of risk decisions through UI and dashboards

The goal is a security project that is both technically rigorous and strong as a portfolio artifact.
