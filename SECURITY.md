# Security Policy

Effective Date: 2026-03-07
Version: 1.0

---

## Reporting a Vulnerability

We take security seriously.

If you discover a security vulnerability in traceflux, please report it responsibly.

### How to Report

Preferred Method: Open a private security advisory on GitHub

1. Go to Security tab (https://github.com/tracer-mohist/traceflux/security)
2. Click "Report a vulnerability"
3. Provide details about the vulnerability
4. We will respond within 7 days

Alternative: If GitHub security advisories unavailable, open a regular issue and mark it as security-related: [SECURITY] Description

### What to Include

- Description: Clear description of the vulnerability
- Impact: What an attacker could achieve
- Reproduction: Steps to reproduce
- Environment: Python version, OS, traceflux version
- Suggestions: Any ideas for fixing (optional)

### Response Timeline

- Acknowledgment: Within 7 days
- Initial Assessment: Within 14 days
- Fix Timeline: Depends on severity

### Severity Levels

| Severity | Response Time | Example |
|----------|---------------|---------|
| Critical | 24-48 hours | Remote code execution, data theft |
| High | 7 days | Privilege escalation, DoS |
| Medium | 14 days | Information disclosure |
| Low | 30 days | Minor security improvements |

---

## Security Best Practices

### For Users

Installation:
```bash
# Recommended: Install via pipx (isolated environment)
pipx install git+https://github.com/tracer-mohist/traceflux.git

# Verify installation
traceflux --version
```

Usage:
- Run traceflux in isolated environments when processing untrusted input
- Review files before processing (traceflux reads files)
- Keep traceflux updated (pipx upgrade traceflux)
- Don't run traceflux on files with unknown permissions
- Don't pipe untrusted input without review

Data Privacy:
- traceflux processes files locally (no network calls)
- No telemetry, no analytics, no data collection
- Your data stays on your machine

### For Contributors

Code Security:
- Sanitize all user input
- Validate file paths (prevent path traversal)
- Handle errors gracefully (no stack traces)
- Use secure defaults
- No hardcoded credentials or API keys
- No external network calls without explicit user action

Git Security:
- Use GitHub noreply email for commits
  ```bash
  git config user.email "YOUR_ID+username@users.noreply.github.com"
  ```
- Sign commits (recommended)
  ```bash
  git commit -S -m "Your message"
  ```
- Don't commit sensitive data (passwords, tokens, personal info)
- Don't commit large binary files (potential DoS)

Dependency Security:
- Keep dependencies minimal (traceflux has zero dependencies)
- Review dependency updates before accepting
- Use pinned versions in development
- Don't add dependencies without security review

---

## Security Architecture

### Design Principles

1. Minimal Attack Surface
   - Zero external dependencies
   - No network calls
   - Local file processing only

2. Defense in Depth
   - Input validation
   - Error handling
   - Graceful degradation

3. Fail Securely
   - Errors don't expose sensitive information
   - No stack traces in normal output
   - Clear error messages without internals

4. Privacy by Design
   - No data collection
   - No telemetry
   - Local processing only

### Threat Model

Protected against:
- Malicious input (handled gracefully)
- Path traversal attempts (validated)
- DoS via large files (streaming processing)
- Dependency vulnerabilities (zero dependencies)

Not protected against:
- Physical access to your machine
- Compromised Python installation
- OS-level vulnerabilities
- Social engineering

---

## Security Updates

### How We Handle Security Issues

1. Private Discussion: Reporter and maintainers discuss privately
2. Fix Development: Fix developed in private branch
3. Testing: Fix tested thoroughly
4. Release: Security release published
5. Disclosure: Public announcement (after users have time to update)

### Release Strategy

- Security patches: Released as patch versions (1.0.0 -> 1.0.1)
- Notification: GitHub release notes, issue comments
- Urgency: Based on severity (see table above)

### Staying Updated

Watch for security updates:
- GitHub release notifications
- pipx upgrade traceflux regularly
- Monitor Security Advisories (https://github.com/tracer-mohist/traceflux/security/advisories)

---

## Known Security Limitations

### Current Limitations

1. File Reading: traceflux reads files provided by user
   - Mitigation: User controls which files to process
   - Recommendation: Don't process untrusted files

2. No Sandboxing: traceflux runs with user's permissions
   - Mitigation: Run in isolated environment if processing untrusted input
   - Recommendation: Use containers or VMs for untrusted data

3. No Encryption: Files processed in plaintext
   - Mitigation: Encrypt sensitive files at rest
   - Recommendation: Don't process highly sensitive data without encryption

### Future Improvements

- Optional sandboxing (container/VM)
- File permission validation
- Audit logging for sensitive operations
- Secure deletion of temporary files (if any)

---

## Contact

Security Questions: Open a GitHub issue or security advisory

General Questions:
- GitHub Issues (https://github.com/tracer-mohist/traceflux/issues)
- Discussions (https://github.com/tracer-mohist/traceflux/discussions)

Non-Security Issues:
- Bug Reports (https://github.com/tracer-mohist/traceflux/issues/new)
- Feature Requests (https://github.com/tracer-mohist/traceflux/issues/new)

---

## Acknowledgments

We thank the following for their security contributions:

- (None yet - be the first!)

---

## License

This security policy is part of traceflux.

License: MIT (same as traceflux)

---

Remember: Security is a shared responsibility. Report issues responsibly, keep your installation updated, and follow best practices.
