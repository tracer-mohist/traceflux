"""Index Command - Build persistent index for directories."""

import sys

from traceflux import PatternDetector, PatternIndex, Scanner
from traceflux.cli.helpers import scan_paths
from traceflux.output import OutputFormatter


def cmd_index(args) -> int:
    """Execute index command.

    Builds a pattern index from text files and saves to disk.
    The index can be used for faster subsequent searches.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)

    Example:
        # Build index for current directory
        traceflux index .

        # Build index with custom output file
        traceflux index src/ -o my_index.json

        # Verbose output
        traceflux index docs/ -v
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
        fmt.error("No documents found to index")
        return 1

    # Build index
    scanner = Scanner()
    detector = PatternDetector(min_support=2, min_length=3)
    index = PatternIndex()

    if args.verbose:
        fmt.info(f"Indexing {len(documents)} document(s)")

    for filepath, content in documents:
        patterns = detector.find_patterns(content)

        for pattern, positions in patterns.items():
            index.add(pattern, filepath, positions)

        if args.verbose:
            fmt.info(f"Indexed {filepath}: {len(patterns)} patterns")

    # Save index
    output_path = args.output or ".traceflux_index.json"
    index.save(output_path)

    stats = index.stats()
    fmt.success(f"Index saved to {output_path}")
    fmt.print(f"  Patterns: {stats['pattern_count']}")
    fmt.print(f"  Documents: {stats['doc_count']}")
    fmt.print(f"  Total occurrences: {stats['total_occurrences']}")

    return 0
