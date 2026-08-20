# nora-retrieval

Auditable purpose-aware retrieval and Context Compiler for heterogeneous evidence and authority corpora.

**Status:** pre-alpha / migration build

## Hard problem

Retrieve the right authorized evidence for a specific purpose while exposing methods, coverage, source diversity, contradictions, omissions and uncertainty.

## Why this exists

This repository isolates one reusable public-interest technology problem from the NORA Foundation platform so developers and researchers can improve it independently.

## Minimum vertical slice

authorized corpus -> exact/lexical/contradiction retrieval -> ContextBundle -> RetrievalLedger

## Non-goals

- NORA One product UI
- private Matter storage
- generic SaaS dashboard work
- autonomous legal advice
- publication of private source corpora
- claims of production readiness without release evidence

## Quick start

```bash
make doctor
make validate
make test
```

## Source provenance

Legacy NORA repositories are component sources, not authorities. Migrated units are recorded in `SOURCE_PROVENANCE.yaml`.

## Contributing

See `CONTRIBUTING.md` and `ROADMAP.md`.

## Security

See `SECURITY.md`.

## License

New clean-room code is Apache-2.0. Migrated/third-party material remains subject to its recorded source license and notices.
