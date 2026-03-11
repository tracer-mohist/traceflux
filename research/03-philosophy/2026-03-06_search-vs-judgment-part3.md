# Research: Search Engine vs Judgment -- Separation of Concerns (Part 3)

DATE: 2026-03-06
STATUS: Design Principle
TOPIC: Search provides associations, user/agent provides judgment

NOTE: This is Part 3 of 3. See part1 for Core Insight through Comparison. See part2 for Philosophical Foundation and Connection to Prompt Engineering.

---

## Implementation Checklist

### Phase 2A (Current)
- [x] Extract 1 degree associations
- [x] No relevance judgment
- [x] Show all results

### Phase 3 (Next)
- [ ] Extract 2-3 degree associations
- [ ] Show degree and path
- [ ] No filtering by "seems irrelevant"
- [ ] Add note: "You decide what's useful"

### Phase 4+ (Future)
- [ ] Extract 4 degree+ associations
- [ ] Confidence indicators (not relevance scores)
- [ ] Path visualization
- [ ] Agent integration (LLM judges relevance)

---

## Key Insights

### 1. Engine != Oracle

traceflux doesn't know what user wants -- and that's okay.
Provide options, not answers.

### 2. Noise is Contextual

What's noise for User A is signal for User B.
Don't filter -- let user decide.

### 3. Cognition has Two Stages

Generation (messy, creative) != Selection (focused, intentional)
Be the generator, not the selector.

### 4. Humility is a Feature

Admitting "I don't know what you need" is honest design.
Provide tools, not assumptions.

---

## Design Mantra

> "Provide associations, not judgments."
>
> Chinese terms (moved from inline to blockquote per style guide):
> 浮想联翩 by engine, 意志判断 by user.

---

STATUS: Design principle clarified
NEXT: Implement Phase 3 with this principle in mind
PHILOSOPHY: Search engine provides options, user/agent provides judgment
