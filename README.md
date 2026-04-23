# PhishRadar

PhishRadar is a phishing and fraud risk analyzer for URLs, messages, and raw
e-mail content. It returns a deterministic risk score, a label, and short
evidence-based reasons that explain which signals were detected.

## What It Does

- Accepts text, URLs, or raw e-mail content.
- Detects MVP phishing signals such as urgency language, URL shorteners,
  suspicious domain patterns, and credential or payment requests.
- Returns:
  - `score`: risk score from 0 to 100.
  - `label`: `LOW_RISK`, `SUSPICIOUS`, or `HIGH_RISK`.
  - `reasons`: short explanations for the detected signals.

## Stack

- Backend: FastAPI, Pydantic, pytest
- Frontend: Next.js, React, TypeScript
- Deploy targets: Railway or Render for the API, Vercel for the frontend

## Production

- Frontend: https://phishradar.vercel.app
- Backend API: https://phishradar-production.up.railway.app

Do not commit secrets or private environment values. The frontend server-side
proxy route reads the API base URL from `PHISHRADAR_API_BASE_URL`.

## Screenshots

Add screenshots after the next production validation pass:

- Home page with empty analysis form
- High-risk analysis result
- Low-risk analysis result

## Local Development

Install and run the backend:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs at `http://localhost:8000`.

Install and run the frontend:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Set `PHISHRADAR_API_BASE_URL` in `frontend/.env.local`:

```text
PHISHRADAR_API_BASE_URL=http://localhost:8000
```

The frontend runs at `http://localhost:3000`.

## Tests

```bash
pytest
```

For the frontend:

```bash
cd frontend
npm run typecheck
npm run build
```

## Deploy

Backend start command for Railway or Render:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The repository includes a `Procfile` with the same command.

Frontend deploy:

1. Deploy the `frontend/` directory to Vercel.
2. Configure `PHISHRADAR_API_BASE_URL` with the production backend URL.
3. Redeploy the frontend after changing environment variables.

## Roadmap

- Add richer URL and e-mail header analysis.
- Add end-to-end tests for the deployed frontend/backend flow.
- Add screenshots and demo links after production validation.
- Expand the risk rules while keeping explanations deterministic.

See `docs/` for product scope, rules, and prompt guidance.
