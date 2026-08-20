import pytest
from nora_retrieval.contracts import (
    CandidateResult,
    ContextBundle,
    CoverageState,
    RetrievalLedger,
    RetrievalLedgerEntry,
    ScopeSnapshot,
    StrategyType
)

def test_nora_retrieval_contracts():
    scope = ScopeSnapshot(
        scope_id="SCOPE-001",
        authorized_corpus_ids={"corpus-A"},
        allowed_data_classes={"public"}
    )
    
    cand = CandidateResult(
        candidate_id="CAND-001",
        corpus_id="corpus-A",
        strategy=StrategyType.EXACT,
        score=1.0,
        content="Synthetic exact match content"
    )
    
    entry = RetrievalLedgerEntry(
        entry_id="ENTRY-001",
        strategy=StrategyType.EXACT,
        query="exact query",
        candidates_count=1,
        execution_ms=1.5
    )
    
    ledger = RetrievalLedger(
        ledger_id="LEDGER-001",
        scope_id=scope.scope_id,
        entries=[entry],
        total_candidates=1
    )
    
    bundle = ContextBundle(
        bundle_id="BUNDLE-001",
        query="exact query",
        scope_id=scope.scope_id,
        coverage=CoverageState.COMPLETE,
        selected_candidates=[cand],
        ledger=ledger
    )
    
    assert bundle.coverage == CoverageState.COMPLETE
    assert len(bundle.selected_candidates) == 1
    assert bundle.ledger.total_candidates == 1
