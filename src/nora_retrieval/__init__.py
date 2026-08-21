"""nora-retrieval package."""

from .authorization import ScopeResolver
from .compiler import ContextCompiler
from .contracts import (
    CandidateResult,
    ContextBundle,
    CorpusCoverageMetadata,
    CoverageState,
    RetrievalLedger,
    RetrievalLedgerEntry,
    ScopeSnapshot,
    StrategyType,
)
from .ledger import FileLedgerStore, InMemoryLedgerStore, RetrievalLedgerStore

__all__ = [
    "CandidateResult",
    "ContextBundle",
    "ContextCompiler",
    "CorpusCoverageMetadata",
    "CoverageState",
    "FileLedgerStore",
    "InMemoryLedgerStore",
    "RetrievalLedger",
    "RetrievalLedgerEntry",
    "RetrievalLedgerStore",
    "ScopeResolver",
    "ScopeSnapshot",
    "StrategyType",
]
__version__ = "0.1.0"
