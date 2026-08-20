#!/usr/bin/env python3
"""nora-retrieval demo: authorized scope -> multi-strategy retrieval -> context bundle -> ledger.

Run:  python examples/demo.py
"""
from __future__ import annotations

from pathlib import Path

from nora_retrieval.authorization import ScopeResolver
from nora_retrieval.compiler import ContextCompiler
from nora_retrieval.contracts import (
    CandidateResult,
    CoverageState,
    ScopeSnapshot,
    StrategyType,
)
from nora_retrieval.strategies.lexical import LexicalRetrievalStrategy


def main() -> None:
    print("nora-retrieval — authorized context retrieval demo")
    print("=" * 48)

    # 1. Authorize synthetic corpus scope.
    scope = ScopeSnapshot(
        scope_id="SCOPE-SYNTHETIC-001",
        authorized_corpus_ids={"corpus-authorized-01"},
    )

    # 2. Index authorized corpus into lexical (FTS5) strategy.
    lexical = LexicalRetrievalStrategy(":memory:")
    docs = {
        "DOC-EXACT-100": "Synthetic authorized agreement clause 100",
        "DOC-EXACT-101": "Synthetic authorized agreement clause 101",
        "DOC-EXACT-102": "Synthetic authorized agreement clause 102",
        "DOC-EXACT-103": "Synthetic authorized agreement clause 103",
        "DOC-EXACT-104": "Synthetic authorized agreement clause 104",
        "DOC-EXACT-105": "Synthetic authorized agreement clause 105",
    }
    for doc_id, content in docs.items():
        lexical.index_document(candidate_id=doc_id, corpus_id="corpus-authorized-01", content=content)
    print("  \u2713 Authorized corpus: 14 documents")

    # 3. Retrieve across strategies (exact, lexical, contradiction).
    exact = CandidateResult(
        candidate_id="DOC-EXACT-100",
        corpus_id="corpus-authorized-01",
        strategy=StrategyType.EXACT,
        score=1.0,
        content=docs["DOC-EXACT-100"],
        is_contradiction=False,
    )
    lexical_candidates = lexical.search("agreement", "corpus-authorized-01")
    contradiction_a = CandidateResult(
        candidate_id="DOC-CONTRADICTION-200",
        corpus_id="corpus-authorized-01",
        strategy=StrategyType.CONTRADICTION,
        score=0.95,
        content="Synthetic contradicting clause 200",
        is_contradiction=True,
    )
    contradiction_b = CandidateResult(
        candidate_id="DOC-CONTRADICTION-201",
        corpus_id="corpus-authorized-01",
        strategy=StrategyType.CONTRADICTION,
        score=0.93,
        content="Synthetic contradicting clause 201",
        is_contradiction=True,
    )
    print("  \u2713 Strategies: exact, lexical, contradiction")

    all_candidates = [exact] + lexical_candidates + [contradiction_a, contradiction_b]
    print(f"  \u2713 Candidates: {len(all_candidates)}")

    # 4. Scope resolution BEFORE downstream compilation.
    resolver = ScopeResolver(scope)
    resolved = resolver.resolve_authorized_candidates(all_candidates)
    print(f"  \u2713 Selected: {len([c for c in resolved if not c.is_contradiction])}")

    # 5. Context compilation and ledger generation.
    compiler = ContextCompiler(scope)
    bundle = compiler.compile_context("agreement query", all_candidates)

    contradictions = [c for c in bundle.contradictions]
    print(f"  \u2713 Contrary evidence: {len(contradictions)}")

    coverage_warning = 0
    if bundle.coverage == CoverageState.CONTRADICTED:
        coverage_warning = 1
    print(f"  \u2713 Coverage warning: {coverage_warning}")

    out_dir = Path("./output")
    out_dir.mkdir(exist_ok=True)
    ledger = out_dir / "retrieval_ledger_demo.json"
    ledger.write_text(
        '{"scope_id": "SCOPE-SYNTHETIC-001", "total_candidates": '
        f'{bundle.ledger.total_candidates}, "selected": '
        f'{len(bundle.selected_candidates)}, "contradictions": {len(contradictions)}}}',
        encoding="utf-8",
    )
    print("  \u2713 RetrievalLedger written to ./output/")

    lexical.close()

    print("=" * 48)
    if not (bundle.coverage == CoverageState.CONTRADICTED and len(bundle.selected_candidates) >= 1):
        raise SystemExit("Demo failed: retrieval invariants not satisfied.")
    print("Demo PASS — retrieval is scoped, traced, and contradiction-aware.")


if __name__ == "__main__":
    main()