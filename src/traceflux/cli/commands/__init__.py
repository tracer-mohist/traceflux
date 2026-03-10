# src/traceflux/cli/commands/__init__.py
"""CLI Commands - Individual command implementations.

Each module implements a single traceflux command:
- search: Find patterns in text
- index: Build persistent index
- patterns: List discovered patterns
- associations: Find related terms
"""

from .associations import cmd_associations
from .index import cmd_index
from .patterns import cmd_patterns
from .search import cmd_search

__all__ = [
    "cmd_search",
    "cmd_index",
    "cmd_patterns",
    "cmd_associations",
]
