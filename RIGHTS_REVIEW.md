# Rights / Provenance Review Register — nora-retrieval

**Gate:** G5 (licensing/provenance) — **STATUS: BLOCKED**

**Review executed 2026-08-20.** Every lineage entry below received an evidence-based disposition
(verified via GitHub API commit/license checks, candidate git-history searches, and harvest-commit
file inspection). BLOCKED entries may not be treated as cleared until a named human reviewer
records a decision. This register is the durable record.

## Verification record (2026-08-20)

- Source commits checked with `gh api repos/{owner}/{repo}/commits/{sha}`.
- Source licenses checked with `gh api repos/{owner}/{repo}/license` and by reading the LICENSE
  file at the recorded commit.
- Contamination search (`git log --all -S`) across this repo for: RAGEmbed, Meridian-Canon,
  NECCL, nora-canon, blakeox, legal-mcp, LawLLama, CC BY-NC, courtlistener-mcp, mcro-mcp,
  agent-canon → **0 hits** (the only `RAGEmbed` string in history is this repo's own G5 register
  commit `5806b72` — a doc mention, not migrated code).
- Harvested files inspected at harvest commits (`git show`): small derived implementations
  importing `nora_retrieval` contracts, docstring-attributed to sources; not verbatim copies.
  No vendor directories.
- Evidence artifacts: `/tmp/g5deep.log`, `/tmp/g5verify.log`, `/tmp/g5ev_nora-retrieval.log`.

## Dispositions

| ID | Source repo / commit | Source → target | License verification (2026-08-20) | Disposition | Required reviewer / decision |
|----|----------------------|-----------------|-----------------------------------|-------------|------------------------------|
| PROV-RETR-001 | `NORA-BITSY/nora-cleanroom-platform` @ `451f8604`; duplicate lineage `NORA-BITSY/nora-foundation-monorepo` @ `dceac8ba` | `packages/context-compiler/src/index.ts`, `packages/retrieval/src/index.ts` → `src/nora_retrieval/compiler.py` | Both commits **EXIST**. **Neither repo has a LICENSE file.** | **BLOCKED — RIGHTS UNCLEAR** (unlicensed internal sources ported TypeScript→Python; relicensing sign-off required for both lineage repos) | Named human reviewer: relicensing sign-off for both lineage repos |
| PROV-RETR-002 | `NORAFoundation/meridian` @ `7059de20` | `src/meridian/search.py`, `src/meridian/timeline.py` → `src/nora_retrieval/strategies/lexical.py`, `src/nora_retrieval/strategies/temporal.py` | Commit **EXISTS**. LICENSE at `7059de20` = **MERIDIAN PROPRIETARY SOFTWARE LICENSE**. | **BLOCKED — LICENSE INCOMPATIBLE** (proprietary source; derived strategies may not be redistributed under Apache-2.0 without relicensing sign-off) | Named human reviewer with NORA Foundation relicensing authority |

## Rights review pending items (2026-08-20)

- RAGEmbed history: contamination search found **no RAGEmbed-derived code** in this repo's
  history (only the register-doc mention). The canon-map RAGEmbed concern is resolved for this
  candidate at the contamination level; the upstream `RAGEmbed` repo itself has **no LICENSE file**
  and is not a recorded source of candidate material.
- Cleanroom/monorepo duplicate lineage (PROV-RETR-001): both commits verified; one lineage, two
  repos, neither licensed.
- Meridian-derived strategies (PROV-RETR-002): proprietary — relicensing or independent
  re-derivation required.

**Status line (required closeout language):**
G5 rights/provenance review executed 2026-08-20 — **result: BLOCKED** (0/2 lineages clear).
Repository remains private. No visibility authorization has been granted.
**NOT READY FOR PUBLICATION — G5 RIGHTS/PROVENANCE BLOCKERS REMAIN.**