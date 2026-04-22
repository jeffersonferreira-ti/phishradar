from app.analyzers.risk_engine import analyze_content


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

    assert analysis.score == 25
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == [
        "Message uses urgent language to pressure the recipient."
    ]


def test_multiple_urgency_terms_count_as_one_category() -> None:
    analysis = analyze_content("Urgent! Verify now")

    assert analysis.score == 25
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == [
        "Message uses urgent language to pressure the recipient."
    ]


def test_url_shortener_increases_score() -> None:
    analysis = analyze_content("Review the document at https://bit.ly/example.")

    assert analysis.score == 25
    assert analysis.label == "LOW_RISK"
    assert analysis.reasons == ["Message contains a URL shortening service."]


def test_credential_or_payment_request_increases_score_and_label() -> None:
    analysis = analyze_content("Please confirm your password to continue.")

    assert analysis.score == 40
    assert analysis.label == "SUSPICIOUS"
    assert analysis.reasons == ["Message requests credentials or payment action."]


def test_multiple_combined_signals_return_high_risk() -> None:
    analysis = analyze_content(
        "Urgent: confirm your password at "
        "https://login-secure-account-update.example.com now."
    )

    assert analysis.score == 100
    assert analysis.label == "HIGH_RISK"
    assert analysis.reasons == [
        "Message uses urgent language to pressure the recipient.",
        "Message contains a suspicious domain pattern.",
        "Message requests credentials or payment action.",
    ]
