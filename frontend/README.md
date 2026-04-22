# PhishRadar Frontend

Small Next.js + TypeScript UI for the PhishRadar API.

## Development

Start the FastAPI backend from the repository root:

```bash
python -m uvicorn app.main:app --reload
```

Start the frontend from this directory:

```bash
npm install
npm run dev
```

The frontend uses `http://127.0.0.1:8000` as the default backend URL.
Override it with:

```bash
PHISHRADAR_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```
