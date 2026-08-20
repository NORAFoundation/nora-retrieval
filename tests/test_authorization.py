import pytest
from nora_retrieval.authorization import ScopeResolver
from nora_retrieval.compiler import ContextCompiler
from nora_retrieval.contracts import CandidateResult, ScopeSnapshot, StrategyType

def test_scope_resolver_authorization_before_retrieval():
    scope = ScopeSnapshot(
        scope_id="SCOPE-TENANT-A",
        authorized_corpus_ids={"corpus-TENANT-A"}
    )
    
    resolver = ScopeResolver(scope)
    candidates = [
        CandidateResult(
            candidate_id="DOC-A-01",
            corpus_id="corpus-TENANT-A",
            strategy=StrategyType.EXACT,
            score=1.0,
            content="Authorized tenant A document"
        ),
        CandidateResult(
            candidate_id="DOC-B-01",
            corpus_id="corpus-TENANT-B",
            strategy=StrategyType.EXACT,
            score=1.0,
            content="Unauthorized tenant B document"
        )
    ]
    
    authorized = resolver.resolve_authorized_candidates(candidates)
    assert len(authorized) == 1
    assert authorized[0].candidate_id == "DOC-A-01"
    
    compiler = ContextCompiler(scope)
    bundle = compiler.compile_context("synthetic query", candidates)
    
    # Assert RetrievalLedger is persisted and zero unauthorized items exist
    assert bundle.ledger.scope_id == "SCOPE-TENANT-A"
    assert all(c.corpus_id == "corpus-TENANT-A" for c in bundle.selected_candidates)
