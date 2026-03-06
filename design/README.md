# Design Documents

**Purpose**: Stable design specifications and architecture decisions.

**Status**: Reviewed and approved (not drafts).

---

## Structure

```
design/
├── README.md              # This file (index)
├── 01-core-concept.md     # Core concept & philosophy
├── 02-cli-design.md       # Command-line interface
├── 03-scoring-algo.md     # Scoring algorithm
└── ...
```

---

## Numbering System

Files are numbered for logical ordering:
- `01-*` — Foundation (concept, philosophy)
- `02-*` — Interface (CLI, API)
- `03-*` — Algorithms (scoring, extraction)
- `04-*` — Implementation (code structure)
- `05-*` — Testing (test strategy)

---

## Template

```markdown
# Design: [Component Name]

**Status**: Draft / Approved / Deprecated  
**Date**: YYYY-MM-DD  
**Replaces**: (if applicable)

## Purpose

What this component does.

## Design Decisions

Key decisions with reasoning.

## Specification

Detailed specification.

## Alternatives Considered

What else was considered and why rejected.

## References

Links to related designs, research, external docs.
```

---

## Change Process

1. **Research** — Explore in `research/`
2. **Draft** — Write in `drafts/`
3. **Review** — Discuss, iterate
4. **Approve** — Move to `design/` with status "Approved"
5. **Deprecate** — Mark as deprecated (don't delete)

---

**Related**:
- `research/` — Exploratory research
- `drafts/` — Work-in-progress
- `docs/` — User-facing documentation
