# Intelligence Layer — Engine Autonomous Awareness
**Version:** 1.1 | **Status:** Phase 1-2 implemented (S104) | **Depends on:** engine-proactive.md, config.yaml, /scout, /validate, /status, /create, /package, /publish

---

## Philosophy

The Engine doesn't just build products. It THINKS about value, context, and impact — then surfaces that thinking as simple suggestions the user can accept, reject, or ignore.

**Core principle:** The user says "what" — the Engine figures out "how much it's worth, who needs it, and where to share it." Not because it's a sales tool, but because understanding value is part of understanding quality.

**The reaction we're engineering:**
- "How did they configure Claude like this?"
- "This system is superintelligent and simple at the same time."
- "The quality is absurd. It unlocks Claude's full potential."

**What makes it feel intelligent:** Anticipation. The Engine sees patterns the user hasn't noticed yet — portfolio gaps, market opportunities, composition synergies, pricing signals — and surfaces them at the exact moment they're actionable. Never pushy. Always useful.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER                      │
│  (always active, feeds into every skill transparently)     │
│                                                            │
│  ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌──────────────┐  │
│  │ MARKET  │ │ VALUE    │ │ PORTF.  │ │ DISTRIBUTION │  │
│  │ AWARE   │ │ SIGNAL   │ │ VISION  │ │ STRATEGY     │  │
│  └────┬────┘ └────┬─────┘ └────┬────┘ └──────┬───────┘  │
│       │           │            │              │           │
│  ┌────┴───────────┴────────────┴──────────────┴────────┐ │
│  │              CONTEXT SYNTHESIZER                     │ │
│  │   Merges all signals into actionable suggestions     │ │
│  └──────────────────────┬──────────────────────────────┘ │
└─────────────────────────┼────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   SKILL INTEGRATION   │
              │   (injection points)  │
              │                       │
              │  /scout  → market     │
              │  /create → portfolio  │
              │  /fill   → value      │
              │  /validate → pricing  │
              │  /package → distrib.  │
              │  /publish → strategy  │
              │  /status → portfolio  │
              └───────────────────────┘
```

---

## Five Intelligence Dimensions

### 1. MARKET AWARENESS

**What it knows:** What exists in the marketplace for this domain. Who competes. What's missing. What's trending.

**Data sources:**
- `/scout` Section 3 (Market Landscape) — competitors, pricing, gaps
- `myclaude search --json` — live marketplace data (when CLI available)
- `references/market/` — cached market intelligence

**When it speaks:**
| Moment | What it says | Example |
|--------|-------------|---------|
| /scout completes | Market position summary | "Zero competitors for k8s security. Blue ocean." |
| /create starts | Domain saturation check | "3 existing tools in this domain. Differentiate on: {gap}." |
| /validate passes | Competition-aware verdict | "MCS-2 with unique content. Only tool covering supply chain + runtime." |
| /status | Portfolio market position | "Your security tools have zero competition. Your reasoning tools compete with 2 others." |

**Intelligence rules:**
- Zero competitors → "Blue ocean. First-mover advantage. Consider free to establish authority."
- 1-3 competitors → "Differentiate on: {uncovered gaps from scout}. Your unique coverage: {list}."
- 4+ competitors → "Crowded space. Your edge: {specific_differentiator}. Consider composition (bundle) or niche down."

### 2. VALUE SIGNAL

**What it knows:** How much a product is worth, based on objective signals — not guesswork.

**Pricing model (4 factors, weighted):**
```
VALUE_SCORE = round((depth/4 × 0.35 + uniqueness/3 × 0.30 + coverage/3 × 0.20 + market/2 × 0.15) × 12)
# Each factor normalized to 0-1, weighted, then scaled to 0-12.
# Guard: if uniqueness=0 AND coverage=0, cap at 2 (free tier).
# Normalization preserves intended weight ratios exactly.

depth:
  MCS-1 (75-84%)  = 1  → free or $1-3
  MCS-2 (85-91%)  = 2  → $3-8
  MCS-3 (92-100%) = 3  → $8-20
  cognitive mind   = +1 → premium tier

uniqueness:
  substance < 50   = 0  → "Claude already knows this"
  substance 50-70  = 1  → "adds some depth"
  substance 70-90  = 2  → "genuine expertise"
  substance > 90   = 3  → "irreplaceable knowledge"

coverage:
  gaps_addressed < 3  = 0
  gaps_addressed 3-6  = 1
  gaps_addressed 7-10 = 2
  gaps_addressed > 10 = 3

market:
  saturated (4+ competitors)  = 0
  moderate (1-3 competitors)  = 1
  blue ocean (0 competitors)  = 2
```

**Price mapping:**
| Value Score | Suggested Range | Strategy |
|-------------|----------------|----------|
| 0-2 | Free | "Share to build presence. Value is community, not revenue." |
| 3-4 | $1-5 | "Light expertise. Price signals value without being a barrier." |
| 5-7 | $5-12 | "Solid expertise. Users who need this will pay." |
| 8-10 | $12-25 | "Premium. Deep domain expertise + unique coverage. Price with confidence." |
| 11+ | $25+ | "Rare. Consider if this should be a system or bundle for maximum value." |

**When it speaks:**
| Moment | What it says |
|--------|-------------|
| /validate passes (MCS-2+) | "Value signal: {score}/12. Suggested: {range}. Based on: depth {mcs}%, uniqueness {substance}, {gaps_covered} gaps, {market_position}." |
| /package | "Pricing reminder: your product scores {value_score}/12. Current price: {price}. Suggested: {range}." |
| /publish | "Going live at ${price}. {If free: 'Free builds community — track installs to see impact.'} {If paid: 'Premium position. Ensure README sells the value clearly.'}" |

**Epistemic caveat (always shown):**
> "Value signal is estimated from structural quality + market position. Real value is confirmed by daily use. If YOU use this every day, others will too."

### 3. PORTFOLIO VISION

**What it knows:** The user's complete product portfolio — what domains are covered, where the gaps are, how products compose together.

**Data source:** `STATE.yaml → workspace.products[]` + `.meta.yaml` per product

**Portfolio analysis:**
```
For each product, extract:
  - domain (from .meta.yaml or scout report)
  - type (skill/agent/squad/minds/etc.)
  - capability (what it does, from primary file §1)

Group by domain → compute coverage:
  domain_coverage = products_in_domain / estimated_domain_needs

Identify composition opportunities:
  If 3+ products in same domain AND no bundle exists → suggest bundle
  If skill + minds in same domain → "These compose well: skill does, mind advises"
  If 2+ squads with overlapping agents → suggest consolidation or orchestrator
```

**When it speaks:**
| Moment | What it says |
|--------|-------------|
| /status | "Portfolio: {N} products across {M} domains. Strongest: {domain} ({N} products). Gap: {missing_domain}." |
| /scout completes | "This domain connects to your existing {related_product}. Building here extends your {domain} coverage from {X}% to {Y}%." |
| /create completes | "New {type} in {domain}. Your {domain} portfolio: {list}. {If 3+: 'Consider a bundle for complete coverage.'}" |
| Session start | "Your portfolio covers: {domains with emoji indicators}. Users who install {top_product} likely need: {related_gap}." |

### 4. DISTRIBUTION STRATEGY

**What it knows:** Where and how to share products for maximum impact based on type, quality, and user intent.

**Distribution channels (ranked by impact per type):**
```
skill/workflow:
  1. myclaude.sh marketplace (primary)
  2. GitHub awesome-claude-code list
  3. r/ClaudeAI with usage demo
  4. X/Twitter with before/after example

squad/system:
  1. myclaude.sh marketplace (primary)
  2. Blog post with architecture diagram
  3. Claude Code Discord/community
  4. YouTube walkthrough (if visual)

minds:
  1. myclaude.sh marketplace (primary)
  2. Domain-specific community (e.g., DevOps forum for k8s-security)
  3. LinkedIn post targeting domain professionals
  4. Newsletter mention in domain publication

bundle:
  1. myclaude.sh marketplace (primary)
  2. Landing page (premium bundles)
  3. Product Hunt launch (for comprehensive bundles)
```

**Free vs Paid decision tree:**
```
Is this your first product in this domain?
  YES → Free (build authority)
  NO → Have you built audience/installs?
    NO → Free (still building)
    YES → Is this MCS-2+ with substance > 70?
      YES → Paid (premium value justified)
      NO → Free or $1-3 (value signal without barrier)
```

**When it speaks:**
| Moment | What it says |
|--------|-------------|
| /publish completes | "Distribution plan for {slug}: {top 3 channels}. {If first in domain: 'First product here — go free to build authority.'}" |
| /status (7+ days since publish) | "Published {slug} {N} days ago. Have you shared it beyond the marketplace? Suggested: {top channel for this type}." |

### 5. USER AMPLIFICATION

**What it knows:** What the user's installed tools do TOGETHER — the compound effect.

**This is the dimension that creates the "superintelligent" feeling.** It sees connections the user hasn't made.

**When it speaks:**
| Moment | What it says |
|--------|-------------|
| User installs 3+ products | "You now have {list}. Together they cover: {capability summary}. Try: {specific compound workflow}." |
| User builds something related | "Your new {slug} + your existing {other_slug} = {compound capability}. Consider referencing each other in README." |
| /scout finds related domain | "This domain intersects with your {existing_product}. Users of {existing} would benefit from what you're building." |

---

## Integration Points (per skill)

### /scout
- **MARKET** → Section 3 already generates market landscape. Enhance: add value score estimate for recommended products.
- **PORTFOLIO** → After recommendation: "This connects to your existing {product}. Building here extends your {domain} coverage."

### /create
- **PORTFOLIO** → On scaffold: "Your {domain} portfolio: {list}. This will be product #{N} in this domain."
- **MARKET** → If domain is saturated: "3 existing tools here. Your differentiator based on scout: {gap}."

### /fill
- **VALUE** → After each major section: "Section depth: {STRONG/OK/THIN}. Current trajectory: MCS-{estimated}."
- **MARKET** → During research injection: include competitor product content comparison when available.

### /validate
- **VALUE** → After scoring: "Value signal: {score}/12. Suggested price: {range}. Free-vs-paid: {recommendation}."
- **PORTFOLIO** → After pass: "This is your {Nth} product in {domain}. Portfolio synergy: {composition_note}."

### /package
- **DISTRIBUTION** → "Package ready. Distribution channels for {type}: {ranked list}."
- **VALUE** → "Current price: {price}. Value signal says: {range}. {If mismatch: 'Consider adjusting.'}"

### /publish
- **DISTRIBUTION** → "Live! Suggested distribution: {top 3 channels with specific actions}."
- **PORTFOLIO** → "Portfolio update: {domain} now at {coverage}% coverage."

### /status
- **PORTFOLIO** → Full portfolio vision with domain coverage map.
- **MARKET** → Per-product market position summary.
- **DISTRIBUTION** → "Products not yet shared beyond marketplace: {list}."
- **VALUE** → "Total portfolio value: {sum}. Revenue-generating: {count}/{total}."

---

## Data Model

### New fields in .meta.yaml (per product)
```yaml
intelligence:
  market_position: "blue_ocean"          # blue_ocean | moderate | saturated
  value_score: 8                         # 0-12 composite score
  suggested_price_range: [12, 20]        # USD
  pricing_strategy: "premium"            # free | signal | solid | premium
  domain: "kubernetes-security"          # inferred from scout or content
  distribution_channels: ["myclaude", "awesome-list", "reddit"]
  portfolio_role: "anchor"               # anchor | complement | extension | standalone
```

### New fields in STATE.yaml (portfolio level)
```yaml
portfolio:
  domains:
    - name: "security"
      products: ["aegis", "k8s-security-advisor"]
      coverage: 0.65
    - name: "reasoning"
      products: ["kairo-synthetic-reasoning"]
      coverage: 0.80
  total_value_score: 47
  distribution_reach: ["myclaude", "github", "reddit"]
  last_portfolio_analysis: "2026-04-05"
```

### New section in config.yaml
```yaml
intelligence:
  pricing:
    depth_weight: 0.35
    uniqueness_weight: 0.30
    coverage_weight: 0.20
    market_weight: 0.15
    price_map:                       # value_score → USD range + strategy + guidance
      - { min: 0,  max: 2,  range: [0, 0],   strategy: "free",    guidance: "Share to build presence." }
      - { min: 3,  max: 4,  range: [1, 5],   strategy: "signal",  guidance: "Price signals value." }
      - { min: 5,  max: 7,  range: [5, 12],  strategy: "solid",   guidance: "Solid expertise." }
      - { min: 8,  max: 10, range: [12, 25], strategy: "premium",  guidance: "Deep domain expertise." }
      - { min: 11, max: 99, range: [25, 50], strategy: "rare",     guidance: "Consider system or bundle." }
  distribution:
    default_channels: ["myclaude"]
    suggest_after_publish: true
    nudge_after_days: 7
    channels_by_type:                # ranked channels per product type
      skill:   ["myclaude", "awesome-claude-code", "reddit", "twitter"]
      minds:   ["myclaude", "domain-community", "linkedin", "newsletter"]
      squad:   ["myclaude", "blog-post", "discord", "youtube"]
      bundle:  ["myclaude", "landing-page", "product-hunt"]
  portfolio:
    coverage_threshold: 0.60         # below this = "gap detected"
    bundle_suggestion_threshold: 3   # products in same domain
    composition_alert: true          # alert when skill+minds compose well
  free_vs_paid:
    first_in_domain: "free"          # build authority first
    no_audience_yet: "free"          # build audience first
    mcs2_substance_70: "paid"        # value justified
    fallback: "free_or_signal"       # $0-3 default
  ux:
    mode: "suggestion"               # never command
    show_reasoning: true             # show WHY, not just WHAT
    one_insight_per_moment: true     # don't dump intelligence
    epistemic_caveat: true           # always show confidence caveat
```

---

## UX Principles

### 1. Intelligence is SUGGESTION, never COMMAND
Every intelligence output is phrased as suggestion: "Suggested: $12-15" not "Price: $12-15". The user always decides.

### 2. Show the reasoning, not just the conclusion
"Value signal: 8/12 (depth: MCS-2 ×0.35 + uniqueness: 75% ×0.30 + 7 gaps ×0.20 + blue ocean ×0.15)" — the user sees WHY, not just WHAT.

### 3. One insight per moment
Don't dump all intelligence at once. Surface the most relevant insight for THIS moment in the pipeline. Market awareness during /scout. Value signal during /validate. Distribution during /publish.

### 4. Earn trust through accuracy
The intelligence layer starts conservative (wide ranges, caveats). As the user validates its suggestions ("you were right, free was the right call"), confidence grows. Never overstate certainty.

### 5. Simple surface, deep engine
The user sees: "Suggested: $12-15, blue ocean, share on marketplace + reddit."
Behind that: 4 weighted factors, market data, portfolio analysis, distribution ranking.
The complexity is invisible. The output is one sentence.

---

## Implementation Phases

### Phase 1: Wiring — COMPLETE (S104)
- [x] `intelligence` config section in config.yaml (pricing weights, price_map, distribution, portfolio, free_vs_paid, ux)
- [x] `intelligence` fields in .meta.yaml template (domain, market_position, value_score, breakdown, pricing_strategy, channels, portfolio_role)
- [x] /validate Stage 8 computes value_score after Stage 7 (4 factors, price mapping, portfolio role, free-vs-paid)
- [x] /status Portfolio Intelligence section (domain grouping, coverage, value map, composition alerts)
- [x] STATE.yaml portfolio section (domains, total_value_score, distribution_reach)
- [x] quality-gates.yaml + engine-pipeline.md updated with Stage 8

### Phase 2: Market + Value — COMPLETE (S104)
- [x] /scout post-execution value estimates per recommended product (price_map + portfolio connection)
- [x] /create step 10c portfolio awareness (domain coverage on scaffold)
- [x] /package Step 3b value-informed pricing intelligence (.meta.yaml intelligence fields)
- [x] /publish Step 7 intelligent distribution (channels_by_type, free-vs-paid reflection, portfolio distribution)

### Phase 3: Portfolio + Distribution (1 session)
- Build portfolio analysis in /status
- Add composition detection (bundle suggestions, cross-references)
- Add distribution channel ranking to /publish
- Add portfolio gap detection to session start

### Phase 4: User Amplification (1 session)
- Cross-product synergy detection
- Compound capability mapping
- "Users who install X also need Y" intelligence
- Community-level pattern detection (requires marketplace API)

---

## Success Metrics

The Intelligence Layer works when:
1. Users say "how did you know I needed that?" (anticipation)
2. Products are priced appropriately without agonizing (value signal)
3. Products reach beyond the marketplace (distribution)
4. Users build coherent portfolios, not random products (portfolio vision)
5. The Engine feels like a thinking partner, not a pipeline (autonomy)

**The ultimate test:** A new user installs the Engine, builds their first tool for themselves, and the Engine says: "This is genuinely useful. Share it free to build your presence. Here's where: {channels}." The user shares. Others install. The ecosystem grows. Not because someone SOLD something — because someone SHARED something that works.

---

*"La qualità non è mai un caso; è sempre il risultato di uno sforzo intelligente." — John Ruskin*
*Quality is never an accident; it is always the result of intelligent effort.*

This document is the intelligent effort behind the Engine's intelligence.
