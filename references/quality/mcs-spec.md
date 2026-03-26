# MCS Specification — MyClaude Creator Spec

## Overview

MCS (MyClaude Creator Spec) is the quality system for the MyClaude marketplace.
Three tiers define ascending quality levels. Products must pass lower tiers to reach
higher ones — MCS-3 requirements include all MCS-1 and MCS-2 requirements.

**CE-D7:** MCS is the "App Store Review Guidelines" of MyClaude.

---

## MCS-1: Publishable

The minimum bar for marketplace listing. Validates automatically via `/validate`.

### Universal Requirements (All Product Types)

- [ ] Valid structure for product type (correct files in correct locations)
- [ ] Required primary file exists: SKILL.md | AGENT.md | SQUAD.md | WORKFLOW.md |
      DESIGN-SYSTEM.md | PROMPT.md | CLAUDE.md | README.md (apps) | SYSTEM.md
- [ ] Has required metadata: name, description, category, version, license
- [ ] README.md present with: what it does, how to install, how to use, requirements
- [ ] No broken file references (all referenced files exist on disk)
- [ ] No syntax errors in markdown, yaml, or json files
- [ ] File size under 50MB total
- [ ] License declared from approved list (CE-D40):
      MIT | Apache-2.0 | GPL-3.0 | BSD-3-Clause | ISC |
      CC-BY-4.0 | CC-BY-SA-4.0 | CC0-1.0 | Proprietary | Custom
- [ ] No hardcoded secrets, API keys, passwords, or tokens
- [ ] No malicious code patterns: eval(), exec(), network calls to unknown hosts

### Automated Checks

```
/validate → runs MCS-1 suite:
  ├── structure-check:   correct files for product type?
  ├── metadata-check:    all required fields present?
  ├── reference-check:   all file references resolve?
  ├── syntax-check:      valid markdown/yaml/json?
  ├── size-check:        under 50MB?
  ├── security-scan:     no secrets or malicious patterns?
  └── readme-check:      required sections present?
```

### Per-Type MCS-1 Requirements

| Type | Required Files | Additional Requirements |
|------|---------------|------------------------|
| Skill | SKILL.md + README | Activation Protocol section, 1+ trigger conditions |
| Agent | AGENT.md + README | Identity section, tool list |
| Squad | SQUAD.md + agents/ (2+ agent definitions) + README | Routing logic, 1+ workflow defined |
| Workflow | WORKFLOW.md + README | Step dependencies, inputs/outputs |
| Design System | tokens/ (1+ token file) + README | Brand identity, platform targets |
| Prompt | PROMPT.md + README | Variables documented |
| CLAUDE.md | CLAUDE.md + README | Boot sequence (2+ steps), 3+ conventions |
| Application | src/ (1+ source file) + README + package manifest | App actually runs |
| System | SYSTEM.md + 1+ subdirectory (skills/, agents/, or workflows/) + README | Component references resolve |

---

## MCS-2: Quality

Products demonstrating craft and thoroughness. Semi-automated — requires creator
self-attestation for manual checks.

### Universal Requirements (Beyond MCS-1)

- [ ] At least 3 exemplars/examples covering different use cases
- [ ] Anti-patterns section (what NOT to do)
- [ ] Tested with at least 5 different user intents/scenarios
- [ ] Quality gate defined (creator's own verification method)
- [ ] Error handling for edge cases
- [ ] No placeholder content (no "TODO", "lorem ipsum", "[placeholder]", "coming soon")
- [ ] Consistent naming and terminology throughout
- [ ] Version follows semver (MAJOR.MINOR.PATCH)

### Semi-Automated Checks

```
/validate --level=2 → runs MCS-2 suite:
  ├── [All MCS-1 checks]
  ├── exemplar-count:      >= 3 exemplars found?
  ├── anti-pattern-check:  anti-patterns section exists?
  ├── placeholder-scan:    no TODO/lorem/placeholder content?
  ├── consistency-check:   naming consistent throughout?
  ├── completeness-score:  % of optional sections filled
  └── [MANUAL] intent-test: tested with 5 intents? (creator self-reports)
```

### Per-Type MCS-2 Requirements

| Type | Additional Requirements |
|------|------------------------|
| Skill | references/exemplars.md (3+ examples), 1+ anti-pattern documented, 1+ optional directory (agents/, tasks/, config/, or workflows/) |
| Agent | architecture.md, examples/ (3+ interactions including edge case), identity.md with full persona, decision protocol covers act vs. ask |
| Squad | handoff-protocol.md with format specs, 3+ workflow examples, capability-index.yaml, all agents at MCS-1+ |
| Workflow | config/variables.yaml, error handling per step, 2+ execution examples, retry/abort conditions |
| Design System | 3+ component specs in components/, guidelines/usage.md, 2+ export formats |
| Prompt | variants/ (2+), 3+ examples, config/variables.yaml |
| CLAUDE.md | rules/ directory with modular rule files, architecture.md with WHY, tested in real project (5+ sessions) |
| Application | CLAUDE.md, docs/architecture.md, tested on clean install, no security vulnerabilities in deps |
| System | config/routing.yaml, all components at MCS-1+, 2+ integration tests, 3+ component types |

---

## MCS-3: State-of-the-Art

The gold standard. Requires agent review. Products that set the bar for the marketplace.

### Universal Requirements (Beyond MCS-2)

- [ ] Deep knowledge base in references/ (domain expertise encoded — not AI-generatable alone)
- [ ] Adaptive modes (works in different contexts/constraints)
- [ ] Composable (works well with other MyClaude products)
- [ ] Stress-tested: ambiguity test, edge case test, adversarial test — all passed
- [ ] Cognitive architecture documented (WHY it's designed this way)
- [ ] Versioning strategy with CHANGELOG
- [ ] At least 5 exemplars covering edge cases
- [ ] Performance-optimized (minimal token usage for maximum value)
- [ ] Differentiation statement (what makes THIS product unique vs. alternatives)

### Agent-Assisted Review

```
/validate --level=3 → runs MCS-3 suite:
  ├── [All MCS-2 checks]
  ├── [AGENT] depth-review:          references contain real domain expertise?
  ├── [AGENT] composability-test:    works with standard products?
  ├── [AGENT] stress-test:           handles ambiguity/adversarial input?
  ├── [AGENT] differentiation-check: not a commodity product?
  ├── [AGENT] architecture-review:   design decisions justified?
  └── [AGENT] token-efficiency:      reasonable context usage?
```

### Per-Type MCS-3 Requirements

| Type | Additional Requirements |
|------|------------------------|
| Skill | Progressive depth modes (surface/dive/radical), question system, full references/ knowledge base, standalone + composable |
| Agent | 7-layer cognitive architecture, tested standalone + as squad component, stress test results documented |
| Squad | All agents at MCS-2+, routing tested adversarially, agent failure handling, tested standalone + as system component |
| Workflow | Composable (can be nested/chained), adaptive modes, failure recovery procedures, performance metrics |
| Design System | Motion tokens, 10+ component specs, 3+ export formats, theming system, WCAG 2.1 AA contrast verified |
| Prompt | Context engineering structure, composability pattern, anti-injection safeguards |
| CLAUDE.md | Hook configurations, MCP integration patterns, permission model, tested across team members |
| Application | CI/CD config, meaningful test coverage, production-ready (logging, error tracking), deployment guide |
| System | All components at MCS-2+, stress-tested routing, adaptive modes, full architecture docs |

---

## MCS Badge Display

CE-D8: MCS level is visible on every marketplace listing.

```
┌──────────────────────────────────────┐
│  ★ SKILL: Kairo Synthetic Reasoning  │
│  MCS-3 ████████████ State-of-the-Art │
│  by @darwim · v2.1.0 · $49          │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  PROMPT: Sales Email Generator       │
│  MCS-1 ████░░░░░░░░ Publishable     │
│  by @creator · v1.0.0 · Free        │
└──────────────────────────────────────┘
```

Badge levels:
- MCS-1: `████░░░░░░░░ Publishable`
- MCS-2: `████████░░░░ Quality`
- MCS-3: `████████████ State-of-the-Art`

---

## Anti-Commodity Gate (CE-D9)

Applied before publishing at MCS-2 or MCS-3. See `references/quality/anti-commodity.md`
for full specification.

**Three questions:**
1. "What domain expertise did the creator inject that AI alone couldn't generate?"
2. "If we removed all AI-generated content, what would remain?"
3. "Does this product solve a specific problem that <5 other products address?"

If all three answers are weak → feedback, not rejection (CE-D26).
