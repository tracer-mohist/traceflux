"""CLI Commands - Individual command implementations.

Each module implements a single traceflux command:
- search: Find patterns in text
- index: Build persistent index
- patterns: List discovered patterns
- associations: Find related terms
"""

from .search import cmd_search
from .index import cmd_index
from .patterns import cmd_patterns
from .associations import cmd_associations

__all__ = ["cmd_search", "cmd_index", "cmd_patterns", "cmd_associations"]
