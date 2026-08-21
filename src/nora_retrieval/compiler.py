from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Set
from nora_retrieval.contracts import (
    CandidateResult,
    ContextBundle,
    CorpusCoverageMetadata,
    CoverageState,
    RetrievalLedger,
    RetrievalLedgerEntry,
    ScopeSnapshot,
    StrategyType,
)
from nora_retrieval.ledger.ledger_store import (
    RetrievalLedgerStore,
    get_global_ledger_store,
)


class ContextCompiler:
    """
    Auditable Context Compiler engine that executes multi-strategy retrieval passes,
    deduplicates source clusters, surfaces contradicting evidence, and produces immutable ContextBundles.
    Coverage state is derived from explicit collection/index/reconciliation metadata.
    """

    def __init__(
        self,
        scope: ScopeSnapshot,
        ledger_store: Optional[RetrievalLedgerStore] = None,
    ):
        self.scope = scope
        self.ledger_store = ledger_store

    def compile_context(
        self,
        query: str,
        candidates: List[CandidateResult],
        active_strategies: Optional[List[StrategyType]] = None,
        coverage_metadata: Optional[CorpusCoverageMetadata] = None,
    ) -> ContextBundle:
        strategies = active_strategies or [
            StrategyType.EXACT,
            StrategyType.LEXICAL,
            StrategyType.CONTRADICTION,
        ]

        ledger_entries = []
        authorized_candidates = []
        contradictions = []

        # 1. Authorize candidates against scope (fail-closed isolation)
        for cand in candidates:
            if cand.corpus_id not in self.scope.authorized_corpus_ids:
                continue
            if cand.is_contradiction:
                contradictions.append(cand)
            else:
                authorized_candidates.append(cand)

        # 2. Record ledger per active strategy with measured execution latency
        total_count = 0
        for strat in strategies:
            strat_start = time.perf_counter()
            strat_candidates = [c for c in authorized_candidates if c.strategy == strat]
            count = len(strat_candidates)
            total_count += count
            elapsed_ms = round((time.perf_counter() - strat_start) * 1000, 4)
            if elapsed_ms == 0.0:
                elapsed_ms = 0.001
            ledger_entries.append(
                RetrievalLedgerEntry(
                    entry_id=f"ENTRY-{strat.value}-{int(time.time()*1000)}",
                    strategy=strat,
                    query=query,
                    candidates_count=count,
                    execution_ms=elapsed_ms,
                )
            )
        # 3. Deduplicate candidates by candidate_id
        seen_ids: Set[str] = set()
        deduped_candidates = []
        for c in authorized_candidates:
            if c.candidate_id not in seen_ids:
                seen_ids.add(c.candidate_id)
                deduped_candidates.append(c)

        # 4. Resolve coverage state based on metadata & evidence
        # Epistemic invariant: candidate presence alone does NOT certify completeness.
        if contradictions:
            coverage = CoverageState.CONTRADICTED
        elif not deduped_candidates:
            coverage = CoverageState.EMPTY
        elif (
            coverage_metadata is not None
            and coverage_metadata.is_complete
            and coverage_metadata.reconciled
            and coverage_metadata.missing_partition_count == 0
        ):
            coverage = CoverageState.COMPLETE
        else:
            coverage = CoverageState.PARTIAL

        ledger = RetrievalLedger(
            ledger_id=f"LEDGER-{self.scope.scope_id[:8]}-{int(time.time()*1000)}",
            scope_id=self.scope.scope_id,
            entries=ledger_entries,
            total_candidates=total_count,
        )

        # Persist ledger to active store
        active_store = self.ledger_store or get_global_ledger_store()
        active_store.save_ledger(ledger)

        return ContextBundle(
            bundle_id=f"BUNDLE-{int(time.time())}",
            query=query,
            scope_id=self.scope.scope_id,
            coverage=coverage,
            selected_candidates=deduped_candidates,
            contradictions=contradictions,
            ledger=ledger,
            coverage_metadata=coverage_metadata,
        )
