"""Search Command - Find patterns in text files.

Search works like grep: finds query in text directly.
Does NOT rely on pre-detected patterns (that's what 'patterns' command is for).
"""

import json
import sys
from typing import List, Tuple

from traceflux.cli.helpers import scan_paths, show_suggestions
from traceflux.output import OutputFormatter


def cmd_search(args) -> int:
    """Execute search command.

    Performs case-insensitive search for query in text files.
    Supports stdin input and JSON output.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for no results)

    Example:
        # Search for "proxy" in current directory
        traceflux search "proxy" .

        # Search with JSON output
        traceflux search "proxy" src/ --json

        # Search from stdin
        cat file.txt | traceflux search "pattern" -
    """
    # Create formatter for this command
    fmt = OutputFormatter()

    # Use stdin if no paths provided and stdin is not a tty
    use_stdin = not args.paths and not sys.stdin.isatty()

    if use_stdin:
        documents = scan_paths([], read_stdin=True)
    else:
        documents = scan_paths(args.paths if args.paths else ["."])

    if not documents:
        fmt.error("No documents found to search")
        return 1

    # Search directly in content (like grep)
    # Case-insensitive search
    query = args.query
    query_lower = query.lower()

    results: List[Tuple[str, List[int]]] = []  # (filepath, [positions])

    for filepath, content in documents:
        positions = []
        content_lower = content.lower()
        start = 0

        # Find all occurrences (case-insensitive)
        while True:
            pos = content_lower.find(query_lower, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1

        if positions:
            results.append((filepath, positions))

    if not results:
        fmt.print(f"No results found for '{query}'")
        return 0

    # Format output
    if args.json:
        output = {
            "query": query,
            "results": [
                {"file": doc_id, "positions": positions, "count": len(positions)}
                for doc_id, positions in results
            ],
            "total_matches": sum(len(pos) for _, pos in results),
        }
        print(json.dumps(output))
    else:
        fmt.success(f"Found '{query}' in {len(results)} file(s)")
        fmt.print()

        for doc_id, positions in results[: args.limit]:
            count = len(positions)
            fmt.print(f"  {doc_id}")
            fmt.print(
                f"    {count} occurrence(s) at positions: {positions[:10]}{'...' if len(positions) > 10 else ''}"
            )

            if args.verbose:
                # Show context for first occurrence
                for filepath, content in documents:
                    if filepath == doc_id:
                        pos = positions[0]
                        start = max(0, pos - 40)
                        end = min(len(content), pos + len(query) + 40)
                        context = content[start:end]
                        fmt.print(f"    Context: ...{context}...")
                        break
            fmt.print()

        # Show suggestions (related terms)
        if not args.json:
            show_suggestions(query, documents, limit=5, formatter=fmt)

    return 0
