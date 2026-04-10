# Marketplace Ecosystem Wiring
**Version:** 1.0 | **Status:** Strategic reference | **Depends on:** config.yaml (intelligence, distribution), distribution-guide.md, /publish SKILL.md, install-spec.md, intelligence-layer.md

---

## Purpose

This document maps the complete Engine-to-Marketplace-to-End-User connection. It identifies what exists, what is missing, and what to build to close the gaps between product creation and sustained marketplace success.

---

## 1. Product Lifecycle Post-Publish

### Current State

The `/publish` skill runs a well-defined 9-step flow:

1. Summary display with version, price, MCS level
2. Explicit creator confirmation
3. CLI pre-flight (`myclaude validate`)
4. CLI publish (`myclaude publish` from `.publish/`)
5. State update (`.meta.yaml` phase -> "published")
6. Celebration report with install command and URL
7. Intelligent distribution plan (channel-specific copy-paste text)
8. Competitive context scan (`myclaude search`)
9. Profile XP reminder

**Where the product lives after publish:**
- Primary listing: `myclaude.sh/p/{slug}`
- Product page includes: description, MCS badge, install command, reviews
- Triple manifests enable cross-platform discovery: vault.yaml (MyClaude), plugin.json (Anthropic), agentskills.yaml (33+ platforms)

**How it is indexed:**
- vault.yaml fields: `name`, `type`, `tags`, `description`, `author`
- MCS level acts as a quality signal in search ranking
- Category assignment from `references/market/categories.md`

**Install flow** (`myclaude install @user/slug`):
- Files land at the `install_target` path defined in `config.yaml` per type:
  - Skills: `.claude/skills/{slug}/`
  - Agents/Minds: `.claude/agents/{slug}.md`
  - Squads: `.claude/squads/{slug}/`
  - Systems: `.claude/systems/{slug}/`
  - Hooks: `.claude/settings.local.json` (merged) + `~/.claude/hooks/{slug}/scripts/`
  - Output styles: `.claude/output-styles/{slug}.md`
  - Claude-md: `.claude/rules/{slug}.md` (manual copy required)
  - Statusline: `~/.claude/statusline-scripts/{slug}.sh`
  - Design system / Application: `myclaude-products/{slug}/`
  - Bundles: N/A (meta-package, installs components)

**Update flow:**
- Creator bumps version in `.meta.yaml`, re-packages, re-publishes
- Step 1c Version Bump Guard blocks same-version re-publish explicitly ("prevents 71+ users from receiving a silent no-change update")

### Gaps

- [ ] **No automatic update notification for end users.** When creator publishes v1.0.1, installed users have no push notification or changelog prompt. Users must manually run `myclaude update {slug}` or `myclaude update --all`. There is no "update available" signal in Claude Code sessions.
- [ ] **No CHANGELOG auto-generation.** Version bumps produce no structured changelog. The creator manually writes release notes or skips them entirely.
- [ ] **No semantic versioning enforcement.** `.meta.yaml` accepts any string as version. Breaking changes (major bump) vs patches are not distinguished in the update flow.
- [ ] **Review/rating system status unclear.** The distribution guide mentions "full product page with reviews" but no skill in the Engine generates or solicits reviews. No post-install prompt asks users to rate.
- [ ] **No install-count visibility for creators.** `config.yaml` intelligence layer references market awareness but provides no dashboard or CLI command to check install counts.

### Recommendations

- [ ] Add `myclaude updates --check` integration to `/status` — show available updates for installed products
- [ ] Build a `/changelog` utility skill that reads git log between version tags and generates `CHANGELOG.md`
- [ ] Define semver policy in `references/best-practices/versioning-guide.md` (if not already) and enforce major/minor/patch semantics in Version Bump Guard
- [ ] Document the review lifecycle: how to solicit, display, and respond to reviews on myclaude.sh
- [ ] Add `myclaude stats {slug}` to Step 9 of /publish so creators see install counts immediately

---

## 2. Intelligent Distribution Post-Publish

### Current State

`/publish` Step 7 generates a distribution plan with channel-specific copy-paste text for 13 channels. The channels are ranked by product type (config.yaml `intelligence.distribution.channels_by_type`). Each channel gets actionable text:

| Channel | Readiness |
|---------|-----------|
| myclaude | Automatic (already published) |
| awesome-claude-code | PR title provided, repo URL included |
| awesome-claude-skills | PR title provided, repo URL included |
| reddit | Post text with slug URL |
| twitter | Tweet text with hashtag |
| domain-community | Guidance to identify forum |
| linkedin | Professional post template |
| blog-post | Outline suggestion |
| discord | Guidance only |
| youtube | Guidance only |
| landing-page | Reference to /premium-lp |
| product-hunt | Guidance only |
| newsletter | Guidance only |

Step 8 runs a competitive scan showing top 5 products in the same category with download counts.

### Gaps

- [ ] **No GitHub release integration.** The Engine does not create a GitHub release, tag, or upload the `.publish/` contents as a release asset. Creators who maintain GitHub repos must do this manually.
- [ ] **No social card / OG image generation.** When sharing a myclaude.sh/p/{slug} link on Twitter/LinkedIn/Discord, the social preview depends entirely on myclaude.sh server-side rendering. The Engine provides no local preview or image asset.
- [ ] **No analytics dashboard reference.** The intelligence layer describes market awareness and value signals, but there is no `myclaude analytics` or `myclaude stats` command documented. Creators cannot monitor installs, usage patterns, or conversion from free to paid.
- [ ] **Distribution plan is ephemeral.** The channel-specific text appears once in the publish output and is not persisted to a file. If the creator's terminal scrolls past it or they close the session, it is gone.
- [ ] **Channels are not truly copy-paste ready for all cases.** "blog-post", "youtube", "discord", "newsletter", and "landing-page" are guidance, not actionable text. Only 7 of 13 channels produce immediately pasteable content.
- [ ] **No post-publish tracking.** After the creator shares on Reddit or Twitter, there is no way to record which channels were actually used or measure which channel drove installs.

### Recommendations

- [ ] Add a `/release` skill or `/publish --github` flag that creates a GitHub release with tag, changelog, and `.publish/` as artifact
- [ ] Persist the distribution plan to `workspace/{slug}/distribution-plan.md` so it survives session end
- [ ] Upgrade guidance-only channels to template-ready: provide draft blog post outline, YouTube script skeleton, Discord message template
- [ ] Document `myclaude stats` / `myclaude analytics` commands (or flag as marketplace platform TODO if they do not exist yet)
- [ ] Add a distribution checklist to `.meta.yaml` that tracks which channels the creator has posted to

---

## 3. Cross-Product Composition

### Current State

The Engine already has composition awareness:
- `config.yaml` intelligence layer: `portfolio.bundle_suggestion_threshold: 3` (products in same domain -> suggest bundle)
- `intelligence.portfolio.composition_alert: true` (alert when skill+minds in same domain compose well)
- `/publish` Step 7d: portfolio distribution intelligence distinguishes "anchor" vs "complement" products
- `references/composition-anatomy.md` documents how products compose
- Bundle type exists with composition integrity validation (Stage 7d)
- Distribution guide Layer 2: cross-product discovery graph linking to `myclaude.sh/explore?category={cat}`

### Gaps

- [ ] **Bundle discovery is passive.** The threshold and alert are defined in config but no skill actively scans workspace/ and says "you have 3 security products, want to create a bundle?" The trigger exists in engine-proactive.md but the actual nudge timing is unclear.
- [ ] **No system composition suggestion.** When a creator has skill + minds + hooks in the same domain, no proactive suggests "these could be a system." The config mentions `composition_alert` but the implementation path from alert to actionable suggestion is not documented.
- [ ] **No portfolio page reference.** `myclaude.sh/u/@username` as a portfolio page is not referenced anywhere in the Engine. Creators do not know it exists (if it does) or how to curate it.
- [ ] **No cross-reference generation in READMEs.** "Works great with [aegis](myclaude.sh/p/aegis)" style cross-links are not injected by `/package` or suggested by `/fill`. The distribution guide mentions Layer 2 (discovery graph) but this is a marketplace-side feature, not a product-side feature.
- [ ] **No composition manifest.** When products compose well, there is no structured way to declare "this skill is designed to work with these other products" beyond free-text in README.

### Recommendations

- [ ] Wire the bundle suggestion proactive: when `/status` detects 3+ products in same domain tag, surface "Consider bundling these into a single installable package with `/create bundle`"
- [ ] Wire the system suggestion proactive: when workspace/ contains skill + minds (or skill + hooks) sharing a domain tag, surface the composition opportunity
- [ ] Add `portfolio_url` field to `creator.yaml` and display it in `/publish` Step 6: "Your portfolio: myclaude.sh/u/@{username}"
- [ ] Add a `composes_with` field to vault.yaml spec — list of slugs this product is designed to work alongside
- [ ] During `/fill`, when composability section is reached, scan workspace/ for same-domain products and suggest cross-references with `myclaude.sh/p/{slug}` links
- [ ] During `/package`, inject cross-reference links into README composability section if `composes_with` is populated

---

## 4. Quality Signals in Marketplace

### Current State

The Engine generates several quality signals:
- **MCS badge:** `https://myclaude.sh/badge/mcs/{level}.svg` — injected into README footer by `/package` (config.yaml `vault_defaults.badges.mcs`)
- **"Available on MyClaude" badge:** `https://myclaude.sh/badge/available.svg` — injected into README footer (config.yaml `vault_defaults.badges.available`)
- **Attribution comment:** `<!-- Published on MyClaude (myclaude.sh) | Quality: MCS-{level} -->` — injected into primary product file
- **Engine provenance:** vault.yaml carries `engine: myclaude-studio-engine` — identifies products built with the Studio Engine
- **Locale-adaptive clause:** runtime contract with marker lines signals engineering rigor
- **Triple manifest backlinks:** vault.yaml + plugin.json + agentskills.yaml all link to myclaude.sh/p/{slug}

### Gaps

- [ ] **MCS badge not confirmed visible in marketplace listing.** The badge is generated for README but whether myclaude.sh renders it prominently on the product page (above the fold, next to title) is a platform question, not an Engine question. No specification exists for marketplace-side badge rendering.
- [ ] **No install count badge.** Social proof through install count (e.g., "500+ installs") is not available as a badge or marketplace display element.
- [ ] **No "Made with Studio Engine" trust signal.** The `engine: myclaude-studio-engine` field in vault.yaml is machine-readable but not rendered as a visible badge or listing tag. Products built with the Engine should visually stand out as quality-validated.
- [ ] **No verified creator badge.** No mechanism to verify creator identity beyond `myclaude whoami`. Verified status (e.g., linked GitHub account, published 5+ products) is not surfaced.
- [ ] **Source language not visible.** The locale-adaptive clause ensures output mirrors user language, but the product's source language (from creator.yaml) is not displayed in the listing. Users cannot filter by language.
- [ ] **No baseline delta visibility.** Stage 7c computes how much value the product adds vs Claude vanilla, but this score is not surfaced in the marketplace listing. "Addresses 8 knowledge gaps Claude misses" would be a powerful quality signal.

### Recommendations

- [ ] Define a marketplace badge spec: which badges appear on the product listing page, their position, and rendering rules
- [ ] Add `install_count` badge URL to `vault_defaults.badges`: `https://myclaude.sh/badge/installs/{slug}.svg`
- [ ] Add "Built with Studio Engine" badge: `https://myclaude.sh/badge/engine.svg` — injected by `/package` when `engine` field is present
- [ ] Design verified creator tiers: (1) email verified, (2) GitHub linked, (3) 5+ published products, (4) 100+ total installs. Surface tier as badge on listings.
- [ ] Add `source_language` field to vault.yaml and marketplace search filters
- [ ] Surface baseline delta score in marketplace listing as "Covers N gaps Claude misses" when Stage 7c data is available
- [ ] Add MCS level as a marketplace search filter: users can filter "MCS-2+" or "MCS-3" products

---

## 5. End-to-End Flow Summary

```
Creator                          Engine                         Marketplace                    End User
───────                          ──────                         ───────────                    ────────
/create + /fill          ->  workspace/{slug}/
/validate                ->  MCS score + intelligence
/package                 ->  .publish/ (vault + plugin + agentskills + README)
/publish                 ->  myclaude publish ─────────->  myclaude.sh/p/{slug}
                             distribution plan              indexed, searchable
                             competitive context             badges rendered
                                                            reviews collected
                                                                                    ->  myclaude install {slug}
                                                                                        files land at install_target
                                                                                        product active in Claude Code
                                                            
                                                            [UPDATE CYCLE]
                                                                                    ->  myclaude update {slug}
                                                                                        new version installed
                                                            
                             [GAPS IN FLOW]
                             No auto-changelog               No update push notification     No "update available" signal
                             No GitHub release                No install count badge          No review prompt post-install
                             Distribution plan ephemeral      No verified creator badge       No language filter
                             No composition manifest          No baseline delta display       No cross-product suggestions
```

---

## 6. Priority Matrix

| Gap | Impact | Effort | Priority |
|-----|--------|--------|----------|
| Persist distribution plan to file | High (prevents data loss) | Low | P0 |
| CHANGELOG auto-generation | High (user trust) | Medium | P1 |
| GitHub release integration | High (distribution reach) | Medium | P1 |
| Bundle/system suggestion proactives | High (revenue, composition) | Medium | P1 |
| Install count visibility for creators | High (motivation) | Low (CLI) | P1 |
| Cross-reference injection in READMEs | Medium (discovery) | Low | P2 |
| Portfolio page reference | Medium (creator identity) | Low | P2 |
| "Made with Studio Engine" badge | Medium (trust) | Low | P2 |
| Verified creator tiers | Medium (trust) | High | P2 |
| Post-install review prompt | Medium (social proof) | Medium | P3 |
| Upgrade guidance channels to templates | Low (convenience) | Medium | P3 |
| Distribution channel tracking | Low (analytics) | High | P3 |
