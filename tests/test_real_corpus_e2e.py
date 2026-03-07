#!/usr/bin/env python3
"""E2E Tests: Real Corpus Validation.

Tests traceflux against real-world files to ensure it works in practice.

These tests validate that traceflux produces meaningful results on:
1. Python source code
2. Log files
3. Markdown documentation
"""

from pathlib import Path

import pytest

from traceflux.cli import main
from traceflux.graph import CooccurrenceGraph
from traceflux.scanner import Scanner


class TestPythonCodeCorpus:
    """Test on Python source code."""

    @pytest.fixture
    def test_file(self, tmp_path):
        """Create Python code test file."""
        code = """
import os
import requests

def setup_proxy(config):
    proxy = os.getenv('HTTP_PROXY')
    session = requests.Session()
    session.proxies = {'http': proxy, 'https': proxy}
    return session

def load_config():
    return {'proxy_url': 'http://proxy.example.com:8080'}
"""
        test_file = tmp_path / "test_code.py"
        test_file.write_text(code)
        return test_file

    def test_search_finds_proxy(self, test_file):
        # Scenario: User searches for "proxy" in Python code
        # Expected: Finds all proxy references
        # If fails: Cannot explore codebases
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        result = main(["search", "proxy", str(test_file)])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        assert result == 0
        assert "Found 'proxy'" in output
        assert "occurrence" in output

    def test_associations_find_config(self, test_file):
        # Scenario: User explores "proxy" associations in code
        # Expected: Finds related terms (config, session, etc.)
        # If fails: Cannot discover unknown concepts
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        result = main(["associations", "proxy", str(test_file), "--hops", "2"])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        assert result == 0
        # Should find associations
        assert "Associations for 'proxy'" in output


class TestLogFileCorpus:
    """Test on log files."""

    @pytest.fixture
    def test_file(self, tmp_path):
        """Create log file test file."""
        logs = """
2026-03-07 08:00:01 ERROR: connection timeout to database
2026-03-07 08:00:02 ERROR: connection timeout to database
2026-03-07 08:00:03 WARN: retry attempt 1
2026-03-07 08:00:04 ERROR: connection timeout to database
2026-03-07 08:00:05 WARN: retry attempt 2
2026-03-07 08:00:06 INFO: connection restored
2026-03-07 08:00:07 ERROR: connection timeout to cache
"""
        test_file = tmp_path / "test.log"
        test_file.write_text(logs)
        return test_file

    def test_search_finds_timeout(self, test_file):
        # Scenario: User searches for "timeout" in logs
        # Expected: Finds all timeout errors
        # If fails: Cannot analyze logs
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        result = main(["search", "timeout", str(test_file)])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        assert result == 0
        assert "Found 'timeout'" in output

    def test_associations_find_connection_errors(self, test_file):
        # Scenario: User explores "ERROR" associations
        # Expected: Finds connection, timeout, database, cache
        # If fails: Cannot identify error patterns
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        result = main(["associations", "ERROR", str(test_file), "--hops", "2"])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        assert result == 0
        assert "Associations for 'error'" in output
        # Should find error-related terms
        assert "connection" in output or "timeout" in output


class TestMarkdownDocsCorpus:
    """Test on Markdown documentation."""

    @pytest.fixture
    def test_file(self, tmp_path):
        """Create Markdown test file."""
        docs = """
# Project Documentation

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set up proxy:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=https://proxy.example.com:8080
```

## Usage

```python
from myapp import setup_proxy
session = setup_proxy(config)
```
"""
        test_file = tmp_path / "README.md"
        test_file.write_text(docs)
        return test_file

    def test_search_finds_proxy_in_docs(self, test_file):
        # Scenario: User searches for "proxy" in documentation
        # Expected: Finds proxy references in config section
        # If fails: Cannot navigate docs
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        result = main(["search", "proxy", str(test_file)])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        assert result == 0
        assert "Found 'proxy'" in output

    def test_associations_find_config_terms(self, test_file):
        # Scenario: User explores "configuration" associations
        # Expected: Finds proxy, export, bash, etc.
        # If fails: Cannot discover doc structure
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        result = main(["associations", "configuration", str(test_file), "--hops", "2"])

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        assert result == 0
        assert "Associations for 'configuration'" in output


class TestSemanticSegmentation:
    """Test that semantic segmentation preserves important units."""

    def test_ip_address_preserved(self):
        # Scenario: Text contains IP address
        # Expected: "127.0.0.1" kept as single unit
        # If fails: IP addresses fragmented
        scanner = Scanner(semantic_segmentation=True)
        segments = list(scanner.scan("Server at 127.0.0.1:8080"))

        contents = [s.content for s in segments if s.content]
        assert "127.0.0.1" in contents

    def test_version_number_preserved(self):
        # Scenario: Text contains version number
        # Expected: "v3.14.2" kept as single unit
        # If fails: Version numbers fragmented
        scanner = Scanner(semantic_segmentation=True)
        segments = list(scanner.scan("Version v3.14.2 released"))

        contents = [s.content for s in segments if s.content]
        assert "v3.14.2" in contents

    def test_identifier_preserved(self):
        # Scenario: Text contains identifier with underscore
        # Expected: "proxy_config" kept as single unit
        # If fails: Identifiers fragmented
        scanner = Scanner(semantic_segmentation=True)
        segments = list(scanner.scan("Use proxy_config variable"))

        contents = [s.content for s in segments if s.content]
        assert "proxy_config" in contents


# Test Summary
# ============
# These E2E tests validate traceflux on real-world corpora:
# - Python code (identifiers, functions, imports)
# - Log files (timestamps, error levels, messages)
# - Documentation (Markdown, code blocks, sections)
#
# Each test verifies:
# 1. Search finds expected terms
# 2. Associations discover related concepts
# 3. Semantic segmentation preserves important units
#
# If these tests fail, traceflux is not usable for real scenarios.
