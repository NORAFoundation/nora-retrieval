# ADR-0001: Context Compiler and Retrieval Ledger Architecture

- **Status:** Accepted
- **Date:** 2026-08-19
- **Deciders:** NORA Foundation Engineering Team

## Context

Retrieval in NORA systems is not a black-box vector lookup ("generic RAG"), but an auditable Context Compiler (`AGENTS.md`, `policies/TERMINOLOGY_FREEZE.md`).

## Decision

We adopt strict, portable execution contracts:
1. `ScopeSnapshot` — Scope resolution enforcing authorization boundaries before candidate generation.
2. `RetrievalStrategy` — Typed interfaces for `exact`, `lexical`, `semantic`, `temporal`, `entity`, `graph`, and `contradiction` retrieval.
3. `RetrievalLedger` — Audit log of every strategy invocation, latency, and candidate yield.
4. `CoverageState` — Explicit status (`COMPLETE`, `PARTIAL`, `EMPTY`, `CONTRADICTED`).
5. `ContextBundle` — Immutable compiled context payload containing selected items, contradiction items, and the execution ledger.

## Consequences

- All retrieved contexts must generate a `RetrievalLedger` recording authorization and candidate provenance.
- Embeddings are treated as one primitive among several, not the whole architecture.
