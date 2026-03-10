#!/usr/bin/env python3
# src/traceflux/cli/__main__.py
"""Allow running traceflux.cli as a module: python -m traceflux.cli"""

import sys

from traceflux.cli.main import main

if __name__ == "__main__":
    sys.exit(main())
