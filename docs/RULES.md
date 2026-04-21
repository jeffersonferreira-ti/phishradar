# Detection Rules

This document defines initial rule ideas for PhishRadar.

Rules should be explainable. Each rule that affects the score should be able to produce a short reason.

## Score Bands

- `0-29`: `safe`
- `30-69`: `suspicious`
- `70-100`: `phishing`

These bands are initial MVP defaults and may change after testing.

## URL Rules

Potential risk signals:

- Uses a URL shortener.
- Contains an IP address instead of a domain.
- Uses many subdomains.
- Contains misleading brand terms.
- Contains unusual characters or encoded values.
- Uses a newly observed or unknown domain.
- Uses HTTP for a page that appears to request sensitive data.

Example reasons:

- `URL uses a shortening service.`
- `Domain contains a brand-like term but does not match the expected domain.`
- `URL contains an IP address instead of a normal hostname.`

## Text Rules

Potential risk signals:

- Urgent language.
- Threats of account closure, fines, or legal action.
- Requests for passwords, one-time codes, payment details, or personal data.
- Suspicious instructions such as bypassing normal support channels.
- Poor alignment between the claimed sender and the requested action.

Example reasons:

- `Message uses urgent language to pressure the recipient.`
- `Message requests sensitive information.`
- `Message asks the recipient to use an unusual verification process.`

## E-mail Rules

Potential risk signals:

- Display name does not match the sender domain.
- Reply-To domain differs from From domain.
- Authentication headers indicate SPF, DKIM, or DMARC failure.
- Message contains suspicious links or attachments.
- Body content uses phishing-like urgency or credential requests.

Example reasons:

- `Reply-To domain differs from sender domain.`
- `E-mail authentication appears to have failed.`
- `E-mail contains a suspicious link.`

## Rule Design Guidelines

- Prefer deterministic and testable rules.
- Keep reasons short and specific.
- Avoid duplicate reasons for the same signal.
- Do not mark content as phishing based on one weak signal alone.
- Record uncertainty through the score instead of vague labels.
