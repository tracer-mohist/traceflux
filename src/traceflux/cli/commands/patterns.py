"""Patterns Command - List discovered patterns in text files."""

import sys

from traceflux import Scanner, PatternDetector
from traceflux.output import OutputFormatter
from traceflux.cli.helpers import scan_paths


def cmd_patterns(args) -> int:
    """Execute patterns command.
    
    Extracts and lists the most frequent patterns found in text files.
    Useful for understanding what repeated structures exist in a corpus.
    
    Args:
        args: Parsed command-line arguments
    
    Returns:
        Exit code (0 for success)
    
    Example:
        # List top 20 patterns
        traceflux patterns src/
        
        # List patterns with minimum length
        traceflux patterns docs/ --min-length 5
        
        # JSON output for processing
        traceflux patterns . --json | jq '.patterns[]'
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
    
    # Extract patterns
    scanner = Scanner()
    detector = PatternDetector(min_support=2, min_length=args.min_length)
    
    all_patterns: dict[str, int] = {}
    
    for filepath, content in documents:
        patterns = detector.find_patterns(content)
        
        for pattern in patterns:
            all_patterns[pattern] = all_patterns.get(pattern, 0) + 1
    
    # Sort by frequency
    sorted_patterns = sorted(all_patterns.items(), key=lambda x: x[1], reverse=True)
    
    # Output
    if args.json:
        output = {
            "patterns": [
                {"pattern": p, "frequency": f}
                for p, f in sorted_patterns[:args.limit]
            ],
            "total_patterns": len(all_patterns),
        }
        fmt.print(output)
    else:
        fmt.print(f"Top {min(args.limit, len(sorted_patterns))} patterns:")
        fmt.print()
        
        for pattern, freq in sorted_patterns[:args.limit]:
            fmt.print(f"  {pattern:30s} {freq:5d} occurrence(s)")
    
    return 0
