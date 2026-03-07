# src/traceflux/pagerank.py
"""Weighted PageRank - Rank patterns by importance.

This module implements the PageRank algorithm for ranking patterns in
co-occurrence graphs. PageRank measures the importance of nodes based on
the structure of incoming links.

## Why PageRank for traceflux?

In a co-occurrence graph:
- **Nodes** = patterns (words, phrases, code structures)
- **Edges** = patterns appearing together
- **Edge weights** = how often they co-occur

PageRank helps identify:
1. **Central concepts** - patterns that co-occur with many others
2. **Hub patterns** - patterns that connect different clusters
3. **Important context** - not just frequent, but structurally important

## How It Works

PageRank simulates a "random surfer" who:
1. Starts at a random node
2. Follows a random outgoing edge with probability **d** (damping)
3. Jumps to a random node with probability **(1-d)**
4. Repeats many times

The PageRank score = long-term probability of being at that node.

## PageRank Formula

```
PR(v) = (1-d)/N + d * sum_{u} PR(u) * w(u,v) / sum_{t} w(u,t)
```

Where:
- **PR(v)**: PageRank score of node v
- **d**: Damping factor (typically 0.85)
- **N**: Total number of nodes
- **w(u,v)**: Weight of edge from u to v
- **sum_{t} w(u,t)**: Total outgoing weight from u

## Intuition

Think of it as a "vote of importance":
- If important pattern A co-occurs with pattern B, B gets a vote
- The vote is weighted by:
  - How important A is (PR(u))
  - How strongly A is associated with B (w(u,v))
  - How selective A is (divided by total connections)

## Example

```python
from traceflux.pagerank import WeightedPageRank

# Create PageRank calculator with default settings
pr = WeightedPageRank(damping=0.85, max_iterations=100)

# Compute scores for a co-occurrence graph
result = pr.compute(graph)

# Get top 10 patterns
top_10 = pr.get_top_k(result.scores, k=10)

for pattern, score in top_10:
    print(f"{pattern}: {score:.4f}")
```

## Algorithm Details

**Method**: Power iteration
- **Time complexity**: O(k * E) where k=iterations, E=edges
- **Convergence**: Typically 20-50 iterations for small graphs
- **Space complexity**: O(N) for score storage

**Convergence criterion**:
- Sum of score changes < tolerance (default: 1e-6)
- Maximum iterations: 100 (safety limit)

## Parameters Explained

### damping (default: 0.85)

**What it controls**: Balance between graph structure vs random exploration

- **High damping (0.9-0.95)**: More weight to graph structure
  - Better for: Well-connected graphs, discovering hubs
  - Risk: Slow convergence, over-emphasizes old nodes

- **Low damping (0.7-0.8)**: More random jumps
  - Better for: Sparse graphs, avoiding "rich get richer"
  - Risk: Loses structural information

- **Why 0.85**: Standard value from web PageRank research
  - Empirically balances convergence speed and quality
  - Works well for most co-occurrence graphs

### max_iterations (default: 100)

**What it controls**: Maximum computation time

- **Typical convergence**: 20-50 iterations for graphs <1000 nodes
- **Safety limit**: Prevents infinite loops on pathological graphs
- **Adjust if**: Graph doesn't converge (increase) or too slow (decrease)

### tolerance (default: 1e-6)

**What it controls**: Convergence precision

- **Tight tolerance (1e-8)**: More precise, more iterations
- **Loose tolerance (1e-4)**: Faster, less precise
- **Why 1e-6**: Good balance for ranking purposes
  - Exact scores not needed, only relative ordering matters

### min_score (default: 0.001)

**What it controls**: Filtering threshold for low-importance nodes

- **Purpose**: Remove noise patterns with negligible importance
- **Typical**: 0.001 = 0.1% of total importance
- **Adjust if**: Too many patterns (increase) or losing signal (decrease)

## References

- Page, L., et al. (1999). "The PageRank Citation Ranking: Bringing Order to the Web."
- Langville, A. N., & Meyer, C. D. (2011). "Google's PageRank and Beyond."
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from traceflux.graph import CooccurrenceGraph


@dataclass
class PageRankResult:
    """Result of PageRank computation.

    Contains computed scores and convergence information.

    Attributes:
        scores: Dict mapping pattern -> PageRank score (0-1)
        iterations: Number of iterations until convergence
        converged: Whether algorithm converged before max_iterations
        final_delta: Final change in scores (should be < tolerance)

    Example:
        >>> result = pr.compute(graph)
        >>> if result.converged:
        ...     print(f"Converged in {result.iterations} iterations")
        ...     top = pr.get_top_k(result.scores, k=5)
    """

    scores: Dict[str, float]
    iterations: int
    converged: bool
    final_delta: float


class WeightedPageRank:
    """Weighted PageRank for co-occurrence graphs.

    Ranks patterns based on their structural importance in the graph.
    Unlike simple frequency counting, PageRank considers:

    1. **Direct connections**: Patterns that co-occur frequently
    2. **Indirect connections**: Patterns connected through other patterns
    3. **Selective associations**: Patterns with focused connections rank higher

    ## Why Not Just Use Frequency?

    Frequency alone is misleading:
    - Common words ("the", "is") have high frequency but low importance
    - Domain-specific terms may have lower frequency but higher importance

    PageRank captures **structural importance**:
    - A pattern connected to many important patterns is itself important
    - A pattern with selective, strong connections ranks higher

    ## How to Use

    ```python
    from traceflux import CooccurrenceGraph
    from traceflux.pagerank import WeightedPageRank

    # Build co-occurrence graph
    graph = CooccurrenceGraph()
    graph.add_document_cooccurrences(["proxy", "config", "http"], window_size=5)

    # Compute PageRank
    pr = WeightedPageRank(damping=0.85)
    result = pr.compute(graph)

    # Get top patterns
    top_10 = pr.get_top_k(result.scores, k=10)

    # Filter low-scoring patterns
    filtered, removed = pr.compute_with_filtering(graph)
    ```

    ## Performance

    - **Small graphs** (<100 nodes): <10ms
    - **Medium graphs** (100-1000 nodes): 10-100ms
    - **Large graphs** (>1000 nodes): 100ms-1s

    For typical traceflux use cases (code files, documents),
    computation is nearly instantaneous.
    """

    def __init__(
        self,
        damping: float = 0.85,
        max_iterations: int = 100,
        tolerance: float = 1e-6,
        min_score: float = 0.001,
    ):
        """Initialize PageRank calculator.

        Args:
            damping: Probability of following an edge vs random jump (0-1).
                Default 0.85 is standard value from web PageRank research.
                - Higher (0.9-0.95): More weight to graph structure
                - Lower (0.7-0.8): More random exploration
                - Why 0.85: Empirically balances convergence and quality

            max_iterations: Maximum iterations before stopping (default: 100).
                Typical convergence: 20-50 iterations for small graphs.
                This is a safety limit to prevent infinite loops.

            tolerance: Convergence threshold for score changes (default: 1e-6).
                Algorithm stops when sum of score changes < tolerance.
                - Tighter (1e-8): More precise, slower
                - Looser (1e-4): Faster, less precise
                - Why 1e-6: Good balance for ranking purposes

            min_score: Minimum score threshold for filtering (default: 0.001).
                Used by compute_with_filtering() to remove low-importance nodes.
                - Higher: More aggressive filtering
                - Lower: Keep more patterns
                - Why 0.001: Removes bottom 0.1% as noise

        Example:
            >>> pr = WeightedPageRank()  # Default settings
            >>> pr.damping
            0.85
            >>> pr.max_iterations
            100
        """
        self.damping = damping
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.min_score = min_score

    def compute(
        self, graph: "CooccurrenceGraph", initial_scores: Optional[Dict[str, float]] = None
    ) -> PageRankResult:
        """Compute PageRank scores using power iteration.

        ## Algorithm: Power Iteration

        Power iteration is an iterative method that:
        1. Starts with uniform scores (or provided initial scores)
        2. Repeatedly applies PageRank formula
        3. Stops when scores converge (change < tolerance)

        ## How It Works

        Each iteration:
        ```
        For each node v:
            new_score[v] = (1-d)/N + d * sum(score[u] * w(u,v) / out_weight[u])
                            ↑                    ↑
                      random jump         contribution from neighbors
        ```

        Then normalize so scores sum to 1.

        ## Convergence

        The algorithm converges when:
        - Sum of score changes < tolerance
        - Typically 20-50 iterations for small graphs

        **Why it converges**: PageRank is finding the stationary distribution
        of a Markov chain. With damping < 1, it's guaranteed to converge.

        ## Parameters

        Args:
            graph: Co-occurrence graph to rank.
                Must have at least one node.
            initial_scores: Optional starting scores for nodes.
                If None, uses uniform distribution (1/N for each node).
                Useful for: Warm starts, incremental updates.

        Returns:
            PageRankResult containing:
            - scores: Dict mapping pattern -> importance score
            - iterations: Number of iterations performed
            - converged: True if converged before max_iterations
            - final_delta: Final score change (should be < tolerance)

        ## Example

        ```python
        # Basic usage
        pr = WeightedPageRank()
        result = pr.compute(graph)

        if result.converged:
            print(f"Converged in {result.iterations} iterations")
            top = pr.get_top_k(result.scores, k=10)
        else:
            print("Did not converge - increase max_iterations")

        # With custom initial scores
        initial = {"proxy": 0.5, "config": 0.3, "http": 0.2}
        result = pr.compute(graph, initial_scores=initial)
        ```

        ## Performance Notes

        - **Time**: O(k * E) where k=iterations, E=edges
        - **Space**: O(N) for score storage
        - **Typical**: 20-50 iterations, <100ms for small graphs
        """
        nodes = graph.nodes()
        n = len(nodes)

        if n == 0:
            return PageRankResult(scores={}, iterations=0, converged=True, final_delta=0.0)

        # Initialize scores uniformly
        scores: Dict[str, float] = {}
        if initial_scores:
            # Use provided initial scores (normalize if needed)
            total = sum(initial_scores.values())
            if total > 0:
                scores = {node: initial_scores.get(node, 1.0 / n) for node in nodes}
                # Normalize
                score_sum = sum(scores.values())
                scores = {k: v / score_sum for k, v in scores.items()}
            else:
                scores = {node: 1.0 / n for node in nodes}
        else:
            scores = {node: 1.0 / n for node in nodes}

        # Get adjacency data
        adj_dict = graph.to_adjacency_dict()

        # Precompute out-weights for each node
        out_weights: Dict[str, float] = {}
        for node in nodes:
            out_weights[node] = sum(adj_dict.get(node, {}).values())

        # Power iteration
        converged = False
        final_delta = 0.0
        iteration = 0

        for iteration in range(1, self.max_iterations + 1):
            new_scores: Dict[str, float] = {}

            # Compute new scores
            for node in nodes:
                # Base score from random jump
                score = (1.0 - self.damping) / n

                # Add contribution from neighbors
                neighbors = adj_dict.get(node, {})
                for neighbor, weight in neighbors.items():
                    if out_weights[neighbor] > 0:
                        score += self.damping * scores[neighbor] * weight / out_weights[neighbor]

                new_scores[node] = score

            # Check convergence
            delta = sum(abs(new_scores[node] - scores[node]) for node in nodes)
            final_delta = delta

            scores = new_scores

            if delta < self.tolerance:
                converged = True
                break

        # Normalize final scores
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}

        return PageRankResult(
            scores=scores, iterations=iteration, converged=converged, final_delta=final_delta
        )

    def compute_with_filtering(self, graph: "CooccurrenceGraph") -> Tuple[Dict[str, float], int]:
        """Compute PageRank and filter out low-importance patterns.

        ## Purpose

        Not all patterns are equally useful. Some have very low PageRank
        scores, indicating they're peripheral or noise.

        This method:
        1. Computes full PageRank
        2. Removes patterns with score < min_score
        3. Returns filtered results

        ## When to Use

        **Use filtering when**:
        - You have many low-frequency patterns
        - You want to focus on important concepts
        - Output size matters (UI, reports)

        **Don't filter when**:
        - You need complete results
        - You're debugging
        - Graph is already small (<50 nodes)

        ## Parameters

        Args:
            graph: Co-occurrence graph to analyze.

        Returns:
            Tuple of:
            - filtered_scores: Dict with only high-importance patterns
            - removed_count: Number of patterns filtered out

        ## Example

        ```python
        pr = WeightedPageRank(min_score=0.001)
        filtered, removed = pr.compute_with_filtering(graph)

        print(f"Removed {removed} low-importance patterns")
        print(f"Kept {len(filtered)} important patterns")

        # Get top patterns from filtered results
        top = pr.get_top_k(filtered, k=10)
        ```

        ## Tuning min_score

        - **Higher (0.01)**: Keep only top ~10% of patterns
        - **Default (0.001)**: Remove bottom ~1% as noise
        - **Lower (0.0001)**: Keep almost all patterns

        Adjust based on your use case and desired output size.
        """
        result = self.compute(graph)
        scores = result.scores

        # Filter low-scoring nodes
        filtered = {node: score for node, score in scores.items() if score >= self.min_score}

        removed = len(scores) - len(filtered)

        return filtered, removed

    def get_top_k(self, scores: Dict[str, float], k: int = 10) -> List[Tuple[str, float]]:
        """Get top-k patterns by PageRank score.

        ## Purpose

        Convenience method to extract the most important patterns
        from PageRank results.

        ## Sorting

        Patterns are sorted by score in descending order:
        - Highest score = most important
        - Ties are broken by pattern name (alphabetical)

        ## Parameters

        Args:
            scores: Dict mapping pattern -> PageRank score.
                Typically from compute() or compute_with_filtering().
            k: Number of top patterns to return (default: 10).
                Use larger k for more results, smaller for summary.

        Returns:
            List of (pattern, score) tuples, sorted by score descending.
            Length is min(k, len(scores)).

        ## Example

        ```python
        pr = WeightedPageRank()
        result = pr.compute(graph)

        # Get top 10 patterns
        top_10 = pr.get_top_k(result.scores, k=10)

        for pattern, score in top_10:
            print(f"{pattern}: {score:.4f}")

        # Get top 5 for UI display
        top_5 = pr.get_top_k(result.scores, k=5)
        ```

        ## Output Format

        ```python
        [
            ("proxy", 0.0523),
            ("config", 0.0489),
            ("http", 0.0456),
            ...
        ]
        ```
        """
        sorted_scores = sorted(scores.items(), key=lambda x: -x[1])
        return sorted_scores[:k]

    def normalize_scores(self, scores: Dict[str, float], method: str = "sum") -> Dict[str, float]:
        """Normalize PageRank scores for different use cases.

        ## Normalization Methods

        ### "sum" (default)

        Normalizes scores so they sum to 1.0.

        **Use when**: You want probability interpretation
        **Example**: [0.5, 0.3, 0.2] → sum = 1.0

        ### "max"

        Normalizes so maximum score = 1.0.

        **Use when**: You want relative importance (best = 1.0)
        **Example**: [0.5, 0.3, 0.2] → [1.0, 0.6, 0.4]

        ### "minmax"

        Normalizes to [0.0, 1.0] range.

        **Use when**: You want full range utilization
        **Example**: [0.5, 0.3, 0.2] → [1.0, 0.33, 0.0]

        ## Why Normalize?

        PageRank scores already sum to 1.0 after computation, but:
        - After filtering, sum may be < 1.0
        - For visualization, you may want different scaling
        - For comparison across graphs, normalization helps

        ## Parameters

        Args:
            scores: Dict mapping pattern -> raw score.
            method: Normalization method:
                - "sum": Normalize to sum=1.0 (probability)
                - "max": Normalize to max=1.0 (relative)
                - "minmax": Normalize to [0,1] range (full scale)

        Returns:
            Dict with normalized scores.
            Same keys as input, values scaled according to method.

        ## Example

        ```python
        pr = WeightedPageRank()
        result = pr.compute(graph)

        # Probability interpretation (default)
        prob_scores = pr.normalize_scores(result.scores, method="sum")
        # Sum = 1.0, each score = probability of being at that node

        # Relative importance
        rel_scores = pr.normalize_scores(result.scores, method="max")
        # Best pattern = 1.0, others = fraction of best

        # Full range for visualization
        viz_scores = pr.normalize_scores(result.scores, method="minmax")
        # Range [0, 1], good for color mapping, bar charts
        ```

        ## Edge Cases

        - Empty scores: Returns empty dict
        - All zeros: Returns original scores (no division by zero)
        - Single pattern: Returns {pattern: 1.0} for all methods
        """
        if not scores:
            return {}

        if method == "sum":
            # Normalize to sum to 1
            total = sum(scores.values())
            if total > 0:
                return {k: v / total for k, v in scores.items()}
            return scores

        elif method == "max":
            # Normalize to max = 1
            max_score = max(scores.values())
            if max_score > 0:
                return {k: v / max_score for k, v in scores.items()}
            return scores

        elif method == "minmax":
            # Normalize to [0, 1] range
            min_score = min(scores.values())
            max_score = max(scores.values())
            range_score = max_score - min_score
            if range_score > 0:
                return {k: (v - min_score) / range_score for k, v in scores.items()}
            return scores

        else:
            raise ValueError(f"Unknown normalization method: {method}")


def compute_pagerank(
    graph: "CooccurrenceGraph",
    damping: float = 0.85,
    max_iterations: int = 100,
    tolerance: float = 1e-6,
) -> Dict[str, float]:
    """Convenience function to compute PageRank scores.

    ## Purpose

    Simple one-liner for common use case: compute PageRank with
    default settings and get scores dict.

    ## When to Use

    **Use this function when**:
    - You want simple, default behavior
    - You don't need convergence info
    - You're writing quick scripts

    **Use WeightedPageRank class when**:
    - You need custom parameters
    - You want convergence information
    - You need filtering or normalization
    - You're computing PageRank multiple times

    ## Parameters

    Args:
        graph: Co-occurrence graph to rank.
        damping: Damping factor (default: 0.85).
            See WeightedPageRank.__init__ for details.
        max_iterations: Maximum iterations (default: 100).
        tolerance: Convergence threshold (default: 1e-6).

    Returns:
        Dict mapping pattern -> PageRank score.
        Scores sum to 1.0 (normalized).

    ## Example

    ```python
    from traceflux import CooccurrenceGraph
    from traceflux.pagerank import compute_pagerank

    # Build graph
    graph = CooccurrenceGraph()
    graph.add_document_cooccurrences(["proxy", "config", "http"], window_size=5)

    # Compute PageRank (simple way)
    scores = compute_pagerank(graph)

    # Get top pattern
    top_pattern = max(scores.items(), key=lambda x: x[1])
    print(f"Most important: {top_pattern[0]} (score: {top_pattern[1]:.4f})")
    ```

    ## Implementation

    This function creates a WeightedPageRank instance and calls compute().
    Equivalent to:

    ```python
    pr = WeightedPageRank(damping, max_iterations, tolerance)
    result = pr.compute(graph)
    scores = result.scores
    ```

    ## See Also

    - WeightedPageRank: Full class with more options
    - WeightedPageRank.compute_with_filtering: Filter low-scoring patterns
    - WeightedPageRank.get_top_k: Get top-k patterns easily
    """
    pr = WeightedPageRank(damping=damping, max_iterations=max_iterations, tolerance=tolerance)
    result = pr.compute(graph)
    return result.scores
