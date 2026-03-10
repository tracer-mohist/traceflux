# src/traceflux/cli/commands/associations.py
"""Associations Command - Find related terms using graph traversal."""

import sys

from traceflux import CooccurrenceGraph, Scanner, compute_pagerank
from traceflux.associations import AssociativeSearch
from traceflux.cli.helpers import scan_paths
from traceflux.output import OutputFormatter


def cmd_associations(args) -> int:
    """Execute associations command.

    Finds terms associated with a query using co-occurrence graph
    and PageRank ranking. Supports multi-hop associations.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)

    Example:
        # Find 1-hop associations
        traceflux associations "proxy" src/

        # Find 2-hop associations with explanations
        traceflux associations "proxy" src/ --hops 2 --explain

        # Show punctuation type distribution
        traceflux associations "proxy" src/ --show-types

        # JSON output for processing
        traceflux associations "proxy" src/ --json | jq '.associations[]'
    """
    # Create formatter
    fmt = OutputFormatter()

    # Use stdin if no paths provided and stdin is not a tty
    use_stdin = not args.paths and not sys.stdin.isatty()

    if use_stdin:
        documents = scan_paths([], read_stdin=True)
    else:
        documents = scan_paths(args.paths if args.paths else ["."])

    if not documents:
        fmt.error("No documents found to analyze")
        return 1

    # Build co-occurrence graph from scanner segments
    # This finds associations between words/terms, not just repeated patterns
    scanner = Scanner(min_content_len=2)  # Skip single-char segments
    graph = CooccurrenceGraph()

    for filepath, content in documents:
        segments = list(scanner.scan(content))

        # Extract content from segments (lowercase for normalization)
        terms = [seg.content.lower() for seg in segments if seg.content]

        # Add co-occurrences within window
        graph.add_document_cooccurrences(terms, window_size=5)

    # Find associations
    query = args.query.lower()

    if not graph.has_node(query):
        fmt.print(f"No associations found for '{query}'")
        return 0

    # Compute PageRank for ranking
    pagerank_scores = compute_pagerank(graph)

    # Use AssociativeSearch for multi-hop associations
    search = AssociativeSearch(graph, pagerank_scores, lambda_param=0.7)
    result = search.find_associations(
        query,
        max_degree=args.hops,
        top_k=args.limit * 2,  # Get more, then filter by min_strength
        min_score=args.min_strength,
    )

    # Output
    if args.json:
        output = {
            "query": query,
            "associations": [
                {
                    "term": assoc.pattern,
                    "strength": assoc.score,
                    "degree": assoc.degree,
                    "pagerank": assoc.pagerank,
                    "path": assoc.path if args.explain else None,
                }
                for assoc in result.associations[: args.limit]
            ],
            "total_found": result.total_found,
        }
        fmt.print(output)
    else:
        fmt.success(f"Associations for '{query}' (hops={args.hops})")
        fmt.print()

        for assoc in result.associations[: args.limit]:
            if args.explain:
                fmt.print(
                    f"  {assoc.pattern:30s} strength: {assoc.score:.3f} (degree {assoc.degree}, path: {' -> '.join(assoc.path)})"
                )
            else:
                fmt.print(
                    f"  {assoc.pattern:30s} strength: {assoc.score:.3f} (degree {assoc.degree})"
                )

        if not result.associations:
            fmt.print("  (no associations found)")

        # Show type distribution if requested
        if args.show_types:
            fmt.print()
            fmt.print(f"Type distribution for '{query}':")
            type_counts = {}
            for filepath, content in documents:
                segments = list(scanner.scan(content))
                for seg in segments:
                    if seg.content.lower() == query:
                        type_key = seg.type_key
                        type_counts[type_key] = type_counts.get(type_key, 0) + 1

            for type_key, count in sorted(type_counts.items(), key=lambda x: -x[1]):
                pre, post = type_key.split("|")
                fmt.print(f"  ({repr(pre)}, {repr(post)}): {count} occurrence(s)")

    return 0
