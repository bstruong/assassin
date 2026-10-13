# Pitch: Spec & design truthfulness

**Status:** Shaped  
**Builder:** Cloud agent (Cloud-Build Mode)  
**Bettor:** Human PM  
**Appetite:** Small Batch (cool-down friendly; ≤2 weeks)

---

## Problem

[`docs/architecture/system_design.md`](../architecture/system_design.md) still reads in places like a future build plan (“as-is” investment-cash-only, “holdings later”, Implementation Sequence as upcoming work, Phase 2 as expansion-to-come). The product has largely shipped that baseline. Stale wording invites agents and humans to re-implement finished work or invent Phase N checklists instead of Shape Up pitches.

## Appetite

**Small Batch / cool-down.** Docs-only preferred. Good enough: a reader can tell **shipped baseline** from **raw ideas** in one pass, and new work is pointed at [`ARCH_PLAN.md`](../../ARCH_PLAN.md) + [`docs/specs/`](.).

## Solution (breadboard)

1. Keep contracts, DDL, and reconciliation math authoritative—do not redesign them.
2. Replace stale “as-is / later / sequence as future” framing with **Shipped baseline** vs pointers to raw backlog / pitches.
3. Mark Implementation Sequence and Phase 2 as historical baseline description where behavior already exists in `app/`.
4. Leave open ops ideas (full Watchtower Grafana stack, new adapters) in [`raw_backlog.md`](raw_backlog.md) or existing pitches—not as Phase 3.

## Rabbit holes

- Rewriting the entire architecture from scratch
- Changing canonical schemas “while we’re here”
- Generating synthetic product features to match old Phase language

## No-gos

- Application code, schema migrations, or adapter behavior changes (unless a factual doc claim is wrong and needs a tiny clarifying comment in code—prefer docs-only)
- Dated multi-quarter roadmap
- Re-listing shipped dashboard/MCP/pipeline items as future bets

## Done-when

- [ ] `system_design.md` preamble and sequence/Phase sections no longer present completed work as upcoming delivery
- [ ] Active planning pointed to `ARCH_PLAN.md` + `docs/specs/`
- [ ] Manual UI QA: not applicable (no user-visible UI)
- [ ] Optional: `scripts/qa_design_truthfulness.py` that greps for banned stale phrases (`holdings later`, “as-is” investment-only as current state) and prints `[PASS]` / `[FAIL]`
- [ ] `ARCH_PLAN.md` archive/cool-down updated

## Circuit breaker

Ship the preamble + sequence/Phase annotations even if every historical paragraph is not rewritten. Deep copy-edits return to cool-down.
