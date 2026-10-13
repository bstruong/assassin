# Pitch: Statements in the browser

**Status:** Bet  
**Builder:** Cloud agent (Cloud-Build Mode)  
**Bettor:** Human PM  
**Appetite:** Small Batch (2 weeks)  
**Institution lock:** Charles Schwab (brokerage) + Chase (depository checking/savings)

---

## Problem

The PM cannot use the Vault UI with real statements today.

- Dashboard **Analyze** returns a **hardcoded** Jinja fragment (`analysis_result.html`) — not Postgres.
- There is **no PDF upload** on `/dashboard` (ingest is API-only: `POST /api/v1/ingest/upload`).
- Existing adapters match **fixture layouts**, not production bank PDFs, so real uploads fail-loud.
- Frontier verify can show aggregates from DB, but that is not a statement ledger the PM can trust as “my data.”

## Appetite

**Small Batch (2 weeks).** Fixed time, variable scope.

**Good enough when time runs out:** From the browser, upload a PDF for **Schwab or Chase**, see a **templated** (non-generative) ledger/summary drawn from persisted Vault rows (integer cents), with loud failure on bad/unmatched PDFs. No third institution. No Watchtower.

## Solution (breadboard)

```mermaid
flowchart LR
  ui[Dashboard_upload] --> ingest[POST_ingest_upload]
  ingest --> adapter[One_institution_adapter]
  adapter --> db[(Postgres_statements_txns)]
  db --> pane2[Templated_Vault_results_pane]
```

1. **Dashboard upload** — HTMX (or form) on Pane 1 posts PDF to existing ingest; surface run status / errors in-pane (fail loud).
2. **Replace fake Analyze** — Pane 2 renders templated HTML from DB (statement header + transactions and/or holdings as applicable). Same template shape every time; values from Vault only.
3. **Adapters** — Schwab (existing brokerage path) + new Chase depository adapter so fixture (and layout-faithful) PDFs reach `canonical_persisted`. Keep fail-loud on drift.
4. **Wireframe** — proposed UI under `docs/specs/visuals/`.

**Institution lock:** Charles Schwab + Chase (checking/savings). Further banks stay on raw backlog.

## Visuals (shaping)

- Baseline: [`visuals/dashboard_baseline_wireframe.html`](visuals/dashboard_baseline_wireframe.html)
- Proposed: [`visuals/statements_in_browser_wireframe.html`](visuals/statements_in_browser_wireframe.html)

## Rabbit holes

- Supporting every bank PDF layout beyond Schwab + Chase in one cycle
- Generative / free-form Pane 2 HTML from an LLM
- Full local-model PII striper productization (keep deterministic adapters unless strip is already in path)
- Grafana / Watchtower / Traefik
- Replacing frontier audit in this bet

## No-gos

- Third institution adapter (Vanguard/Amex/etc. out of appetite)
- SaaS APM or cloud upload of raw PDFs
- Floating-point money; logging PII or raw `amount_cents`
- Redesigning the whole dashboard chrome beyond upload + results
- Treating Watchtower telemetry as part of this appetite

## Done-when

- [ ] `uv run python scripts/qa_statements_in_browser.py` — happy: fixture/seed PDF upload via dashboard path persists and Pane 2 shows templated DB-backed rows; negative: empty upload / unmatched PDF fails loud with `[PASS]` on expected rejection
- [ ] Manual UI QA: start uvicorn → `/dashboard` → upload → see templated ledger; bad PDF shows error (not silent empty success)
- [ ] Proposed wireframe linked and matched by Manual UI QA
- [ ] Institution lock recorded on this pitch + `ARCH_PLAN.md`
- [ ] CI gates green; bet archived or circuit-broken on the board

## Circuit breaker

At 2 weeks: ship upload + DB-templated Pane 2 even if the real-institution adapter is only partially done (fixture path green). Unfinished second banks return to raw backlog. If institution never locks, ship UI-only and circuit-break the adapter slice.
