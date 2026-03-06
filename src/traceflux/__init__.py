# src/traceflux/__init__.py
"""traceflux - Lightweight text search engine with associative discovery."""

__version__ = "0.1.0"
__author__ = "Tracer"

from traceflux.scanner import Scanner
from traceflux.index import PatternIndex

__all__ = ["Scanner", "PatternIndex"]
