from __future__ import annotations
import sqlite3
from typing import List, Tuple
from nora_retrieval.contracts import CandidateResult, StrategyType

class LexicalRetrievalStrategy:
    """
    Local FTS5 / BM25 lexical and phrase/NEAR search strategy derived from Meridian baselines.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS corpus_fts USING fts5(
                    candidate_id UNINDEXED,
                    corpus_id UNINDEXED,
                    content
                )
            """)

    def index_document(self, candidate_id: str, corpus_id: str, content: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO corpus_fts VALUES (?, ?, ?)",
                (candidate_id, corpus_id, content)
            )

    def search(self, query: str, corpus_id: str) -> List[CandidateResult]:
        cursor = self.conn.execute(
            """
            SELECT candidate_id, content, rank
            FROM corpus_fts
            WHERE corpus_fts MATCH ? AND corpus_id = ?
            ORDER BY rank
            """,
            (query, corpus_id)
        )
        
        results = []
        for row in cursor.fetchall():
            cand_id, text, r = row
            # fts5 rank is negative (lower = better match)
            normalized_score = round(1.0 / (1.0 + abs(r)), 4)
            results.append(CandidateResult(
                candidate_id=cand_id,
                corpus_id=corpus_id,
                strategy=StrategyType.LEXICAL,
                score=normalized_score,
                content=text
            ))
        return results

    def close(self) -> None:
        self.conn.close()
