# Research Index

PURPOSE: Organized research notes for traceflux development.

STRUCTURE: By topic, not just date.

---

## Categories

### 01-foundations/ -- Mathematical & Theoretical Foundations

Core mathematical principles underlying traceflux.

- `character-level-analysis.md` - Character sequences, n-grams, set theory, graph theory
- (Future) Information theory, formal language theory

### 02-associations/ -- Association Discovery

How to find and present associations.

- `six-degrees-theory.md` - Small-world networks, multi-hop associations
- (Future) Co-occurrence algorithms, graph traversal

### 03-philosophy/ -- Design Philosophy & Principles

Why we design this way, not that way.

- `search-vs-judgment.md` - Search provides associations, user provides judgment
- `multi-hop-noise.md` - Embracing "noise" as feature, not bug
- (Future) User experience principles, ethical considerations

---

## Quick Reference

| Question | Read This |
|----------|-----------|
| How to handle multiple languages? | `01-foundations/character-level-analysis.md` |
| Why multi-hop associations? | `02-associations/six-degrees-theory.md` |
| Should we filter "noise"? | `03-philosophy/multi-hop-noise.md` |
| What is traceflux's role? | `03-philosophy/search-vs-judgment.md` |

---

## Filing New Research

TEMPLATE:
```text
research/
├── 01-foundations/     # Math, theory, algorithms
├── 02-associations/    # Discovery methods
├── 03-philosophy/      # Design principles
└── README.md           # This index
```

NAMING: `YYYY-MM-DD_topic.md`

---

RELATED:
- `../design/` - Stable design documents
- `../drafts/` - Work-in-progress
