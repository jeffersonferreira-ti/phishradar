from dataclasses import dataclass
import re
import unicodedata
from urllib.parse import urlparse


@dataclass(frozen=True)
class RiskAnalysis:
    score: int
    label: str
    reasons: list[str]


SHORTENER_DOMAINS: set[str] = {
    "bit.ly",
    "cutt.ly",
    "t.co",
    "tinyurl.com",
}

URGENCY_PATTERNS: tuple[str, ...] = (
    "urgent",
    "verify now",
    "your account will be suspended",
    "acao imediata",
    "urgente",
)

CREDENTIAL_PAYMENT_PATTERNS: tuple[str, ...] = (
    "confirm your password",
    "update your payment",
    "informe sua senha",
    "regularize seu pagamento",
)

URL_PATTERN = re.compile(r"https?://[^\s<>\"]+|www\.[^\s<>\"]+", re.IGNORECASE)
DOMAIN_PATTERN = re.compile(
    r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\b",
    re.IGNORECASE,
)


def analyze_content(content: str) -> RiskAnalysis:
    normalized_content = _normalize_text(content)
    score = 0
    reasons: list[str] = []

    if _contains_any(normalized_content, URGENCY_PATTERNS):
        score += 25
        reasons.append("Message uses urgent language to pressure the recipient.")

    domains = _extract_domains(content)

    if _has_url_shortener(domains):
        score += 25
        reasons.append("Message contains a URL shortening service.")

    if _has_suspicious_domain_pattern(domains):
        score += 40
        reasons.append("Message contains a suspicious domain pattern.")

    if _contains_any(normalized_content, CREDENTIAL_PAYMENT_PATTERNS):
        score += 40
        reasons.append("Message requests credentials or payment action.")

    final_score = min(score, 100)
    return RiskAnalysis(
        score=final_score,
        label=_label_for_score(final_score),
        reasons=reasons,
    )


def _contains_any(content: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern.casefold() in content for pattern in patterns)


def _normalize_text(content: str) -> str:
    normalized = unicodedata.normalize("NFKD", content.casefold())
    return "".join(
        character for character in normalized if not unicodedata.combining(character)
    )


def _extract_domains(content: str) -> list[str]:
    domains: list[str] = []
    seen_domains: set[str] = set()

    for match in URL_PATTERN.finditer(content):
        raw_url = match.group(0).rstrip(".,;:!?)']}")
        parseable_url = raw_url if "://" in raw_url else f"https://{raw_url}"
        parsed_url = urlparse(parseable_url)

        if parsed_url.hostname:
            _append_domain(domains, seen_domains, parsed_url.hostname)

    for match in DOMAIN_PATTERN.finditer(content):
        _append_domain(domains, seen_domains, match.group(0))

    return domains


def _append_domain(domains: list[str], seen_domains: set[str], domain: str) -> None:
    normalized_domain = domain.casefold()

    if normalized_domain not in seen_domains:
        domains.append(normalized_domain)
        seen_domains.add(normalized_domain)


def _has_url_shortener(domains: list[str]) -> bool:
    return any(
        domain == shortener or domain.endswith(f".{shortener}")
        for domain in domains
        for shortener in SHORTENER_DOMAINS
    )


def _has_suspicious_domain_pattern(domains: list[str]) -> bool:
    return any(_is_suspicious_domain(domain) for domain in domains)


def _is_suspicious_domain(domain: str) -> bool:
    labels = domain.split(".")
    root_label = labels[-2] if len(labels) >= 2 else labels[0]

    has_many_hyphens = root_label.count("-") >= 2 or domain.count("-") >= 3
    has_many_subdomains = len(labels) >= 5
    has_long_subdomain = any(len(label) >= 20 for label in labels[:-2])
    has_digit_heavy_label = any(
        any(character.isdigit() for character in label)
        and any(character.isalpha() for character in label)
        and len(label) >= 10
        for label in labels
    )

    return (
        has_many_hyphens
        or has_many_subdomains
        or has_long_subdomain
        or has_digit_heavy_label
    )


def _label_for_score(score: int) -> str:
    if score >= 70:
        return "HIGH_RISK"

    if score >= 35:
        return "SUSPICIOUS"

    return "LOW_RISK"
