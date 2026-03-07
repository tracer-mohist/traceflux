# traceflux Documentation Index

**Purpose**: Navigate traceflux documentation.

**Last Updated**: 2026-03-07  
**Version**: v1.0.0

---

## 📖 Quick Navigation

### For Users

1. **[README.md](../README.md)** - Start here!
   - What is traceflux?
   - Installation (pipx recommended)
   - Quick start guide
   - Basic usage examples

2. **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation
   - 4 installation methods
   - Platform-specific notes (Linux, macOS, Windows)
   - Troubleshooting

3. **[OUTPUT-FORMAT.md](OUTPUT-FORMAT.md)** - Output format reference
   - ASCII-only labels (INFO, SUCCESS, WARNING, ERROR)
   - Stream separation (stdout/stderr)
   - Machine-readable JSON output

### For Contributors

1. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to contribute
   - Development setup
   - Code style guidelines
   - PR process
   - Issue reporting

2. **[CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)** - Community guidelines
   - Our pledge (inclusive community)
   - Enforcement guidelines

3. **[SECURITY.md](../SECURITY.md)** - Security policy
   - Reporting vulnerabilities
   - Security best practices

### For Developers

1. **[PHILOSOPHY.md](PHILOSOPHY.md)** - Design philosophy
   - Core insight (associative discovery)
   - UNIX philosophy
   - Technical architecture

2. **[IMPLEMENTATION-DESIGN.md](IMPLEMENTATION-DESIGN.md)** - Implementation details
   - Algorithm design
   - Data structures
   - Performance considerations

3. **[TESTING.md](TESTING.md)** - Testing strategy
   - Limited testing principles
   - Test categories
   - Running tests

### For Researchers

1. **[PROJECT-STATUS.md](PROJECT-STATUS.md)** - Project status report
   - Current phase
   - Completed milestones
   - Future directions

2. **[TASKS.md](../TASKS.md)** - Development tasks
   - Completed phases (5 & 6)
   - Future backlog

3. **research/** - Research notes
   - Foundations (algorithms, math)
   - Associations (six degrees theory)
   - Philosophy (design decisions)

---

## 📊 Documentation Statistics

| Category | Files | Lines | Purpose |
|----------|-------|-------|---------|
| **User Docs** | 3 | ~1,000 | Installation, usage, output |
| **Contributor Docs** | 3 | ~800 | Contributing, security, conduct |
| **Developer Docs** | 3 | ~1,000 | Philosophy, implementation, testing |
| **Research Docs** | 15+ | ~2,000+ | Theoretical foundations |
| **Total** | 24+ | ~4,800+ | Complete documentation |

---

## 🗂️ File Structure

```
traceflux/
├── README.md                    # Main documentation (start here)
├── INSTALLATION.md              # Installation guide
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md           # Community guidelines
├── SECURITY.md                  # Security policy
├── TESTING.md                   # Testing strategy
├── TASKS.md                     # Development tasks
├── RELEASE_NOTES.md             # v1.0.0 release notes
├── RELEASE_ANNOUNCEMENT.md      # Public release announcement
│
├── docs/
│   ├── PHILOSOPHY.md            # Design philosophy
│   ├── IMPLEMENTATION-DESIGN.md # Implementation details
│   ├── OUTPUT-FORMAT.md         # Output format reference
│   ├── PROJECT-STATUS.md        # Project status report
│   ├── TESTING.md               # Testing strategy (detailed)
│   └── INSTALLATION.md          # Installation guide (detailed)
│
├── design/
│   ├── README.md                # Design documents index
│   └── 00-search-flowchart.md   # Search process flowchart
│
├── research/
│   ├── README.md                # Research notes index
│   ├── 01-foundations/          # Algorithm foundations
│   ├── 02-associations/         # Association theory
│   └── 03-philosophy/           # Design philosophy
│
├── examples/
│   └── README.md                # Usage examples
│
└── test_corpus/
    └── README.md                # Test data documentation
```

---

## 🎯 Documentation Goals

### Principles

1. **Clarity Over Completeness**
   - Clear, concise explanations
   - Examples over abstract descriptions
   - Progressive disclosure (simple → complex)

2. **Multiple Audiences**
   - Users: How to install and use
   - Contributors: How to help
   - Developers: How it works
   - Researchers: Why it works this way

3. **Living Documentation**
   - Updated with each release
   - Reflects current state
   - Honest about limitations

### Quality Standards

- ✅ ASCII-only (encoding-safe)
- ✅ Lists over tables (readability)
- ✅ Examples for all APIs
- ✅ Cross-references where helpful
- ✅ Search-friendly headings

---

## 📝 Document Types

### User-Facing

- **README.md**: First impression, quick start
- **INSTALLATION.md**: Step-by-step installation
- **OUTPUT-FORMAT.md**: What to expect from commands

### Community-Facing

- **CONTRIBUTING.md**: How to help
- **CODE_OF_CONDUCT.md**: How we treat each other
- **SECURITY.md**: How to report issues safely

### Technical

- **PHILOSOPHY.md**: Why we built it this way
- **IMPLEMENTATION-DESIGN.md**: How it works
- **TESTING.md**: How we ensure quality

### Meta

- **PROJECT-STATUS.md**: Where we are
- **TASKS.md**: What we're working on
- **RELEASE_NOTES.md**: What changed

---

## 🔗 External Links

- **GitHub Repository**: https://github.com/tracer-mohist/traceflux
- **Issues**: https://github.com/tracer-mohist/traceflux/issues
- **Releases**: https://github.com/tracer-mohist/traceflux/releases
- **v1.0.0 Release**: https://github.com/tracer-mohist/traceflux/releases/tag/v1.0.0

---

## 📞 Getting Help

**Need help?**

1. Check [README.md](../README.md) for quick start
2. Check [INSTALLATION.md](INSTALLATION.md) for installation issues
3. Search [existing issues](https://github.com/tracer-mohist/traceflux/issues)
4. Open a [new issue](https://github.com/tracer-mohist/traceflux/issues/new)

**Want to help?**

1. Read [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Pick an issue or report a bug
3. Submit a PR!

---

**Documentation is a letter to future users and contributors.**

*— traceflux team*
