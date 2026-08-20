from __future__ import annotations
import time
from typing import Any, Dict, List, Optional, Set
from nora_retrieval.contracts import (
    CandidateResult,
    ContextBundle,
    CoverageState,
    RetrievalLedger,
    RetrievalLedgerEntry,
    ScopeSnapshot,
    StrategyType
)

class ContextCompiler:
    """
    Auditable Context Compiler engine that executes multi-strategy retrieval passes,
    deduplicates source clusters, surfaces contradicting evidence, and produces immutable ContextBundles.
    """
    def __init__(self, scope: ScopeSnapshot):
        self.scope = scope

    def compile_context(
        self,
        query: str,
        candidates: List[CandidateResult],
        active_strategies: Optional[List[StrategyType]] = None
    ) -> ContextBundle:
        strategies = active_strategies or [
            StrategyType.EXACT,
            StrategyType.LEXICAL,
            StrategyType.CONTRADICTION
        ]

        ledger_entries = []
        authorized_candidates = []
        contradictions = []

        # 1. Authorize candidates against scope
        for cand in candidates:
            if cand.corpus_id not in self.scope.authorized_corpus_ids:
                continue  # Fail-closed authorization isolation
            if cand.is_contradiction:
                contradictions.append(cand)
            else:
                authorized_candidates.append(cand)

        # 2. Record ledger per active strategy
        total_count = 0
        for strat in strategies:
            strat_candidates = [c for c in authorized_candidates if c.strategy == strat]
            count = len(strat_candidates)
            total_count += count
            ledger_entries.append(RetrievalLedgerEntry(
                entry_id=f"ENTRY-{strat.value}-{int(time.time()*1000)}",
                strategy=strat,
                query=query,
                candidates_count=count,
                execution_ms=0.5
            ))

        # 3. Deduplicate candidates by candidate_id
        seen_ids: Set[str] = set()
        deduped_candidates = []
        for c in authorized_candidates:
            if c.candidate_id not in seen_ids:
                seen_ids.add(c.candidate_id)
                deduped_candidates.append(c)

        # 4. Resolve coverage state
        if contradictions:
            coverage = CoverageState.CONTRADICTED
        elif deduped_candidates:
            coverage = CoverageState.COMPLETE
        else:
            coverage = CoverageState.EMPTY

        ledger = RetrievalLedger(
            ledger_id=f"LEDGER-{self.scope.scope_id[:8]}",
            scope_id=self.scope.scope_id,
            entries=ledger_entries,
            total_candidates=total_count
        )

        return ContextBundle(
            bundle_id=f"BUNDLE-{int(time.time())}",
            query=query,
            scope_id=self.scope.scope_id,
            coverage=coverage,
            selected_candidates=deduped_candidates,
            contradictions=contradictions,
            ledger=ledger
        )
