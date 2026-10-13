#!/usr/bin/env python3
"""QA: Spec & design truthfulness (Shape Up bet).

Happy path: system_design.md frames shipped baseline and points to Shape Up.
Negative path: banned stale phrases that present completed work as future must be absent.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs" / "architecture" / "system_design.md"
ARCH_PLAN = ROOT / "ARCH_PLAN.md"
PITCH = ROOT / "docs" / "specs" / "pitch_design_truthfulness.md"


def _pass(msg: str) -> None:
    print(f"[PASS] {msg}")


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def main() -> int:
    print("QA: Spec & design truthfulness — shipped baseline vs stale future framing")
    failures = 0

    if not DESIGN.is_file():
        _fail(f"missing {DESIGN.relative_to(ROOT)}")
        print("\nResult: [FAIL]")
        return 1

    text = DESIGN.read_text(encoding="utf-8")

    required = (
        "shipped baseline",
        "ARCH_PLAN.md",
        "docs/specs",
        "CREATE TABLE holdings",
        "Code alignment (shipped)",
        "Deployment Architecture (single Vault)",
    )
    for needle in required:
        if needle in text:
            _pass(f"system_design.md contains `{needle}`")
        else:
            _fail(f"system_design.md missing `{needle}`")
            failures += 1

    # Banned: phrases that present completed work as upcoming delivery.
    banned_patterns: list[tuple[str, re.Pattern[str]]] = [
        (
            "holdings later",
            re.compile(r"holdings\s+later", re.IGNORECASE),
        ),
        (
            "remain a later table",
            re.compile(r"remain\s+a\s+later\s+table", re.IGNORECASE),
        ),
        (
            "As-is: investment-only current-state framing",
            re.compile(r"^\*\*As-is:\*\*", re.MULTILINE),
        ),
        (
            "Optional synthetic PDF later",
            re.compile(r"Optional\s+synthetic\s+PDF\s+later", re.IGNORECASE),
        ),
        (
            "future-tense mapping todo (`become signed`)",
            re.compile(r"become\s+signed\s+primary-balance", re.IGNORECASE),
        ),
        (
            "splits into the three abstract subclasses (migration todo)",
            re.compile(r"splits\s+into\s+the\s+three\s+abstract", re.IGNORECASE),
        ),
        (
            "AI Brain workstation deployment as architecture",
            re.compile(
                r"The AI Brain \(Workstation/Local GPU\)",
                re.IGNORECASE,
            ),
        ),
        (
            "Ollama workstation:11434 inference box",
            re.compile(r"workstation-ip>:11434|11434", re.IGNORECASE),
        ),
    ]
    for label, pattern in banned_patterns:
        if pattern.search(text):
            _fail(f"banned stale phrase present: {label}")
            failures += 1
        else:
            _pass(f"negative: banned phrase absent — {label}")

    if "Historical / baseline reference" in text and "Phase 2" in text:
        _pass("sequence/Phase sections marked as baseline/historical")
    else:
        _fail("missing historical/baseline markers on sequence or Phase 2")
        failures += 1

    # Board: bet should be archived (or at least pitch file present).
    if PITCH.is_file():
        _pass("pitch_design_truthfulness.md exists")
    else:
        _fail("pitch_design_truthfulness.md missing")
        failures += 1

    arch = ARCH_PLAN.read_text(encoding="utf-8") if ARCH_PLAN.is_file() else ""
    if "Spec & design truthfulness" in arch and "Shipped" in arch:
        _pass("ARCH_PLAN.md records design truthfulness as shipped")
    else:
        _fail("ARCH_PLAN.md does not archive Spec & design truthfulness as shipped")
        failures += 1

    if failures:
        print(f"\nResult: [FAIL] ({failures} check(s) failed)")
        return 1
    print("\nResult: [PASS] design truthfulness checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
