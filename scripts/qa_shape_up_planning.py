#!/usr/bin/env python3
"""QA: Shape Up planning artifacts (Cloud-Build Mode).

Verifies control-plane docs exist and key process phrases are present.
Happy path: required files and markers found.
Negative path: intentionally checks that a non-existent pitch path is absent.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _pass(msg: str) -> None:
    print(f"[PASS] {msg}")


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def main() -> int:
    print("QA: Shape Up planning (Cloud-Build) — artifact and marker verification")
    failures = 0

    required = [
        ROOT / "ARCH_PLAN.md",
        ROOT / "docs" / "specs" / "PITCH_TEMPLATE.md",
        ROOT / "docs" / "specs" / "raw_backlog.md",
        ROOT / "docs" / "specs" / "pitch_watchtower_telemetry.md",
        ROOT / "docs" / "specs" / "pitch_design_truthfulness.md",
        ROOT / "AGENTS.md",
        ROOT / "docs" / "architecture" / "system_design.md",
        ROOT / "docs" / "specs" / "visuals" / "README.md",
        ROOT / "docs" / "specs" / "visuals" / "dashboard_baseline_wireframe.html",
    ]
    for path in required:
        if path.is_file():
            _pass(f"exists: {path.relative_to(ROOT)}")
        else:
            _fail(f"missing: {path.relative_to(ROOT)}")
            failures += 1

    arch = (ROOT / "ARCH_PLAN.md").read_text(encoding="utf-8")
    for needle in (
        "Cloud-Build",
        "Betting table",
        "Shipped bets archive",
        "Cool-down queue",
        "circuit breaker",
        "Visuals in shaping",
        "Single Vault",
    ):
        if needle.lower() in arch.lower():
            _pass(f"ARCH_PLAN.md contains `{needle}`")
        else:
            _fail(f"ARCH_PLAN.md missing `{needle}`")
            failures += 1

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "Cloud-Build Mode" in agents:
        _pass("AGENTS.md declares Cloud-Build Mode")
    else:
        _fail("AGENTS.md missing Cloud-Build Mode")
        failures += 1
    if "STRICTLY FORBIDDEN from writing application code" in agents:
        _fail("AGENTS.md still forbids cloud implementation (Cloud-Build not applied)")
        failures += 1
    else:
        _pass("AGENTS.md no longer hard-forbids cloud implementation")

    design = (ROOT / "docs" / "architecture" / "system_design.md").read_text(
        encoding="utf-8"
    )
    for needle in ("shipped baseline", "ARCH_PLAN.md", "docs/specs"):
        if needle in design:
            _pass(f"system_design.md references `{needle}`")
        else:
            _fail(f"system_design.md missing `{needle}`")
            failures += 1

    # Negative: a fabricated pitch must not exist (guards against silent invent).
    fake = ROOT / "docs" / "specs" / "pitch_does_not_exist_xyz.md"
    if fake.exists():
        _fail(f"unexpected file present: {fake.relative_to(ROOT)}")
        failures += 1
    else:
        _pass("negative: fabricated pitch path correctly absent")

    if failures:
        print(f"\nResult: [FAIL] ({failures} check(s) failed)")
        return 1
    print("\nResult: [PASS] all Shape Up planning checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
