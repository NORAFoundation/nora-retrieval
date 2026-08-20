import pytest
from nora_retrieval.authorization import ScopeResolver
from nora_retrieval.compiler import ContextCompiler
from nora_retrieval.contracts import (
    CandidateResult,
    ContextBundle,
    CoverageState,
    ScopeSnapshot,
    StrategyType
)
from nora_retrieval.strategies.lexical import LexicalRetrievalStrategy

def test_nora_retrieval_minimum_vertical_slice():
    """
    Minimum Vertical Slice:
    authorized synthetic corpus -> exact + lexical + contradiction retrieval
    -> ContextBundle -> RetrievalLedger
    """
    # 1. Authorize synthetic corpus scope
    scope = ScopeSnapshot(
        scope_id="SCOPE-SYNTHETIC-001",
        authorized_corpus_ids={"corpus-authorized-01"}
    )
    
    # 2. Index synthetic corpus into lexical FTS5 strategy
    lexical_strat = LexicalRetrievalStrategy(":memory:")
    lexical_strat.index_document(
        candidate_id="DOC-EXACT-100",
        corpus_id="corpus-authorized-01",
        content="Synthetic authorized agreement clause 100"
    )
    
    # 3. Retrieve candidates across strategies
    lexical_candidates = lexical_strat.search("agreement", "corpus-authorized-01")
    
    contradiction_candidate = CandidateResult(
        candidate_id="DOC-CONTRADICTION-200",
        corpus_id="corpus-authorized-01",
        strategy=StrategyType.CONTRADICTION,
        score=0.95,
        content="Synthetic contradicting clause 200",
        is_contradiction=True
    )
    
    unauthorized_candidate = CandidateResult(
        candidate_id="DOC-UNAUTHORIZED-999",
        corpus_id="corpus-UNAUTHORIZED-OTHER-TENANT",
        strategy=StrategyType.EXACT,
        score=1.0,
        content="Leaked tenant document"
    )
    
    all_candidates = lexical_candidates + [contradiction_candidate, unauthorized_candidate]
    
    # 4. Scope resolution BEFORE downstream compilation
    resolver = ScopeResolver(scope)
    scope_resolved_candidates = resolver.resolve_authorized_candidates(all_candidates)
    assert len(scope_resolved_candidates) == 2
    assert all(c.corpus_id == "corpus-authorized-01" for c in scope_resolved_candidates)

    # 5. Context Compilation and Ledger Generation
    compiler = ContextCompiler(scope)
    bundle = compiler.compile_context("agreement query", all_candidates)

    assert bundle.scope_id == "SCOPE-SYNTHETIC-001"
    assert bundle.coverage == CoverageState.CONTRADICTED
    assert len(bundle.selected_candidates) == 1
    assert bundle.selected_candidates[0].candidate_id == "DOC-EXACT-100"
    assert len(bundle.contradictions) == 1
    assert bundle.contradictions[0].candidate_id == "DOC-CONTRADICTION-200"
    assert bundle.ledger.total_candidates == 1  # Authorized non-contradiction candidates logged
    
    lexical_strat.close()
