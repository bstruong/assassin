"""USD form input → integer cents (fail-loud, no float money)."""

from __future__ import annotations

import pytest

from app.models.exceptions import TokenError
from app.presentation.usd_parse import parse_usd_form_to_cents


def test_happy_two_decimal_usd() -> None:
    assert parse_usd_form_to_cents("50.00") == 5_000
    assert parse_usd_form_to_cents("$1,245.00") == 124_500


def test_rejects_wrong_decimal_places() -> None:
    with pytest.raises(TokenError):
        parse_usd_form_to_cents("12.3")
    with pytest.raises(TokenError):
        parse_usd_form_to_cents("12.345")
    with pytest.raises(TokenError):
        parse_usd_form_to_cents("12")


def test_rejects_zero_and_negative_for_assign() -> None:
    with pytest.raises(TokenError):
        parse_usd_form_to_cents("0.00")
    with pytest.raises(TokenError):
        parse_usd_form_to_cents("-1.00")


def test_rejects_non_string() -> None:
    with pytest.raises(TokenError):
        parse_usd_form_to_cents(12.34)  # type: ignore[arg-type]
