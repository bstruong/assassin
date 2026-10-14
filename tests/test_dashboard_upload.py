"""Dashboard PDF upload returns templated DB-backed ledger HTML."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def client(postgres_url: str, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("DATABASE_URL", postgres_url)
    from app.api.app import create_app
    from app.db.connection import init_db

    init_db()
    return TestClient(create_app())


def _render_pdf_from_fixture(fixture_name: str, target_path: Path) -> Path:
    data = json.loads(
        (FIXTURES_DIR / f"{fixture_name}.json").read_text(encoding="utf-8")
    )
    lines = data["raw_text"].split("\n")
    c = canvas.Canvas(str(target_path))
    y = 750
    for line in lines:
        line = re.sub(r"(\t|\s{2,})", " | ", line)
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    return target_path


class TestDashboardUpload:
    def test_upload_chase_returns_ledger(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        pdf = _render_pdf_from_fixture("chase_checking_happy", tmp_path / "chase.pdf")
        with pdf.open("rb") as handle:
            response = client.post(
                "/api/v1/dashboard/upload",
                files={"file": ("chase.pdf", handle, "application/pdf")},
                headers={"HX-Request": "true"},
            )
        assert response.status_code == 200
        assert "Vault Ledger" in response.text
        assert "chase_depository" in response.text
        assert "SYNTHETIC Payroll" in response.text
        assert re.findall(r"\$\d+\.\d{2,}", response.text) == []

    def test_upload_schwab_returns_ledger(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        pdf = _render_pdf_from_fixture("brokerage_cash_happy", tmp_path / "schwab.pdf")
        with pdf.open("rb") as handle:
            response = client.post(
                "/api/v1/dashboard/upload",
                files={"file": ("schwab.pdf", handle, "application/pdf")},
                headers={"HX-Request": "true"},
            )
        assert response.status_code == 200
        assert "Vault Ledger" in response.text
        assert "schwab_brokerage" in response.text

    def test_upload_unmatched_fails_loud(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        pdf_path = tmp_path / "unknown.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(50, 750, "UNKNOWN CREDIT UNION")
        c.drawString(50, 735, "CHECKING")
        c.save()
        with pdf_path.open("rb") as handle:
            response = client.post(
                "/api/v1/dashboard/upload",
                files={"file": ("unknown.pdf", handle, "application/pdf")},
                headers={"HX-Request": "true"},
            )
        assert response.status_code == 400
        assert "ADAPTER_MATCH_FAILED" in response.text

    def test_upload_missing_file_fails_loud(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/dashboard/upload",
            headers={"HX-Request": "true"},
        )
        assert response.status_code == 400
        assert "MISSING_FILE" in response.text
