<div align="center">

<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Next.js-Frontend-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/>
<img src="https://img.shields.io/badge/Chrome%20Extension-MV3-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white"/>
<img src="https://img.shields.io/badge/Focus-Phishing%20Detection%20Engine-8E24AA?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-Advanced%20Engine-00C853?style=for-the-badge"/>

<br/><br/>

# PhishRadar

**Full-stack phishing detection platform with explainable scoring, correlation rules, and browser-assisted analysis**

*Analyze. Explain. Prevent.*

</div>

---

## Project Overview

PhishRadar is a security-focused project that analyzes suspicious text and URLs through an explainable phishing risk engine. What started as a simple heuristic analyzer has evolved into a more capable detection layer that combines message content, URL structure, domain traits, brand signals, and multi-signal correlations.

The platform returns a deterministic risk assessment designed for debugging, calibration, and product presentation:

- `score`: final risk score from `0` to `100`
- `label`: final classification (`LOW_RISK`, `MODERATE`, `SUSPICIOUS`, `HIGH_RISK`)
- `reasons`: human-readable explanations for triggered signals
- `breakdown`: category-level score attribution for explainability

PhishRadar is exposed through a FastAPI backend, a Next.js web interface, and a Chrome extension that can analyze the active page and surface risk through a badge.

---

## Key Features

### Detection Engine

- explainable and deterministic phishing scoring
- hybrid detection across content, URLs, domains, brand signals, and correlation rules
- improved calibration with a four-level risk model
- category-level score breakdown for debugging and tuning
- focused coverage for real-world phishing and scam narratives

---

### Explainability

- explicit `reasons` for every matched signal
- structured `breakdown` by scoring family:
  - `content_score`
  - `url_score`
  - `domain_score`
  - `brand_score`
  - `correlation_score`
- stable output that is easy to inspect in tests, demos, and portfolio reviews

---

### Delivery Surfaces

- FastAPI analysis API for programmatic use
- Next.js web app for manual analysis
- Chrome extension with badge-based risk feedback and cached URL results

---

## How It Works

```text
Text/URL -> FastAPI /analyze -> Risk Engine -> Base Signals + Correlation Rules -> Score + Label + Reasons + Breakdown -> Web App / Chrome Extension
```

High-level engine flow:

1. Normalize message content and extract URLs and domains.
2. Evaluate base rules across content, URL, domain, and brand signals.
3. Apply additive correlation rules when risky signals appear together.
4. Aggregate raw category totals into a final score, then cap at `MAX_SCORE = 100`.
5. Return the final risk label, matched reasons, and score breakdown.

---

## Risk Levels Explanation

| Score | Label | Meaning |
|---|---|---|
| 0-19 | `LOW_RISK` | No meaningful phishing indicators or only weak isolated signals |
| 20-44 | `MODERATE` | Noticeable suspicious behavior that merits review |
| 45-69 | `SUSPICIOUS` | Multi-signal phishing characteristics are present |
| 70+ | `HIGH_RISK` | Strong or correlated phishing indicators with high confidence |

The final score is capped at `100`. The `breakdown` remains uncapped by category so calibration work can see which signal families drove the raw total.

---

## Detection Capabilities

PhishRadar currently covers a practical set of phishing and scam scenarios, including:

- urgency and pressure-based language
- credential or payment requests
- URL shorteners in suspicious contexts
- suspicious domain traits and risky URL structures
- sensitive URL keywords and high-risk TLD usage
- brand lookalike domains such as visual substitutions
- brand mismatch between message content and linked domains
- additive correlation rules such as:
  - urgency + sensitive action
  - shortener + sensitive action
  - suspicious domain + sensitive action
- Brazilian scam narratives involving:
  - delivery retention
  - pending fees
  - customs and Correios scams
  - PIX release payments
  - account update and device confirmation messages

This makes the engine useful for real-world scenarios such as payment phishing, account takeover lures, fake delivery notices, domain impersonation, and mixed-signal social engineering attempts.

---

## Example API Response

### Input

```text
Urgent PayPal notice: entrega retida. Confirm your password at https://bit.ly/login now.
```

### Output

```json
{
  "score": 100,
  "label": "HIGH_RISK",
  "reasons": [
    "Message uses urgent language to pressure the recipient.",
    "Message requests credentials or payment action.",
    "Content matches common Brazilian delivery, fee, or payment scam patterns.",
    "Message contains a URL shortening service.",
    "URL contains suspicious phishing-related keywords.",
    "URL structure includes suspicious phishing-related patterns.",
    "Message mentions Paypal but linked URLs do not use its official domains.",
    "Urgent language is combined with a sensitive action request.",
    "A URL shortener is combined with a sensitive action signal."
  ],
  "breakdown": {
    "content_score": 55,
    "url_score": 30,
    "domain_score": 0,
    "brand_score": 30,
    "correlation_score": 40
  }
}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Pydantic, Uvicorn |
| Risk Engine | Python, deterministic scoring rules |
| Testing | pytest |
| Frontend | Next.js, React, TypeScript |
| Browser Extension | Chrome Extension, Manifest V3, JavaScript |
| Deployment | Railway, Vercel |

---

## Production

- Web app: https://phishradar.vercel.app
- Backend API: https://phishradar-production.up.railway.app

---

## Architecture

```text
phishradar/
|-- app/
|   |-- analyzers/
|   |   `-- risk_engine.py
|   |-- api/
|   |   `-- routes/
|   |       |-- analyze.py
|   |       `-- health.py
|   |-- schemas/
|   |   `-- analyze.py
|   `-- main.py
|-- extension/
|   |-- background.js
|   |-- manifest.json
|   |-- popup.html
|   |-- popup.css
|   `-- popup.js
|-- frontend/
|   |-- app/
|   |   |-- api/analyze/route.ts
|   |   `-- page.tsx
|   |-- lib/
|   |   `-- phishradar-api.ts
|   `-- types/
|       `-- analysis.ts
|-- tests/
|   `-- test_risk_engine.py
|-- docs/
|-- Procfile
`-- requirements.txt
```

---

## Screenshots

Reserved space for portfolio visuals:

- web app analysis form
- `LOW_RISK` result view
- `MODERATE` and `HIGH_RISK` result views
- extension popup with automatic analysis
- extension badge across multiple risk levels

---

## Limitations

- no machine learning or reputation feeds
- no external threat intelligence enrichment
- no mailbox-native email parsing pipeline yet
- no behavioral or historical browsing analysis
- not a replacement for human review in incident response workflows

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| M1-M4 | Initial backend, API, and rule engine | Completed |
| M5-M6 | Next.js web interface | Completed |
| M7-M9 | Chrome extension, badge logic, and caching | Completed |
| Current | Correlation rules, calibration, brand mismatch, BR scam coverage, explainable breakdown | Completed |
| Next | Additional email signals, richer UI visualization, broader scenario coverage | Planned |

---

## Objective

PhishRadar demonstrates:

- security-oriented backend engineering with FastAPI
- design of an explainable phishing detection engine
- calibration-aware scoring and regression-tested rule evolution
- integration across API, web application, and Chrome extension
- product-minded security tooling suitable for portfolio presentation

---

## Project Summary

PhishRadar shows how a lean security product can move beyond basic heuristics into a more mature phishing detection engine without relying on opaque models. The result is a practical system that favors explainability, engineering clarity, and realistic threat scenarios over black-box scoring.

It is designed to be both demo-ready and technically inspectable: every major risk signal is visible, attributable, and testable.

---

## Developed by **Jefferson Ferreira**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/jefferson-ferreira-ti/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/jeffersonferreira-ti)

---

<div align="center">
  <sub>PhishRadar · 2026</sub>
</div>
