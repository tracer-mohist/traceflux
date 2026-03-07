"""traceflux version information.

Single source of truth for traceflux version.
Used by CLI (--version) and pyproject.toml.

## Version Format

Semantic Versioning: MAJOR.MINOR.PATCH

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

## Example

```python
from traceflux import __version__
print(__version__)  # "1.0.0"
```
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
