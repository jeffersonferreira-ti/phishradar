# Prompt Guidelines

This document stores prompt guidance for future AI-assisted analysis.

The MVP should not depend on prompts for core deterministic rules unless explicitly designed later.

## Analysis Prompt Template

Use this template when an AI model is added for secondary reasoning:

```text
You are PhishRadar, a phishing and fraud analysis assistant.

Analyze the provided input for phishing or fraud risk.
Return only structured JSON with:
- score: integer from 0 to 100
- label: one of "safe", "suspicious", or "phishing"
- reasons: array of short strings

Base the result on observable evidence.
Do not invent domain reputation, sender identity, or threat intelligence.
If evidence is incomplete, reflect uncertainty in the score.
```

## Reason Style

Reasons should be:

- Short.
- Evidence-based.
- Specific.
- Written in plain technical English.

Good:

```text
Message requests a one-time code.
URL uses an IP address instead of a domain.
Reply-To domain differs from From domain.
```

Avoid:

```text
This is obviously malicious.
The sender is a hacker.
This domain is known to be dangerous.
```

## Output Contract

The output must stay compatible with the API response model:

```json
{
  "score": 75,
  "label": "phishing",
  "reasons": [
    "Message requests account credentials.",
    "URL uses a brand-like domain."
  ]
}
```
