from app.analyzers.risk_engine import _label_for_score, analyze_content


def test_neutral_text_returns_low_risk_without_reasons() -> None:
    analysis = analyze_content("Hello team, see you in tomorrow's meeting.")

    assert analysis.score == 0
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == []


def test_empty_text_returns_low_risk_without_reasons() -> None:
    analysis = analyze_content("   ")

    assert analysis.score == 0
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == []


def test_urgency_language_increases_score() -> None:
    analysis = analyze_content("Urgent: verify now to keep your account active.")

    assert analysis.score == 10
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == [
        "Message uses urgent language to pressure the recipient."
    ]


def test_multiple_urgency_terms_count_as_one_category() -> None:
    analysis = analyze_content("Urgent! Verify now")

    assert analysis.score == 10
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == [
        "Message uses urgent language to pressure the recipient."
    ]


def test_url_shortener_increases_score() -> None:
    analysis = analyze_content("Review the document at https://bit.ly/example.")

    assert analysis.score == 10
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == ["Message contains a URL shortening service."]


def test_credential_or_payment_request_increases_score_and_label() -> None:
    analysis = analyze_content("Please confirm your password to continue.")

    assert analysis.score == 20
    assert analysis.label == "MODERATE"
    assert analysis.reasons == ["Message requests credentials or payment action."]


def test_multiple_combined_signals_return_high_risk() -> None:
    analysis = analyze_content(
        "Urgent: confirm your password at "
        "https://login-secure-account-update.example.com now."
    )

    assert analysis.score == 56
    assert analysis.label == "SUSPICIOUS"
    assert analysis.reasons == [
        "Message uses urgent language to pressure the recipient.",
        "Message contains a suspicious domain pattern.",
        "Message requests credentials or payment action.",
        "URL contains suspicious phishing-related keywords.",
    ]


def test_suspicious_url_keywords_raise_url_only_analysis() -> None:
    analysis = analyze_content("https://example.com/login/verify/account")

    assert analysis.score == 20
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "URL contains suspicious phishing-related keywords.",
        "URL structure includes suspicious phishing-related patterns.",
    ]


def test_high_risk_tld_requires_sensitive_context() -> None:
    analysis = analyze_content("https://example.top/news")

    assert analysis.score == 0
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == []


def test_high_risk_tld_with_sensitive_context_is_flagged() -> None:
    analysis = analyze_content("https://verify.top")

    assert analysis.score == 18
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == [
        "URL contains suspicious phishing-related keywords.",
        "URL uses a higher-risk top-level domain for sensitive content.",
    ]


def test_brand_lookalike_detection_flags_leetspeak_domain() -> None:
    analysis = analyze_content("https://paypa1.com")

    assert analysis.score == 25
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "URL appears to mimic a known brand name.",
    ]


def test_suspicious_query_parameters_raise_structure_signal() -> None:
    analysis = analyze_content(
        "https://example.com/home?session=abc123&redirect=login&token=xyz"
    )

    assert analysis.score == 20
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "URL contains suspicious phishing-related keywords.",
        "URL structure includes suspicious phishing-related patterns.",
    ]


def test_score_at_moderate_threshold_returns_moderate() -> None:
    analysis = analyze_content("Please confirm your password to continue.")

    assert analysis.score == 20
    assert analysis.label == "MODERATE"


def test_score_at_suspicious_threshold_returns_suspicious() -> None:
    assert _label_for_score(45) == "SUSPICIOUS"


def test_score_at_high_risk_threshold_returns_high_risk() -> None:
    assert _label_for_score(70) == "HIGH_RISK"
