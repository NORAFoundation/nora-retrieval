from __future__ import annotations
from typing import List, Set
from nora_retrieval.contracts import CandidateResult, ScopeSnapshot

class ScopeResolver:
    """
    Enforces authorization-before-retrieval. Resolves authorized corpora and filters out
    unauthorized candidate documents before candidate processing.
    """
    def __init__(self, scope: ScopeSnapshot):
        self.scope = scope

    def resolve_authorized_candidates(self, candidates: List[CandidateResult]) -> List[CandidateResult]:
        authorized = []
        for cand in candidates:
            # Scope filter BEFORE downstream processing
            if cand.corpus_id in self.scope.authorized_corpus_ids:
                authorized.append(cand)
        return authorized
