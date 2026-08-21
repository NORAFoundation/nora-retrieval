"""Durable persistence for RetrievalLedgers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional
import json
from nora_retrieval.contracts import RetrievalLedger


class RetrievalLedgerStore(ABC):
    """Abstract store for durable retrieval ledger persistence."""

    @abstractmethod
    def save_ledger(self, ledger: RetrievalLedger) -> None:
        pass

    @abstractmethod
    def get_ledger(self, ledger_id: str) -> Optional[RetrievalLedger]:
        pass

    @abstractmethod
    def list_ledgers(self, scope_id: Optional[str] = None) -> List[RetrievalLedger]:
        pass


class InMemoryLedgerStore(RetrievalLedgerStore):
    """In-memory retrieval ledger store."""

    def __init__(self) -> None:
        self._ledgers: dict[str, RetrievalLedger] = {}

    def save_ledger(self, ledger: RetrievalLedger) -> None:
        self._ledgers[ledger.ledger_id] = ledger

    def get_ledger(self, ledger_id: str) -> Optional[RetrievalLedger]:
        return self._ledgers.get(ledger_id)

    def list_ledgers(self, scope_id: Optional[str] = None) -> List[RetrievalLedger]:
        if scope_id:
            return [l for l in self._ledgers.values() if l.scope_id == scope_id]
        return list(self._ledgers.values())


class FileLedgerStore(RetrievalLedgerStore):
    """File-backed durable retrieval ledger store."""

    def __init__(self, storage_dir: str | Path) -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, ledger_id: str) -> Path:
        clean_id = ledger_id.replace("/", "_").replace("\\", "_")
        return self.storage_dir / f"{clean_id}.json"

    def save_ledger(self, ledger: RetrievalLedger) -> None:
        filepath = self._file_path(ledger.ledger_id)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(ledger.model_dump_json(indent=2))

    def get_ledger(self, ledger_id: str) -> Optional[RetrievalLedger]:
        filepath = self._file_path(ledger_id)
        if not filepath.exists():
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return RetrievalLedger.model_validate(data)

    def list_ledgers(self, scope_id: Optional[str] = None) -> List[RetrievalLedger]:
        ledgers = []
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                ledger = RetrievalLedger.model_validate(data)
                if scope_id is None or ledger.scope_id == scope_id:
                    ledgers.append(ledger)
            except Exception:
                continue
        return ledgers


_GLOBAL_LEDGER_STORE: RetrievalLedgerStore = InMemoryLedgerStore()


def set_global_ledger_store(store: RetrievalLedgerStore) -> None:
    global _GLOBAL_LEDGER_STORE
    _GLOBAL_LEDGER_STORE = store


def get_global_ledger_store() -> RetrievalLedgerStore:
    return _GLOBAL_LEDGER_STORE
