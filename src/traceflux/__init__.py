"""traceflux - Lightweight text search engine with associative discovery."""

from traceflux.__version__ import __version__, __version_info__
from traceflux.associations import Association, AssociationResult, AssociativeSearch
from traceflux.graph import CooccurrenceGraph, GraphStats
from traceflux.index import PatternIndex
from traceflux.pagerank import PageRankResult, WeightedPageRank, compute_pagerank
from traceflux.patterns import Pattern, PatternDetector
from traceflux.scanner import Scanner

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
