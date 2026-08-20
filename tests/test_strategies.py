from datetime import datetime
import pytest
from nora_retrieval.contracts import CandidateResult, StrategyType
from nora_retrieval.strategies.lexical import LexicalRetrievalStrategy
from nora_retrieval.strategies.temporal import TemporalRetrievalStrategy

def test_lexical_fts5_strategy():
    strat = LexicalRetrievalStrategy(":memory:")
    strat.index_document("DOC-1", "corpus-A", "Synthetic contract agreement terms")
    strat.index_document("DOC-2", "corpus-A", "Unrelated synthetic document")
    
    results = strat.search("agreement", "corpus-A")
    assert len(results) == 1
    assert results[0].candidate_id == "DOC-1"
    assert results[0].strategy == StrategyType.LEXICAL
    strat.close()

def test_temporal_strategy_filter():
    strat = TemporalRetrievalStrategy()
    candidates = [
        CandidateResult(
            candidate_id="DOC-JAN",
            corpus_id="corpus-A",
            strategy=StrategyType.TEMPORAL,
            score=1.0,
            content="Jan event",
            metadata={"event_date": "2026-01-15T00:00:00"}
        ),
        CandidateResult(
            candidate_id="DOC-AUG",
            corpus_id="corpus-A",
            strategy=StrategyType.TEMPORAL,
            score=1.0,
            content="Aug event",
            metadata={"event_date": "2026-08-15T00:00:00"}
        )
    ]

    filtered = strat.filter_by_timerange(
        candidates,
        start_date=datetime(2026, 6, 1),
        end_date=datetime(2026, 12, 31)
    )

    assert len(filtered) == 1
    assert filtered[0].candidate_id == "DOC-AUG"
