from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class StrategyType(str, Enum):
    EXACT = "exact"
    LEXICAL = "lexical"
    SEMANTIC = "semantic"
    TEMPORAL = "temporal"
    ENTITY = "entity"
    GRAPH = "graph"
    CONTRADICTION = "contradiction"


class CoverageState(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    EMPTY = "empty"
    CONTRADICTED = "contradicted"


class CorpusCoverageMetadata(BaseModel):
    """
    Metadata certifying collection/index completeness and reconciliation.
    Coverage state depends on index reconciliation proof, not candidate presence alone.
    """

    is_complete: bool = False
    reconciled: bool = False
    total_indexed_documents: Optional[int] = None
    missing_partition_count: int = 0
    coverage_percentage: float = 100.0
    notes: Optional[str] = None


class ScopeSnapshot(BaseModel):
    scope_id: str
    authorized_corpus_ids: Set[str] = Field(default_factory=set)
    allowed_data_classes: Set[str] = Field(default_factory=set)
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CandidateResult(BaseModel):
    candidate_id: str
    corpus_id: str
    strategy: StrategyType
    score: float
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_contradiction: bool = False


class RetrievalLedgerEntry(BaseModel):
    entry_id: str
    strategy: StrategyType
    query: str
    candidates_count: int
    execution_ms: float


class RetrievalLedger(BaseModel):
    ledger_id: str
    scope_id: str
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    entries: List[RetrievalLedgerEntry] = Field(default_factory=list)
    total_candidates: int = 0


class ContextBundle(BaseModel):
    bundle_id: str
    query: str
    scope_id: str
    coverage: CoverageState
    selected_candidates: List[CandidateResult] = Field(default_factory=list)
    contradictions: List[CandidateResult] = Field(default_factory=list)
    ledger: RetrievalLedger
    coverage_metadata: Optional[CorpusCoverageMetadata] = None
    compiled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
