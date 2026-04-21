# MVP Scope

## In Scope

The MVP will provide an API for phishing and fraud analysis.

Supported inputs:

- URL.
- Plain text.
- Raw e-mail content.

Expected output:

- `score`: integer from 0 to 100.
- `label`: one of `safe`, `suspicious`, or `phishing`.
- `reasons`: list of short explanations.

Initial analysis may include:

- Suspicious URL patterns.
- URL shorteners.
- Lookalike domains.
- Urgent or threatening language.
- Requests for credentials, payment, or personal information.
- Mismatched links and visible text.
- Basic e-mail header signals when raw e-mail is provided.

## Out of Scope

The MVP will not include:

- Browser extension.
- Frontend application.
- User accounts.
- Database storage.
- Real-time mailbox integration.
- Automated blocking or takedown.
- Machine learning model training.
- External threat intelligence integrations unless added in a later phase.

## Technical Scope

The initial backend should be small and testable.

Planned stack:

- FastAPI for the API.
- Pydantic for request and response models.
- Pytest for tests.
- Uvicorn for local development.

No application code is implemented in the repository setup task.
