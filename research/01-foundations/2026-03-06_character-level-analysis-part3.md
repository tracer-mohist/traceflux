### 4. Graph Traversal Finds Associations

BFS on co-occurrence graph:
- 1deg: Direct neighbors (same word or adjacent n-grams)
- 2deg: Neighbors of neighbors (co-occur in same context)
- 3deg+: Distant associations (bridge concepts)

---

## Next Steps

1. IMPLEMENT-LEVEL-0-1 -- Character and n-gram indexing
2. IMPLEMENT-LEVEL-2 -- Co-occurrence graph construction
3. IMPLEMENT-LEVEL-3 -- Query processing with BFS
4. TEST-ON-MULTILINGUAL-CORPUS -- Verify language independence

---

STATUS: Foundational design complete, ready for implementation
NEXT: Implement character-level indexing (no linguistic assumptions)
PHILOSOPHY: Pure mathematics (sets, sequences, graphs) over linguistics
