---
name: publish
description: >-
  Publish a packaged product to myclaude.sh via the CLI. Shows summary,
  requires confirmation, runs myclaude validate + myclaude publish.
  Use when the creator says "publish", "ship it", "go live", or after /package.
argument-hint: "[product-slug]"
allowed-tools:
  - Read
  - Bash(myclaude *)
  - AskUserQuestion
---

# Publisher

Publish a packaged product to the MyClaude marketplace via CLI delegation.

**When to use:** After /package has staged .publish/ directory.

**When NOT to use:** If product hasn't been packaged yet (run /package first).

---

## Activation Protocol

1. Identify product: `$ARGUMENTS` as slug → `workspace/{slug}/`
2. Read `.meta.yaml` → verify state is "packaged"
3. Verify `.publish/` exists with vault.yaml
4. Check CLI: `which myclaude` — if not found, show install instructions
5. Check CLI auth: run `myclaude whoami` — if "not logged in", show: "Not authenticated. Run `myclaude login` first." and stop.
6. Read `creator.yaml` → load author metadata. If missing — "Creator profile not found. Run `/onboard` first." and stop.
7. **Load voice identity**: Read `references/quality/engine-voice.md` → use publish celebration format. "Published to myclaude.sh — live now." + install command + distribution vector note. Brief, proud, specific.

---

## Core Instructions

### PUBLISH FLOW

**Step 1 — Summary**

Display what will be published:

```
Ready to publish:

  Name:     {displayName}
  Slug:     {slug}
  Type:     {type}
  Version:  {version}
  Price:    {price == 0 ? "Free" : "$" + price}
  License:  {license}
  MCS:      {level} ({score}%)
  Files:    {N} in .publish/

Publish to myclaude.sh? (yes/no)
```

**Step 1b — Type-Specific Constraints**

If `type` is `claude-md`, append this note to the summary display before asking for confirmation:

```
Note: Rules files (.claude/rules/) cannot be auto-installed via the plugin system.
Buyers must manually copy the rules file to ~/.claude/rules/ or .claude/rules/ in
their project. Include this instruction in your README.md.
```

**Step 2 — Confirmation**

Wait for explicit "yes" from creator. Do NOT proceed without confirmation.

**Step 3 — CLI Pre-flight**

```bash
cd workspace/{slug}/.publish && myclaude validate --json 2>/dev/null
```

Parse JSON result. If exit code != 0 or JSON parse fails, report: "CLI validation failed or unavailable. Verify manually or run `/validate` first." and abort.

**Step 4 — Publish**

```bash
cd workspace/{slug}/.publish && myclaude publish
```

Report CLI output verbatim.

**Step 5 — Update State**

On success:
```yaml
# .meta.yaml updates
state:
  phase: "published"
  published_at: "{ISO timestamp}"
  version: "{version}"
```

**Step 6 — Report**

**UX Stack (load before rendering report):**
1. `references/ux-experience-system.md` §1 Context Assembly + §2.3 Moment Awareness (publish = peak emotion, scaled by journey) + §4.1 Celebration Triggers + §5.1 Creator Journey Narrative
2. `references/ux-vocabulary.md` — translate all terms
3. `references/quality/engine-voice.md` — Brand DNA + signature patterns for publish

**Cognitive rendering:** /publish is the HIGHEST EMOTION moment in the pipeline. But emotion scales with journey position:
- **First publish ever**: Full celebration. Identity moment. "Your first product is live. You're a creator now." Show the full distribution plan.
- **2nd-5th publish**: Warm but briefer. "Another one live. Portfolio growing." Focus on portfolio composition.
- **6th+ publish**: Peer observation. Surface only the non-obvious: market position, competitive context, portfolio gap that just closed.
- **Always**: The install command (`myclaude install {slug}`) is the most satisfying line — it makes the product REAL. Feature it prominently.
- **Brand moment**: This is where the creator's identity fuses with the myClaude ecosystem. Their product, our platform, shared universe.

```
Published! {displayName} v{version} is live on myclaude.sh

  URL:     https://myclaude.sh/p/{slug}
  Install: myclaude install {slug}
  MCS:     {mcs_level} ({score}%)
  Platforms: MyClaude + Anthropic Plugin + 33 Agent Skills platforms
```

**Step 7 — Intelligent Distribution** (Intelligence Layer integration)

After successful publish, generate a distribution plan informed by the Intelligence Layer. Reference: `config.yaml → intelligence.distribution` + `references/intelligence-layer.md`.

**7a. Load intelligence context:**
Read `.meta.yaml → intelligence` fields. Extract: `value_score`, `pricing_strategy`, `distribution_channels`, `market_position`, `portfolio_role`.

**7b. Free-vs-paid reflection:**
If price == 0 AND `value_score >= 5`:
```
Pricing note: Your product scores {value_score}/12 — you chose free distribution.
  {If first in domain: "Smart move. Free builds authority in a new domain."}
  {If not first: "Consider a paid tier for your next product in {domain} — you've built presence."}
```
If price > 0:
```
Premium positioning: ${price} for {pricing_strategy}-tier product.
  Ensure your README clearly communicates the value proposition.
  Users who need {domain} expertise will pay for verified quality (MCS-{level}).
```

**7c. Intelligent channel ranking:**
Read `config.yaml → intelligence.distribution.channels_by_type.{type}`. Display channels ranked by impact for this product type, with specific actionable instructions:

```
Distribution plan for {slug} ({type}):

  {For each channel in channels_by_type[type], ranked:}
  {rank}. {channel_name}
     {channel-specific copy-paste text — see below}
```

**Channel-specific copy (all directly copy-pasteable):**

| Channel | Copy Template |
|---------|--------------|
| myclaude | "Live at myclaude.sh/p/{slug}" (already done) |
| awesome-claude-code | PR title: "Add {displayName}" → github.com/hesreallyhim/awesome-claude-code |
| awesome-claude-skills | PR title: "Add {displayName}" → github.com/travisvn/awesome-claude-skills |
| reddit | "I just published {displayName} — {description}. {Free/price} on myclaude.sh/p/{slug}" |
| twitter | "Just shipped {displayName} for Claude Code. {one-line-description} myclaude.sh/p/{slug} #ClaudeCode" |
| domain-community | "Identify the top forum/subreddit for {domain}. Post: '{displayName} — {description}'" |
| linkedin | "For {domain} professionals: {displayName} brings {capability} to Claude Code. myclaude.sh/p/{slug}" |
| blog-post | "Write a walkthrough: problem → how {slug} solves it → architecture → install" |
| discord | "Share in Claude Code community Discord with usage example" |
| youtube | "Record 3-min walkthrough showing before/after with {slug}" |
| landing-page | "Build a landing page for premium bundles — /premium-lp can help" |
| product-hunt | "Launch on Product Hunt for comprehensive bundles — coordinate with community" |
| newsletter | "Pitch to domain-specific newsletters covering {domain}" |

**7d. Portfolio distribution intelligence:**
If `portfolio_role` is "anchor" (first in domain): "This is your anchor product in {domain}. Building visibility here creates a funnel for future {domain} products."
If `portfolio_role` is "complement" or "extension": "Cross-promote with your existing {domain} products: {list existing slugs}. Users who install one likely need the others."

**Step 8 — Competitive Context** (post-publish intelligence)

After successful publish, run competitive scan silently:

```bash
myclaude search --category {type_category} --sort downloads --limit 5 --json 2>/dev/null
```

If successful, display:

```
Competitive landscape ({type}):
  #1. {name} by @{author} — {downloads} downloads
  #2. {name} by @{author} — {downloads} downloads
  #3. {name} by @{author} — {downloads} downloads
  
  Your product: {slug} (newly published)
  Tip: differentiate by {suggestion based on top products' descriptions}
```

This gives creators immediate market awareness — they see who they're competing with the moment they ship. Skip silently if CLI unavailable or search returns no results.

**Step 9 — Profile XP Update**

After publish, remind: "Your marketplace XP increases with each publish. Run `myclaude profile pull` to see your updated level."

Rules:
- {displayName} = from vault.yaml `display_name` or humanized `name`
- {description} = from vault.yaml `description` (first sentence only if >100 chars)
- {slug} = from vault.yaml `name`
- {type} = from vault.yaml `type`
- {price} = "Free" if 0, else "$X" from vault.yaml `price`
- This prompt is INFORMATIONAL — does not block the flow or require interaction
- Every line is immediately copy-pasteable

---

## CLI Not Found

If `myclaude` CLI is not installed:

```
MyClaude CLI not found. Install it:
  npm install -g @myclaude-cli/cli

Then run /publish again.

Alternative: upload manually at myclaude.sh/publish
```

---

## Anti-Patterns

1. **Publishing without confirmation** — Always require explicit "yes".
2. **Publishing unpackaged product** — Check .meta.yaml state first.
3. **Swallowing CLI errors** — Report all CLI output, don't hide failures.
4. **Re-publishing without version bump** — If already published, require version increment.
5. **Publishing with secrets** — CLI pre-flight catches this, but mention it if found.
