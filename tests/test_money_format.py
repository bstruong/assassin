"""USD display formatting from integer cents (presentation only)."""

from __future__ import annotations

import pytest

from app.presentation.money_format import format_usd_cents


class TestFormatUsdCents:
    def test_zero(self) -> None:
        assert format_usd_cents(0) == "$0.00"

    def test_positive_dollars_and_cents(self) -> None:
        assert format_usd_cents(129500) == "$1,295.00"
        assert format_usd_cents(99) == "$0.99"
        assert format_usd_cents(100) == "$1.00"
        assert format_usd_cents(1_000_000_50) == "$1,000,000.50"
        assert format_usd_cents(10_000_000_50) == "$10,000,000.50"

    def test_negative(self) -> None:
        assert format_usd_cents(-180000) == "-$1,800.00"
        assert format_usd_cents(-5) == "-$0.05"

    def test_rejects_bool(self) -> None:
        with pytest.raises(TypeError):
            format_usd_cents(True)  # type: ignore[arg-type]

    def test_rejects_float(self) -> None:
        with pytest.raises(TypeError):
            format_usd_cents(12.34)  # type: ignore[arg-type]

    def test_rejects_str(self) -> None:
        with pytest.raises(TypeError):
            format_usd_cents("100")  # type: ignore[arg-type]
