"""traceflux version information.

Single source of truth: pyproject.toml

The version is automatically determined from the installed package metadata.
For development installations, it falls back to a dev version.

## Why This Design?

**Problem**: Maintaining version in multiple files leads to inconsistency.

**Solution**: Runtime reading from package metadata (single source of truth).

## Example

```python
from traceflux import __version__
print(__version__)  # "1.0.0" (installed) or "0.0.0-dev" (development)
```
"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("traceflux")
except importlib.metadata.PackageNotFoundError:
    # Development mode: package not installed
    __version__ = "0.0.0-dev"
