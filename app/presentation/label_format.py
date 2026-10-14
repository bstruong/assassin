"""Format internal snake_case tokens for UI display."""

from __future__ import annotations


def format_snake_label(value: str) -> str:
    """Turn ``brokerage_cash`` / ``transfer_in`` into title-cased labels.

    Internal enum values stay snake_case in the Vault; this is presentation only.
    """
    if type(value) is not str:
        raise TypeError(f"label value must be str, got {type(value).__name__}")
    cleaned = value.replace("_", " ").strip()
    if not cleaned:
        return ""
    return cleaned.title()
