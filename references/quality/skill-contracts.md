# Skill Contracts — Pipeline Interface Specification

> Every component defines what it receives and what it delivers.

Every skill in the pipeline has a formal contract. When the output of Skill A doesn't match the expected input of Skill B, the pipeline breaks silently. These contracts prevent that.

---

## Pipeline Flow with Contracts

```
/onboard ──[C1]──→ /map ──[C2]──→ /create ──[C3]──→ /fill ──[C4]──→ /validate ──[C5]──→ /package ──[C6]──→ /publish
```

---

## C1: /onboard → ALL SKILLS

**Output contract (what /onboard guarantees):**
```yaml
file: creator.yaml
guaranteed_fields:
  - profile.name        # string, non-empty
  - profile.type        # enum: developer|prompt-engineer|domain-expert|marketer|operator|agency|hybrid
  - technical_level     # enum: beginner|intermediate|advanced|expert
  - preferred_categories # string[] (at least 1)
optional_fields:
  - default_license
  - default_category
  - pricing_strategy
  - communication_language
  - document_language
  - quality_target        # enum: MCS-1|MCS-2|MCS-3
```

**Downstream expectation:** Every skill reads `creator.yaml` and adapts persona. If `creator.yaml` is missing, skill MUST stop with: "Profile not found. Run `/onboard` first (~3 min)."

---

## C2: /map → /create

**Output contract:**
```yaml
file: workspace/domain-map.md
guaranteed_fields:
  - Domain summary (≥100 words)
  - Key concepts (≥3)
  - Relationships between concepts
optional_fields:
  - Vocabulary / glossary
  - Anti-patterns in the domain
  - Reference sources
```

**Downstream expectation:** /create checks for `workspace/domain-map.md`. If present, prefills scaffold sections with domain knowledge. If absent, /create works without it (domain-map is OPTIONAL enrichment).

---

## C3: /create → /fill

**Output contract:**
```yaml
directory: workspace/{slug}/
guaranteed_files:
  - {PRIMARY_FILE}      # SKILL.md, AGENT.md, etc. — with WHY comments
  - README.md           # skeleton with install/usage sections
  - .meta.yaml          # product.type, state.phase=scaffold, mcs_target
optional_files:
  - references/         # directory for domain knowledge
  - domain-map.md       # moved from workspace/ if existed

meta_yaml_contract:
  product:
    slug: string
    type: enum (13 types)
    display_name: string
  state:
    phase: "scaffold"
    created_at: ISO-8601
  mcs_target: "MCS-1" | "MCS-2" | "MCS-3"
```

**Downstream expectation:** /fill reads `.meta.yaml` for type and phase. Expects `phase: "scaffold"` or `phase: "content"`. If phase is `validated` or later, warns about regression.

---

## C4: /fill → /validate

**Output contract:**
```yaml
modified_files:
  - {PRIMARY_FILE}      # sections filled with creator expertise
  - README.md           # real description (not template boilerplate)
  
meta_yaml_additions:
  state:
    phase: "content"    # promoted from scaffold
  creator_intent:
    target_audience: string
    differentiator: string
    primary_use_case: string
  acceptance_criteria:
    truths: string[]    # observable behaviors (≥1)
    artifacts: string[] # required files with content (≥1)
    key_links: string[] # cross-file references (≥1)
```

**Downstream expectation:** /validate reads `creator_intent.acceptance_criteria` for goal-backward verification in Stage 2. If absent, skips acceptance_criteria checks silently (backward compatible with products created before this feature).

---

## C5: /validate → /package

**Output contract:**
```yaml
meta_yaml_additions:
  state:
    phase: "validated"
    last_validated: ISO-8601
    last_validation_score: number (0-100)
    dna_compliance:
      tier1: number
      tier2: number
      tier3: number | null
    overall_score: number
    score_history:
      - { date, score, delta, level }

state_yaml_additions:
  mcs_results.{slug}:
    level: number
    overall_score: number
    # ... (full schema in STATE.yaml)
```

**Downstream expectation:** /package reads `.meta.yaml` and REQUIRES:
- `state.phase == "validated"`
- `state.last_validation_score >= 75`
If either fails, /package stops: "Product not validated. Run /validate first."

---

## C6: /package → /publish

**Output contract:**
```yaml
directory: workspace/{slug}/.publish/
guaranteed_files:
  - vault.yaml          # MyClaude marketplace manifest
  - plugin.json         # Anthropic plugin manifest
  - {product files}     # WHY comments stripped, production-ready
  - README.md           # with install instructions
  - LICENSE             # from creator.yaml default or specified
optional_files:
  - agentskills.yaml    # universal agent skills manifest
  - references/         # if product has references

meta_yaml_additions:
  state:
    phase: "packaged"
```

**Downstream expectation:** /publish reads `.publish/vault.yaml` and REQUIRES all mandatory fields (name, version, type, description, entry, license). Runs `myclaude validate` as preflight.

---

## Contract Violations

When a skill detects a contract violation (expected input missing or malformed):

1. **STOP** — don't try to work around it
2. **NAME** the violation: "Expected `.meta.yaml` with `state.phase: validated`, found `state.phase: content`"
3. **PRESCRIBE** the fix: "Run `/validate` to promote product to validated state"
4. **NEVER** silently degrade — a contract violation is a wiring failure, not a user error
