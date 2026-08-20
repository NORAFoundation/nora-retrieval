# Current State — nora-retrieval

**Status:** OSS EXTRACTION / RECONCILIATION IN PROGRESS
**Version:** 0.0.1

## Implemented Reference Slice

The minimum reference vertical slice is complete and verified:
`authorized corpus -> exact + lexical + contradiction retrieval -> ContextBundle -> RetrievalLedger`

- `src/nora_retrieval/contracts.py`: Dataclasses for `ScopeSnapshot`, `StrategyType`, `CoverageState`, `CandidateResult`, `RetrievalLedger`, and `ContextBundle`.
- `src/nora_retrieval/authorization.py`: `ScopeResolver` enforcing authorization-before-retrieval and zero cross-tenant leakage.
- `src/nora_retrieval/compiler.py`: `ContextCompiler` engine with multi-strategy candidate deduplication, contradiction surfacing, and ledger compilation.
- `src/nora_retrieval/strategies/lexical.py`: Local FTS5/BM25 phrase and NEAR search strategy derived from Meridian baselines.
- `src/nora_retrieval/strategies/temporal.py`: Date-range bounded temporal retrieval strategy.

## Verified

- `make test` / `pytest`: **7 passed in 0.12s**.
- Vertical-slice test path: `tests/test_vertical_slice.py`.
- End-to-end multi-strategy retrieval, scope authorization, and ledger compilation demonstrated.

## Not Yet Established

- canonical feature parity;
- public extraction completeness;
- production deployment status;
- vector/pgvector embedding strategy integration and hybrid scoring calibration.
