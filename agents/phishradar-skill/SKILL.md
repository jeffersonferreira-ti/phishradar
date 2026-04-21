---
name: phishradar
description: Analyze URLs, text, and raw e-mail for phishing and fraud risk, returning a score, label, and evidence-based reasons.
---

# PhishRadar Skill

Use this skill when working on PhishRadar analysis behavior, prompts, scoring rules, or API contracts.

## Objective

PhishRadar receives a URL, text, or raw e-mail and returns:

- `score`: integer from 0 to 100.
- `label`: `safe`, `suspicious`, or `phishing`.
- `reasons`: short evidence-based explanations.

## Guidance

- Keep analysis explainable.
- Prefer deterministic rules for the MVP.
- Use simple technical English.
- Avoid unsupported claims about reputation or sender identity.
- Keep output structured and stable for API clients.

## Labels

- `safe`: low risk, no strong phishing indicators.
- `suspicious`: some risk signals, but not enough for high confidence.
- `phishing`: strong indicators of phishing or fraud.

## Development Notes

- Do not add a frontend for the MVP.
- Do not add a browser extension for the MVP.
- Keep dependencies limited to the approved backend stack unless the project scope changes.
