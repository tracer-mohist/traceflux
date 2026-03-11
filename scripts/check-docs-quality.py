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
    .gitignore (required) - Project ignore patterns
    .docs-quality-config.yaml (optional) - Additional config
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

try:
    import pathspec

    PATHSPEC_AVAILABLE = True
except ImportError:
    PATHSPEC_AVAILABLE = False

# Configuration
MAX_LINES = 256
DEFAULT_LINE_WHITELIST = {"CHANGELOG.md", "CHANGELOG", "HISTORY.md"}


def load_gitignore_patterns() -> List[str]:
    """Load patterns from .gitignore file."""
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        print(
            "ERROR: .gitignore not found. This is not a normal project structure.",
            file=sys.stderr,
        )
        print(
            "Please create a .gitignore file or run from project root.",
            file=sys.stderr,
        )
        sys.exit(1)

    patterns = []
    with open(gitignore_path) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            patterns.append(line)

    return patterns


def load_config() -> dict:
    """Load configuration from .docs-quality-config.yaml if available."""
    config_path = Path(".docs-quality-config.yaml")
    line_whitelist = set(DEFAULT_LINE_WHITELIST)

    if config_path.exists() and YAML_AVAILABLE:
        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)
            line_whitelist = set(config.get("line_whitelist", DEFAULT_LINE_WHITELIST))
        except Exception:
            pass

    return {"line_whitelist": line_whitelist}


def is_emoji(code: int) -> bool:
    """Check if a character code is emoji."""
    EMOJI_RANGES = [
        (0x1F300, 0x1F5FF),
        (0x1F600, 0x1F64F),
        (0x1F680, 0x1F6FF),
        (0x2600, 0x26FF),
        (0x2700, 0x27BF),
        (0xFE00, 0xFE0F),
        (0x1F900, 0x1F9FF),
        (0x1F1E6, 0x1F1FF),
    ]
    return any(lo <= code <= hi for lo, hi in EMOJI_RANGES)


def collect_md_files(paths: List[str], gitignore_patterns: List[str]) -> List[Path]:
    """Collect markdown files from paths, respecting .gitignore."""
    files = []

    # Use pathspec if available, otherwise use simple pattern matching
    if PATHSPEC_AVAILABLE:
        spec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_patterns)
    else:
        spec = None

    for path in paths:
        p = Path(path)
        if not p.exists():
            continue

        if p.is_file() and p.suffix == ".md":
            if not is_ignored(str(p), spec, gitignore_patterns):
                files.append(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                f_str = str(f)
                if not is_ignored(f_str, spec, gitignore_patterns):
                    files.append(f)

    return files


def is_ignored(path: str, spec: Optional["pathspec.PathSpec"], patterns: List[str]) -> bool:
    """Check if a path should be ignored."""
    if spec is not None:
        return spec.match_file(path)

    # Fallback: simple pattern matching
    for pattern in patterns:
        # Convert gitignore pattern to regex
        regex = pattern.replace(".", r"\.").replace("*", ".*").replace("/", r"\/")
        if re.search(regex, path):
            return True
    return False


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
    """Check a line for ASCII and emoji violations per issue #40."""
    errors = []

    if in_code_block or in_blockquote:
        return errors

    i = 0
    in_inline = in_inline_code
    while i < len(line):
        ch = line[i]
        code = ord(ch)

        if ch == "`":
            backtick_count = 1
            j = i + 1
            while j < len(line) and line[j] == "`":
                backtick_count += 1
                j += 1
            if backtick_count % 2 == 1:
                in_inline = not in_inline
            i = j
            continue

        if in_inline:
            i += 1
            continue

        if 0x20 <= code <= 0x7E:
            i += 1
            continue

        if code in (9, 10, 13):
            i += 1
            continue

        if is_emoji(code):
            errors.append(f"{filepath}:{line_num}: Emoji not allowed (U+{code:04X})")
        else:
            errors.append(f"{filepath}:{line_num}: Non-ASCII character not allowed (U+{code:04X})")

        i += 1

    return errors


def check_markdown_emphasis(
    line: str, filepath: Path, line_num: int, in_code_block: bool
) -> Optional[str]:
    """Check for markdown emphasis syntax (**text**) - suggest LABEL: content."""
    if in_code_block:
        return None

    if line.strip().startswith(">"):
        return None

    if re.search(r"(?<!\*)\*\*[^*]+\*\*(?!\*)", line):
        stripped = line.strip()
        if not (stripped.startswith("** ") and len(stripped) <= 4):
            return f"{filepath}:{line_num}: Markdown emphasis (**) not allowed. Use 'LABEL: content' format instead"

    return None


def check_file(filepath: Path, line_whitelist: Set[str]) -> Tuple[List[str], List[str]]:
    """Check a single markdown file. Returns (errors, warnings)."""
    errors = []
    warnings = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{filepath}: Failed to read: {e}"]

    error = check_file_length(content, filepath, line_whitelist)
    if error:
        errors.append(error)

    lines = content.split("\n")
    in_code_block = False
    code_blocks_in_scope = 0

    for line_num, line in enumerate(lines, 1):
        if line.startswith("#"):
            code_blocks_in_scope = 0

        if line.strip().startswith("```"):
            if not in_code_block:
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

        in_inline_code = "`" in line
        in_blockquote = line.strip().startswith(">")

        line_errors = check_line_ascii_and_emoji(
            line, filepath, line_num, in_code_block, in_inline_code, in_blockquote
        )
        errors.extend(line_errors)

        emphasis_error = check_markdown_emphasis(line, filepath, line_num, in_code_block)
        if emphasis_error:
            errors.append(emphasis_error)

    return errors, warnings


def main(args: List[str]) -> int:
    """Main entry point."""
    config = load_config()
    line_whitelist = config["line_whitelist"]

    gitignore_patterns = load_gitignore_patterns()

    if args:
        files = [Path(f) for f in args if f.endswith(".md")]
    else:
        files = collect_md_files(["."], gitignore_patterns)

    if not files:
        print("No markdown files to check.")
        return 0

    all_errors = []
    all_warnings = []
    for filepath in sorted(files):
        errors, warnings = check_file(filepath, line_whitelist)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    for error in all_errors:
        print(error, file=sys.stderr)

    for warning in all_warnings:
        print(warning, file=sys.stderr)

    print(f"Checked {len(files)} files: {len(all_errors)} error(s), {len(all_warnings)} warning(s)")

    return 1 if len(all_errors) > 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
