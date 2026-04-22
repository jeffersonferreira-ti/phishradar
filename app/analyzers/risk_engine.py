from dataclasses import dataclass
import re
from typing import Literal
import unicodedata
from urllib.parse import urlparse


RiskLabel = Literal["LOW_RISK", "SUSPICIOUS", "HIGH_RISK"]


@dataclass(frozen=True)
class RiskAnalysis:
    score: int
    label: RiskLabel
    reasons: list[str]


MAX_SCORE = 100
URGENCY_SCORE = 25
URL_SHORTENER_SCORE = 25
SUSPICIOUS_DOMAIN_SCORE = 40
CREDENTIAL_PAYMENT_SCORE = 40

SUSPICIOUS_THRESHOLD = 35
HIGH_RISK_THRESHOLD = 70

URGENCY_REASON = "Message uses urgent language to pressure the recipient."
URL_SHORTENER_REASON = "Message contains a URL shortening service."
SUSPICIOUS_DOMAIN_REASON = "Message contains a suspicious domain pattern."
CREDENTIAL_PAYMENT_REASON = "Message requests credentials or payment action."

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
    normalized_content = _normalize_text(content.strip())

    if not normalized_content:
        return _build_analysis(score=0, reasons=[])

    score = 0
    reasons: list[str] = []

    if _contains_pattern(normalized_content, URGENCY_PATTERNS):
        score += URGENCY_SCORE
        reasons.append(URGENCY_REASON)

    domains = _extract_unique_domains(content)

    if _has_url_shortener(domains):
        score += URL_SHORTENER_SCORE
        reasons.append(URL_SHORTENER_REASON)

    if _has_suspicious_domain_pattern(domains):
        score += SUSPICIOUS_DOMAIN_SCORE
        reasons.append(SUSPICIOUS_DOMAIN_REASON)

    if _contains_pattern(normalized_content, CREDENTIAL_PAYMENT_PATTERNS):
        score += CREDENTIAL_PAYMENT_SCORE
        reasons.append(CREDENTIAL_PAYMENT_REASON)

    return _build_analysis(score=score, reasons=reasons)


def _build_analysis(score: int, reasons: list[str]) -> RiskAnalysis:
    capped_score = min(score, MAX_SCORE)
    return RiskAnalysis(
        score=capped_score,
        label=_label_for_score(capped_score),
        reasons=reasons.copy(),
    )


def _contains_pattern(content: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern.casefold() in content for pattern in patterns)


def _normalize_text(content: str) -> str:
    normalized = unicodedata.normalize("NFKD", content.casefold())
    return "".join(
        character for character in normalized if not unicodedata.combining(character)
    )


def _extract_unique_domains(content: str) -> list[str]:
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
        _is_url_shortener_domain(domain, shortener)
        for domain in domains
        for shortener in SHORTENER_DOMAINS
    )


def _is_url_shortener_domain(domain: str, shortener: str) -> bool:
    return domain == shortener or domain.endswith(f".{shortener}")


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


def _label_for_score(score: int) -> RiskLabel:
    if score >= HIGH_RISK_THRESHOLD:
        return "HIGH_RISK"

    if score >= SUSPICIOUS_THRESHOLD:
        return "SUSPICIOUS"

    return "LOW_RISK"
