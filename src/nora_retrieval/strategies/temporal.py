from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from nora_retrieval.contracts import CandidateResult, StrategyType

class TemporalRetrievalStrategy:
    """
    Temporal / date-bounded retrieval strategy adapter derived from Meridian timeline baselines.
    """
    def filter_by_timerange(
        self,
        candidates: List[CandidateResult],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[CandidateResult]:
        filtered = []
        for cand in candidates:
            date_str = cand.metadata.get("event_date")
            if not date_str:
                filtered.append(cand)
                continue
            
            try:
                dt = datetime.fromisoformat(date_str)
                if start_date and dt < start_date:
                    continue
                if end_date and dt > end_date:
                    continue
                filtered.append(cand)
            except ValueError:
                filtered.append(cand)
                
        return filtered
