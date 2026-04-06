# Bundle Exemplar: Claude Code Security Suite

**MCS Level:** 2 (Quality)
**Demonstrates:** Bundle-specific validation (no primary file), curation rationale,
pricing strategy, graceful degradation when included products are unavailable.

---

## File: `vault.yaml`

```yaml
name: "claude-code-security-suite"
version: "1.0.0"
description: "Complete security toolkit for Claude Code projects — audit, monitor, and harden in one install."
author: "@security-creator"
category: "bundles"
license: "MIT"
price: 15

bundle:
  includes:
    - "aegis-security-audit"
    - "sentinel-code-review"
    - "guardian-dependency-scan"
  rationale: >
    Security requires multiple perspectives. AEGIS audits architecture,
    Sentinel reviews code changes, Guardian scans dependencies.
    Together they cover the full security surface — something no single
    product achieves alone.
  pricing_note: >
    Individual products total $22. Bundle saves 32%.
    Buyers get a coherent security workflow, not just a discount.

compatibility:
  claude_code: ">=1.0.0"

engine: "myclaude-studio-engine"
```

---

## File: `README.md`

```markdown
# Claude Code Security Suite

> Complete security toolkit — audit, review, and scan in one install.

## What's Included

| Product | Type | What It Does |
|---------|------|-------------|
| [AEGIS Security Audit](https://myclaude.sh/p/aegis-security-audit) | Skill | Architecture-level security audit with STRIDE threat modeling |
| [Sentinel Code Review](https://myclaude.sh/p/sentinel-code-review) | Agent | Automated code review focused on security vulnerabilities |
| [Guardian Dependency Scan](https://myclaude.sh/p/guardian-dependency-scan) | Skill | Scans dependencies for known CVEs and supply chain risks |

## Why This Bundle

Security isn't a single tool — it's a layered defense:
1. **AEGIS** finds architectural vulnerabilities before code is written
2. **Sentinel** catches security issues in code as you write it
3. **Guardian** monitors the supply chain you didn't write

No single product covers all three layers.

## Installation

\`\`\`bash
myclaude install claude-code-security-suite
\`\`\`

## Anti-Patterns

- **Running only one tool:** The bundle's value is layered coverage. Use all three.
- **Ignoring Guardian:** Dependency vulnerabilities are the most common attack vector.
- **Running AEGIS after code is done:** AEGIS finds architectural issues — run it early.

---

**Version:** 1.0.0 | **License:** MIT | **Author:** @security-creator

[![MCS 2](https://myclaude.sh/badge/mcs/2.svg)](https://myclaude.sh/quality)
```

---

## Quality Verification

- [x] No primary .md file (vault.yaml IS the product)
- [x] vault.yaml has bundle.includes[] with 3 products
- [x] Curation rationale explains WHY these together
- [x] Pricing strategy documented
- [x] README lists all included products with descriptions
- [x] Anti-patterns documented
- [x] MCS-2 criteria met
