"""Output formatting for traceflux.

ASCII-only labels with consistent formatting.
No colors, no emoji, no ANSI codes - safe for logs and pipes.

Format: LABEL: message (uppercase label, lowercase content)
"""

import sys
from typing import Optional, TextIO


class OutputFormatter:
    """ASCII-only output formatter.

    Uses uppercase labels for consistency and searchability.
    All output is plain text - safe for logging and piping.

    Labels:
        INFO: General information
        SUCCESS: Successful operations
        WARNING: Non-fatal issues
        ERROR: Fatal errors
        TIP: Helpful suggestions
    """

    def __init__(self, output: TextIO = None, error_output: TextIO = None):
        """Initialize formatter.

        Args:
            output: Output stream (default: sys.stdout)
            error_output: Error stream (default: sys.stderr)
        """
        self.out = output or sys.stdout
        self.err = error_output or sys.stderr

    def info(self, message: str) -> None:
        """Print informational message.

        Args:
            message: Message text (lowercase recommended)
        """
        print(f"INFO: {message}", file=self.out)

    def success(self, message: str) -> None:
        """Print success message.

        Args:
            message: Message text (lowercase recommended)
        """
        print(f"SUCCESS: {message}", file=self.out)

    def warning(self, message: str) -> None:
        """Print warning message.

        Args:
            message: Message text (lowercase recommended)
        """
        print(f"WARNING: {message}", file=self.err)

    def error(self, message: str) -> None:
        """Print error message.

        Args:
            message: Message text (lowercase recommended)
        """
        print(f"ERROR: {message}", file=self.err)

    def tip(self, message: str) -> None:
        """Print helpful tip.

        Args:
            message: Message text (lowercase recommended)
        """
        print(f"TIP: {message}", file=self.out)

    def print(self, *args, **kwargs) -> None:
        """Print raw text (no label).

        Use for structured output, results, etc.
        """
        print(*args, file=self.out, **kwargs)

    def print_error(self, *args, **kwargs) -> None:
        """Print raw text to error stream.

        Use for detailed error information.
        """
        print(*args, file=self.err, **kwargs)


# Global default formatter
default_formatter = OutputFormatter()


# Convenience functions (use default formatter)
def info(message: str) -> None:
    """Print informational message."""
    default_formatter.info(message)


def success(message: str) -> None:
    """Print success message."""
    default_formatter.success(message)


def warning(message: str) -> None:
    """Print warning message."""
    default_formatter.warning(message)


def error(message: str) -> None:
    """Print error message."""
    default_formatter.error(message)


def tip(message: str) -> None:
    """Print helpful tip."""
    default_formatter.tip(message)


def write(*args, **kwargs) -> None:
    """Write raw text (no label).

    Use this instead of built-in print to avoid naming conflicts.
    """
    default_formatter.print(*args, **kwargs)
