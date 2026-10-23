# ARCH_PLAN — Shape Up process (board pointer)

**Operating mode: Cloud-Build** (temporary). Cloud agents shape and build. The human PM bets and accepts via QA. Local Tier-1 / `pi-up.sh` is out of process until explicitly re-enabled.

## Live board (source of truth)

The Shape Up **betting table / in-bet / shipped / cool-down / raw** board lives in a **private GitHub Project** (Projects v2 — not a repository):

| Field | Value |
|-------|--------|
| **Project** | [SAPPHIRE Shape Up](https://github.com/users/bstruong/projects/5) (`PVT_kwHOAujBHc4Bm78V`, #5) |
| **Visibility** | **Private** (`public: false`) |
| **Owner** | `@bstruong` (personal Projects) |
| **Linked repo** | [bstruong/sapphire](https://github.com/bstruong/sapphire) |
| **Primary view** | **Board by Lane** (not Roadmap); Table optional for betting |
| **Fields** | Lane · Appetite · Cycle · Pitch path |
| **Cycle** | `cycle-2026-w42` |

**Verified snapshot (2026-10-14):** Raw 6 · Shaped 1 (YNAB budgets / envelopes) · In-bet 0 · Shipped 9 · Deferred 1 (Watchtower) · Cool-down 4 · Circuit-broken 0.

Re-seed / refresh: `bash scripts/migrate_shape_up_github_project.sh` (owner workstation). Cloud `cursor[bot]` cannot read/write this private user Project without a user PAT (`GH_PROJECT_PAT`).

Pitches and wireframes stay in-repo under [`docs/specs/`](docs/specs/). Architecture contracts stay in [`docs/architecture/`](docs/architecture/). Do **not** append undated “Phase N” checklists to `system_design.md`.

**Agents:** [projects/5](https://github.com/users/bstruong/projects/5) is board SoT. Keep pitch markdown in git; do not reintroduce a second live board table in this file.

---

## How we work

- **Fixed time, variable scope.** Each bet has an appetite. When the appetite ends: ship cut scope or circuit-break (drop the bet). No silent extensions.
- **No endless backlog commitment.** Raw ideas are not scheduled. Only shaped pitches may be bet on.
- **Cloud-Build Mode.** One cloud agent surface shapes pitches and implements chosen bets (TDD, QA script, PR). **No local coding models** required for development.
- **Single Vault product.** One trust boundary. **Local models stay for the PII strip/parse pipeline** (Vault-side runtime). Optional frontier sees sanitized aggregates only. Not a separate “AI Brain” product box.
- **Visuals in shaping.** For user-visible work, fat-marker wireframes land in `docs/specs/visuals/` **before** betting—not during the build. See [`docs/specs/visuals/README.md`](docs/specs/visuals/README.md).
- **Circuit breaker.** Appetite expiry is final for that cycle. Unfinished scope returns to raw backlog (Project Lane=Raw) or is reshaped—never carried as “almost done” debt without a new bet.
- **Acceptance.** PM verifies with `uv run python scripts/qa_<feature>.py`, wireframes (if UI), and Manual UI QA when browser-visible—not by reading diffs alone.

---

## Roles

| Role | Who | Does |
|------|-----|------|
| **Shaper / Builder** | Cloud agent | Write/edit pitches; keep the **GitHub Project** current; implement chosen bets |
| **Bettor / QA** | Human PM | Choose ≤2 bets per cycle; run QA; accept or reject |

No local Tier-1 builder role while Cloud-Build Mode is active.

---

## Board → Project mapping

| Shape Up concept | GitHub Project |
|------------------|----------------|
| Raw backlog | Item with Lane=**Raw** |
| Betting table (shaped, not committed) | Lane=**Shaped** (or **Deferred**) |
| In-bet | Lane=**In-bet** |
| Shipped archive | Lane=**Shipped** |
| Cool-down chores | Lane=**Cool-down** |
| Pitch doc | Custom field **Pitch path** → `docs/specs/pitch_*.md` |
| Appetite | Custom field **Appetite** |
| Cycle id | Custom field **Cycle** (e.g. `cycle-2026-w42`) |

One-liners may still be sketched in [`docs/specs/raw_backlog.md`](docs/specs/raw_backlog.md) before they become Project items; the Project wins when they disagree.

Shipped / cool-down / deferred items (including Account overview home [#50](https://github.com/bstruong/sapphire/pull/50)) live on [Project #5](https://github.com/users/bstruong/projects/5)—not as a second table in this file.

---

## Migrate / refresh the Project

```bash
gh auth refresh -s project,read:project
bash scripts/migrate_shape_up_github_project.sh
```

Then paste the printed URL into the pointer table at the top of this file.

---

## Pitch template

New shaped work: copy [`docs/specs/PITCH_TEMPLATE.md`](docs/specs/PITCH_TEMPLATE.md), add a Project item (Lane=**Shaped**), link **Pitch path**.
