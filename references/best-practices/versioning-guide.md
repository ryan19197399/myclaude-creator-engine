# Versioning Guide

Semver rules, CHANGELOG format, and pre-release versioning for MyClaude products.

---

## Semver Rules

All products use **Semantic Versioning**: `MAJOR.MINOR.PATCH`

```
1.0.0    First stable release
^         ^     ^
│         │     └── PATCH: backwards-compatible bug fixes
│         └──────── MINOR: new functionality, backwards-compatible
└────────────────── MAJOR: breaking changes
```

### MAJOR Version (breaking changes)

Bump MAJOR when:
- Changing the required file structure (adding required files that don't have defaults)
- Changing the primary activation interface (SKILL.md required sections, AGENT.md required sections)
- Removing or renaming functionality that buyers have integrated with
- Changing the output format in a way that breaks downstream consumers
- Changing required metadata fields

Examples:
```
1.5.2 → 2.0.0  (renamed primary activation command)
2.3.0 → 3.0.0  (removed support for a product type variant)
```

### MINOR Version (new functionality)

Bump MINOR when:
- Adding new modes, variants, or capabilities that don't break existing usage
- Adding new optional files or sections
- Adding new exemplars or knowledge base files
- Expanding the references/ knowledge base
- Adding composability patterns that were missing before

Examples:
```
1.2.0 → 1.3.0  (added `radical` mode to progressive depth)
1.3.0 → 1.4.0  (added new agent to squad roster)
```

### PATCH Version (bug fixes)

Bump PATCH when:
- Fixing a broken reference
- Correcting an anti-pattern that was causing wrong behavior
- Fixing a typo in the primary file that affected functionality
- Updating a broken link in README
- Fixing a YAML syntax error

Examples:
```
1.2.0 → 1.2.1  (fixed broken reference in Activation Protocol)
1.2.1 → 1.2.2  (corrected incorrect step dependency in workflow)
```

---

## When NOT to Bump Version

- **Formatting changes only** (whitespace, indentation, comment reformatting)
  → No version bump needed; update the file but don't publish a new version
- **README typos** that don't affect functionality → PATCH only if material
- **Adding guidance comments** to templates → no bump (comments are stripped on publish)

**Rule of thumb:** If a buyer who already has the product needs to re-install or change
their usage to benefit from the change → MINOR or MAJOR. If they benefit automatically → PATCH.

---

## CHANGELOG Format

Every published version must have a CHANGELOG entry.
Format: Keep a Changelog (keepachangelog.com compatible).

```markdown
# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [Unreleased]
### Added
- [Planned additions]

## [2.1.0] — 2026-03-25

### Added
- Progressive depth `radical` mode — full 6-step analysis plus devil's advocate section
- `references/second-order-effects.md` — second-order effect framework for radical mode
- Composability section documenting upstream/downstream product connections

### Changed
- Activation Protocol now loads `anti-patterns.md` before `exemplars.md` (order change — faster failure detection)

### Fixed
- Quality gate check 3 was referencing the wrong mode condition

## [2.0.0] — 2026-02-10

### Breaking Changes
- Renamed `quick` mode to `surface` mode — update any workflows referencing the old name
- Required SKILL.md section 3 now named "Activation Protocol" (was "Context Loading")

### Added
- `dive` mode as new default (previously `standard`)
- `references/` knowledge base with 3 files

## [1.2.1] — 2026-01-15

### Fixed
- Broken reference to `references/domain-knowledge.md` (file was in wrong path)

## [1.2.0] — 2026-01-10

### Added
- Anti-patterns section with 5 documented patterns
- 2 additional exemplars in references/exemplars.md

## [1.0.0] — 2025-12-01

### Initial Release
- Core skill with Activation Protocol
- 3 exemplars
- Basic references/ structure
```

**CHANGELOG rules:**
- Latest version at top
- Each version has a date
- Breaking changes are explicitly labeled
- Changes are grouped: Added | Changed | Deprecated | Removed | Fixed | Security
- Every published version has an entry — no gaps

---

## Pre-Release Versions

For products in testing before stable release:

```
1.0.0-alpha.1   Very early, expect breaking changes
1.0.0-beta.1    Feature complete, may have bugs
1.0.0-rc.1      Release candidate — code complete
```

**Pre-release rules:**
- Pre-release versions are NOT guaranteed stable
- MAJOR.MINOR.PATCH must reflect what the stable release will be when ready
- Pre-releases are visible in marketplace with explicit pre-release badge
- Use for testing with willing early adopters only

**Pre-release CHANGELOG:**
```markdown
## [1.0.0-beta.2] — 2026-03-20 [PRE-RELEASE]

### Fixed
- Corrected Activation Protocol load order

### Known Issues
- `radical` mode depth may be inconsistent on very short inputs
```

---

## Version Lifecycle

```
0.x.x       Development (pre-stability)
1.0.0       First stable release
1.x.x       Active development
2.0.0       Major revision (breaking changes from 1.x)
[last].x.x  Maintenance (bug fixes only, no new features)
```

**For new products:** Start at `1.0.0` when publishing, not `0.1.0`.
A published product signals "stable enough to use." Pre-release versions use the
`-beta` or `-alpha` suffix instead of a low major version.

---

## Common Versioning Mistakes

| Mistake | Fix |
|---------|-----|
| Shipping at `0.1.0` | Start at `1.0.0`. Pre-stability belongs in your workspace, not the marketplace. |
| `v` prefix in version field: `v1.0.0` | No prefix: `1.0.0`. The `v` is for git tags, not version fields. |
| Version bump without CHANGELOG entry | Every bump needs a CHANGELOG entry. Automate this with the `/package` command. |
| Using PATCH for new features | New features are MINOR, even small ones. |
| Using MAJOR for small breaking changes | Consistent: if buyers need to change usage, it's MAJOR. Scope doesn't matter. |
