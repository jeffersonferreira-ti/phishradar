# PhishRadar

PhishRadar is an MVP for phishing and fraud analysis.

It will accept a URL, text, or raw e-mail and return:

- `score`: risk score from 0 to 100.
- `label`: `safe`, `suspicious`, or `phishing`.
- `reasons`: short explanations for the result.

## Status

Initial repository structure and documentation are in place. Application code is not implemented yet.

## Project Structure

```text
app/
tests/
docs/
agents/phishradar-skill/
```

## Development

Install the planned MVP dependencies:

```bash
pip install -r requirements.txt
```

See `docs/` for product scope, rules, and prompt guidance.
