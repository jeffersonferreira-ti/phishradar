from dataclasses import dataclass
import re
from typing import Literal
import unicodedata
from urllib.parse import parse_qsl, urlparse


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
SUSPICIOUS_URL_KEYWORD_SCORE = 25
HIGH_RISK_TLD_SCORE = 15
BRAND_LOOKALIKE_SCORE = 40
SUSPICIOUS_URL_STRUCTURE_SCORE = 25

SUSPICIOUS_THRESHOLD = 35
HIGH_RISK_THRESHOLD = 70

URGENCY_REASON = "Message uses urgent language to pressure the recipient."
URL_SHORTENER_REASON = "Message contains a URL shortening service."
SUSPICIOUS_DOMAIN_REASON = "Message contains a suspicious domain pattern."
CREDENTIAL_PAYMENT_REASON = "Message requests credentials or payment action."
SUSPICIOUS_URL_KEYWORD_REASON = (
    "URL contains suspicious phishing-related keywords."
)
HIGH_RISK_TLD_REASON = "URL uses a higher-risk top-level domain for sensitive content."
BRAND_LOOKALIKE_REASON = "URL appears to mimic a known brand name."
SUSPICIOUS_URL_STRUCTURE_REASON = (
    "URL structure includes suspicious phishing-related patterns."
)

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

SUSPICIOUS_URL_KEYWORDS: tuple[str, ...] = (
    "login",
    "secure",
    "verify",
    "update",
    "account",
    "password",
    "billing",
    "bank",
    "wallet",
    "invoice",
    "confirm",
)

HIGH_RISK_TLDS: set[str] = {
    "top",
    "xyz",
    "click",
    "shop",
    "site",
    "online",
}

KNOWN_BRANDS: tuple[str, ...] = (
    "paypal",
    "microsoft",
    "google",
    "apple",
    "facebook",
    "instagram",
    "amazon",
    "netflix",
)

SUSPICIOUS_QUERY_KEYS: set[str] = {
    "token",
    "session",
    "redirect",
    "verify",
    "password",
}

LEETSPEAK_TRANSLATION = str.maketrans({
    "0": "o",
    "1": "l",
    "3": "e",
    "4": "a",
    "5": "s",
})

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
    parsed_urls = _extract_urls(content)

    if _has_url_shortener(domains):
        score += URL_SHORTENER_SCORE
        reasons.append(URL_SHORTENER_REASON)

    if _has_suspicious_domain_pattern(domains):
        score += SUSPICIOUS_DOMAIN_SCORE
        reasons.append(SUSPICIOUS_DOMAIN_REASON)

    if _contains_pattern(normalized_content, CREDENTIAL_PAYMENT_PATTERNS):
        score += CREDENTIAL_PAYMENT_SCORE
        reasons.append(CREDENTIAL_PAYMENT_REASON)

    if _has_suspicious_url_keywords(parsed_urls):
        score += SUSPICIOUS_URL_KEYWORD_SCORE
        reasons.append(SUSPICIOUS_URL_KEYWORD_REASON)

    if _has_high_risk_tld_in_sensitive_context(parsed_urls):
        score += HIGH_RISK_TLD_SCORE
        reasons.append(HIGH_RISK_TLD_REASON)

    if _has_brand_lookalike(parsed_urls):
        score += BRAND_LOOKALIKE_SCORE
        reasons.append(BRAND_LOOKALIKE_REASON)

    if _has_suspicious_url_structure(parsed_urls):
        score += SUSPICIOUS_URL_STRUCTURE_SCORE
        reasons.append(SUSPICIOUS_URL_STRUCTURE_REASON)

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


def _extract_urls(content: str) -> list[str]:
    urls: list[str] = []
    seen_urls: set[str] = set()

    for match in URL_PATTERN.finditer(content):
        raw_url = match.group(0).rstrip(".,;:!?)']}")
        parseable_url = raw_url if "://" in raw_url else f"https://{raw_url}"

        if parseable_url not in seen_urls:
            urls.append(parseable_url)
            seen_urls.add(parseable_url)

    return urls


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


def _has_suspicious_url_keywords(urls: list[str]) -> bool:
    return any(_url_has_sensitive_keyword(url) for url in urls)


def _has_high_risk_tld_in_sensitive_context(urls: list[str]) -> bool:
    for url in urls:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname or ""

        if not hostname:
            continue

        tld = hostname.rsplit(".", 1)[-1].casefold()
        if tld not in HIGH_RISK_TLDS:
            continue

        if (
            _url_has_sensitive_keyword(url)
            or _url_has_suspicious_structure(url)
            or _url_has_brand_lookalike(url)
        ):
            return True

    return False


def _has_brand_lookalike(urls: list[str]) -> bool:
    return any(_url_has_brand_lookalike(url) for url in urls)


def _has_suspicious_url_structure(urls: list[str]) -> bool:
    return any(_url_has_suspicious_structure(url) for url in urls)


def _url_has_sensitive_keyword(url: str) -> bool:
    parsed_url = urlparse(url)
    url_parts = (
        parsed_url.hostname or "",
        parsed_url.path or "",
        parsed_url.query or "",
        parsed_url.fragment or "",
    )
    combined = _normalize_text(" ".join(url_parts))
    tokens = set(re.findall(r"[a-z0-9]+", combined))

    return any(keyword in tokens for keyword in SUSPICIOUS_URL_KEYWORDS)


def _url_has_suspicious_structure(url: str) -> bool:
    parsed_url = urlparse(url)
    normalized_path = _normalize_text(parsed_url.path or "")
    normalized_query = _normalize_text(parsed_url.query or "")
    path_tokens = set(re.findall(r"[a-z0-9]+", normalized_path))
    query_pairs = parse_qsl(parsed_url.query, keep_blank_values=True)
    query_keys = {_normalize_text(key) for key, _ in query_pairs}

    has_sensitive_path = any(keyword in path_tokens for keyword in SUSPICIOUS_URL_KEYWORDS)
    has_sensitive_query_key = any(key in SUSPICIOUS_QUERY_KEYS for key in query_keys)
    separator_count = sum(
        normalized_path.count(separator) + normalized_query.count(separator)
        for separator in ("/", "-", "_", "=", "&")
    )
    has_dense_sensitive_structure = (
        separator_count >= 5
        and (
            any(keyword in normalized_path for keyword in SUSPICIOUS_URL_KEYWORDS)
            or any(keyword in normalized_query for keyword in SUSPICIOUS_URL_KEYWORDS)
        )
    )

    return has_sensitive_path or has_sensitive_query_key or has_dense_sensitive_structure


def _url_has_brand_lookalike(url: str) -> bool:
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or ""

    if not hostname:
        return False

    for label in hostname.split("."):
        normalized_label = _normalize_text(label)
        translated_label = normalized_label.translate(LEETSPEAK_TRANSLATION)
        alphanumeric_label = re.sub(r"[^a-z0-9]", "", normalized_label)
        translated_alphanumeric = re.sub(r"[^a-z0-9]", "", translated_label)

        if translated_alphanumeric == alphanumeric_label:
            continue

        for brand in KNOWN_BRANDS:
            if brand in translated_alphanumeric and brand not in alphanumeric_label:
                return True

    return False


def _label_for_score(score: int) -> RiskLabel:
    if score >= HIGH_RISK_THRESHOLD:
        return "HIGH_RISK"

    if score >= SUSPICIOUS_THRESHOLD:
        return "SUSPICIOUS"

    return "LOW_RISK"
