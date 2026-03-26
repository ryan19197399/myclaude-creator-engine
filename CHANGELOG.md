# Changelog

All notable changes to the myClaude Creator Engine.

## [1.1.0] — 2026-03-26

### Added
- `/create-content` skill — guided content filling after scaffold, adapts by creator type
- `/package` skill — standalone packaging without publishing
- `/test` skill — sandbox testing against sample inputs
- `/engine-status` skill — dashboard with profile, workspace, stale builds
- `/engine-help` skill — complete command listing
- `/quick-skill` skill — idea-to-marketplace pipeline shortcut
- `/quick-publish` skill — validate-to-publish pipeline shortcut
- `/differentiate` skill — anti-commodity coaching (Porter + Godin + Ries)
- `/quality-review` skill — deep MCS-3 quality audit (Feathers + Deming + Popper)
- Exemplar-first experience in `/create` — shows MCS-3 reference before building
- Guided iteration in `/validate` — drafts domain-aware fixes, not just reports failures
- Description optimization in `/publish` — reviews descriptions for marketplace discoverability
- Pricing guidance in `/publish` — shows category benchmarks from pricing guide
- Progressive disclosure for cognitive agents — SKILL.md < 150 lines + references/

### Changed
- All skills migrated to Anthropic Agent Skills spec (`.claude/skills/{name}/SKILL.md` with frontmatter)
- Skills renamed for natural invocation: onboarder→onboard, scaffolder→create, validator→validate, publisher→publish
- Agents converted to skills with `disable-model-invocation: true`
- Internal paths use `${CLAUDE_SKILL_DIR}` for reliable resolution
- MCS-spec aligned with validator checks (eliminated divergence)
- Description length limit corrected to 500 chars (matching CLI)
- Onboarder environment scan distinguishes engine tools from creator products

### Removed
- Legacy `skills/` and `agents/` directories at project root (migrated to `.claude/skills/`)
- Redundant `.claude/commands/` wrappers
- Broken hooks in settings.json

## [1.0.0] — 2026-03-25

### Added
- Initial release — 4 core skills, 5 cognitive agents, 9 product specs, 9 templates, 9 exemplars
- MCS 3-tier quality system
- CONDUIT v2 vault.yaml manifest integration
- myClaude CLI publishing support
