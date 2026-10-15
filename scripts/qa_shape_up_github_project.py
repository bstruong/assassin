#!/usr/bin/env python3
"""QA: Shape Up board migration artifacts (GitHub Project pointer)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _pass(msg: str) -> None:
    print(f"[PASS] {msg}")


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def main() -> int:
    print("QA: Shape Up GitHub Project migration — artifact verification")
    failures = 0

    arch = ROOT / "ARCH_PLAN.md"
    script = ROOT / "scripts" / "migrate_shape_up_github_project.sh"
    if arch.is_file():
        _pass("exists: ARCH_PLAN.md")
    else:
        _fail("missing ARCH_PLAN.md")
        failures += 1
    if script.is_file() and script.stat().st_mode & 0o111:
        _pass("exists + executable: migrate_shape_up_github_project.sh")
    elif script.is_file():
        _fail("migrate script exists but is not executable")
        failures += 1
    else:
        _fail("missing migrate_shape_up_github_project.sh")
        failures += 1

    text = arch.read_text(encoding="utf-8") if arch.is_file() else ""
    for needle in (
        "GitHub Project",
        "PRIVATE",
        "Lane",
        "migrate_shape_up_github_project.sh",
        "source of truth",
    ):
        if needle.lower() in text.lower():
            _pass(f"ARCH_PLAN contains `{needle}`")
        else:
            _fail(f"ARCH_PLAN missing `{needle}`")
            failures += 1

    # Must not still claim the markdown tables are the live betting table
    if "| **In-bet pitches** |" in text and "GitHub Project" in text:
        # pointer file should not revive the old cycle table as SoT
        if "Live board (source of truth)" in text:
            _pass("ARCH_PLAN declares Project as live board SoT")
        else:
            _fail("ARCH_PLAN unclear about Project SoT")
            failures += 1
    elif "Live board (source of truth)" in text:
        _pass("ARCH_PLAN declares Project as live board SoT")
    else:
        _fail("ARCH_PLAN missing live board SoT section")
        failures += 1

    if "Betting table" in text and "Shaped candidates for the **next** bet" in text:
        _fail("ARCH_PLAN still embeds the old markdown betting table as live board")
        failures += 1
    else:
        _pass("old markdown betting table not present as live SoT")

    if failures:
        print(f"\nResult: [FAIL] ({failures} check(s) failed)")
        return 1
    print("\nResult: [PASS] shape-up github project migration checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
