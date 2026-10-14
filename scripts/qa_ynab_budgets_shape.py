#!/usr/bin/env python3
"""QA: YNAB budgets / envelopes — shaping artifacts."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _pass(msg: str) -> None:
    print(f"[PASS] {msg}")


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def main() -> int:
    print("QA: YNAB budgets / envelopes — shaping verification")
    failures = 0

    pitch = ROOT / "docs" / "specs" / "pitch_ynab_budgets.md"
    wire = ROOT / "docs" / "specs" / "visuals" / "ynab_budgets_wireframe.html"
    arch = ROOT / "ARCH_PLAN.md"
    migrate = ROOT / "scripts" / "migrate_shape_up_github_project.sh"

    for path in (pitch, wire, arch, migrate):
        if path.is_file():
            _pass(f"exists: {path.relative_to(ROOT)}")
        else:
            _fail(f"missing: {path.relative_to(ROOT)}")
            failures += 1

    text = pitch.read_text(encoding="utf-8") if pitch.is_file() else ""
    for needle in (
        "Status:** Shaped",
        "Ready to Assign",
        "envelope",
        "integer cents",
        "No-gos",
        "ynab_budgets_wireframe.html",
        "ASSIGN_EXCEEDS_AVAILABLE",
    ):
        if needle.lower() in text.lower():
            _pass(f"pitch contains `{needle}`")
        else:
            _fail(f"pitch missing `{needle}`")
            failures += 1

    if "Goals" in text or "goals" in text.lower():
        _pass("goals called out as exclusion/rabbit hole")
    else:
        _fail("pitch should exclude goals")
        failures += 1

    wire_text = wire.read_text(encoding="utf-8") if wire.is_file() else ""
    for needle in ("Ready to Assign", "SYNTHETIC Groceries", "ASSIGN_EXCEEDS_AVAILABLE"):
        if needle in wire_text:
            _pass(f"wireframe contains `{needle}`")
        else:
            _fail(f"wireframe missing `{needle}`")
            failures += 1

    arch_text = arch.read_text(encoding="utf-8") if arch.is_file() else ""
    if "GitHub Project" in arch_text and "migrate_shape_up_github_project.sh" in arch_text:
        _pass("ARCH_PLAN points at GitHub Project + migrate script")
    else:
        _fail("ARCH_PLAN missing GitHub Project pointer")
        failures += 1

    fake = ROOT / "docs" / "specs" / "pitch_ynab_full_parity.md"
    if not fake.is_file():
        _pass("negative: full-parity YNAB pitch path absent")
    else:
        _fail("unexpected full-parity pitch file")
        failures += 1

    if failures:
        print(f"\nResult: [FAIL] ({failures} check(s) failed)")
        return 1
    print("\nResult: [PASS] ynab budgets shaping checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
