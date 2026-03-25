# Context Caching Strategy — MyClaude Creator Engine

> How the Engine manages context loading for efficiency and consistency.

---

## Principle: Load Once, Reference Many

The Engine operates in Claude Code sessions where context is precious.
Strategy: load heavy files once at session start, reference lightweight files on demand.

---

## Loading Tiers

### Tier 0 — Always Loaded (Boot Sequence)
Loaded by CLAUDE.md boot sequence at EVERY session start:

| File | Size | Purpose |
|------|------|---------|
| `creator.yaml` | ~500 tokens | Creator identity, preferences, defaults |
| `.engine-meta.yaml` (root) | ~100 tokens | Engine version, last action |
| workspace scan (glob) | ~50 tokens | Active product count and states |

**Total Tier 0 cost:** ~650 tokens per session

### Tier 1 — Loaded on Skill Activation
Loaded when a specific skill is invoked (activation protocol):

| Skill | Files Loaded | Est. Tokens |
|-------|-------------|-------------|
| `/onboard` | (none — generates new) | 0 |
| `/create` | product-spec for category + template | ~1,500 |
| `/validate` | product-spec + mcs-{level}-checks.md | ~2,000 |
| `/publish` | creator.yaml + manifest schema | ~800 |

### Tier 2 — Loaded on Agent Activation
Loaded when an agent is invoked (part of agent's activation protocol):

| Agent | Files Loaded | Est. Tokens |
|-------|-------------|-------------|
| quality-reviewer | mcs-spec.md + product-spec + exemplars (for calibration) | ~3,000 |
| market-analyst | categories.md + pricing-guide.md + creator.yaml | ~1,500 |
| packaging-specialist | naming-guide.md + readme-guide.md | ~1,000 |
| domain-expert | product-spec for category + best-practices | ~1,500 |
| differentiation-coach | anti-commodity.md + creator.yaml | ~800 |

### Tier 3 — Loaded on Demand
Loaded only when specifically needed during a session:

| File | Loaded When |
|------|------------|
| `references/exemplars/*.md` | When comparing product against gold standard |
| `references/best-practices/*.md` | When creator asks for guidance |
| `references/market/*.md` | During /scan-market |
| `references/shared-vocabulary.md` | During cross-agent handoffs |

---

## Cache Invalidation

| Event | Action |
|-------|--------|
| `/onboard` completes | Reload creator.yaml (Tier 0) |
| Product validated | Reload .engine-meta.yaml for that product |
| New product scaffolded | Reload workspace scan |
| Agent handoff occurs | Load shared-vocabulary.md + target agent's Tier 2 files |

---

## Token Budget Guidelines

| Session Type | Typical Budget | Strategy |
|-------------|---------------|----------|
| Quick validation (/validate) | ~3,000 tokens context | Tier 0 + Tier 1 only |
| Full creation session | ~6,000 tokens context | Tier 0 + Tier 1 + Tier 2 (one agent) |
| MCS-3 review | ~8,000 tokens context | Tier 0 + Tier 1 + Tier 2 (quality-reviewer + handoffs) |
| Market scan + create | ~5,000 tokens context | Tier 0 + Tier 2 (market-analyst) + Tier 1 (/create) |

---

*Context caching strategy for the MyClaude Creator Engine.*
*Principle: minimal context, maximum relevance, load on demand.*
