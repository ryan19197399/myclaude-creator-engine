# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.2.x   | Yes       |
| < 2.0   | No        |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

If you discover a security vulnerability in the Studio Engine, the CLI, or the marketplace, please report it responsibly:

1. **Email:** security@myclaude.sh
2. **Subject:** `[SECURITY] Brief description`
3. **Include:** Steps to reproduce, impact assessment, suggested fix (if any)

### Response Timeline

| Severity | Acknowledgment | Resolution Target |
|----------|---------------|-------------------|
| **Critical** (auth bypass, RCE, data leak) | 24 hours | 72 hours |
| **High** (path traversal, injection, secret exposure) | 48 hours | 7 days |
| **Medium** (privilege escalation, validation bypass) | 48 hours | 14 days |
| **Low** (information disclosure, minor logic errors) | 72 hours | 30 days |

## Scope

This policy covers:

- **Studio Engine** — product creation pipeline, validation, packaging
- **MyClaude CLI** (`@myclaude-cli/cli`) — install, publish, marketplace commands
- **Marketplace** (myclaude.sh) — product distribution, authentication, payments

## What We Consider Vulnerabilities

- Authentication bypass or token leakage
- Path traversal in product install or packaging
- Command injection through product content
- Secret exposure in published products
- Cross-site scripting or injection in marketplace listings
- Privilege escalation in CLI operations

## What We Do NOT Consider Vulnerabilities

- Products with low MCS scores (quality, not security)
- Feature requests or usability issues
- Denial of service through large product uploads (rate-limited by design)

## Security Architecture

The Engine and CLI implement defense-in-depth:

- **CLI:** PKCE S256 authentication, zip-slip defense, secret scanning before publish, path containment on install, SSRF prevention
- **Engine:** Slug validation (`^[a-z0-9][a-z0-9-]{2,39}$`), workspace boundary enforcement, no path traversal
- **Marketplace:** Server-side content scanning, rate limiting, signed download URLs

See [Architecture](docs/reference/architecture.md) for the full security model.

## Recognition

We gratefully acknowledge security researchers who report vulnerabilities responsibly. With your permission, we will credit you in the changelog and release notes.

## Updates

This policy may be updated as the project evolves. Check this file for the latest version.
