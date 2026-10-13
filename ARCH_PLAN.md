# ARCH_PLAN — Shape Up Control Plane

**Operating mode: Cloud-Build** (temporary). Cloud agents shape and build. The human PM bets and accepts via QA. Local Tier-1 / `pi-up.sh` is out of process until explicitly re-enabled.

Active work lives here and in [`docs/specs/`](docs/specs/). Architecture contracts stay in [`docs/architecture/`](docs/architecture/). Do not append undated “Phase N” checklists to `system_design.md`.

---

## How we work

- **Fixed time, variable scope.** Each bet has an appetite. When the appetite ends: ship cut scope or circuit-break (drop the bet). No silent extensions.
- **No endless backlog commitment.** Raw ideas are not scheduled. Only shaped pitches may be bet on.
- **Cloud-Build Mode.** One cloud agent surface shapes pitches and implements chosen bets (TDD, QA script, PR).
- **Circuit breaker.** Appetite expiry is final for that cycle. Unfinished scope returns to raw backlog or is reshaped—never carried as “almost done” debt without a new bet.
- **Acceptance.** PM verifies with `uv run python scripts/qa_<feature>.py` (and Manual UI QA when the surface is browser-visible)—not by reading diffs.

---

## Roles

| Role | Who | Does |
|------|-----|------|
| **Shaper / Builder** | Cloud agent | Write/edit pitches; keep this board current; implement chosen bets |
| **Bettor / QA** | Human PM | Choose ≤2 bets per cycle; run QA; accept or reject |

No local Tier-1 builder role while Cloud-Build Mode is active.

---

## Current cycle

| Field | Value |
|-------|--------|
| **Cycle id** | `cycle-2026-w42` |
| **Mode** | Cloud-Build |
| **Appetite budget** | Small Batch (default 2 weeks); Big Batch only if a pitch says so |
| **In-bet pitches** | _None — awaiting next PM bet_ |
| **Hill status** | _n/a_ |

**Hill language:** *uphill* = unknowns still being resolved; *downhill* = known work being executed.

---

## Betting table

Shaped candidates for the **next** bet. Listing here is **not** a commitment.

| Pitch | Appetite | Summary | Status |
|-------|----------|---------|--------|
| [Watchtower telemetry path](docs/specs/pitch_watchtower_telemetry.md) | Small Batch (2 weeks) | Verifiable OTel → collector smoke path for Watchtower; no SaaS APM | Shaped — ready to bet |

Unshaped one-liners live in [`docs/specs/raw_backlog.md`](docs/specs/raw_backlog.md).

---

## Shipped bets archive

Do not re-queue these as roadmap items.

| Bet | Outcome |
|-----|---------|
| Pipeline steps 1–9 (contracts → extract → depository/card → Postgres → investment → registry → combined → ingest) | Shipped — baseline |
| Phase 2 HTMX dashboard + tiered MCP + frontier aggregate audit | Shipped — baseline |
| Local HTMX asset + AGENTS frontend SRI ban + Playwright dashboard E2E | Shipped |
| Holdings (`quantity_nanos` / `market_value_cents`), Vanguard adapter, portfolio bridge | Shipped |
| App-side telemetry helpers + QA scripts | Shipped (full Watchtower stack remains a separate pitch) |
| Spec & design truthfulness (`system_design.md` shipped vs raw framing + `qa_design_truthfulness.py`) | Shipped |

---

## Cool-down queue

Unshaped chores only—not new features. Pick up between cycles.

- CI nits that do not change product surface.
- Mutation nightly / coverage hygiene with no new capability.
- Deep copy-edit of remaining historical paragraphs in architecture docs (optional polish; not a feature).

---

## Pitch template

New shaped work: copy [`docs/specs/PITCH_TEMPLATE.md`](docs/specs/PITCH_TEMPLATE.md).
