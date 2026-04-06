---
name: create
description: >-
  Scaffold a new product with MCS-1 valid structure and WHY comments. Supports all
  13 types. Use when the creator says 'new skill', 'create', 'scaffold', 'start
  building', or wants to start a new product.
argument-hint: "[product-type]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Scaffolder

Generate complete, MCS-1-valid project structure for any product type with guidance comments baked in.

**When to use:** Starting a new product — any of the 13 types.

**When NOT to use:** When the product already exists in `workspace/` and you want to add content (use `/fill`). Do not use to overwrite an existing scaffold unless `--force` is specified.

---

## Activation Protocol

1. Read `creator.yaml` — load defaults. Missing → **micro-onboard**: scan silently, infer defaults, ask ONE name question, generate minimal `creator.yaml`. Never block.
2. **Persona**: Adapt to `profile.type` + `technical_level`. Load `references/quality/engine-voice.md`.
3. **Gates**: Read `config.yaml → gates.confirm_create`. Confirm if `true`; proceed if `false`.
4. **Brownfield check**: Glob `workspace/*/`. If same `product.type` or overlapping tags found, surface slugs and ask before continuing.
5. **Exemplar guard**: Glob `references/exemplars/{category}*`. If found: show condensed preview. If not: skip gracefully — never halt.
6. Load `product-dna/{category}.yaml` → DNA requirements.
7. Load `${CLAUDE_SKILL_DIR}/references/discovery-questions.md` → category questions.
8. Load `references/product-specs/{category}-spec.md` + `templates/{category}/`.
9. Load `workspace/domain-map.md` if exists → prefill scaffold sections.
9b. **Link scout report** if used — record `scout_source: "scout-{slug}.md"` in `.meta.yaml`. Do NOT inject domain content — that's /fill's job.
9c. **Portfolio intelligence (back-reference from /validate)**: Read `STATE.yaml → workspace.products[]` AND `STATE.yaml → mcs_results`. Group by domain. If domain has existing products:
   - Show: "Your {domain} portfolio: {slugs}. This will be product #{N}."
   - If N >= bundle threshold (`config.yaml → intelligence.portfolio.bundle_suggestion_threshold`): suggest bundling.
   - If complementary type opportunity exists: surface composition suggestion.
   - **MCS target calibration**: If domain has 0 products → default MCS-1 (ship fast, test market). If domain has 2+ validated products → default MCS-2 (quality matters, audience exists).
   - Record `intelligence.domain` and `intelligence.market_position` in `.meta.yaml`.
10. Generate scaffold in `workspace/{product-slug}/` with DNA patterns + WHY comments.
11. Create `.meta.yaml` (see template below).
12. Move `workspace/domain-map.md` → `workspace/{product-slug}/domain-map.md` if loaded.
13. Engine voice: "Scaffold ready. {N} sections with WHY guidance. Run /fill to start."

---

## Router Logic

**Read `${CLAUDE_SKILL_DIR}/references/create-router.md`** for:
- Scout-aware routing (check for existing scout reports first)
- Level-based menu (advanced/expert creators vs. beginner/intermediate)
- Full Q1/Q2/Q3 Decision Tree routing all 13 types
- Per-category scaffold structures (all 13 types)
- Prefilling strategy for SKILL.md and README.md

**Direct sub-commands** skip the menu and go straight to category flow:
`/create skill` | `/create agent` | `/create squad` | `/create workflow` | `/create ds` | `/create claude-md` | `/create app` | `/create system` | `/create bundle` | `/create statusline` | `/create hooks` | `/create minds` | `/create output-style`

**Quick mode** (`--quick` flag or `creator.preferences.workflow_style: autonomous` + `products_published >= 5`):
Skip discovery questions, marketplace scan, and exemplar preview. Go straight to: name → scaffold → done.
Example: `/create skill my-tool --quick` → generates scaffold with minimal interaction.
For experienced creators who know exactly what they want. All structural quality (MCS-1) still verified.

---

## Universal Creation Flow

| Step | Action | Detail |
|------|--------|--------|
| 1 | Name + Description | Derive slug: lowercase, hyphens, validate `^[a-z0-9][a-z0-9-]{2,39}$`. Existing `workspace/{slug}/` → offer `/fill` or `--force`. CLI init: vault.yaml but no .meta.yaml → import into Engine workspace. Suggest `/map` if deep domain knowledge involved. |
| 1.5 | Marketplace Scan | `myclaude search --category {type} --sort downloads --limit 3 --json 2>/dev/null`. Show top 3 with downloads + "What will yours do differently?" Coaching only — never blocking. **First-product guard:** If `is_first_product`, SKIP this step — a first-timer seeing competitor data before articulating their own idea causes second-guessing. Show marketplace context AFTER scaffold, not before. |
| 2 | Discovery Questions | Load + ask from `${CLAUDE_SKILL_DIR}/references/discovery-questions.md`. Ask conversationally. `workflow_style=guided` → AskUserQuestion; `autonomous` → plain text. |
| 3 | Load Defaults | From `creator.yaml`: license, version (always 1.0.0), author, quality target. |
| 4 | Generate Scaffold | **Structure only** — files, YAML frontmatter, section headers with WHY comments, template vars for metadata. Never generate substantive prose. Leave `[To be filled — run /fill]` for expertise sections. See router.md for per-category structures. |
| 5 | MCS-1 Structural Validation | Silently verify: required files present, metadata fields populated, README.md has 4 sections (what/install/usage/requirements), no YAML/JSON syntax errors. Auto-fix and note corrections. |
| 6 | Print Next Steps — Cognitive UX | **Load full UX stack:** `references/ux-experience-system.md` (§1 context assembly, §2.3 moment awareness for "first scaffold"), `references/ux-vocabulary.md` (type naming), `references/quality/engine-voice.md` (brand DNA). Output is REASONED, not templated — adapt based on creator context. |

**Step 6 Cognitive Output Protocol:**

Assemble context from creator.yaml + STATE.yaml, then REASON about output:

```
IF is_first_product:
  → Full journey map. Warm tone. "Your first product exists."
  → Show all 4 pipeline steps explicitly.
  → Use encouraging language: "I'll guide you through each step."

IF products_published >= 5:
  → Compact. "✦ {name} scaffolded. {N} files. /fill when ready."
  → Skip journey map (they know the pipeline).
  → Surface only non-obvious: portfolio position, domain intelligence.

IF scout_source exists:
  → Reference the research: "Scaffolded from your {domain} research. {gaps_found} gaps mapped."

IF same domain has existing products:
  → Surface composition: "This joins {existing_slugs} in your {domain} portfolio."

ALWAYS:
  → Use ux_type_name from ux-vocabulary.md (e.g., "Deep Intelligence" not "minds")
  → Brand frame: ✦ marker, MyClaude Studio box (for first product or guided mode)
  → Pipeline position: "scaffold → ▸ fill → validate → test → package → publish"
  → Clear next action: "/fill" (always the next step after create)
```

**Default frame (guided mode or first 3 products):**
```
┌─ MyClaude Studio ───────────────────────────┐
│  ✦ {product_name} — {ux_type_name}          │
│                                              │
│  {cognitive_insight based on context}        │
│                                              │
│  ▸ scaffold → fill → validate → test → ship │
│  Next: /fill                                │
└──────────────────────────────────────────────┘
```

**Compact frame (autonomous mode or 5+ products):**

For developers:
```
✦ {product_name} scaffolded. {N} files. {cognitive_insight}. /fill
```

For non-developers (profile.type != developer):
```
✦ {product_name} is ready. {N} files created. {cognitive_insight}. Add your expertise next → /fill
```

---

## .meta.yaml Template

Create `workspace/{product-slug}/.meta.yaml`:

```yaml
# Product metadata — not distributed, stripped during /package
product:
  slug: "{product-slug}"
  type: "{category}"               # skill|agent|squad|workflow|design-system|claude-md|application|system|bundle|statusline|hooks|minds|output-style
  created: "{YYYY-MM-DD}"
  mcs_target: "{MCS-1|MCS-2|MCS-3}"
  # NOTE: For type=minds, cap mcs_target at MCS-2 (Tier 3 DNA patterns are mostly N/A).
  # Show: "Minds ceiling is MCS-2 (Tier 3 DNA patterns not applicable). Setting target to MCS-2." (G015)
  # Minds-specific (only when type=minds):
  # minds_depth: "advisory|cognitive"
  # minds_sub_type: "self|genius|domain"  # cognitive only
  # genius_profile: "{name}"              # genius only

state:
  phase: "scaffold"                # scaffold | content | validated | packaged | published
  last_validated: null
  last_validation_score: null
  dna_compliance:
    tier1: null                    # 0-100
    tier2: null
    tier3: null
  overall_score: null
  last_tested: null
  test_result: null              # "pass" | "fail" | null
  test_scenarios: null           # "{passed}/{total}" | null

history:
  created_at: "{YYYY-MM-DD}"
  validated_at: []                 # append timestamps
  packaged_at: null
  published_at: null
  version: "1.0.0"

# Intelligence Layer fields (populated by /validate Stage 8, /scout, /package)
# Reference: references/intelligence-layer.md + config.yaml intelligence section
intelligence:
  domain: null                     # inferred from scout or content (e.g., "kubernetes-security")
  market_position: null            # blue_ocean | moderate | saturated
  value_score: null                # 0-12 composite (depth + uniqueness + coverage + market)
  value_score_breakdown: null      # { depth: N, uniqueness: N, coverage: N, market: N }
  suggested_price_range: null      # [min, max] USD
  pricing_strategy: null           # free | signal | solid | premium | rare
  distribution_channels: []       # ranked channels for this product type
  portfolio_role: null             # anchor | complement | extension | standalone
  scored_at: null                  # ISO-8601 timestamp of last intelligence computation
```

---

## Quality Gate

Generated scaffold must pass MCS-1 before being shown to the creator:
- All required files for the product type are present
- All required metadata fields are populated (even with placeholders)
- README.md skeleton contains: what it does, install, usage, requirements
- No syntax errors in any generated YAML or JSON
- `.meta.yaml` is valid and contains all required fields

---

## Anti-Patterns

1. **Generating content during scaffold** — /create generates structure only. Substantive prose, domain knowledge, examples: all /fill's job. Content here bypasses the Sparring Protocol → generic latão polido.
2. **Blocking on missing creator.yaml** — Always micro-onboard and continue.
3. **Overwriting without --force** — Never touch existing workspace products without explicit flag.
4. **Skipping brownfield check** — Always check same-type products before scaffolding.
5. **Skipping portfolio intelligence (step 9c)** — Domain grouping and bundle suggestions must fire when threshold is met.

---

## Decision Notes

**CE-D12:** WHY comments (`<!-- WHY: ... -->`) explain what the creator must fill in. Stripped during `/package`. Creators should NOT remove them — harmless in workspace.

**Pre-validate at scaffold time:** Starting at MCS-1 means creators never fix basics. Scaffold failures are bugs in the Scaffolder, not creator errors.

**Sub-command routing:** `/create skill` etc. skip the menu for experienced creators. Menu exists for first-time users who don't know the vocabulary.

**Scaffold vs content separation:** Content generated by /create bypasses /fill's Sparring Protocol → zero unique expertise. Structure (scaffold) and content (expertise) must stay separate. That separation is what makes the Engine produce gold.
