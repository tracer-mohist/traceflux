"""CLI helpers - Path scanning and suggestion utilities.

Shared helper functions used by multiple CLI commands.
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple

from traceflux.output import OutputFormatter


def scan_paths(
    paths: List[str], read_stdin: bool = False, verbose: bool = False
) -> List[Tuple[str, str]]:
    """Scan paths and return list of (filepath, content) tuples.

    Handles files, directories, and stdin. Skips binary files and
    common non-text directories.

    Args:
        paths: List of file/directory paths to scan
        read_stdin: If True and no paths provided, read from stdin
        verbose: If True, print warnings for unreadable files

    Returns:
        List of (filepath, content) tuples

    Example:
        >>> docs = scan_paths(["./src", "./docs"])
        >>> len(docs)
        15
        >>> filepath, content = docs[0]
    """
    documents: List[Tuple[str, str]] = []

    # Handle stdin
    if read_stdin and (not paths or paths == ["-"]):
        content = sys.stdin.read()
        if content.strip():
            documents.append(("stdin", content))
        return documents

    # Filter out "-" from paths if present
    paths = [p for p in paths if p != "-"]

    for path_str in paths:
        path = Path(path_str)

        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                documents.append((str(path), content))
            except Exception as e:
                print(f"WARNING: Could not read {path}: {e}", file=sys.stderr)

        elif path.is_dir():
            # Walk directory, skip common non-text dirs
            skip_dirs = {
                ".git",
                ".svn",
                ".hg",
                "node_modules",
                "__pycache__",
                ".venv",
                "venv",
                ".tox",
                ".nox",
                "build",
                "dist",
                ".pytest_cache",
                ".coverage",
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
                        ".pyc",
                        ".pyo",
                        ".so",
                        ".dll",
                        ".exe",
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".gif",
                        ".ico",
                        ".pdf",
                        ".doc",
                        ".docx",
                        ".xls",
                        ".xlsx",
                        ".zip",
                        ".tar",
                        ".gz",
                        ".bz2",
                        ".7z",
                    }

                    if file.suffix.lower() in binary_exts:
                        continue

                    try:
                        content = file.read_text(encoding="utf-8", errors="ignore")
                        if content.strip():  # Skip empty files
                            documents.append((str(file), content))
                    except Exception as e:
                        if verbose:
                            print(f"WARNING: Could not read {file}: {e}", file=sys.stderr)

    return documents


def show_suggestions(
    query: str,
    documents: List[Tuple[str, str]],
    limit: int = 5,
    formatter: Optional[OutputFormatter] = None,
) -> None:
    """Show related term suggestions after search results.

    Builds a co-occurrence graph from documents and finds
    patterns associated with the query.

    Args:
        query: Original search query
        documents: List of (filepath, content) tuples
        limit: Maximum suggestions to show
        formatter: Output formatter (uses default if None)

    Example:
        >>> docs = scan_paths(["./src"])
        >>> show_suggestions("proxy", docs, limit=5)
        Related terms:
          - config                    (strength: 0.320, degree 1)
          - session                   (strength: 0.318, degree 1)
    """
    from traceflux import CooccurrenceGraph, PatternDetector, compute_pagerank
    from traceflux.associations import AssociativeSearch
    from traceflux.output import OutputFormatter

    fmt = formatter or OutputFormatter()

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
        fmt.print("Related terms:")
        for assoc in result.associations[:limit]:
            fmt.print(
                f"  - {assoc.pattern:25s} (strength: {assoc.score:.3f}, degree {assoc.degree})"
            )
        fmt.print()
