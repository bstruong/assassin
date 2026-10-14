"""Human-readable labels from internal snake_case tokens."""

from __future__ import annotations

import pytest

from app.presentation.label_format import format_snake_label


class TestFormatSnakeLabel:
    def test_account_types(self) -> None:
        assert format_snake_label("brokerage_cash") == "Brokerage Cash"
        assert format_snake_label("checking") == "Checking"

    def test_transaction_categories(self) -> None:
        assert format_snake_label("transfer_in") == "Transfer In"
        assert format_snake_label("transfer_out") == "Transfer Out"
        assert format_snake_label("deposit") == "Deposit"

    def test_empty(self) -> None:
        assert format_snake_label("") == ""

    def test_rejects_non_string(self) -> None:
        with pytest.raises(TypeError):
            format_snake_label(12)  # type: ignore[arg-type]
