#!/usr/bin/env python3
# scripts/check-headers.py
# Automate relative path header insertion for traceflux project
# NOTE: Inspired by check-headers.mjs, adapted for Python ecosystem

import os
import sys
from pathlib import Path
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

ROOT = Path(__file__).resolve().parent.parent

IGNORE_LIST = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "generated",
    ".next",
    ".DS_Store",
    "__pycache__",
    ".venv",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    # traceflux specific
    "test_corpus",
    "drafts",
    "design",
    "research",
}

# Extension to Comment Style Mapping
RULES = {
    "//": ["js", "ts", "jsx", "tsx", "mjs", "cjs", "mts", "cts", "java", "go"],
    "#": ["py", "sh", "bash", "yaml", "yml", "dockerfile", "toml", "ini", "cfg"],
    "--": ["sql", "lua", "vhdl"],
    "/*": ["css", "scss", "less", "rs"],
    "<!--": ["html", "xml", "vue", "svg", "md"],
}

# =============================================================================
# LOGGING (LogLight Style)
# =============================================================================

class Log:
    """Simple logging utility with LogLight-style output."""

    @staticmethod
    def _timestamp():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def sect(msg):
        print(f"\n{Log._timestamp()}  {msg}")

    @staticmethod
    def step(msg):
        print(f"\n{Log._timestamp()}  → {msg}")

    @staticmethod
    def work(msg):
        print(f"{Log._timestamp()}    • {msg}")

    @staticmethod
    def find(msg):
        print(f"{Log._timestamp()}    ✓ {msg}")

    @staticmethod
    def fail(msg):
        print(f"{Log._timestamp()}    ✗ {msg}")

    @staticmethod
    def warn(msg):
        print(f"{Log._timestamp()}    ⚠ {msg}")

    @staticmethod
    def end(msg):
        print(f"\n{Log._timestamp()}  {msg}\n")


log = Log()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_style(file_path):
    """Get comment style for file extension."""
    ext = file_path.suffix.lower().lstrip(".")
    for token, exts in RULES.items():
        if ext in exts:
            end = ""
            if token == "/*":
                end = " */"
            elif token == "<!--":
                end = " -->"
            return {"start": token + " ", "end": end}
    return None


def make_header(file_path, style):
    """Create header comment with relative path."""
    rel_path = file_path.relative_to(ROOT).as_posix()
    return f"{style['start']}{rel_path}{style['end']}"


def get_insert_line(lines, header, style):
    """Determine where to insert header."""
    # Check if header already exists
    if lines and lines[0].strip() == header.strip():
        return -1

    # Check for shebang or XML declaration
    if lines:
        first = lines[0]
        if first.startswith("#!") or first.startswith("<?xml"):
            if len(lines) > 1 and lines[1].strip() == header.strip():
                return -1
            return 1

    return 0


def is_existing_header(line, style):
    """Check if line is an existing file path header."""
    if not line:
        return False

    trimmed = line.strip()
    if not trimmed.startswith(style["start"]):
        return False

    if not trimmed.endswith(style["end"]):
        return False

    # Extract content between comment markers
    content = trimmed[len(style["start"]) : len(trimmed) - len(style["end"])].strip()

    # Check if it looks like a file path (contains /)
    return "/" in content


# =============================================================================
# CORE LOGIC
# =============================================================================


def scan_directory(dir_path):
    """Recursively scan directory for supported files."""
    files = []

    for entry in os.scandir(dir_path):
        if entry.name in IGNORE_LIST:
            continue

        if entry.is_dir():
            files.extend(scan_directory(entry.path))
        elif entry.is_file():
            file_path = Path(entry.path)
            if get_style(file_path):
                files.append(file_path)

    return files


def process_file(file_path):
    """Add or fix header for a single file."""
    try:
        style = get_style(file_path)
        if not style:
            return "skipped"

        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read()

        lines = raw.split("\n")
        header = make_header(file_path, style)

        insert_idx = get_insert_line(lines, header, style)

        if insert_idx == -1:
            return "skipped"

        # Check if we should replace or insert
        if insert_idx < len(lines) and is_existing_header(lines[insert_idx], style):
            # Replace existing header
            lines[insert_idx] = header
        else:
            # Insert new header
            lines.insert(insert_idx, header)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return "added"

    except Exception as e:
        log.fail(f"Error processing {file_path}: {e}")
        return "error"


# =============================================================================
# MAIN EXECUTION
# =============================================================================


def main():
    """Main entry point."""
    start_time = datetime.now()

    log.sect("Check Headers")

    # Determine targets
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["."]

    # Phase 1: Collect files
    log.step("Collect files")
    file_set = set()

    for target in targets:
        target_path = Path(target).resolve()
        log.work(f"Processing target: {target}")

        if not target_path.exists():
            log.fail(f"Invalid target: {target}")
            continue

        if target_path.is_file():
            if get_style(target_path):
                file_set.add(target_path)
        else:
            scanned = scan_directory(target_path)
            file_set.update(scanned)

    files = sorted(file_set)
    log.find(f"Found {len(files)} supported files")

    if not files:
        log.end("Check Headers")
        return

    # Phase 2: Process files
    log.step("Apply file headers")

    stats = {"added": 0, "skipped": 0, "error": 0}

    for file_path in files:
        result = process_file(file_path)
        stats[result] += 1

        if result == "added":
            rel_path = file_path.relative_to(ROOT)
            log.find(f"Added: {rel_path}")
        elif result == "error":
            rel_path = file_path.relative_to(ROOT)
            log.fail(f"Failed: {rel_path}")

    # Phase 3: Summary
    log.step("Process summary")

    if stats["added"] > 0:
        log.find(f"Modified {stats['added']} files")
    if stats["skipped"] > 0:
        log.warn(f"Skipped {stats['skipped']} files (already valid)")
    if stats["error"] > 0:
        log.fail(f"Failed {stats['error']} files")

    elapsed = (datetime.now() - start_time).total_seconds()
    log.work(f"Time taken: {elapsed:.2f}s")

    log.end("Check Headers")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(1)
    except Exception as e:
        log.fail(f"Unexpected error: {e}")
        sys.exit(1)
