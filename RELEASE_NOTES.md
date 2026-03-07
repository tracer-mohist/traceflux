# traceflux v1.0.0 - Initial Release

**Date**: 2026-03-07  
**GitHub**: [v1.0.0](https://github.com/tracer-mohist/traceflux/releases/tag/v1.0.0)

---

## 🎉 Welcome to traceflux!

traceflux is a lightweight text search engine with associative discovery.

Unlike traditional search (find what you know), traceflux helps you **discover what you don't know to search for**.

---

## ✨ Key Features

### 🔍 Pattern Search
Find repeated patterns in text files using LZ77-style pattern detection.

### 🔗 Associative Discovery
Multi-hop association traversal using PageRank and BFS on co-occurrence graphs.

### 📊 Semantic Segmentation
Preserves IP addresses, version numbers, and identifiers during tokenization.

### 🤖 UNIX Philosophy
- Simple, composable tools
- stdin/stdout support
- Pipe-friendly (`rg pattern | traceflux associations term -`)

---

## 📦 Installation

```bash
# Install via pipx (recommended)
pipx install git+https://github.com/tracer-mohist/traceflux.git@v1.0.0

# Verify installation
traceflux --version
# Output: traceflux 1.0.0
```

---

## 🚀 Quick Start

```bash
# Search for patterns
traceflux search "proxy" src/

# Find associations
traceflux associations "proxy" src/ --hops 2

# List patterns
traceflux patterns src/ --limit 20
```

---

## 📚 Documentation

- [README.md](https://github.com/tracer-mohist/traceflux/blob/main/README.md) - Installation and quick start
- [INSTALLATION.md](https://github.com/tracer-mohist/traceflux/blob/main/docs/INSTALLATION.md) - Detailed installation guide
- [CONTRIBUTING.md](https://github.com/tracer-mohist/traceflux/blob/main/CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](https://github.com/tracer-mohist/traceflux/blob/main/SECURITY.md) - Security policy

---

## 🔒 Security

No known security issues in this release.

Report vulnerabilities via [GitHub Security Advisories](https://github.com/tracer-mohist/traceflux/security/advisories/new).

---

## 📊 Statistics

- **Total Commits**: 35+
- **Lines of Code**: ~2,400
- **Documentation**: +1,100 lines
- **Test Coverage**: 92%+
- **Python Versions**: 3.10, 3.11, 3.12, 3.13

---

## 🙏 Acknowledgments

Built on the shoulders of giants:
- LZ77 compression algorithm
- PageRank algorithm (Google)
- Six Degrees of Separation theory
- UNIX philosophy

---

## 📝 License

MIT License - See [LICENSE](https://github.com/tracer-mohist/traceflux/blob/main/LICENSE) for details.

---

**Full Changelog**: [Initial release](https://github.com/tracer-mohist/traceflux/compare/0.1.0...v1.0.0)
