# traceflux Output Format

**Principle**: ASCII-only, log-friendly, pipe-safe output.

No colors, no emoji, no ANSI codes. All output is plain text suitable for logging and piping.

---

## Label Format

**Format**: `LABEL: message`

- **LABEL**: Uppercase English word
- **message**: Lowercase content (recommended)

### Standard Labels

| Label | Usage | Stream | Example |
|-------|-------|--------|---------|
| `INFO` | General information | stdout | `INFO: Indexing 5 document(s)` |
| `SUCCESS` | Successful operations | stdout | `SUCCESS: Found 'proxy' in 2 file(s)` |
| `WARNING` | Non-fatal issues | stderr | `WARNING: Could not read file.txt: Permission denied` |
| `ERROR` | Fatal errors | stderr | `ERROR: No documents found to search` |
| `TIP` | Helpful suggestions | stdout | `TIP: Use --json for machine-readable output` |

---

## Output Streams

### stdout (Standard Output)

- Search results
- Success messages
- Informational messages
- Tips
- JSON output

### stderr (Standard Error)

- Error messages
- Warning messages
- Debug information (verbose mode)

---

## Examples

### Search Command

```bash
$ traceflux search "proxy" src/

SUCCESS: Found 'proxy' in 2 file(s)

  src/config.py
    9 occurrence(s) at positions: [103, 131, 144, 180, 194, 266, 325, 411, 472]

  src/utils.py
    12 occurrence(s) at positions: [81, 109, 135, 159, 178, 193, 213, 303, 327, 430]...

Related terms:
  - config                    (strength: 0.320, degree 1)
  - session                   (strength: 0.318, degree 1)
```

### Associations Command

```bash
$ traceflux associations "proxy" src/ --hops 2

SUCCESS: Associations for 'proxy' (hops=2)

  - config                    (strength: 0.320, degree 1)
  - session                   (strength: 0.318, degree 1)
  - timeout                   (strength: 0.318, degree 1)
```

### Patterns Command

```bash
$ traceflux patterns src/ --limit 10

Top 10 patterns:

  def                              45 occurrence(s)
  return                           32 occurrence(s)
  import                           28 occurrence(s)
```

### Index Command (Verbose)

```bash
$ traceflux index src/ -v

INFO: Indexing 5 document(s)
INFO: Indexed src/config.py: 23 patterns
INFO: Indexed src/utils.py: 18 patterns
SUCCESS: Index saved to .traceflux_index.json
  Patterns: 156
  Documents: 5
  Total occurrences: 892
```

### Error Cases

```bash
$ traceflux search "xyz" /nonexistent/

ERROR: No documents found to search
```

```bash
$ traceflux associations "missing" src/

No associations found for 'missing'
```

```bash
$ traceflux search "test" /root/

WARNING: Could not read /root/secret.txt: Permission denied
SUCCESS: Found 'test' in 1 file(s)
...
```

---

## Machine-Readable Output

### JSON Format

All commands support `--json` flag for machine-readable output:

```bash
$ traceflux associations "proxy" src/ --json | jq '.associations[]'

{
  "term": "config",
  "strength": 0.320,
  "degree": 1,
  "pagerank": 0.156,
  "path": null
}
```

**JSON output is always plain ASCII** - safe for parsing and piping.

---

## Environment Variables

### NO_COLOR

Disable any future color support (currently no colors by default):

```bash
NO_COLOR=1 traceflux search "proxy" src/
```

### FORCE_COLOR

Force color output (if color support is added in future):

```bash
FORCE_COLOR=1 traceflux search "proxy" src/
```

---

## Design Rationale

### Why No Colors?

1. **Log-friendly** - No ANSI escape codes in logs
2. **Pipe-safe** - Clean output when piped to other tools
3. **Encoding-safe** - No UTF-8/ASCII compatibility issues
4. **Searchable** - Easy to grep for `ERROR:`, `WARNING:`, etc.
5. **Accessible** - Screen readers handle plain text better

### Why Uppercase Labels?

1. **Visibility** - Stands out in output
2. **Consistency** - All labels follow same format
3. **Searchability** - Easy to grep: `grep "ERROR:" logfile.txt`
4. **Convention** - Follows UNIX tool traditions (make, gcc, etc.)

### Why ASCII Only?

1. **Compatibility** - Works on all terminals and systems
2. **Encoding** - No UTF-8 issues in logs or pipes
3. **Simplicity** - No font or rendering dependencies
4. **Tradition** - UNIX tools use ASCII

---

## Migration Guide

### From Colored Output

If you're used to tools with colors (rg, grep --color):

```bash
# Old (colored):
# Found 'proxy' in 2 file(s)

# New (plain):
SUCCESS: Found 'proxy' in 2 file(s)
```

### From Emoji Output

If you're used to tools with emoji:

```bash
# Old (emoji):
# ✅ Found 'proxy' in 2 file(s)
# ⚠️  Could not read file.txt

# New (plain):
SUCCESS: Found 'proxy' in 2 file(s)
WARNING: Could not read file.txt
```

---

## Best Practices

### Parsing Output

**Use JSON for parsing**:

```bash
# Good: Parse JSON
traceflux associations "proxy" src/ --json | jq '.associations[].term'

# Bad: Parse human-readable output
traceflux associations "proxy" src/ | grep -oP '^\s+\K\S+'
```

### Filtering Output

**Grep for labels**:

```bash
# Find all errors
traceflux search "pattern" src/ 2>&1 | grep "^ERROR:"

# Find all warnings
traceflux index src/ -v 2>&1 | grep "^WARNING:"

# Find successful searches
traceflux search "pattern" src/ 2>&1 | grep "^SUCCESS:"
```

### Logging

**Redirect both streams**:

```bash
# Capture everything
traceflux search "pattern" src/ > output.log 2>&1

# Or separate
traceflux search "pattern" src/ > output.log 2> errors.log
```

---

## Related Documents

- `README.md` - Project overview
- `TESTING.md` - Testing philosophy
- `PHILOSOPHY.md` - Design principles

---

**Last Updated**: 2026-03-07  
**Status**: Implemented in v0.1.0
