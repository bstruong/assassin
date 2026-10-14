# Shape Up visuals

## When do mockups and wireframes happen?

**During shaping — before the betting table.** Not during the build cycle.

| Phase | Visual work |
|-------|-------------|
| **Raw backlog** | None. One-liners only. |
| **Shaping** | Fat-marker sketches, breadboards, and **low-fi wireframes** for any user-visible surface. These make the pitch reviewable. |
| **Betting** | PM reviews pitch **plus** linked wireframes. No visual → UI bet is not ready. |
| **Building** | Implement against the shaped wireframe. Do not invent a second design pass mid-cycle (rabbit hole). |
| **Cool-down** | Optional polish sketches for the *next* cycle’s pitches—not unscoped redesign of what just shipped. |

Shape Up intentionally avoids high-fidelity pixel comps as a gating artifact. Prefer:

1. **Breadboard** (elements + connections) in the pitch  
2. **Fat-marker / low-fi wireframe** (layout, hierarchy, primary actions) in this folder  
3. **Done-when** Manual UI QA that matches the wireframe  

## Conventions

- Path: `docs/specs/visuals/<pitch_or_surface>_wireframe.html` (open in a browser) or `.md` with ASCII/mermaid when HTML is overkill.
- Label the file and pitch: **baseline** (current shipped UI) vs **proposed** (shaped change).
- Synthetic copy only (`SYNTHETIC`, `*0000`). No real customer data.
- No hallucinated SRI hashes or asset UUIDs.

## Baseline artifacts

| File | Surface |
|------|---------|
| [dashboard_baseline_wireframe.html](dashboard_baseline_wireframe.html) | Current Vault dashboard (dual pane: ask + results / frontier verify) |
| [statements_in_browser_wireframe.html](statements_in_browser_wireframe.html) | **Proposed** — PDF upload + templated DB ledger (statements-in-browser bet) |
