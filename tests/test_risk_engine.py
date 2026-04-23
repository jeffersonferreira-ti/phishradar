from app.analyzers.risk_engine import _label_for_score, analyze_content


def test_neutral_text_returns_low_risk_without_reasons() -> None:
    analysis = analyze_content("Hello team, see you in tomorrow's meeting.")

    assert analysis.score == 0
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == []
    assert analysis.breakdown == {
        "content_score": 0,
        "url_score": 0,
        "domain_score": 0,
        "brand_score": 0,
        "correlation_score": 0,
    }


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


def test_brazilian_scam_pattern_increases_score() -> None:
    analysis = analyze_content("Seu pacote está com entrega retida e taxa pendente.")

    assert analysis.score == 25
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "Content matches common Brazilian delivery, fee, or payment scam patterns."
    ]


def test_brazilian_scam_pattern_supports_normalized_text_matching() -> None:
    analysis = analyze_content(
        "Alfândega informa atualização cadastral para pix para liberação."
    )

    assert analysis.score == 25
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "Content matches common Brazilian delivery, fee, or payment scam patterns."
    ]


def test_multiple_combined_signals_return_high_risk() -> None:
    analysis = analyze_content(
        "Urgent: confirm your password at "
        "https://login-secure-account-update.example.com now."
    )

    assert analysis.score == 91
    assert analysis.label == "HIGH_RISK"
    assert analysis.reasons == [
        "Message uses urgent language to pressure the recipient.",
        "Message contains a suspicious domain pattern.",
        "Message requests credentials or payment action.",
        "URL contains suspicious phishing-related keywords.",
        "Urgent language is combined with a sensitive action request.",
        "Suspicious domain traits are combined with a sensitive action signal.",
    ]
    assert analysis.breakdown == {
        "content_score": 30,
        "url_score": 8,
        "domain_score": 18,
        "brand_score": 0,
        "correlation_score": 35,
    }


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


def test_brand_mismatch_detects_brand_mention_with_non_official_domain() -> None:
    analysis = analyze_content(
        "Your PayPal account needs review: https://secure-check.example.com"
    )

    assert analysis.score == 38
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "URL contains suspicious phishing-related keywords.",
        "Message mentions Paypal but linked URLs do not use its official domains.",
    ]


def test_brand_mismatch_does_not_trigger_for_official_brand_domain() -> None:
    analysis = analyze_content(
        "Google security notice: https://accounts.google.com/verify"
    )

    assert analysis.score == 20
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "URL contains suspicious phishing-related keywords.",
        "URL structure includes suspicious phishing-related patterns.",
    ]


def test_brand_mismatch_supports_multiword_brands() -> None:
    analysis = analyze_content(
        "Mercado Pago alerta importante: https://billing-check.example.com"
    )

    assert analysis.score == 38
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "URL contains suspicious phishing-related keywords.",
        "Message mentions Mercado Pago but linked URLs do not use its official domains.",
    ]


def test_brand_mismatch_and_brand_lookalike_can_both_trigger() -> None:
    analysis = analyze_content("PayPal support: https://paypa1.com/login")

    assert analysis.score == 75
    assert analysis.label == "HIGH_RISK"
    assert analysis.reasons == [
        "URL contains suspicious phishing-related keywords.",
        "URL appears to mimic a known brand name.",
        "Message mentions Paypal but linked URLs do not use its official domains.",
        "URL structure includes suspicious phishing-related patterns.",
    ]
    assert analysis.breakdown == {
        "content_score": 0,
        "url_score": 20,
        "domain_score": 0,
        "brand_score": 55,
        "correlation_score": 0,
    }


def test_breakdown_keeps_raw_category_sums_when_total_is_capped() -> None:
    analysis = analyze_content(
        "Urgent PayPal: entrega retida, confirme sua senha e atualizacao cadastral em "
        "https://bit.ly/login e https://paypa1-secure-login.example.top/"
        "home?session=abc&redirect=verify"
    )

    assert analysis.score == 100
    assert sum(analysis.breakdown.values()) > analysis.score
    assert analysis.breakdown == {
        "content_score": 35,
        "url_score": 40,
        "domain_score": 18,
        "brand_score": 55,
        "correlation_score": 55,
    }


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


def test_urgency_and_sensitive_action_correlation_adds_score() -> None:
    analysis = analyze_content("Urgent: confirm your password immediately.")

    assert analysis.score == 50
    assert analysis.label == "SUSPICIOUS"
    assert analysis.reasons == [
        "Message uses urgent language to pressure the recipient.",
        "Message requests credentials or payment action.",
        "Urgent language is combined with a sensitive action request.",
    ]


def test_shortener_and_sensitive_action_correlation_adds_score() -> None:
    analysis = analyze_content("Review here: https://bit.ly/login")

    assert analysis.score == 50
    assert analysis.label == "SUSPICIOUS"
    assert analysis.reasons == [
        "Message contains a URL shortening service.",
        "URL contains suspicious phishing-related keywords.",
        "URL structure includes suspicious phishing-related patterns.",
        "A URL shortener is combined with a sensitive action signal.",
    ]


def test_suspicious_domain_and_sensitive_action_correlation_adds_score() -> None:
    analysis = analyze_content("Visit https://login-secure-account-update.example.com")

    assert analysis.score == 41
    assert analysis.label == "MODERATE"
    assert analysis.reasons == [
        "Message contains a suspicious domain pattern.",
        "URL contains suspicious phishing-related keywords.",
        "Suspicious domain traits are combined with a sensitive action signal.",
    ]
