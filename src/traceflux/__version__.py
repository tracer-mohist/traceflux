# src/traceflux/__version__.py
"""traceflux version information.

Single source of truth: pyproject.toml

The version is automatically determined from the installed package metadata.
For development installations, it falls back to a dev version.

## Why This Design?

**Problem**: Maintaining version in multiple files leads to inconsistency.

**Solution**: Runtime reading from package metadata (single source of truth).

## Example

```python
from traceflux import __version__, __version_info__
print(__version__)        # "1.0.0" (installed) or "0.0.0-dev" (development)
print(__version_info__)   # (1, 0, 0) or (0, 0, 0)
```
"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("traceflux")
    # Parse version string to tuple (major, minor, patch)
    try:
        parts = __version__.split("-")[0].split(".")  # Remove pre-release suffix
        __version_info__ = tuple(int(p) for p in parts[:3])
    except (ValueError, IndexError):
        __version_info__ = (0, 0, 0)
except importlib.metadata.PackageNotFoundError:
    # Development mode: package not installed
    __version__ = "0.0.0-dev"
    __version_info__ = (0, 0, 0)
