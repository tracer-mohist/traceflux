<!-- docs/INSTALLATION.md -->
# traceflux Installation Guide

**Last Updated**: 2026-03-07  
**Version**: v1.0 (Ready)

---

## Quick Start

**Recommended**: Install via pipx from GitHub

```bash
pipx install git+https://github.com/tracer-mohist/traceflux.git
traceflux --help
```

---

## Installation Methods

### Method 1: pipx from GitHub (Recommended)

**Best for**: Most users, simple installation, automatic updates

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
```

**Pros**:
- ✅ No PyPI registration required
- ✅ Instant access to latest features
- ✅ Easy to update (`pipx upgrade traceflux`)
- ✅ Isolated environment (no dependency conflicts)
- ✅ No sudo required

**Cons**:
- ⚠️ Installation command is longer
- ⚠️ Requires git to be installed

**Requirements**:
- Python 3.10+
- pipx (`pip install pipx` or `pipx install pipx`)
- git

---

### Method 2: pip from GitHub

**Best for**: System-wide installation, custom environments

```bash
# Install to current Python environment
pip install git+https://github.com/tracer-mohist/traceflux.git

# Install with specific Python version
python3.11 -m pip install git+https://github.com/tracer-mohist/traceflux.git

# Install editable (for development)
pip install -e git+https://github.com/tracer-mohist/traceflux.git#egg=traceflux
```

**Pros**:
- ✅ Works with any Python environment
- ✅ No additional tools needed (just pip)
- ✅ Flexible installation options

**Cons**:
- ⚠️ May conflict with system packages
- ⚠️ Requires proper Python environment setup

---

### Method 3: Install from Source

**Best for**: Developers, offline installation, customization

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
```

**Pros**:
- ✅ Full control over installation
- ✅ Can modify source code
- ✅ Works offline after cloning

**Cons**:
- ⚠️ Requires git clone
- ⚠️ More steps than other methods

---

### Method 4: Run Directly (Development)

**Best for**: Testing, development, no installation needed

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
```

**Pros**:
- ✅ No installation required
- ✅ Quick testing
- ✅ Easy debugging

**Cons**:
- ⚠️ Need to specify full path or activate venv
- ⚠️ Not convenient for regular use

---

## Platform-Specific Notes

### Linux

```bash
# Install pipx (if not installed)
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install traceflux
pipx install git+https://github.com/tracer-mohist/traceflux.git
```

### macOS

```bash
# Install pipx via Homebrew
brew install pipx
pipx ensurepath

# Install traceflux
pipx install git+https://github.com/tracer-mohist/traceflux.git
```

### Windows

```powershell
# Install pipx
python -m pip install --user pipx
python -m pipx ensurepath

# Restart terminal, then install traceflux
pipx install git+https://github.com/tracer-mohist/traceflux.git
```

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
```

Expected output:
```
SUCCESS: Found 'hello' in 1 file(s)

  test.txt
    2 occurrence(s) at positions: [0, 12]
```

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
```

### Update Source Installation

```bash
# Navigate to source directory
cd /path/to/traceflux

# Pull latest changes
git pull origin main

# Reinstall
pip install -e . --upgrade
```

---

## Uninstalling

### Uninstall pipx Installation

```bash
pipx uninstall traceflux
```

### Uninstall pip Installation

```bash
pip uninstall traceflux
```

### Manual Cleanup

```bash
# Remove source directory
rm -rf /path/to/traceflux

# Remove cache files
rm -rf ~/.cache/pip/wheels/traceflux*
```

---

## Troubleshooting

### Issue: `pipx: command not found`

**Solution**:
```bash
# Install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Restart terminal or reload shell
source ~/.bashrc  # or ~/.zshrc
```

### Issue: `permission denied` during installation

**Solution**:
- Don't use `sudo` with pipx
- Use `--user` flag with pip: `pip install --user ...`
- Use virtual environment

### Issue: Python version too old

**Solution**:
traceflux requires Python 3.10+. Check version:
```bash
python --version
```

If older than 3.10:
- Install newer Python (pyenv, deadsnakes PPA, etc.)
- Use specific Python: `pipx install --python python3.11 ...`

### Issue: Installation hangs or fails

**Solution**:
```bash
# Try with verbose output
pipx install -v git+https://github.com/tracer-mohist/traceflux.git

# Clear pip cache
pip cache purge

# Try again
pipx install git+https://github.com/tracer-mohist/traceflux.git
```

---

## Why GitHub Installation Instead of PyPI?

**Short answer**: Simpler, faster, no extra authentication needed.

**Long answer**:

| Aspect | GitHub Installation | PyPI Publication |
|--------|--------------------|------------------|
| **Setup** | None (just git) | PyPI account + API token |
| **Publication** | `git push` | Complex upload process |
| **Updates** | Instant | Requires PyPI upload |
| **Version Control** | Tags/branches | Semantic versioning required |
| **Authentication** | None (public repo) | API token management |
| **Best For** | Early stage, personal projects | Mature projects, wide distribution |

**Current Decision**: GitHub installation is sufficient for traceflux v1.0.

**Future**: May publish to PyPI if user base grows and demand increases.

---

## Related Documents

- `README.md` - Project overview and quick start
- `docs/OUTPUT-FORMAT.md` - Output format specification
- `docs/TESTING.md` - Testing philosophy and strategy
- `TESTING.md` - Quick testing reference

---

**Support**: Open an issue on [GitHub](https://github.com/tracer-mohist/traceflux/issues)

**License**: MIT
