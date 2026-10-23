"""Parse USD form strings into integer cents for budget assign.

Reuses the extraction currency parser so form input and statement tokens
share the same fail-loud two-decimal contract. Never uses ``float``.
"""

from __future__ import annotations

from typing import Any

from app.extraction.core import parse_currency_to_cents
from app.models.exceptions import TokenError


def parse_usd_form_to_cents(amount_usd: Any) -> int:
    """Parse a positive USD form value into integer cents.

    Accepts positive dollar amounts with or without minor currency digits
    (e.g., '50', '$50', '50.00', '$1,245.00'). Rejects sub-cent precision,
    non-two decimal places (e.g. '12.3', '12.345'), zero, and negatives.
    Never uses ``float``.
    """
    if not isinstance(amount_usd, str):
        raise TokenError(
            f"amount_usd must be a string, got {type(amount_usd).__name__}"
        )
    cleaned = amount_usd.strip()
    if "." not in cleaned:
        cleaned = f"{cleaned}.00"
    cents = parse_currency_to_cents(cleaned, allow_zero=False)
    if cents <= 0:
        raise TokenError("amount_usd must be a positive USD amount")
    return cents
