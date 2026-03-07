#!/usr/bin/env python3
"""traceflux CLI - Main entry point and argument parsing."""

import argparse
import sys
from typing import Optional

from traceflux import __version__
from traceflux.cli.commands import cmd_search, cmd_index, cmd_patterns, cmd_associations


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
        version=f"%(prog)s {__version__}",
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
        default=[],
        help="Paths to search (default: stdin or current directory)",
    )
    search_parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=20,
        help="Maximum results to show (default: 20)",
    )
    search_parser.add_argument(
        "-v",
        "--verbose",
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
        default=[],
        help="Paths to index (default: stdin or current directory)",
    )
    index_parser.add_argument(
        "-o",
        "--output",
        help="Output file for index (default: .traceflux_index.json)",
    )
    index_parser.add_argument(
        "-v",
        "--verbose",
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
        default=[],
        help="Paths to analyze (default: stdin or current directory)",
    )
    patterns_parser.add_argument(
        "--min-length",
        type=int,
        default=3,
        help="Minimum pattern length (default: 3)",
    )
    patterns_parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=20,
        help="Maximum patterns to show (default: 20)",
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
        description="Find patterns associated with a query using graph traversal.",
    )
    assoc_parser.add_argument(
        "query",
        help="Query pattern to find associations for",
    )
    assoc_parser.add_argument(
        "paths",
        nargs="*",
        default=[],
        help="Paths to analyze (default: stdin or current directory)",
    )
    assoc_parser.add_argument(
        "--hops",
        type=int,
        default=2,
        help="Maximum degrees of separation (default: 2)",
    )
    assoc_parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=10,
        help="Maximum associations to show (default: 10)",
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
        help="Show association paths",
    )
    assoc_parser.add_argument(
        "--show-types",
        action="store_true",
        help="Show punctuation type distribution",
    )
    assoc_parser.set_defaults(func=cmd_associations)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point.

    Args:
        argv: Command-line arguments (uses sys.argv if None)

    Returns:
        Exit code
    """
    parser = setup_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
