#!/usr/bin/env python3
# scripts/check-code-quality.py
"""Code quality checker for traceflux.

Philosophy: Divide and Conquer

WHY 256 lines?
- 256 is 2^8 (computer-friendly number)
- ~6-10 screens of code (depending on editor)
- Beyond this, humans struggle to "see it all at once"

WHY enforce?
- Long files indicate design problems (complexity or coupling)
- Solution: refactor into modules/packages, not write long comments
- Unix philosophy: "If code is complex, refactor first, don't write long comments"

RULE:
- Max 256 lines per Python file
- If exceeded: split into submodules (file → directory/package)
- Whitelist: __init__.py (package navigation can be exceptions)

REFERENCE:
- Unix comment style: explain WHY, not WHAT
- Bertrand Meyer's Design by Contract: clear boundaries
- Divide and Conquer: complex tasks → mother task + subtasks

Usage:
    python scripts/check-code-quality.py <directory>
    python scripts/check-code-quality.py . --max-lines 256
"""

import sys
from pathlib import Path

# Configuration
MAX_LINES = 256
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", "node_modules", "dist", "build"}
EXCLUDE_FILES = {"__init__.py"}  # Package init files can be exceptions
EXCLUDE_PATTERNS = {"tests/*", "test_*"}  # Test files have different standards


def count_lines(file_path: Path) -> tuple[int, int, int]:
    """Count total, code, and blank lines."""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    total = len(lines)
    blank = sum(1 for line in lines if not line.strip())
    code = total - blank
    return total, code, blank


def check_file(file_path: Path, max_lines: int = MAX_LINES) -> tuple[bool, str]:
    """Check if file exceeds line limit."""
    if file_path.suffix != ".py":
        return True, "Not a Python file"

    if file_path.name in EXCLUDE_FILES:
        return True, f"Excluded: {file_path.name}"

    # Exclude test files (different standards for tests)
    if "tests/" in str(file_path) or file_path.name.startswith("test_"):
        return True, f"Excluded (test): {file_path.name}"

    total, code, blank = count_lines(file_path)

    if total > max_lines:
        rel_path = file_path.relative_to(file_path.parent.parent)
        return False, f"[FAIL] {rel_path}: {total} lines (max {max_lines}) — Consider splitting"

    return True, f"[OK] {file_path.name}: {total} lines"


def check_directory(root: Path, max_lines: int = MAX_LINES) -> tuple[list[str], list[str]]:
    """Check all Python files in directory."""
    passed = []
    failed = []

    for file_path in root.rglob("*.py"):
        if any(excl in file_path.parts for excl in EXCLUDE_DIRS):
            continue

        ok, message = check_file(file_path, max_lines)
        if ok:
            passed.append(message)
        else:
            failed.append(message)

    return passed, failed


def main():
    """Run code quality checks."""
    if len(sys.argv) < 2:
        # Default: check src/traceflux/ source directory only
        root = Path("src/traceflux")
        if not root.exists():
            print("Usage: check-code-quality.py [directory] [--max-lines N]")
            print("  Default: check src/traceflux/ directory")
            print("  Default max lines: 256")
            sys.exit(1)
    else:
        root = Path(sys.argv[1])
    max_lines = MAX_LINES

    if "--max-lines" in sys.argv:
        idx = sys.argv.index("--max-lines")
        if idx + 1 < len(sys.argv):
            max_lines = int(sys.argv[idx + 1])

    if not root.exists():
        print(f"Error: Directory not found: {root}")
        sys.exit(1)

    print(f"Checking Python files in {root}/")
    print(f"Max lines per file: {max_lines} (Divide and Conquer)")
    print("-" * 60)

    passed, failed = check_directory(root, max_lines)

    if passed:
        print("\nPassed files:")
        for msg in passed:
            print(f"  {msg}")

    if failed:
        print("\nFiles exceeding limit (refactor needed):")
        for msg in failed:
            print(f"  {msg}")

        print("\n" + "=" * 60)
        print("Refactoring suggestions (Divide and Conquer):")
        print("  1. Group related functions into submodules")
        print("  2. Move classes to separate files")
        print("  3. Extract constants to constants.py")
        print("  4. File → directory (becomes a package)")
        print("=" * 60)

    print(f"\nSummary: {len(passed)} passed, {len(failed)} failed")

    # Exit 0 (warning only) - technical debt tracked via issues
    # New files should not exceed limit, existing debt will be refactored
    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())
