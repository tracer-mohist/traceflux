# traceflux Installation Guide

LAST UPDATED: 2026-03-07
VERSION: v1.0 (Ready)

---

## Quick Start

RECOMMENDED: Install via pipx from GitHub

```bash
pipx install git+https://github.com/tracer-mohist/traceflux.git
traceflux --help
```text

---

## Installation Methods

### Method 1: pipx from GitHub (Recommended)

BEST FOR: Most users, simple installation, automatic updates

```bash
# Install latest development version
pipx install git+https://github.com/tracer-mohist/traceflux.git

# Install specific version (tag)
pipx install git+https://github.com/tracer-mohist/traceflux.git@v1.0.0

# Install specific branch
pipx install git+https://github.com/tracer-mohist/traceflux.git@main

# Verify installation
traceflux --help
traceflux search "pattern" .
```text

PROS:
-  No PyPI registration required
-  Instant access to latest features
-  Easy to update (`pipx upgrade traceflux`)
-  Isolated environment (no dependency conflicts)
-  No sudo required

CONS:
-  Installation command is longer
-  Requires git to be installed

REQUIREMENTS:
- Python 3.10+
- pipx (`pip install pipx` or `pipx install pipx`)
- git

---

### Method 2: pip from GitHub

BEST FOR: System-wide installation, custom environments

```bash
# Install to current Python environment
pip install git+https://github.com/tracer-mohist/traceflux.git

# Install with specific Python version
python3.11 -m pip install git+https://github.com/tracer-mohist/traceflux.git

# Install editable (for development)
pip install -e git+https://github.com/tracer-mohist/traceflux.git#egg=traceflux
```text

PROS:
-  Works with any Python environment
-  No additional tools needed (just pip)
-  Flexible installation options

CONS:
-  May conflict with system packages
-  Requires proper Python environment setup

---

### Method 3: Install from Source

BEST FOR: Developers, offline installation, customization

```bash
# Clone repository
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux

# Install with pip
pip install .

# Or install in development mode
pip install -e .

# Or use PDM (if available)
pipx install pdm
pdm install
```text

PROS:
-  Full control over installation
-  Can modify source code
-  Works offline after cloning

CONS:
-  Requires git clone
-  More steps than other methods

---

### Method 4: Run Directly (Development)

BEST FOR: Testing, development, no installation needed

```bash
# Clone repository
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux

# Run directly
python -m traceflux.cli --help

# Or activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
traceflux --help
```text

PROS:
-  No installation required
-  Quick testing
-  Easy debugging

CONS:
-  Need to specify full path or activate venv
-  Not convenient for regular use

---

## Platform-Specific Notes

### Linux

```bash
# Install pipx (if not installed)
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install traceflux
pipx install git+https://github.com/tracer-mohist/traceflux.git
```text

### macOS

```bash
# Install pipx via Homebrew
brew install pipx
pipx ensurepath

# Install traceflux
pipx install git+https://github.com/tracer-mohist/traceflux.git
```text

### Windows

```powershell
# Install pipx
python -m pip install --user pipx
python -m pipx ensurepath

# Restart terminal, then install traceflux
pipx install git+https://github.com/tracer-mohist/traceflux.git
```text

---

## Verification

After installation, verify it works:

```bash
# Check version
traceflux --version

# Show help
traceflux --help

# Test search
echo "hello world hello universe" > test.txt
traceflux search "hello" test.txt

# Test associations
traceflux associations "hello" test.txt --hops 1
```text

Expected output:
```bash
SUCCESS: Found 'hello' in 1 file(s)

  test.txt
    2 occurrence(s) at positions: [0, 12]
```text

---

## Updating

### Update pipx Installation

```bash
# Update to latest version
pipx upgrade traceflux

# Upgrade all pipx packages
pipx upgrade-all

# Reinstall (if upgrade fails)
pipx reinstall traceflux
```text

### Update Source Installation

```bash
# Navigate to source directory
cd /path/to/traceflux

# Pull latest changes
git pull origin main

# Reinstall
pip install -e . --upgrade
```text

---

## Uninstalling

### Uninstall pipx Installation

```bash
pipx uninstall traceflux
```text

### Uninstall pip Installation

```bash
pip uninstall traceflux
```text

### Manual Cleanup

```bash
# Remove source directory
rm -rf /path/to/traceflux

# Remove cache files
rm -rf ~/.cache/pip/wheels/traceflux*
```text

---

## Troubleshooting

### Issue: `pipx: command not found`

SOLUTION:
```bash
# Install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Restart terminal or reload shell
source ~/.bashrc  # or ~/.zshrc
```text

### Issue: `permission denied` during installation

SOLUTION:
- Don't use `sudo` with pipx
- Use `--user` flag with pip: `pip install --user ...`
- Use virtual environment

### Issue: Python version too old

SOLUTION:
traceflux requires Python 3.10+. Check version:
```bash
python --version
```text

If older than 3.10:
- Install newer Python (pyenv, deadsnakes PPA, etc.)
- Use specific Python: `pipx install --python python3.11 ...`

### Issue: Installation hangs or fails

SOLUTION:
```bash
# Try with verbose output
pipx install -v git+https://github.com/tracer-mohist/traceflux.git

# Clear pip cache
pip cache purge

# Try again
pipx install git+https://github.com/tracer-mohist/traceflux.git
```text

---

## Why GitHub Installation Instead of PyPI?

SHORT ANSWER: Simpler, faster, no extra authentication needed.

LONG ANSWER:

| Aspect | GitHub Installation | PyPI Publication |
|--------|--------------------|------------------|
| SETUP | None (just git) | PyPI account + API token |
| PUBLICATION | `git push` | Complex upload process |
| UPDATES | Instant | Requires PyPI upload |
| VERSION CONTROL | Tags/branches | Semantic versioning required |
| AUTHENTICATION | None (public repo) | API token management |
| BEST FOR | Early stage, personal projects | Mature projects, wide distribution |

CURRENT DECISION: GitHub installation is sufficient for traceflux v1.0.

FUTURE: May publish to PyPI if user base grows and demand increases.

---

## Related Documents

- `README.md` - Project overview and quick start
- `docs/OUTPUT-FORMAT.md` - Output format specification
- `docs/TESTING.md` - Testing philosophy and strategy
- `TESTING.md` - Quick testing reference

---

SUPPORT: Open an issue on [GitHub](https://github.com/tracer-mohist/traceflux/issues)

LICENSE: MIT
