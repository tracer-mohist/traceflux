"""traceflux - Lightweight text search engine with associative discovery."""

from traceflux.__version__ import __version__, __version_info__
from traceflux.scanner import Scanner
from traceflux.patterns import PatternDetector, Pattern
from traceflux.index import PatternIndex
from traceflux.graph import CooccurrenceGraph, GraphStats
from traceflux.pagerank import WeightedPageRank, compute_pagerank, PageRankResult
from traceflux.associations import AssociativeSearch, Association, AssociationResult

__all__ = [
    "Scanner",
    "PatternDetector",
    "Pattern",
    "PatternIndex",
    "CooccurrenceGraph",
    "GraphStats",
    "WeightedPageRank",
    "compute_pagerank",
    "PageRankResult",
    "AssociativeSearch",
    "Association",
    "AssociationResult",
    "__version__",
    "__version_info__",
]
