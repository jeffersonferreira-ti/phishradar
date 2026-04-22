# PhishRadar

PhishRadar is an MVP for phishing and fraud analysis.

It accepts a URL, text, or raw e-mail and returns:

- `score`: risk score from 0 to 100.
- `label`: `LOW_RISK`, `SUSPICIOUS`, or `HIGH_RISK`.
- `reasons`: short explanations for the result.

## Status

The MVP includes a FastAPI backend, a deterministic risk engine, unit tests, and
a small Next.js frontend.

## Project Structure

```text
app/
frontend/
tests/
docs/
agents/phishradar-skill/
```

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

## Backend Deploy

For Railway or Render, use this start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The repository also includes a `Procfile` with the same command.

## Frontend Deploy

Deploy the `frontend/` directory to Vercel.

Configure this environment variable in Vercel:

```text
PHISHRADAR_API_BASE_URL=https://your-backend-host.example.com
```

See `docs/` for product scope, rules, and prompt guidance.
