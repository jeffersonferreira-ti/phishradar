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
cp .env.example .env.local
npm run dev
```

Configure the backend URL with:

```bash
PHISHRADAR_API_BASE_URL=http://localhost:8000
```
