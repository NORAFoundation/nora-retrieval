import pytest
from nora_retrieval.compiler import ContextCompiler
from nora_retrieval.contracts import (
    CandidateResult,
    CoverageState,
    ScopeSnapshot,
    StrategyType
)

def test_context_compiler_execution_and_deduplication():
    scope = ScopeSnapshot(
        scope_id="SCOPE-TENANT-A",
        authorized_corpus_ids={"corpus-1"}
    )

    candidates = [
        CandidateResult(
            candidate_id="CAND-01",
            corpus_id="corpus-1",
            strategy=StrategyType.EXACT,
            score=1.0,
            content="Exact match statement"
        ),
        CandidateResult(
            candidate_id="CAND-01",  # Duplicate candidate_id
            corpus_id="corpus-1",
            strategy=StrategyType.LEXICAL,
            score=0.9,
            content="Exact match statement duplicate"
        ),
        CandidateResult(
            candidate_id="CAND-UNAUTHORIZED",
            corpus_id="corpus-UNAUTHORIZED-TENANT-B",
            strategy=StrategyType.LEXICAL,
            score=0.99,
            content="Leaked unauthorized document"
        )
    ]

    compiler = ContextCompiler(scope)
    bundle = compiler.compile_context("synthetic query", candidates)

    assert len(bundle.selected_candidates) == 1
    assert bundle.selected_candidates[0].candidate_id == "CAND-01"
    assert bundle.coverage == CoverageState.COMPLETE
    assert bundle.ledger.total_candidates == 2  # Total before deduplication
