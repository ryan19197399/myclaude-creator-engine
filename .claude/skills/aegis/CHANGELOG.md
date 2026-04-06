# Changelog

## 1.0.0 (2026-03-29)

### Added
- Three-cycle security framework: AUDIT, FIX, HARDEN
- STRIDE threat modeling for all entry points and trust boundaries
- 6-layer detection engine: secrets, dependencies, pattern match, taint analysis, semantic reasoning, compliance
- 300+ vulnerability detection patterns mapped to CWE/OWASP
- 5-dimension risk scoring (Severity, Confidence, Exploitability, Prevalence, Fixability)
- 3 engagement modes: RAPID, STANDARD, DEEP
- 11 stack-specific modules: Next.js, Express, Django, FastAPI, Firebase, Stripe, Docker, K8s, AWS, GCP, Vercel
- 8 compliance frameworks: OWASP Top 10, NIST 800-53, CIS, PCI DSS, SOC 2, ISO 27001, GDPR, HIPAA
- AI/LLM security: OWASP LLM Top 10 + Agentic Top 10
- Privacy: LINDDUN threat model for PII handling
- Auto-fix transforms for common vulnerabilities
- Hardening: security headers, Zod schemas, pre-commit hooks, CI/CD pipelines, Semgrep rules
- State persistence: .aegis/last-audit.json for delta analysis across sessions
- Adversarial self-review: findings challenged before delivery
- 3 usage examples: standard audit, rapid PR review, compliance check
