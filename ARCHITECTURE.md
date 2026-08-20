# Architecture

## Invariants

1. The public repository contains reusable technology, not private Matter data.
2. Every important output has an inspectable basis appropriate to this project's domain.
3. Authorization is evaluated before data is exposed to retrieval/tool/model paths where applicable.
4. Model output is a transformation, not a source of truth.
5. Unknown and disputed states are valid outputs.
6. Tests/evals use synthetic or redistributable fixtures.
7. Migration provenance is explicit.

## Target-specific architecture

Pipeline:
ScopeSnapshot → eligible corpus → retrieval plan → strategies → fusion/rerank →
coverage analysis → RetrievalLedger → ContextCompiler → ContextBundle.

Strategies include exact/structured, lexical, semantic, temporal, entity,
graph-neighborhood, contradiction-seeking, source-diversity and external-authority adapters.

## Extension points

Strategy plugins, rerankers, vector stores, graph stores, coverage estimators, ledger stores, context policies.

## Compatibility

Public contracts should be versioned and provider-neutral where practical.

## Architecture decisions

Record consequential changes under `docs/decisions/`.
