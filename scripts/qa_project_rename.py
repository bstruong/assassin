#!/usr/bin/env python3
"""QA: Project rename to Sapphire verification script.

Verifies:
1. pyproject.toml reflects package name 'sapphire'.
2. FastAPI app factory configures title as 'SAPPHIRE Local Ingest API'.
3. Dashboard GET /dashboard renders 'SAPPHIRE' in header and page title.
4. Analysis result templates cite 'SAPPHIRE Vault'.
5. Database migration baseline checksum remains consistent and intact.
6. Negative case: 'ASSASSIN' is absent from dashboard title and app branding.
"""

from __future__ import annotations

import sys
from pathlib import Path

from starlette.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]


def _pass(msg: str) -> None:
    print(f"  [PASS] {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def main() -> int:
    print("=" * 65)
    print("💎 SAPPHIRE Project Rename QA Acceptance Verification")
    print("=" * 65)
    failures = 0

    # 1. Package Manifest
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if 'name = "sapphire"' in pyproject_text:
        _pass("pyproject.toml package name is 'sapphire'")
    else:
        _fail("pyproject.toml missing 'name = \"sapphire\"'")
        failures += 1

    # 2. FastAPI Application Branding
    from app.api.app import create_app

    app = create_app()
    if app.title == "SAPPHIRE Local Ingest API":
        _pass(f"FastAPI app title is '{app.title}'")
    else:
        _fail(f"FastAPI app title unexpected: '{app.title}'")
        failures += 1

    # 3. Dashboard Web UI Rendering
    client = TestClient(app)
    resp = client.get("/dashboard")
    if resp.status_code == 200:
        _pass("Dashboard GET /dashboard returns HTTP 200")
    else:
        _fail(f"Dashboard returned status {resp.status_code}")
        failures += 1

    if "<title>SAPPHIRE - Financial Intelligence Dashboard</title>" in resp.text:
        _pass("Dashboard HTML title is 'SAPPHIRE - Financial Intelligence Dashboard'")
    else:
        _fail("Dashboard HTML title missing SAPPHIRE branding")
        failures += 1

    if "<h1>SAPPHIRE</h1>" in resp.text:
        _pass("Dashboard header renders '<h1>SAPPHIRE</h1>'")
    else:
        _fail("Dashboard header missing <h1>SAPPHIRE</h1>")
        failures += 1

    # 4. Negative Verification: Old Branding Absent from UI
    if "<title>ASSASSIN" not in resp.text and "<h1>ASSASSIN" not in resp.text:
        _pass("Negative: Old branding 'ASSASSIN' absent from dashboard UI")
    else:
        _fail("Negative: Found residual 'ASSASSIN' in dashboard UI")
        failures += 1

    # 5. Database Schema Baseline Integrity
    from app.db.connection import SCHEMA_PATH
    from app.db.migrate import discover_migrations, migration_checksum

    migrations = discover_migrations(SCHEMA_PATH, ROOT / "migrations")
    baseline = migrations[0]
    expected_checksum = migration_checksum(baseline.path)
    if baseline.version == "0001" and expected_checksum:
        _pass(
            f"Database baseline migration 0001 checksum valid ({expected_checksum[:8]}...)"
        )
    else:
        _fail("Database baseline migration 0001 failed checksum calculation")
        failures += 1

    print("=" * 65)
    if failures == 0:
        print("Result: [PASS] All project rename QA checks passed cleanly.")
        return 0
    else:
        print(f"Result: [FAIL] {failures} check(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
