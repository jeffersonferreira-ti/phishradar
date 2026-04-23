<div align="center">

# PhishRadar

**Phishing and fraud risk analysis across API, web app, and Chrome extension**

Paste text, inspect URLs, and surface deterministic risk signals with clear explanations.

</div>

## Overview

PhishRadar is a full-stack security MVP focused on explainable phishing detection. It analyzes text, URLs, and raw email-style content using a deterministic heuristic engine and returns a risk `score`, a final `label`, and the `reasons` behind the decision.

The project includes three user-facing surfaces:

- a FastAPI backend with the risk engine and public analysis endpoints
- a Next.js web app for manual analysis
- a Manifest V3 Chrome extension with manual analysis, automatic page analysis, badge updates, and URL-based caching

## Production

- Web app: https://phishradar.vercel.app
- Backend API: https://phishradar-production.up.railway.app

## Core Features

- Deterministic phishing risk engine with explicit scoring and reasons
- URL heuristics for suspicious keywords, risky TLD context, brand lookalikes, and suspicious URL structure
- Text heuristics for urgency, credential/payment requests, URL shorteners, and suspicious domain patterns
- Web interface for analyzing free-form text, URLs, and raw email content
- Chrome extension popup for manual analysis of the current tab or pasted content
- Automatic extension analysis for the active page with dynamic risk badge
- Local URL cache in the extension to avoid repeated API calls for the same page

## Example Response

```json
{
  "score": 100,
  "label": "HIGH_RISK",
  "reasons": [
    "Message uses urgent language to pressure the recipient.",
    "Message contains a suspicious domain pattern.",
    "Message requests credentials or payment action.",
    "URL contains suspicious phishing-related keywords."
  ]
}
```

## Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Pydantic, Uvicorn |
| Risk Engine | Python, deterministic heuristics |
| Frontend | Next.js, React, TypeScript |
| Browser Extension | Chrome Extension, Manifest V3, vanilla JavaScript |
| Testing | pytest, TypeScript typecheck |
| Deploy | Railway for backend, Vercel for frontend |

## Architecture

```text
User Input
  |-- Web app (Next.js)
  |-- Chrome extension popup
  |-- Chrome extension automatic tab analysis
          |
          v
      FastAPI /analyze
          |
          v
     Heuristic risk engine
          |
          v
  score + label + reasons
```

### Repository Structure

```text
phishradar/
|-- app/
|   |-- analyzers/
|   |   `-- risk_engine.py
|   |-- api/routes/
|   |   |-- analyze.py
|   |   `-- health.py
|   |-- schemas/
|   `-- main.py
|-- extension/
|   |-- manifest.json
|   |-- background.js
|   |-- popup.html
|   |-- popup.css
|   `-- popup.js
|-- frontend/
|   |-- app/
|   |   |-- api/analyze/route.ts
|   |   `-- page.tsx
|   |-- lib/phishradar-api.ts
|   `-- types/analysis.ts
|-- tests/
|   `-- test_risk_engine.py
|-- docs/
|-- Procfile
`-- requirements.txt
```

## Running Locally

### 1. Backend

From the repository root:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend local URL:

```text
http://localhost:8000
```

Useful endpoints:

- `GET /health`
- `POST /analyze`

### 2. Frontend

From [`frontend/`](/c:/Users/jluiz/Documents/GitHub/phishradar/frontend):

```bash
npm install
npm run dev
```

Set `frontend/.env.local` with:

```text
PHISHRADAR_API_BASE_URL=http://localhost:8000
```

Frontend local URL:

```text
http://localhost:3000
```

### 3. Chrome Extension

The extension lives in [`extension/`](/c:/Users/jluiz/Documents/GitHub/phishradar/extension).

To load it locally:

1. Open `chrome://extensions`
2. Enable `Developer mode`
3. Click `Load unpacked`
4. Select the `extension/` folder

Current extension behavior:

- manual analysis of pasted text or URLs
- manual analysis of the current tab
- automatic analysis when the active page changes
- dynamic badge color and label based on backend risk output
- per-URL cache using `chrome.storage.local`

## Consistency Across Interfaces

The backend is the single source of truth for scoring. Both the web app and the extension consume the same analysis contract:

```json
{
  "score": 0,
  "label": "LOW_RISK | SUSPICIOUS | HIGH_RISK",
  "reasons": []
}
```

This keeps the result format consistent across API responses, the Next.js UI, and the Chrome extension popup.

## Testing

### Backend

```bash
pytest
```

### Frontend

From `frontend/`:

```bash
npm run typecheck
npm run build
```

### Extension

There is no dedicated automated test suite for the extension yet. Current validation is done through local loading in Chrome and syntax checks for the extension scripts.

## Extension Notes

The extension is built with Manifest V3 and keeps the implementation intentionally simple:

- `background.js` handles automatic tab analysis and badge updates
- `popup.js` handles manual analysis and automatic result display for the active tab
- `chrome.storage.local` caches analysis results by URL
- unsupported URLs such as internal browser pages are ignored safely

## Screenshots

Placeholders for repository visuals:

- web app home screen with analysis form
- web app result state showing `HIGH_RISK`
- extension popup showing cached page analysis
- extension badge in `LOW_RISK`, `SUSPICIOUS`, and `HIGH_RISK` states

## Roadmap

- add more phishing heuristics for email header and sender analysis
- add repository screenshots and extension GIF demo
- add integration or end-to-end coverage for key user flows
- refine UI polish for the web app and extension popup

## Limitations

- no machine learning or third-party reputation feeds
- no browser history analysis or background crawling
- no authentication or user accounts
- heuristic output is useful for triage, not a substitute for full incident response

## Portfolio Value

This project demonstrates:

- backend API design with FastAPI
- deterministic security-oriented rule design
- frontend integration with Next.js and TypeScript
- browser extension development with Manifest V3
- production deployment split across Railway and Vercel
- clean separation between analysis engine, API layer, and clients

## Author

Jefferson Ferreira

- GitHub: [jeffersonferreira-ti](https://github.com/jeffersonferreira-ti)
- LinkedIn: [Jefferson Ferreira](https://www.linkedin.com/in/jefferson-ferreira-ti)
