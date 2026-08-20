# Publication Review — nora-retrieval

**Status: BLOCKED**

This review is fail-closed. A scaffold cannot pass it merely because required files exist.

## Closeout status

- Technical publication preparation complete.
- G5 rights/provenance review executed 2026-08-20 — **result: BLOCKED** (see `RIGHTS_REVIEW.md`).
- Repository remains private.
- No visibility authorization has been granted.

## Evidence (2026-08-20)

- **G0 identity**: clean target history from "Initial clean scaffold baseline" (9cef82c); no legacy repo reused.
- **G1 technical**: `make doctor` PASS, `make validate` PASS, pytest 7 passed; `examples/demo.py` exit 0 (scoped retrieval PASS). HEAD `3a5665e`.
- **G2 claims**: CURRENT_STATE.md test count 7 matches; no production-ready claims.
- **G3 privacy / G4 secrets**: working-tree + full-history scans PASS (2026-08-20, `/tmp/scan2_*.log`); only synthetic fixture values matched.
- **G5 rights/provenance**: review executed 2026-08-20 — **BLOCKED** (PROV-RETR-001 cleanroom/monorepo: **RIGHTS UNCLEAR** — neither lineage repo has a LICENSE; PROV-RETR-002 Meridian: **LICENSE INCOMPATIBLE** — verified proprietary at `7059de20`; RAGEmbed: no code found in history, only register-doc mention). See `RIGHTS_REVIEW.md`.
- **G6 contributor readiness**: CONTRIBUTING/CODE_OF_CONDUCT/SECURITY/ROADMAP/ARCHITECTURE present; issue + PR templates; 6 issue seeds; good-first-issue #4 open.
- **G7 pre-flip remote assurance**: ci PASS on pushed main (runs 32335414204, 32334862395); codeql workflow pinned v4 + actions:read (commit 8503d84).
- **G7 post-flip security verification**: DEFERRED — codeql SARIF upload requires Advanced Security (not available for private repos on GitHub Free); branch protection/rulesets 403. Features unlock at authorized visibility switch.
- **G8 publication acknowledgement**: NOT RUN — no visibility authorization.

Full evidence and run IDs in PUBLICATION_EVIDENCE.yaml (authoritative).

**Not publishable until: (1) formal rights review completes (G5), (2) post-flip security
features are verified after an authorized visibility switch (G7-post), and (3) explicit
visibility authorization is granted (G8).**