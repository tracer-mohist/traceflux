# src/traceflux/__init__.py
"""traceflux - Lightweight text search engine with associative discovery."""

__version__ = "0.1.0"
__author__ = "Tracer"

from traceflux.scanner import Scanner
from traceflux.index import PatternIndex
from traceflux.patterns import PatternDetector
from traceflux.graph import CooccurrenceGraph
from traceflux.pagerank import WeightedPageRank, compute_pagerank

__all__ = [
    "Scanner",
    "PatternIndex",
    "PatternDetector",
    "CooccurrenceGraph",
    "WeightedPageRank",
    "compute_pagerank",
]
