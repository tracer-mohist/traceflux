#!/usr/bin/env python3
"""traceflux CLI - Command-line interface for traceflux search engine."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from traceflux import Scanner, PatternDetector, PatternIndex, CooccurrenceGraph, compute_pagerank
from traceflux.associations import AssociativeSearch


def setup_parser() -> argparse.ArgumentParser:
    """Create argument parser with all commands."""
    parser = argparse.ArgumentParser(
        prog="traceflux",
        description="Lightweight text search engine with associative discovery",
        epilog="Use '%(prog)s <command> --help' for command-specific help.",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s 0.1.0",
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        metavar="<command>",
    )
    
    # Search command
    search_parser = subparsers.add_parser(
        "search",
        help="Search for patterns in text files",
        description="Search for text patterns and show results with relevance scores.",
    )
    search_parser.add_argument(
        "query",
        help="Search query (keyword or phrase)",
    )
    search_parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Paths to search (default: current directory)",
    )
    search_parser.add_argument(
        "-n", "--limit",
        type=int,
        default=20,
        help="Maximum results to show (default: 20)",
    )
    search_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output",
    )
    search_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    search_parser.set_defaults(func=cmd_search)
    
    # Index command
    index_parser = subparsers.add_parser(
        "index",
        help="Build index for directories",
        description="Build a pattern index from text files.",
    )
    index_parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Paths to index (default: current directory)",
    )
    index_parser.add_argument(
        "-o", "--output",
        help="Output file for index (default: .traceflux_index.json)",
    )
    index_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output",
    )
    index_parser.set_defaults(func=cmd_index)
    
    # Patterns command
    patterns_parser = subparsers.add_parser(
        "patterns",
        help="List discovered patterns",
        description="List patterns found in text files.",
    )
    patterns_parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Paths to analyze (default: current directory)",
    )
    patterns_parser.add_argument(
        "--min-length",
        type=int,
        default=3,
        help="Minimum pattern length (default: 3)",
    )
    patterns_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum patterns to show (default: 50)",
    )
    patterns_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    patterns_parser.set_defaults(func=cmd_patterns)
    
    # Associations command
    assoc_parser = subparsers.add_parser(
        "associations",
        help="Find related terms",
        description="Discover terms related to your query using co-occurrence graph.",
    )
    assoc_parser.add_argument(
        "query",
        help="Starting query term",
    )
    assoc_parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Paths to analyze (default: current directory)",
    )
    assoc_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum associations to show (default: 10)",
    )
    assoc_parser.add_argument(
        "--hops",
        type=int,
        default=2,
        help="Maximum degrees of separation (default: 2)",
    )
    assoc_parser.add_argument(
        "--min-strength",
        type=float,
        default=0.0,
        help="Minimum association strength (default: 0.0)",
    )
    assoc_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    assoc_parser.add_argument(
        "--explain",
        action="store_true",
        help="Show explanation for associations",
    )
    assoc_parser.set_defaults(func=cmd_associations)
    
    return parser


def scan_paths(paths: list[str]) -> list[tuple[str, str]]:
    """Scan paths and return list of (filepath, content) tuples."""
    documents = []
    
    for path_str in paths:
        path = Path(path_str)
        
        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                documents.append((str(path), content))
            except Exception as e:
                print(f"Warning: Could not read {path}: {e}", file=sys.stderr)
        
        elif path.is_dir():
            # Walk directory, skip common non-text dirs
            skip_dirs = {
                ".git", ".svn", ".hg",
                "node_modules", "__pycache__", ".venv", "venv",
                ".tox", ".nox", "build", "dist",
                ".pytest_cache", ".coverage",
            }
            
            for file in path.rglob("*"):
                if file.is_file():
                    # Skip if any parent is in skip_dirs
                    skip = False
                    for parent in file.parents:
                        if parent.name in skip_dirs:
                            skip = True
                            break
                    
                    if skip:
                        continue
                    
                    # Skip binary files by extension
                    binary_exts = {
                        ".pyc", ".pyo", ".so", ".dll", ".exe",
                        ".jpg", ".jpeg", ".png", ".gif", ".ico",
                        ".pdf", ".doc", ".docx", ".xls", ".xlsx",
                        ".zip", ".tar", ".gz", ".bz2", ".7z",
                    }
                    
                    if file.suffix.lower() in binary_exts:
                        continue
                    
                    try:
                        content = file.read_text(encoding="utf-8", errors="ignore")
                        if content.strip():  # Skip empty files
                            documents.append((str(file), content))
                    except Exception as e:
                        if verbose:
                            print(f"Warning: Could not read {file}: {e}", file=sys.stderr)
    
    return documents


verbose = False  # Global flag for scan_paths


def cmd_search(args: argparse.Namespace) -> int:
    """Execute search command."""
    global verbose
    verbose = args.verbose
    
    documents = scan_paths(args.paths)
    
    if not documents:
        print("No documents found to search.", file=sys.stderr)
        return 1
    
    # Build index
    scanner = Scanner()
    detector = PatternDetector(min_support=2, min_length=3)
    index = PatternIndex()
    
    for filepath, content in documents:
        patterns = detector.find_patterns(content)
        
        for pattern, positions in patterns.items():
            index.add(pattern, filepath, positions)
    
    # Search
    query = args.query.lower()
    results = index.get(query)
    
    if not results:
        print(f"No results found for '{query}'")
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
        print(json.dumps(output, indent=2))
    else:
        print(f"Found '{query}' in {len(results)} file(s):\n")
        
        for doc_id, positions in results[:args.limit]:
            count = len(positions)
            print(f"  {doc_id}")
            print(f"    {count} occurrence(s) at positions: {positions[:10]}{'...' if len(positions) > 10 else ''}")
            
            if args.verbose:
                # Show context for first occurrence
                for filepath, content in documents:
                    if filepath == doc_id:
                        pos = positions[0]
                        start = max(0, pos - 40)
                        end = min(len(content), pos + len(query) + 40)
                        context = content[start:end]
                        print(f"    Context: ...{context}...")
                        break
            print()
        
        # Show suggestions (related terms)
        if not args.json:
            _show_suggestions(query, documents, limit=5)
    
    return 0


def cmd_index(args: argparse.Namespace) -> int:
    """Execute index command."""
    global verbose
    verbose = args.verbose
    
    documents = scan_paths(args.paths)
    
    if not documents:
        print("No documents found to index.", file=sys.stderr)
        return 1
    
    # Build index
    scanner = Scanner()
    detector = PatternDetector(min_support=2, min_length=3)
    index = PatternIndex()
    
    if verbose:
        print(f"Indexing {len(documents)} document(s)...")
    
    for filepath, content in documents:
        patterns = detector.find_patterns(content)
        
        for pattern, positions in patterns.items():
            index.add(pattern, filepath, positions)
        
        if verbose:
            print(f"  Indexed {filepath}: {len(patterns)} patterns")
    
    # Save index
    output_path = args.output or ".traceflux_index.json"
    index.save(output_path)
    
    stats = index.stats()
    print(f"Index saved to {output_path}")
    print(f"  Patterns: {stats['pattern_count']}")
    print(f"  Documents: {stats['doc_count']}")
    print(f"  Total occurrences: {stats['total_occurrences']}")
    
    return 0


def cmd_patterns(args: argparse.Namespace) -> int:
    """Execute patterns command."""
    documents = scan_paths(args.paths)
    
    if not documents:
        print("No documents found to analyze.", file=sys.stderr)
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
        print(json.dumps(output, indent=2))
    else:
        print(f"Top {min(args.limit, len(sorted_patterns))} patterns:\n")
        
        for pattern, freq in sorted_patterns[:args.limit]:
            print(f"  {pattern:30s} {freq:5d} occurrence(s)")
    
    return 0


def cmd_associations(args: argparse.Namespace) -> int:
    """Execute associations command."""
    documents = scan_paths(args.paths)
    
    if not documents:
        print("No documents found to analyze.", file=sys.stderr)
        return 1
    
    # Build co-occurrence graph
    scanner = Scanner()
    detector = PatternDetector(min_support=2, min_length=3)
    graph = CooccurrenceGraph()
    
    for filepath, content in documents:
        patterns = detector.find_patterns(content)
        
        # Add patterns to graph
        pattern_list = list(patterns.keys())
        graph.add_document_cooccurrences(pattern_list, window_size=5)
    
    # Find associations
    query = args.query.lower()
    
    if not graph.has_node(query):
        print(f"No associations found for '{query}'")
        return 0
    
    # Compute PageRank for ranking
    pagerank_scores = compute_pagerank(graph)
    
    # Use AssociativeSearch for multi-hop associations
    search = AssociativeSearch(graph, pagerank_scores, lambda_param=0.7)
    result = search.find_associations(
        query,
        max_degree=args.hops,
        top_k=args.limit * 2,  # Get more, then filter by min_strength
        min_score=args.min_strength
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
                for assoc in result.associations[:args.limit]
            ],
            "total_found": result.total_found,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Associations for '{query}' (hops={args.hops}):\n")
        
        for assoc in result.associations[:args.limit]:
            if args.explain:
                print(f"  {assoc.pattern:30s} strength: {assoc.score:.3f} (degree {assoc.degree}, path: {' → '.join(assoc.path)})")
            else:
                print(f"  {assoc.pattern:30s} strength: {assoc.score:.3f} (degree {assoc.degree})")
        
        if not result.associations:
            print("  (no associations found)")
    
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point."""
    parser = setup_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 0
    
    return args.func(args)


def _show_suggestions(query: str, documents: list[tuple[str, str]], limit: int = 5) -> None:
    """Show related term suggestions after search results.
    
    Args:
        query: Original search query
        documents: List of (filepath, content) tuples
        limit: Maximum suggestions to show
    """
    # Build co-occurrence graph
    detector = PatternDetector(min_support=2, min_length=3)
    graph = CooccurrenceGraph()
    
    for filepath, content in documents:
        patterns = detector.find_patterns(content)
        pattern_list = list(patterns.keys())
        graph.add_document_cooccurrences(pattern_list, window_size=5)
    
    # Check if query exists in graph
    if not graph.has_node(query):
        return
    
    # Get associations
    pagerank_scores = compute_pagerank(graph)
    search = AssociativeSearch(graph, pagerank_scores, lambda_param=0.7)
    result = search.find_associations(query, max_degree=2, top_k=limit * 2)
    
    if result.associations:
        print("Related terms:")
        for assoc in result.associations[:limit]:
            print(f"  • {assoc.pattern:25s} (strength: {assoc.score:.3f}, degree {assoc.degree})")
        print()


if __name__ == "__main__":
    sys.exit(main())
