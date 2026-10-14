# ARCH_PLAN — Shape Up process (board pointer)

**Operating mode: Cloud-Build** (temporary). Cloud agents shape and build. The human PM bets and accepts via QA. Local Tier-1 / `pi-up.sh` is out of process until explicitly re-enabled.

## Live board (source of truth)

The Shape Up **betting table / in-bet / shipped / cool-down / raw** board lives in a **private GitHub Project** (Projects v2 — not a repository):

| Field | Value |
|-------|--------|
| **Project** | [ASSASSIN Shape Up](https://github.com/users/bstruong/projects/5) |
| **Visibility** | **Private** |
| **Owner** | `@bstruong` (personal Projects) |
| **Primary view** | **Board** by **Lane** (Table optional for betting; avoid Roadmap) |
| **Lane field** | Raw \| Shaped \| In-bet \| Shipped \| Circuit-broken \| Cool-down \| Deferred |

Re-seed / refresh fields+items: `bash scripts/migrate_shape_up_github_project.sh` (owner workstation; cloud bot cannot access private Projects).

Pitches and wireframes stay in-repo under [`docs/specs/`](docs/specs/). Architecture contracts stay in [`docs/architecture/`](docs/architecture/). Do **not** append undated “Phase N” checklists to `system_design.md`.

**Agents:** treat [projects/5](https://github.com/users/bstruong/projects/5) as board SoT when the PM grants access; until then, keep pitch markdown + this pointer in git. Do not reintroduce a second live board table in this file.

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
