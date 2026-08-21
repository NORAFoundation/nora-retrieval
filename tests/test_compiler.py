import pytest
from nora_retrieval.compiler import ContextCompiler
from nora_retrieval.contracts import (
    CandidateResult,
    CorpusCoverageMetadata,
    CoverageState,
    ScopeSnapshot,
    StrategyType,
)
from nora_retrieval.ledger.ledger_store import FileLedgerStore


def test_context_compiler_coverage_requires_metadata():
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
        )
    ]

    compiler = ContextCompiler(scope)
    # Without explicit complete metadata, hits default to PARTIAL
    bundle_partial = compiler.compile_context("synthetic query", candidates)
    assert bundle_partial.coverage == CoverageState.PARTIAL

    # With explicit complete & reconciled metadata, coverage becomes COMPLETE
    meta_complete = CorpusCoverageMetadata(is_complete=True, reconciled=True)
    bundle_complete = compiler.compile_context("synthetic query", candidates, coverage_metadata=meta_complete)
    assert bundle_complete.coverage == CoverageState.COMPLETE


def test_context_compiler_execution_deduplication_and_durable_ledger(tmp_path):
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

    ledger_dir = tmp_path / "ledgers"
    ledger_store = FileLedgerStore(ledger_dir)

    compiler = ContextCompiler(scope, ledger_store=ledger_store)
    meta = CorpusCoverageMetadata(is_complete=True, reconciled=True)
    bundle = compiler.compile_context("synthetic query", candidates, coverage_metadata=meta)

    assert len(bundle.selected_candidates) == 1
    assert bundle.selected_candidates[0].candidate_id == "CAND-01"
    assert bundle.coverage == CoverageState.COMPLETE
    assert bundle.ledger.total_candidates == 2  # Total before deduplication

    # Verify durable ledger persistence and readback across store instance restart
    restarted_store = FileLedgerStore(ledger_dir)
    loaded_ledger = restarted_store.get_ledger(bundle.ledger.ledger_id)
    assert loaded_ledger is not None
    assert loaded_ledger.ledger_id == bundle.ledger.ledger_id
    assert loaded_ledger.scope_id == "SCOPE-TENANT-A"
    assert loaded_ledger.total_candidates == 2
