import pytest
from nora_retrieval.authorization import ScopeResolver
from nora_retrieval.compiler import ContextCompiler
from nora_retrieval.contracts import CandidateResult, ScopeSnapshot, StrategyType
from nora_retrieval.strategies.lexical import LexicalRetrievalStrategy


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

    assert bundle.ledger.scope_id == "SCOPE-TENANT-A"
    assert all(c.corpus_id == "corpus-TENANT-A" for c in bundle.selected_candidates)


def test_negative_leakage_pre_search_exclusion():
    """
    Negative leakage test proving unauthorized corpus is excluded at the search
    substrate layer BEFORE candidate construction or context compilation.
    """
    scope = ScopeSnapshot(
        scope_id="SCOPE-TENANT-SECRET",
        authorized_corpus_ids={"corpus-AUTHORIZED-1"}
    )

    strategy = LexicalRetrievalStrategy(":memory:")
    # Index both authorized and unauthorized documents containing the exact same search term "confidential"
    strategy.index_document("DOC-AUTH-1", "corpus-AUTHORIZED-1", "confidential agreement for authorized tenant")
    strategy.index_document("DOC-UNAUTH-1", "corpus-UNAUTHORIZED-2", "confidential salary details for secret tenant")

    # Search with scope snapshot directly passed to strategy
    results = strategy.search("confidential", scope)

    # Prove unauthorized corpus content was NEVER returned by the retrieval engine
    assert len(results) == 1
    assert results[0].candidate_id == "DOC-AUTH-1"
    assert results[0].corpus_id == "corpus-AUTHORIZED-1"
    assert not any(r.corpus_id == "corpus-UNAUTHORIZED-2" for r in results)

    strategy.close()
