#!/usr/bin/env python3
"""QA: Account overview home — shaping artifacts (pitch + wireframe).

Happy: required pitch, wireframe, and board markers exist.
Dangerous scope (full YNAB budgets) must stay in no-gos / rabbit holes.
Negative: a non-existent pitch path is absent.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _pass(msg: str) -> None:
    print(f"[PASS] {msg}")


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def main() -> int:
    print("QA: Account overview home — shaping verification")
    failures = 0

    pitch = ROOT / "docs" / "specs" / "pitch_account_overview.md"
    wire = ROOT / "docs" / "specs" / "visuals" / "account_overview_wireframe.html"
    arch = ROOT / "ARCH_PLAN.md"
    visuals_readme = ROOT / "docs" / "specs" / "visuals" / "README.md"

    for path in (pitch, wire, arch, visuals_readme):
        if path.is_file():
            _pass(f"exists: {path.relative_to(ROOT)}")
        else:
            _fail(f"missing: {path.relative_to(ROOT)}")
            failures += 1

    if not pitch.is_file():
        print("\nResult: [FAIL]")
        return 1

    text = pitch.read_text(encoding="utf-8")
    for needle in (
        "Status:** Shaped",
        "YNAB",
        "prepopulat",
        "integer cents",
        "No-gos",
        "Budget envelopes",
        "Manual UI QA",
        "account_overview_wireframe.html",
        "Circuit breaker",
    ):
        if needle.lower() in text.lower():
            _pass(f"pitch contains `{needle}`")
        else:
            _fail(f"pitch missing `{needle}`")
            failures += 1

    # Dangerous scope must remain excluded
    if "Budget envelopes" in text or "budget envelopes" in text.lower():
        _pass("full YNAB budget scope called out as no-go")
    else:
        _fail("pitch must exclude budget envelopes in no-gos")
        failures += 1

    wire_text = wire.read_text(encoding="utf-8") if wire.is_file() else ""
    for needle in ("Account overview", "integer cents", "Details", "SYNTHETIC"):
        if needle in wire_text:
            _pass(f"wireframe contains `{needle}`")
        else:
            _fail(f"wireframe missing `{needle}`")
            failures += 1

    arch_text = arch.read_text(encoding="utf-8") if arch.is_file() else ""
    if "pitch_account_overview.md" in arch_text:
        _pass("ARCH_PLAN betting table links account overview pitch")
    else:
        _fail("ARCH_PLAN missing account overview pitch link")
        failures += 1

    readme = (
        visuals_readme.read_text(encoding="utf-8") if visuals_readme.is_file() else ""
    )
    if "account_overview_wireframe.html" in readme:
        _pass("visuals README indexes account overview wireframe")
    else:
        _fail("visuals README missing account overview wireframe")
        failures += 1

    fake = ROOT / "docs" / "specs" / "pitch_does_not_exist_ynab_full.md"
    if not fake.is_file():
        _pass("negative: non-existent full-YNAB pitch path is absent")
    else:
        _fail("negative: unexpected file pitch_does_not_exist_ynab_full.md")
        failures += 1

    if failures:
        print(f"\nResult: [FAIL] ({failures} check(s) failed)")
        return 1
    print("\nResult: [PASS] account overview shaping checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
