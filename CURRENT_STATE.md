# Current State — nora-retrieval

**Status:** IMPLEMENTED (Minimum Vertical Slice Verified)  
**Version:** 0.0.1  

## Implemented Vertical Slice

The required minimum vertical slice is complete and verified:
`authorized corpus -> exact + lexical + contradiction retrieval -> ContextBundle -> RetrievalLedger`

- `src/nora_retrieval/contracts.py`: Dataclasses for `ScopeSnapshot`, `StrategyType`, `CoverageState`, `CandidateResult`, `RetrievalLedger`, and `ContextBundle`.
- `src/nora_retrieval/authorization.py`: `ScopeResolver` enforcing authorization-before-retrieval and zero cross-tenant leakage.
- `src/nora_retrieval/compiler.py`: `ContextCompiler` engine with multi-strategy candidate deduplication, contradiction surfacing, and ledger compilation.
- `src/nora_retrieval/strategies/lexical.py`: Local FTS5/BM25 phrase and NEAR search strategy derived from Meridian baselines.
- `src/nora_retrieval/strategies/temporal.py`: Date-range bounded temporal retrieval strategy.

## Verification Evidence

- `make test` / `pytest`: **7 passed in 0.12s**.
- Full end-to-end multi-strategy retrieval, scope authorization, and ledger compilation demonstrated in `tests/test_vertical_slice.py`.
