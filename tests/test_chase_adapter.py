"""Tests for the Chase depository adapter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from reportlab.pdfgen import canvas

from app.adapters.chase import ChaseDepositoryAdapter
from app.adapters.depository import StandardDepositoryAdapter
from app.adapters.registry import get_default_registry
from app.extraction.core import extract_pdf_to_raw
from app.models.enums import AccountType
from app.models.exceptions import AdapterRegistryError

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _render_pdf_from_fixture(fixture_name: str, target_path: Path) -> Path:
    import re

    data = json.loads(
        (FIXTURES_DIR / f"{fixture_name}.json").read_text(encoding="utf-8")
    )
    lines = data["raw_text"].split("\n")
    c = canvas.Canvas(str(target_path))
    y = 750
    for line in lines:
        if "\t" in line or "    " in line:
            line = re.sub(r"(\t|\s{2,})", " | ", line)
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    return target_path


def _render_lines(path: Path, lines: list[str]) -> Path:
    c = canvas.Canvas(str(path))
    y = 750
    for line in lines:
        c.drawString(50, y, line)
        y -= 15
    c.save()
    return path


class TestChaseMatching:
    def test_matches_chase_checking_fixture(self, tmp_path: Path) -> None:
        pdf = _render_pdf_from_fixture("chase_checking_happy", tmp_path / "chase.pdf")
        adapter = ChaseDepositoryAdapter()
        assert adapter.matches(pdf) is True
        assert StandardDepositoryAdapter().matches(pdf) is False

    def test_registry_exclusive_chase(self, tmp_path: Path) -> None:
        pdf = _render_pdf_from_fixture("chase_checking_happy", tmp_path / "chase.pdf")
        matched = get_default_registry().match(pdf)
        assert matched.adapter_id == "chase_depository"

    def test_does_not_match_standard_bank(self, tmp_path: Path) -> None:
        pdf = _render_pdf_from_fixture("checking_happy", tmp_path / "std.pdf")
        assert ChaseDepositoryAdapter().matches(pdf) is False

    def test_combined_chase_does_not_match_chase_adapter(self, tmp_path: Path) -> None:
        pdf = _render_lines(
            tmp_path / "chase_combined.pdf",
            ["CHASE BANK", "COMBINED STATEMENT", "CHECKING", "SAVINGS"],
        )
        assert ChaseDepositoryAdapter().matches(pdf) is False


class TestChaseParse:
    def test_parse_canonical_happy_path(self, tmp_path: Path) -> None:
        pdf = _render_pdf_from_fixture("chase_checking_happy", tmp_path / "chase.pdf")
        adapter = ChaseDepositoryAdapter()
        raw = extract_pdf_to_raw(
            file_path=pdf,
            adapter_id=adapter.adapter_id,
            adapter_version=adapter.adapter_version,
            original_basename="chase.pdf",
        )
        account, statement, summary, txns = adapter.parse_canonical(raw)
        assert account.institution == "Chase"
        assert account.account_type == AccountType.CHECKING
        assert account.account_mask == "*0000"
        assert statement.opening_balance_cents == 100_000
        assert statement.closing_balance_cents == 129_500
        assert summary.deposits_cents == 50_000
        assert len(txns) == 4
        assert sum(t.amount_cents for t in txns) == statement.net_change_cents

    def test_unmatched_bank_fails_registry(self, tmp_path: Path) -> None:
        pdf = _render_lines(
            tmp_path / "unknown.pdf",
            ["SOME OTHER BANK", "CHECKING", "Account Number: *9999"],
        )
        with pytest.raises(AdapterRegistryError):
            get_default_registry().match(pdf)
