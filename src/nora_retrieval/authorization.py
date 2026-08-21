from __future__ import annotations

from typing import Iterable, List, Set
from nora_retrieval.contracts import CandidateResult, ScopeSnapshot


class ScopeResolver:
    """
    Enforces authorization-before-retrieval. Resolves authorized corpora and constrains
    retrieval queries to authorized boundaries before candidate retrieval or context construction.
    """

    def __init__(self, scope: ScopeSnapshot):
        self.scope = scope

    def is_corpus_authorized(self, corpus_id: str) -> bool:
        """Check if a specific corpus ID is authorized in this scope."""
        return corpus_id in self.scope.authorized_corpus_ids

    def authorize_query_corpora(self, requested_corpus_ids: Iterable[str]) -> Set[str]:
        """
        Constrain requested target corpora to authorized scope before query execution.
        """
        return {
            cid for cid in requested_corpus_ids if cid in self.scope.authorized_corpus_ids
        }

    def resolve_authorized_candidates(
        self, candidates: List[CandidateResult]
    ) -> List[CandidateResult]:
        """
        Safety-net post-filter for candidate collections.
        """
        return [
            cand
            for cand in candidates
            if self.is_corpus_authorized(cand.corpus_id)
        ]
