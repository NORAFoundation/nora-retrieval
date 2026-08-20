# Rights / Provenance Review Register — nora-retrieval

**Gate:** G5 (licensing/provenance) — **STATUS: BLOCKED**

Formal external rights/provenance review is outstanding for every entry below.
This register is the durable record of each unresolved item. It is **not** a
resolution of any legal/rights question; no item below may be treated as cleared
until a named reviewer records a decision.

| ID | Source repo / commit / lineage | Source path(s) | Why review required | License / rights question | Evidence already collected | Required reviewer / decision | Remediation if rejected | Publication impact |
|----|-------------------------------|----------------|---------------------|---------------------------|---------------------------|------------------------------|-------------------------|--------------------|
| PROV-RETR-001 | `NORA-BITSY/nora-cleanroom-platform` @ `451f8604` (unlicensed); duplicate lineage `NORA-BITSY/nora-foundation-monorepo` @ `dceac8ba` | `packages/context-compiler/src/index.ts`, `packages/retrieval/src/index.ts` → `src/nora_retrieval/compiler.py` | Unlicensed internal repo relicensed Apache-2.0; duplicate lineage recorded; TypeScript→Python port. | Was relicensing authorized for both lineage repos? Does the port carry any derived third-party code? | SOURCE_PROVENANCE.yaml entry incl. `duplicate_lineage`; secret/privacy/license scan pass (agent-level); `authorization_reference: INTERNAL_CLEANROOM_TRANSPLANT_PENDING_EXPLICIT_SIGN_OFF` | Named human reviewer; relicensing sign-off for both lineage repos. | Re-derive or replace ported compiler; re-run gates. | Blocks publication of nora-retrieval (hard blocker per G5). |
| PROV-RETR-002 | `NORAFoundation/meridian` @ `7059de20` (internal, Proprietary) | `src/meridian/search.py`, `src/meridian/timeline.py` → `src/nora_retrieval/strategies/lexical.py`, `src/nora_retrieval/strategies/temporal.py` | Proprietary internal repo relicensed Apache-2.0; explicit sign-off required. | Was internal relicensing authorized? Any contributor competing rights? | SOURCE_PROVENANCE.yaml entry; secret/privacy/license scan pass (agent-level); `authorization_reference: INTERNAL_CLEANROOM_TRANSPLANT_PENDING_EXPLICIT_SIGN_OFF` | Named human reviewer with relicensing authority. | Re-derive strategies independently; re-run gates. | Blocks publication of nora-retrieval (hard blocker per G5). |

**Rights review pending items (inherited from evidence file):**
- RAGEmbed history: earlier RAGEmbed-derived concepts/lineage must be confirmed as either
  NORA-authored or cleared (record lineage before sign-off).

**Status line (required closeout language):**
Technical publication preparation complete. Formal rights/provenance review remains
outstanding. Repository remains private. No visibility authorization has been granted.