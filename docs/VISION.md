# PhishRadar Vision

PhishRadar is an MVP for phishing and fraud analysis.

The product receives one of three input types:

- A URL.
- A text message.
- A raw e-mail.

It returns a structured result with:

- `score`: numeric risk score from 0 to 100.
- `label`: risk category.
- `reasons`: short evidence-based explanations.

The goal is to help users quickly identify suspicious content and understand why it may be risky.

## Product Principles

- Be simple to use.
- Return structured and predictable outputs.
- Explain decisions with clear reasons.
- Avoid claiming certainty when evidence is weak.
- Keep the MVP focused on analysis, not enforcement.

## Target Users

- Security analysts.
- Small teams without a full security operations center.
- Developers building phishing detection workflows.
- Users who need a first-pass risk assessment.

## MVP Success

The MVP is successful when it can accept supported input, apply clear detection rules, and return a consistent risk score, label, and reasons that are useful for further review.
