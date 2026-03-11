#!/usr/bin/env python3
"""
Documentation Quality Checker for traceflux

Enforces documentation standards per issue #40:
- File length < 256 lines (whitelist: CHANGELOG.md)
- ASCII printable only (0x20-0x7E) with exemptions for quotes/code
- No emoji (except in quotes/code)
- Code blocks must have type
- One code block per heading scope (warning)

Usage:
    python scripts/check-docs-quality.py [files...]
    python scripts/check-docs-quality.py

Exit codes:
    0 - All checks passed
    1 - Errors found

Configuration:
    .docs-quality-config.yaml (optional)
"""

import re
import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Configuration
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

# ASCII printable range per issue #40
ASCII_MIN = 0x20
ASCII_MAX = 0x7E

# Emoji ranges to block (outside of quotes/code)
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
        return {
            "line_whitelist": DEFAULT_LINE_WHITELIST,
            "ignore_patterns": DEFAULT_IGNORE_PATTERNS,
        }


def is_emoji(code: int) -> bool:
    """Check if a character code is emoji."""
    return any(lo <= code <= hi for lo, hi in EMOJI_RANGES)


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
                f_normalized = f_str.replace("\\", "/")
                if not should_ignore(f_normalized, ignore_patterns):
                    files.append(f)
    return files


def check_file_length(content: str, filepath: Path, line_whitelist: Set[str]) -> Optional[str]:
    """Check if file exceeds maximum line count."""
    if filepath.name in line_whitelist:
        return None

    lines = content.split("\n")
    if len(lines) > MAX_LINES:
        return f"{filepath}:{len(lines)}: File exceeds {MAX_LINES} lines (found {len(lines)})"
    return None


def check_code_block_type(line: str) -> Optional[str]:
    """Check if opening code block has type annotation."""
    if line.strip().startswith("```"):
        code_type = line.strip()[3:].strip()
        if not code_type:
            return "Code block without type annotation"
    return None


def check_line_ascii_and_emoji(
    line: str,
    filepath: Path,
    line_num: int,
    in_code_block: bool,
    in_inline_code: bool,
    in_blockquote: bool,
) -> List[str]:
    """
    Check a line for ASCII and emoji violations per issue #40.

    Rules:
    - ASCII printable only (0x20-0x7E) in normal text
    - No emoji in normal text
    - Exemptions: blockquotes (>), code blocks (```), inline code (`)

    Returns list of error messages (empty if no errors)
    """
    errors = []

    # Exempt: inside code blocks or blockquotes
    if in_code_block or in_blockquote:
        return errors

    # Check each character
    i = 0
    in_inline = in_inline_code
    while i < len(line):
        ch = line[i]
        code = ord(ch)

        # Track inline code state
        if ch == "`":
            # Count backticks
            backtick_count = 1
            j = i + 1
            while j < len(line) and line[j] == "`":
                backtick_count += 1
                j += 1

            # Toggle inline code if odd number of backticks
            if backtick_count % 2 == 1:
                in_inline = not in_inline

            i = j
            continue

        # Skip if inside inline code
        if in_inline:
            i += 1
            continue

        # Check ASCII printable
        if ASCII_MIN <= code <= ASCII_MAX:
            i += 1
            continue

        # Common whitespace (tab, newline, CR)
        if code in (9, 10, 13):
            i += 1
            continue

        # Check if emoji
        if is_emoji(code):
            errors.append(f"{filepath}:{line_num}: Emoji not allowed (U+{code:04X})")
        else:
            # Non-ASCII, non-emoji character
            errors.append(f"{filepath}:{line_num}: Non-ASCII character not allowed (U+{code:04X})")

        i += 1

    return errors


def check_markdown_emphasis(
    line: str, filepath: Path, line_num: int, in_code_block: bool
) -> Optional[str]:
    """Check for markdown emphasis syntax (**text**) - suggest LABEL: content."""
    if in_code_block:
        return None

    # Skip blockquotes
    if line.strip().startswith(">"):
        return None

    # Check for **text** pattern
    if re.search(r"(?<!\*)\*\*[^*]+\*\*(?!\*)", line):
        stripped = line.strip()
        # Allow ** at start if it's a list marker or separator
        if not (stripped.startswith("** ") and len(stripped) <= 4):
            return f"{filepath}:{line_num}: Markdown emphasis (**) not allowed. Use 'LABEL: content' format instead"

    return None


def check_file(filepath: Path, line_whitelist: Set[str], ignore_patterns: List[str]) -> List[str]:
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

    # Check 2-5: Line-by-line checks
    lines = content.split("\n")
    in_code_block = False
    code_blocks_in_scope = 0

    for line_num, line in enumerate(lines, 1):
        # Track heading scope
        if line.startswith("#"):
            code_blocks_in_scope = 0

        # Track code blocks
        if line.strip().startswith("```"):
            if not in_code_block:
                # Opening code block - check for type
                type_error = check_code_block_type(line)
                if type_error:
                    errors.append(f"{filepath}:{line_num}: {type_error}")

                code_blocks_in_scope += 1
                if code_blocks_in_scope > 1:
                    warnings.append(
                        f"{filepath}:{line_num}: WARNING: Multiple code blocks under same heading"
                    )
            in_code_block = not in_code_block
            continue

        # Check inline code state
        in_inline_code = "`" in line

        # Check blockquote state
        in_blockquote = line.strip().startswith(">")

        # Check ASCII and emoji
        line_errors = check_line_ascii_and_emoji(
            line, filepath, line_num, in_code_block, in_inline_code, in_blockquote
        )
        errors.extend(line_errors)

        # Check markdown emphasis
        emphasis_error = check_markdown_emphasis(line, filepath, line_num, in_code_block)
        if emphasis_error:
            errors.append(emphasis_error)

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

    error_count = len([e for e in all_errors if "WARNING:" not in e])
    warning_count = len([e for e in all_errors if "WARNING:" in e])

    print(f"Checked {len(files)} files: {error_count} error(s), {warning_count} warning(s)")

    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
