# Changelog

All notable changes to the MyClaude Studio Engine.

## [3.0.0] — 2026-04-10

### Added
- **Intent topology** — products declare cognitive intent (advisory, procedural, generative, analytical, creative) that shapes validation criteria and structural expectations
- **10 validation stages** (was 7+1) — Stage 0: Intent Coherence, Stage 1: Structural, Stage 2: Integrity, Stage 3-5: DNA Tiers 1-3, Stage 6: CLI Preflight, Stage 7: Anti-Commodity, Stage 8: Value Intelligence, Stage 9: Voice Coherence
- **Voice coherence validation** (Stage 9) — detects persona leakage, tone inconsistency, register drift across product sections
- **Intent coherence validation** (Stage 0) — verifies the product delivers what the creator set out to build
- **Fill protocol reference** — structured content-filling guide loaded on-demand by `/fill`
- **Onboard protocol reference** — extended onboarding flow with 8 persona adaptation paths
- **GitHub issue templates** — migrated from markdown to YAML forms (bug report, feature request, friction report)
- **GitHub funding** — FUNDING.yml for sponsorship support
- **Organization profile** — `.github/profile/README.md` for the myclaude-sh org
- **Plugin manifest** — `.claude-plugin/marketplace.json` for structured marketplace discovery
- **README product template** — `templates/readme/README.md.template` with 13-section blueprint
- **CLI references** — `references/cli-commands.md`, `references/cli-contract.md`, `references/marketplace-ecosystem.md`
- **System product template** — `templates/system/SYSTEM.md.template`

### Changed
- **Validation stages decomposed** — monolithic `validation-stages.md` split into 10 individual stage files with dedicated index
- **Create router expanded** — product creation routing with deeper type-specific guidance (+386 lines)
- **Status skill rewritten** — richer dashboard with portfolio analytics (+264 lines)
- **Package skill hardened** — README quality gate added before badge injection, advisory warnings for missing sections
- **Publish skill expanded** — enhanced pre-flight checks and confirmation flow
- **Import skill refined** — better type detection and `.meta.yaml` generation
- **Onboard skill refined** — deeper persona profiling with protocol reference
- **13 blindspots resolved** — pipeline hardening across create, fill, validate, and package
- **Version drift aligned** — all version references consolidated to v3.0.0
- **`.gitignore` hardened** — internal docs, beta data, distillation artifacts, session notes fully excluded
- **Structural DNA Pattern 10** (README) — expanded from 4 generic sections to 13-section tiered structure with trilingual support (EN/PT-BR/ES)
- **CLI version references** updated from 0.8.4 to 0.9.0
- **CLI contract wired into all 9 skills** — every skill that invokes `myclaude` CLI now references `references/cli-contract.md` with per-skill severity maps (blocking/warning/silent-skip) and context-dependent escalation rules
- **`/think` permission fix** — added missing `Bash(myclaude *)` permission (had marketplace commands but no tool access)
- **CLI contract expanded** — severity table updated with escalation rules, 5 missing commands added (`--version`, `install`, `my-products`, `profile sync`, `setup-mcp`), conventions section completed

### Removed
- Legacy GitHub issue templates (markdown format, replaced by YAML forms)

## [2.2.0] — 2026-04-06

### Added
- **Public documentation suite** — README rewritten, getting-started guide, persona guides (developers, domain experts, teams), command reference, product types reference, quality system reference, FAQ
- **Agent discoverability** — `.claude-plugin/marketplace.json`, `llms.txt`, HTML metadata in README
- **SVG logo** — dark/light mode support via `<picture>` element
- **UX Experience System** — cognitive experience protocol with tact engine, sfumato celebrations, ASCII identity
- **UX Vocabulary** — non-developer translation layer for all engine output
- **Token efficiency modes** — eco, balanced, unlimited with proactive priority tiers (P0/P1/P2)
- **19 proactive behaviors** — pipeline guidance, confusion detection, language mirroring, stale nudges, first-time WOW moment, intelligent error recovery
- **First-time experience** — welcome frame, auto-onboard, personalized next step by profile type
- **Quick mode** — `--quick` flag for experienced creators (auto-triggers with 5+ products)
- `/scout` skill — domain research before building (gap analysis, marketplace scan, recommendations)
- `/think` skill — brainstorm and evaluate before committing
- `/explore` skill — marketplace search and competition analysis
- `/aegis` skill — security audit (STRIDE, vulnerability detection, compliance)

### Changed
- **15 skills** total (was 11)
- **20 DNA patterns** (was 18) — added Attention-Aware Authoring and Cache-Friendly Design
- **13 product types** (was 12) — added output-style
- **8 persona types** for creator adaptation (was 3)
- Engine voice system with dual signatures (developer / non-developer)
- Validation expanded to 8 stages + 3 sub-stages
- `.gitignore` hardened for public release — all personal/session/workspace data excluded

## [2.1.0] — 2026-04-02

### Added
- **Intelligence layer** — market awareness, value signals, portfolio vision, distribution strategy
- **Value Intelligence** (validation stage 8) — pricing, market position, portfolio role analysis
- **Scout methodology** — 5-phase domain research with baseline delta computation
- **Friction system** — institutional memory from real usage (13 tracked frictions)
- **Meta-learning registry** — 26 codified principles from 100+ sessions

### Changed
- Validation scoring includes value intelligence as advisory stage
- `/validate` supports `--batch` mode for portfolio-wide checks
- Scout reports feed directly into `/create` and `/fill`

## [2.0.0] — 2026-03-28

### Added
- **Structural DNA system** — 18 patterns in 3 tiers with validation checks (`structural-dna.md`)
- **Product DNA files** — 9 type-specific DNA requirement files (`product-dna/*.yaml`)
- **Quality gates** — state machine: scaffold→content→validated→packaged→published (`quality-gates.yaml`)
- **MCS v2 scoring** — DNA-based formula: `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
- `/map` skill — domain knowledge extraction with structured output
- `/fill` skill — guided content filling (replaces `/create-content`)
- `/status` skill — engine dashboard with workspace overview
- `/help` skill — command reference with edition detection
- `/test` skill — worktree-isolated sandbox testing (3 scenarios)
- **LITE/PRO edition detection** — glob `.claude/skills/forge-master/` in boot
- **Dual manifest generation** — `/package` creates both vault.yaml + plugin.json
- **WHY comments** — templates use `<!-- WHY: D{N} -->` format (stripped by `/package`)

### Changed
- `CLAUDE.md` rewritten to <200 lines with lean boot, edition detection, skill routing
- `config.yaml` rebuilt with MCS scoring weights, 9 product routes, feature flags, validation pipeline
- `STATE.yaml` redesigned with workspace product tracking and MCS results
- `README.md` updated for v2.0 — new architecture, DNA system, editions
- `/validate` evolved — 7-stage DNA pipeline, product-dna/ loading, DNA scoring formula
- `/create` evolved — DNA injection, product-dna/ refs, `/fill` reference
- `/package` rewritten — dual manifests (vault.yaml + plugin.json), SHA-256 checksum
- `/publish` rewritten — lean CLI delegation (~100 lines)
- `/onboard` updated — `.meta.yaml` refs
- Template comments migrated from `GUIDANCE:` to `WHY:` format (9 templates)
- `.engine-meta.yaml` bumped to v2.0.0
- All `.engine-meta.yaml` references → `.meta.yaml` (PRD v2.0 naming)

### Removed
- `/create-content` (replaced by `/fill`)
- `/quick-skill` (streamline: use individual commands)
- `/quick-publish` (streamline: use `/package` then `/publish`)
- `/engine-status` (replaced by `/status`)
- `/engine-help` (replaced by `/help`)
- `/differentiate` (moved to PRO Quality Sentinel agent)
- `/quality-review` (moved to PRO Quality Sentinel agent)
- `/domain-consult` (moved to PRO Domain Cartographer agent)
- `/market-scan` (moved to PRO Market Scout agent)
- `/packaging-review` (absorbed into `/package`)
- `/my-products` (moved to PRO Market Scout agent)
- `references/caching-strategy.md` (obsolete)
- **Net: 11 skills killed, 22 files removed, ~4,257 lines deleted**

## [1.1.0] — 2026-03-26

### Added
- `/create-content` skill — guided content filling after scaffold
- `/package` skill — standalone packaging without publishing
- `/test` skill — sandbox testing against sample inputs
- `/engine-status` skill — dashboard with profile, workspace, stale builds
- `/engine-help` skill — complete command listing
- `/quick-skill` skill — idea-to-marketplace pipeline shortcut
- `/quick-publish` skill — validate-to-publish pipeline shortcut
- `/differentiate` skill — anti-commodity coaching
- `/quality-review` skill — deep MCS-3 quality audit
- Exemplar-first experience in `/create`
- Guided iteration in `/validate`

### Changed
- All skills migrated to Anthropic Agent Skills spec
- Skills renamed for natural invocation
- MCS-spec aligned with validator checks

### Removed
- Legacy `skills/` and `agents/` directories at project root
- Redundant `.claude/commands/` wrappers

## [1.0.0] — 2026-03-25

### Added
- Initial release — 4 core skills, 5 cognitive agents, 9 product specs, 9 templates, 9 exemplars
- MCS 3-tier quality system
- CONDUIT v2 vault.yaml manifest integration
- MyClaude CLI publishing support
