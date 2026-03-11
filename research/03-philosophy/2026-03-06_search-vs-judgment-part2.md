# Research: Search Engine vs Judgment -- Separation of Concerns (Part 2)

DATE: 2026-03-06
STATUS: Design Principle
TOPIC: Search provides associations, user/agent provides judgment

NOTE: This is Part 2 of 3. See part1 for Core Insight through Comparison. See part3 for Implementation Checklist, Key Insights, and Design Mantra.

---

## Philosophical Foundation

### Engineering Humility

ADMISSION: Engine doesn't know user's intent.

RESPONSE: Don't pretend to know -- provide options, let user decide.

### Information Freedom

PRINCIPLE: Information should be accessible, not pre-filtered.

APPLICATION: All associations visible, user filters as needed.

### Cognitive Mirror

GOAL: Mirror human cognition (generate first, judge later).

IMPLEMENTATION: Separate association extraction from relevance judgment.

---

## Connection to Prompt Engineering

### Directional Prompting

```markdown
# System Instruction (traceflux engine)
- EXTRACT all associations up to 4 degrees
- DISPLAY paths and co-occurrence counts
- DO NOT judge relevance or filter by "meaning"

# User Instruction (agent/human)
- SELECT associations relevant to your task
- IGNORE distant terms if not useful
- JUDGE based on your context
```

### Vocabulary Disambiguation

| Term | Definition |
|------|------------|
| Association | Co-occurrence-based connection (objective) |
| Relevance | Context-dependent usefulness (subjective) |
| Noise | Association that seems irrelevant in current context |

NOTE: "Noise" is not inherent -- it's context-dependent.
