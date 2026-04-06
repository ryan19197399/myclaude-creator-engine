# Scout Agent — Domain Intelligence Protocol

> The intelligence layer of the Creator Engine. Researches a domain BEFORE any product is built.
> Transforms "I want to build something for X" into a data-backed recommendation of WHAT to build.

---

## Inputs

- `domain`: The domain query (e.g., "kubernetes security", "email marketing automation")
- `slug`: Sanitized slug derived from domain (e.g., "kubernetes-security")
- `creator`: Loaded creator.yaml profile (type, level, language, expertise)
- `language`: Output language (from creator.yaml or auto-detected)
- `intent`: personal | marketplace | explore — determines report depth and sections

## Output

- `workspace/scout-{slug}.md` — Complete scout report

---

## STEP 1: BASELINE TEST — What Claude Already Knows

**Purpose:** Establish the FREE alternative. What does any user get from Claude vanilla, without products?

**Method:**
1. Generate a comprehensive response AS IF you were Claude with no special products, answering:
   > "You are an expert in {domain}. Explain the key concepts, common approaches, best practices,
   > common pitfalls, and how a professional would approach this domain."
2. Write this response verbatim — this IS the baseline
3. Be honest and thorough — a weak baseline makes the gap analysis meaningless
4. Adapt depth to creator profile:
   - **developer** → include code patterns, tooling, debugging approaches
   - **prompt-engineer** → include cognitive patterns, prompt structures
   - **domain-expert** → include what Claude ADDS beyond their existing knowledge
   - **marketer** → include conversion patterns, audience psychology
   - **operator** → include automation, monitoring, scaling patterns
   - **agency** → include multi-client patterns, customization
   - **hybrid** → balanced across all dimensions

**Output section:** `## 1. Baseline — What Claude Knows`

**Quality gates:**
- 300-600 words. Shorter → domain may be too narrow. Longer → consider decomposing.
- Must be substantive enough to stand alone as useful content (it IS the competition).
- Rate the baseline: Strong (80%+ coverage) / Moderate (50-80%) / Weak (<50%).

---

## STEP 2: GAP ANALYSIS — Where Claude Falls Short

**Purpose:** Identify what's MISSING, SHALLOW, WRONG, or GENERIC in the baseline.

**Method:** Read the baseline critically through 4 lenses:

| Lens | Question | Example finding |
|------|----------|----------------|
| **Missing** | What topics weren't mentioned at all? | "No mention of supply chain attacks in k8s security" |
| **Shallow** | What was mentioned but lacks depth? | "RBAC mentioned but no real-world role design patterns" |
| **Wrong** | What common misconceptions appear? | "Implies network policies are enabled by default" |
| **Generic** | What lacks real-world specificity? | "Best practices are textbook, no production war stories" |

**For each gap, rate severity:**
- **Critical** — Without this, Claude's advice could cause harm or significant waste
- **Significant** — Noticeable quality difference; expert would spot this immediately
- **Minor** — Nice to have; improves experience but baseline is functional

**Output section:** `## 2. Gap Analysis`

**Quality gates:**
- Minimum 5 gaps. Fewer than 3 → baseline was too generous or domain too narrow.
- More than 15 → ask creator to narrow scope before proceeding.
- Each gap must be specific and actionable (not "could be more detailed").
- At least 1 gap per lens. If a lens has 0, explicitly state "No {lens} gaps found."

**CRITICAL: After this step, RETURN CONTROL TO SKILL.MD for the mid-protocol gate.**
The creator must see and approve the gaps before research begins.

---

## STEP 3: MARKET SCAN — What Already Exists

**Purpose:** Know the competitive landscape before building.

**Method:**
1. Check if `myclaude` CLI is available:
   ```bash
   myclaude --version 2>/dev/null
   ```
2. If available, run market queries:
   ```bash
   myclaude search "{domain}" --json 2>/dev/null
   myclaude search "{related-term-1}" --json 2>/dev/null
   myclaude trending --json 2>/dev/null
   ```
3. If CLI unavailable, note it and continue — market scan is valuable but not blocking.

**For each competing product found, capture:**
- Name, type, author, downloads
- What it covers (from description)
- What it DOESN'T cover (gap relative to our analysis)
- Price point (if marketplace intent)

**If intent = "explore":** Lighter analysis — list products found, note obvious gaps, skip deep comparison.

**Output section:** `## 3. Market Landscape`

**Quality gate:** Even with no results, document the absence — "No existing products found
for {domain}" is itself a valuable market signal (blue ocean or non-obvious niche).

---

## STEP 4: RESEARCH — Fill the Gaps with Real Intelligence

**Purpose:** Transform identified gaps into actual knowledge using external research.

**Prerequisite:** WebSearch and WebFetch tools must be available. If not:
- Write to report: "Research skipped — no web tools available. Recommendations based on baseline + gap analysis only. Confidence: medium."
- Skip to Step 5.

**Method:**
1. For each **Critical** gap from Step 2, run targeted research:
   ```
   WebSearch: "{domain} {gap-topic} best practices 2025 2026"
   WebSearch: "{domain} {gap-topic} common mistakes production"
   ```
2. For each **Significant** gap, run focused research:
   ```
   WebSearch: "{domain} {gap-topic} expert guide"
   ```
3. For the most promising results (relevance + recency), fetch full content:
   ```
   WebFetch: {url} — extract key patterns, heuristics, examples
   ```
4. Synthesize findings per gap:
   - **Key patterns** — things experts do that Claude didn't mention
   - **Common mistakes** — things beginners do that experts warn against
   - **Expert heuristics** — decision rules that only come from experience
   - **Real examples** — case studies, war stories, production incidents
   - **Source** — URL and date (unsourced claims stay in baseline, not research)

**Research budget:**
- Critical gaps: 2-3 searches + 1-2 fetches each
- Significant gaps: 1-2 searches each
- Minor gaps: skip (unless quick win is obvious)
- Total ceiling: 12 searches, 5 fetches. Substantive, not exhaustive.

**If intent = "explore":** Reduce to 4-6 searches, 1-2 fetches. Just enough for a directional signal.

**Output section:** `## 4. Research Findings`

**Quality gate:** Each finding must cite its source URL. Minimum 3 sourced findings for a
non-explore report. If research yields nothing useful, state that honestly rather than
inflating baseline knowledge as "research."

---

## STEP 5: SETUP RECOMMENDATION — What to Build

**Purpose:** Translate intelligence into a concrete product recommendation.

**Method:**
1. Review: gaps (severity) + research (what was found) + market (what exists/doesn't)
2. Apply the Engine's product taxonomy decision tree (all 13 types):

   ```
   Q1: Does the domain need DOING, THINKING, GOVERNING, INFRASTRUCTURE, or APPEARANCE?
     DO → Q2: Single action or sequence?
       Single → Q3: Needs judgment? → Yes: agent | No: skill
       Sequence → workflow
       Automatic reaction → hooks
     THINK → Q2: One perspective or multiple?
       One → Q3: Also acts? → Yes: agent | No: minds
       Multiple → squad
     GOVERN → Q2: Always active or event-triggered?
       Always → claude-md
       Event → hooks
     INFRASTRUCTURE → Q2: Dedicated project, extensions, or deployable app?
       Dedicated → system
       Extensions → bundle
       Deployable app → application
     APPEARANCE → Q2: Visual consistency, output formatting, or ambient display?
       Visual consistency → design-system
       Output formatting → output-style
       Ambient display → statusline
   ```

3. For each recommended product, specify:
   - **Type** (from 13 Engine types)
   - **Name** (descriptive slug, following `^[a-z0-9][a-z0-9-]{2,39}$`)
   - **Purpose** (1 sentence: which specific gap it fills)
   - **Key content** (3-5 bullet points of what the product should contain)
   - **MCS target** (1, 2, or 3 — based on gap severity and audience)
   - **Gap refs** (which gaps from Step 2 this product addresses — traceability)

4. Show composition relationships explicitly:
   ```
   {product-A} ──uses──▶ {product-B} (as instrument)
   {product-C} ──consults──▶ {product-D} (for advice)
   {squad} ──contains──▶ {agent-1}, {agent-2}, {minds-1}
   ```

**Composition rules (enforced):**
- Skills NEVER use other products (they ARE the instruments)
- Agents use skills as instruments, consult minds for advice
- Squads contain agents/minds, use skills as shared instruments
- If recommending >3 products → consider a bundle
- If recommending >5 with shared infrastructure → consider a system
- NEVER recommend more than 7 products total. If the analysis suggests more, the domain needs decomposition.

**Pricing guidance (marketplace intent only):**
- Free: simple utilities, community tools, first-time creators
- $1-5: solid single-purpose skills with real domain depth
- $5-15: deep expertise (minds, agents with judgment)
- $15-30: multi-product squads with specialized collaboration
- $30+: complete systems with dedicated infrastructure

**If intent = "explore":** Show recommendation as "Possible directions" not "Build plan."
Keep it to 1-3 products max. No pricing.

**If intent = "personal":** Skip pricing. Focus on which products will improve THEIR specific workflow.

**Output section:** `## 5. Setup Recommendation`

---

## STEP 6: SAVE & CONDUCT

**Purpose:** Persist the report and guide the creator to next steps.

**Method:**
1. Assemble all sections into the scout report. Use this structure:

   ```markdown
   # Scout Report: {domain}
   **Date:** {YYYY-MM-DD} | **Creator:** {name} | **Intent:** {intent}
   **Baseline rating:** {Strong/Moderate/Weak} | **Gaps:** {N} ({critical}C/{significant}S/{minor}M)

   ## 1. Baseline — What Claude Knows
   {baseline_content}

   ## 2. Gap Analysis
   | # | Gap | Lens | Severity | Detail |
   |---|-----|------|----------|--------|
   {gap_rows}

   ## 3. Market Landscape
   {market_content_or_unavailable_note}

   ## 4. Research Findings
   {research_content_or_skipped_note}

   ## 5. Setup Recommendation
   {recommendation_with_composition_map}

   ## 6. Confidence & Caveats
   - Baseline limitation: simulated (Claude assessing itself with Engine context loaded — may inflate baseline quality)
   - Baseline model: claude-opus-4-6 (record the exact model ID used for this baseline — if a future /validate runs on a different model, delta accuracy may be affected)
   - Research depth: {full/partial/none}
   - Market data: {available/unavailable}
   - Creator expertise overlap: {high/medium/low/unknown}
   - Overall confidence: {high/medium/low}

   ---
   *Generated by MyClaude Creator Engine — /scout*
   ```

2. Write to `workspace/scout-{slug}.md`

3. Return control to SKILL.md for post-execution (STATE update + summary + next step).

---

## Error Handling

| Situation | Response |
|-----------|----------|
| WebSearch/WebFetch unavailable | Skip Step 4, note in report. Reduce confidence to "medium" max. |
| myclaude CLI unavailable | Skip Step 3 market queries. Note: "Marketplace scan unavailable." |
| Domain too broad (>15 gaps) | Pause. Ask creator to narrow: "'{domain}' is broad. Focus on '{sub-1}' or '{sub-2}'?" |
| Domain too narrow (<3 gaps) | Complete report but note. Recommend simpler product type (skill vs system). |
| Creator has domain expertise | Weight gap analysis toward what Claude ADDS, not what creator already knows. |
| Research returns nothing useful | State honestly. Don't inflate baseline knowledge as "findings." |
| All searches fail (network/rate limit) | Note in report. Proceed with baseline + gaps only. Flag low confidence. |

---

## Report Quality Standards

**A good scout report:**
- Baseline could stand alone as useful content (it IS the free alternative to measure against)
- Every gap is specific, actionable, and severity-rated
- Every research finding cites its source URL
- Every recommended product traces back to specific gaps (traceability)
- Composition relationships are explicit (what uses what)
- Confidence section is honest about what's known vs assumed
- Creator has enough information to make a build/buy/skip decision

**A bad scout report:**
- Thin baseline that undersells Claude's real capability (inflates gaps artificially)
- Vague gaps like "could be more detailed" or "needs improvement"
- Zero external research (just Claude analyzing itself — circular)
- Products recommended without gap traceability ("build a minds" — why?)
- Over-recommends (8 products when 2 would cover the critical gaps)
- States "high confidence" without research or market data to support it
