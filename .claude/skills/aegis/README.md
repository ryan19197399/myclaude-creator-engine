# AEGIS — AI Code Auditor Security Skill

Audit, fix, and harden any codebase for security vulnerabilities. STRIDE threat modeling, 300+ vulnerability patterns, 8 compliance frameworks, 5-dimension risk scoring, secure code transforms, and hardening configurations.

## Install

### Quick (marketplace — core skill)
```bash
myclaude install aegis
```

### Full (with detection knowledge base)
```bash
myclaude install aegis
cd ~/.claude/skills/aegis
myclaude install aegis-references
```

The `references/` directory contains 9 domain knowledge files (detection patterns, compliance matrices, stack modules, hardening configs) that power the 6-layer detection engine. AEGIS works without them using AI reasoning, but with them it applies 300+ codified patterns systematically.

## Usage

```
/aegis                    # Full STANDARD audit of current project
/aegis --mode=rapid       # Quick check (~15 min): secrets + deps + top 25 patterns
/aegis --mode=deep        # Pre-release deep audit: PASTA + attack trees + supply chain
/aegis harden             # Skip to hardening: headers, validation, hooks, CI/CD
/aegis compliance         # Compliance-only: 52 checks x 8 frameworks
/aegis deps               # Dependency-only: CVE scan + supply chain heuristics
```

## What It Does

### Cycle 1: AUDIT (Detect & Classify)
- **Reconnaissance:** Maps entry points, trust boundaries, data flows, dependencies
- **STRIDE Threat Model:** Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation
- **6-Layer Detection:** Secrets scan, dependency CVEs, 300+ code patterns, taint analysis, semantic reasoning, compliance mapping
- **5-Dimension Risk Scoring:** Severity, Confidence, Exploitability, Prevalence, Fixability → CRITICAL/HIGH/MEDIUM/LOW

### Cycle 2: FIX (Remedy & Verify)
- **Auto-fix:** Deterministic transforms (SQLi → parameterized, XSS → sanitize, path traversal → basename)
- **Guided fix:** Context-dependent with explanation, user confirms
- **Manual:** Architectural changes documented with guidance

### Cycle 3: HARDEN (Prevent & Monitor)
- Security headers (CSP, HSTS, X-Frame-Options)
- Input validation schemas (Zod)
- Pre-commit hooks (Husky + gitleaks)
- CI/CD security pipeline (5 workflows)
- Semgrep rules (10 production rules)

## Supported Stacks

Next.js, Express.js, Django, FastAPI, Firebase, Stripe, Docker, Kubernetes, AWS Terraform, GCP Terraform, Vercel — with stack-specific detection modules.

## Compliance Frameworks

OWASP Top 10, NIST 800-53, CIS Controls, PCI DSS, SOC 2, ISO 27001, GDPR (technical), HIPAA (technical).

## Requirements

- Claude Code >= 1.0.0
- Tools: Read, Write, Edit, Bash, Glob, Grep
- Project with source code to audit

## Reference Files

AEGIS loads domain knowledge from `references/` on demand. These files are distributed separately due to marketplace content policies (they contain security detection patterns).

| File | Contains |
|------|----------|
| `detection-patterns.md` | 300+ code vulnerability patterns, taint analysis definitions |
| `axioms-and-stride.md` | STRIDE threat model patterns per category |
| `compliance-matrix.md` | 52 checks across 8 compliance frameworks |
| `stack-modules.md` | 11 stack-specific detection modules |
| `hardening.md` | Security headers, validation schemas, browser security |
| `devops-artifacts.md` | CI/CD workflows, static analysis rules, pre-commit configs |
| `auth-crypto.md` | Authentication and cryptography best practices |
| `privacy-and-agentic.md` | OWASP LLM Top 10, Agentic Top 10, LINDDUN privacy |
| `report-template.md` | Audit report structure and finding templates |
