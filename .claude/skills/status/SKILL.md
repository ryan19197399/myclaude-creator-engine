---
name: status
description: >-
  Display Studio Engine status dashboard. Shows version, edition, creator profile,
  products with scores, and stale warnings. Use when: 'status', 'dashboard', 'show my
  products', or at session start.
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Status Dashboard

Display comprehensive engine status in a compact terminal-style dashboard.

**When to use:** Session start, or anytime the creator wants a status overview.

---

## Activation Protocol

### SESSION-START VALUE (automatic on first /status)

Before displaying the dashboard, scan for actionable intelligence:

1. **Stale products**: Any product with `last_validated` > 30 days ago → surface with warning
2. **Next action**: For each product in non-terminal state, suggest the logical next command:
   - scaffold → "Run /fill to add content"
   - content → "Run /validate to check quality"
   - validated → "Run /package to bundle for distribution"
   - packaged → "Run /publish to ship to marketplace"
3. **Score trajectory**: If score_history exists in .meta.yaml, show trend arrow (↑↓→)
4. **Creator pattern insight**: If usage.common_dna_gaps has entries, surface: "Tip: D{N} ({name}) is your most common gap. [link to structural-dna.md section]"

This transforms /status from a passive dashboard into an active coaching surface.

---

1. Read `STATE.yaml` — engine version, edition, last session, workspace state
2. Read `creator.yaml` — creator name, type, expertise domains. If missing, show "Creator: not configured — run /onboard" in dashboard and continue with available data.
3. Glob `workspace/*/` — list all product directories
4. For each product, read `.meta.yaml` — slug, type, state, scores, timestamps
5. Detect edition: glob `.claude/skills/forge-master/SKILL.md`
   - Found → PRO edition
   - Not found → LITE edition
6. Render dashboard

---

## Dashboard Format

**CRITICAL — UX Stack (load in order before rendering):**
1. `references/ux-experience-system.md` §1 Context Assembly — build creator context from creator.yaml + STATE.yaml + all .meta.yaml files
2. `references/ux-experience-system.md` §2 Tact Engine — adapt dashboard depth and tone to creator level + journey position
3. `references/ux-vocabulary.md` — translate all internal terms (MCS→tiers, DNA→invisible, types→human names)
4. `references/quality/engine-voice.md` — apply Brand DNA (✦ marker, box frames, Master Craftsperson voice)

**Cognitive rendering:** /status is the ENGINE'S FACE — it's where creators form their relationship with myClaude. Apply §5 Identity Reinforcement and §3.2 Portfolio Progress from the experience system. For beginners, this is encouragement. For experts, this is strategic intelligence. Same data, different lens.

```
┌─────────────────────────────────────────────┐
│  ✦ MyClaude Studio Engine v{version}        │
│  Creator: {name} | {total} products built   │
│  {published} live on marketplace             │
└─────────────────────────────────────────────┘

YOUR PRODUCTS
  ✦ {display_name}  {ux_type_name}  {ux_tier} {stars}  {state_emoji}
  # ux_type_name from ux-vocabulary.md (e.g., "Deep Intelligence" not "minds cognitive")
  # ux_tier: "Verified ✓" / "Premium ★★" / "Elite ★★★" (not MCS-1/2/3)
  # state_emoji: 🟢 live | 📦 ready to ship | ✏️ in progress | 🔨 just started

  Example:
  ✦ K8s Security Advisor   Deep Intelligence   Premium ★★   🟢 live
  ✦ AEGIS                  Tool                Elite ★★★    🟢 live
  ✦ NOCTIS                 Complete Setup      Elite ★★★    📦 ready

{if any product needs attention}
NEXT STEPS
  {slug}: {human_action} — {why_it_matters}
  # Examples:
  # "k8s-hardening: Add your expertise → /fill"
  # "my-tool: Ready to go live → /publish"
{/if}

{if stale > 0}
💡 {stale} product(s) haven't been touched in 30+ days. Want to revisit?
{/if}

QUICK ACTIONS
  /create  — Build something new
  /scout   — Research a domain first
  /explore — See what's on the marketplace
```

**Technical details (appended only if creator.yaml technical_level == "expert"):**
```
Technical: {total_validated}/{total} validated | Pitfalls: {pitfall_count} tracked
```

### Portfolio Intelligence Section

After the main dashboard and before the CLI marketplace section, compute and display portfolio intelligence. Reference: `references/intelligence-layer.md` + `config.yaml → intelligence`.

**Data gathering:**
1. For each product in workspace, read `.meta.yaml → intelligence` fields (if present)
2. Group products by `intelligence.domain` (fall back to inferring domain from slug/type if not set)
3. Read `config.yaml → intelligence.portfolio` for thresholds

**Portfolio Vision display:**

```
PORTFOLIO VISION
  Domains: {N} covered
  {For each domain, sorted by product count desc:}
    {domain}: {product_count} products ({types_list})
      {If product_count >= bundle_suggestion_threshold: "→ Bundle opportunity: combine these into a {domain} suite"}
      {If domain has skill + minds: "→ Composition: {minds_slug} advises, {skill_slug} executes"}
  
  {If any domain has coverage < coverage_threshold:}
  GAPS
    {domain}: {coverage}% coverage — {suggestion based on missing types}

  {If any product has intelligence.value_score:}
  VALUE MAP
    {slug}: {value_score}/12 → ${range[0]}-${range[1]} ({strategy})
    ...
    Portfolio total estimated value: ${sum of midpoint prices}
    Revenue-generating: {count with price > 0}/{total published}
```

**Intelligence rules for portfolio analysis:**
- 3+ products in same domain AND no bundle → suggest bundle composition
- skill + minds in same domain → suggest cross-reference in README
- 2+ squads with overlapping agent names → suggest consolidation or orchestrator
- Domain with only 1 product type → suggest complementary type ("You have a {type} for {domain}. A {complementary_type} would complete the coverage.")

**Complementary type suggestions:**
| Has | Suggest |
|-----|---------|
| minds only | skill ("an executor for the advisor's recommendations") |
| skill only | minds ("an advisor to guide when/how to use the skill") |
| skill + minds | workflow ("orchestrate them into a sequence") |
| 3+ individual products | bundle ("package for complete domain coverage") |

**Display only when data exists.** If no product has intelligence fields populated, show a minimal note:
```
PORTFOLIO
  Run /validate --level=2 on products to unlock value intelligence.
```

This transforms /status from a passive list into an active strategic surface that reveals portfolio patterns the creator hasn't noticed.

### Trajectory Display

| Trend | Symbol | When |
|-------|--------|------|
| Improving | `+{N}%` | Current > previous score |
| Stable | `={score}%` | Current == previous |
| Declining | `-{N}%` | Current < previous (flag with warning) |
| New | `(new)` | Only 1 score entry |

### State Display Rules

| State | Display | Color Hint |
|-------|---------|------------|
| scaffold | `scaffold` | dim |
| content | `content` | default |
| validated | `validated` | green |
| packaged | `packaged` | cyan |
| published | `published vX.Y.Z` | gold |
| stale | append ` (stale)` | warning |

### CLI Marketplace Intelligence (if myclaude available)

After the main dashboard, if `myclaude` CLI is in PATH, display marketplace context:

```bash
# Run silently, don't block dashboard if CLI unavailable
myclaude my-products --json 2>/dev/null
```

If successful, append to dashboard:

```
MARKETPLACE (@{username})
  Published: {count} products | Downloads: {total_dl} | Revenue: {revenue}
  {For top 3 by downloads:}
  {slug}: {downloads} downloads {if rating: "★{rating}"}
  
  Run: myclaude trending     — see what's hot
  Run: myclaude stats {slug} — detailed product analytics
```

If CLI not in PATH or not authenticated, show:

```
MARKETPLACE
  Install myclaude CLI for marketplace intelligence: npm i -g @myclaude-cli/cli
```

**Per-product stats enrichment:** For each published product in workspace, run `myclaude stats {slug} --json 2>/dev/null`. If successful, append to the product's WORKSPACE line:
```
  {slug}  [{type}]  published  MCS-{level}  {score}%  📊 {downloads}dl {likes}❤ ${revenue}
```

**Profile level:** Run `myclaude profile pull --json 2>/dev/null` (if available). Display creator level:
```
CREATOR: {name} | @{username} Level {level} ({xp} XP) | {followers} followers
```

**Notifications:** Run `myclaude notifications --json 2>/dev/null`. If any new activity since last check:
```
ACTIVITY: {count} new since last session
  {latest notification summary}
```

This surfaces real marketplace data inside the Engine — creators see their impact without leaving Claude Code.

---

## Anti-Patterns

1. **Verbose status** — Keep it compact. One line per product. No essays.
2. **Stale data** — Always read fresh from files. Never cache.
3. **Missing files** — If STATE.yaml or creator.yaml missing, say so clearly and suggest /onboard.
4. **Empty workspace** — If no products, show: "Workspace empty. Run /create to start your first product."
5. **Broken meta** — If .meta.yaml is malformed, show product with `[error]` state, don't crash.
