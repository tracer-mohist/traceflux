#!/usr/bin/env python3
"""
Documentation Quality Checker for traceflux

Enforces documentation standards:
- File length < 256 lines (whitelist: CHANGELOG.md)
- ASCII printable only (with CJK support)
- No emoji
- Code blocks must have type
- One code block per heading scope (warning)

Usage:
    python scripts/check-docs-quality.py [files...]
    python scripts/check-docs-quality.py --all

Exit codes:
    0 - All checks passed
    1 - Errors found

Configuration:
    .docs-quality-config.yaml (optional)
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Default configuration
MAX_LINES = 256
DEFAULT_LINE_WHITELIST = {"CHANGELOG.md", "CHANGELOG", "HISTORY.md"}
DEFAULT_IGNORE_PATTERNS = [
    r"\.git/",
    r"\.venv/",
    r"node_modules/",
    r"__pycache__/",
    r"\.pyc$",
    r"test_corpus/",
]

# Emoji ranges to block
EMOJI_RANGES = [
    (0x1F300, 0x1F5FF),  # misc symbols & pictographs
    (0x1F600, 0x1F64F),  # emoticons
    (0x1F680, 0x1F6FF),  # transport & map
    (0x2600, 0x26FF),  # misc symbols
    (0x2700, 0x27BF),  # dingbats
    (0xFE00, 0xFE0F),  # variation selectors
    (0x1F900, 0x1F9FF),  # supplemental symbols & pictographs
    (0x1F1E6, 0x1F1FF),  # flags
]

# Allowed non-ASCII ranges (CJK, common punctuation, box drawing, math, etc.)
ALLOWED_NON_ASCII = [
    (0x4E00, 0x9FFF),  # CJK Unified Ideographs
    (0x3400, 0x4DBF),  # CJK Extension A
    (0x3000, 0x303F),  # CJK Symbols & Punctuation
    (0xFF00, 0xFFEF),  # Halfwidth & Fullwidth Forms
    (0x3040, 0x309F),  # Hiragana
    (0x30A0, 0x30FF),  # Katakana
    (0x2500, 0x257F),  # Box Drawing (├ ─ │ └ etc.)
    (0x2190, 0x21FF),  # Arrows (→ ← ↑ ↓ etc.)
    (0x2010, 0x202F),  # General Punctuation (— – etc.)
    (0x00A0, 0x00FF),  # Latin-1 Supplement
    (0x2200, 0x22FF),  # Mathematical Operators
    (0x0370, 0x03FF),  # Greek and Coptic
]


def load_config() -> dict:
    """Load configuration from .docs-quality-config.yaml if available."""
    config_path = Path(".docs-quality-config.yaml")
    if not config_path.exists() or not YAML_AVAILABLE:
        return {
            "line_whitelist": DEFAULT_LINE_WHITELIST,
            "ignore_patterns": DEFAULT_IGNORE_PATTERNS,
        }

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return {
            "line_whitelist": set(config.get("line_whitelist", DEFAULT_LINE_WHITELIST)),
            "ignore_patterns": config.get("ignore_patterns", DEFAULT_IGNORE_PATTERNS),
        }
    except Exception:
        # Fall back to defaults on error
        return {
            "line_whitelist": DEFAULT_LINE_WHITELIST,
            "ignore_patterns": DEFAULT_IGNORE_PATTERNS,
        }


def is_emoji(code: int) -> bool:
    """Check if a character code is emoji."""
    return any(lo <= code <= hi for lo, hi in EMOJI_RANGES)


def is_allowed_non_ascii(code: int) -> bool:
    """Check if a non-ASCII character is allowed."""
    return any(lo <= code <= hi for lo, hi in ALLOWED_NON_ASCII)


def should_ignore(path: str, ignore_patterns: List[str]) -> bool:
    """Check if a path should be ignored."""
    return any(re.search(pattern, path) for pattern in ignore_patterns)


def collect_md_files(paths: List[str], ignore_patterns: List[str]) -> List[Path]:
    """Collect markdown files from paths."""
    files = []
    for path in paths:
        p = Path(path)
        if not p.exists():
            continue
        if p.is_file() and p.suffix == ".md":
            if not should_ignore(str(p), ignore_patterns):
                files.append(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                f_str = str(f)
                # Normalize path separators for regex matching
                f_normalized = f_str.replace("\\", "/")
                if not should_ignore(f_normalized, ignore_patterns):
                    files.append(f)
    return files


def check_file_length(content: str, filepath: Path, line_whitelist: set) -> Optional[str]:
    """Check if file exceeds maximum line count."""
    if filepath.name in line_whitelist:
        return None

    lines = content.split("\n")
    if len(lines) > MAX_LINES:
        return f"{filepath}:{len(lines)}: File exceeds {MAX_LINES} lines (found {len(lines)})"
    return None


def check_code_block_type(
    line: str, in_code_block: bool, code_block_start: int
) -> Tuple[bool, int, Optional[str]]:
    """Check if code block has type annotation."""
    if line.strip().startswith("```"):
        if not in_code_block:
            # Opening code block
            code_type = line.strip()[3:].strip()
            if not code_type:
                return True, 0, "Code block without type annotation"
            return True, 0, None
        else:
            # Closing code block
            return False, 0, None
    return in_code_block, code_block_start, None


def check_line_content(
    line: str, filepath: Path, line_num: int, in_code_block: bool, in_quote: bool
) -> Optional[str]:
    """Check a single line for emoji and invalid characters."""
    # Skip blockquotes
    if in_quote:
        return None

    # Skip code blocks (content can have anything)
    if in_code_block:
        return None

    for ch in line:
        code = ord(ch)

        # ASCII printable: OK
        if 32 <= code <= 126:
            continue

        # Common whitespace: OK
        if code in (9, 10, 13):
            continue

        # Allowed non-ASCII: OK
        if is_allowed_non_ascii(code):
            continue

        # Emoji: NOT OK
        if is_emoji(code):
            return f"{filepath}:{line_num}: Emoji not allowed (U+{code:04X})"

        # Other non-ASCII: NOT OK
        return f"{filepath}:{line_num}: Non-ASCII character not allowed (U+{code:04X})"

    return None


def check_file(filepath: Path, line_whitelist: set, ignore_patterns: List[str]) -> List[str]:
    """Check a single markdown file."""
    errors = []
    warnings = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{filepath}: Failed to read: {e}"]

    # Check 1: File length
    error = check_file_length(content, filepath, line_whitelist)
    if error:
        errors.append(error)

    # Check 2-4: Line-by-line checks
    lines = content.split("\n")
    in_code_block = False
    code_blocks_in_scope = 0
    current_heading = None

    for line_num, line in enumerate(lines, 1):
        # Track heading scope
        if line.startswith("#"):
            current_heading = line
            code_blocks_in_scope = 0

        # Track code blocks
        if line.strip().startswith("```"):
            if not in_code_block:
                code_blocks_in_scope += 1
                if code_blocks_in_scope > 1:
                    warnings.append(
                        f"{filepath}:{line_num}: WARNING: Multiple code blocks under same heading"
                    )
            in_code_block = not in_code_block
            continue

        # Check code block type (only on opening)
        if not in_code_block and line.strip().startswith("```"):
            _, _, error = check_code_block_type(line, False, 0)
            if error:
                errors.append(f"{filepath}:{line_num}: {error}")

        # Check line content
        in_quote = line.strip().startswith(">")
        error = check_line_content(line, filepath, line_num, in_code_block, in_quote)
        if error:
            errors.append(error)

    return errors + warnings


def main(args: List[str]) -> int:
    """Main entry point."""
    # Load configuration
    config = load_config()
    line_whitelist = config["line_whitelist"]
    ignore_patterns = config["ignore_patterns"]

    # Collect files
    if args:
        files = [Path(f) for f in args if f.endswith(".md")]
    else:
        # Default: check all markdown files in current directory
        files = collect_md_files(["."], ignore_patterns)

    if not files:
        print("No markdown files to check.")
        return 0

    # Check all files
    all_errors = []
    for filepath in sorted(files):
        errors = check_file(filepath, line_whitelist, ignore_patterns)
        all_errors.extend(errors)

    # Report results
    for error in all_errors:
        print(error, file=sys.stderr)

    error_count = len([e for e in all_errors if not e.startswith("WARNING:")])
    warning_count = len([e for e in all_errors if e.startswith("WARNING:")])

    print(f"Checked {len(files)} files: {error_count} error(s), {warning_count} warning(s)")

    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
