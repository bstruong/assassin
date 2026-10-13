# Pitch: \<short name\>

**Status:** Shaping | Shaped | Bet | Shipped | Circuit-broken  
**Builder:** Cloud agent (Cloud-Build Mode)  
**Bettor:** Human PM

---

## Problem

Who is stuck, and what is broken or missing? One or two short paragraphs. No solution yet.

## Appetite

- **Small Batch (default):** 2 weeks fixed time, variable scope  
- **Big Batch:** 6 weeks — only when this pitch explicitly requires it  

State the chosen appetite and what “good enough” means when time runs out.

## Solution (breadboard)

Sketch the elements and how they connect. Prefer boxes and arrows in prose or a small mermaid diagram. Not a pixel-perfect design and not a task checklist.

## Visuals (shaping — required if user-visible)

Mockups / wireframes are produced in **shaping**, before the betting table—not mid-build.

- Link a fat-marker or low-fi wireframe under [`docs/specs/visuals/`](visuals/).
- Baseline vs proposed must be obvious in the filename or caption.
- Skip only when Done-when says Manual UI QA is not applicable.
- High-fidelity pixel comps are optional and must not gate the bet.

See [`visuals/README.md`](visuals/README.md).

## Rabbit holes

Known places where builders can sink unlimited time. Call them out so the bet stays honest.

## No-gos

Explicit exclusions for this appetite. What we will **not** build even if it seems related.

## Done-when

- [ ] Executable QA: `uv run python scripts/qa_<name>.py` prints `[PASS]` / `[FAIL]` for happy and negative cases  
- [ ] Manual UI QA: click path + expected screen result matching the shaping wireframe, **or** `Manual UI QA: not applicable (no user-visible UI).`  
- [ ] If user-visible: wireframe linked from this pitch under `docs/specs/visuals/`  

- [ ] Core invariants held: integer cents, fail-loud contracts, no PII/amount logging  
- [ ] CI gates: `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest --cov=app --cov-fail-under=90 -v`  
- [ ] `ARCH_PLAN.md` updated (shipped archive or circuit-break note)

## Circuit breaker

At appetite end: ship the cut scope **or** drop the bet. Do not silently extend. Unfinished scope returns to [`raw_backlog.md`](raw_backlog.md) or a reshaped pitch.
