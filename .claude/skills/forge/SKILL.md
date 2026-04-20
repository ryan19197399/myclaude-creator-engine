# Forge Skill

> Build, compile, and package creator engine artifacts with reproducible pipelines.

## Metadata

```yaml
name: forge
version: 0.1.0
author: myclaude-creator-engine
license: MIT
tags: [build, compile, package, pipeline, artifacts]
depends_on: [scout, aegis]
```

---

## Overview

The **Forge** skill provides a structured build pipeline for the creator engine. It handles compilation of skill bundles, validation of manifests, artifact packaging, and publishing to the marketplace registry.

Forge operates in three stages:

1. **Lint** — validate all SKILL.md manifests and rule files
2. **Build** — compile skill bundles into distributable artifacts
3. **Publish** — push validated artifacts to the marketplace registry

---

## Triggers

Forge activates when any of the following conditions are met:

- A `SKILL.md` file is created or modified under `.claude/skills/`
- A `marketplace.json` entry references a skill version not yet built
- The user explicitly invokes `@forge build` or `@forge publish`
- The `aegis` skill flags a dependency drift requiring rebuild

---

## Commands

### `@forge lint`

Validate all skill manifests in the project.

```
@forge lint [--skill <name>] [--strict]
```

**Options:**
- `--skill <name>` — lint only the named skill
- `--strict` — treat warnings as errors

**Checks performed:**
- Required metadata fields present (`name`, `version`, `author`, `license`)
- `depends_on` skills exist in `.claude/skills/`
- No circular dependencies
- Changelog entry exists for current version
- LICENSE.md present in skill directory

**Example output:**
```
✓ aegis@1.2.0   — OK
✓ scout@0.3.1   — OK
✗ forge@0.1.0   — WARN: no CHANGELOG.md found
```

---

### `@forge build`

Compile one or all skills into distributable bundles.

```
@forge build [--skill <name>] [--output <dir>] [--clean]
```

**Options:**
- `--skill <name>` — build only the named skill
- `--output <dir>` — output directory (default: `.forge/dist/`)
- `--clean` — remove previous build artifacts before building

**Build process:**
1. Run `@forge lint` (fails fast on errors)
2. Resolve dependency graph via `scout`
3. Bundle `SKILL.md`, `README.md`, `CHANGELOG.md`, `LICENSE.md`
4. Generate `skill.bundle.json` with resolved metadata
5. Compute SHA-256 checksum of bundle
6. Write artifact to `<output>/<name>@<version>.bundle.tar.gz`

**Artifact structure:**
```
<name>@<version>.bundle.tar.gz
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE.md
└── skill.bundle.json   # resolved metadata + checksum
```

---

### `@forge publish`

Publish a built artifact to `.claude-plugin/marketplace.json`.

```
@forge publish --skill <name> [--dry-run]
```

**Options:**
- `--skill <name>` — skill to publish (required)
- `--dry-run` — preview changes without writing

**Publish process:**
1. Verify artifact exists in `.forge/dist/`
2. Validate checksum matches bundle
3. Check marketplace.json for version conflicts
4. Append or update entry in `marketplace.json`
5. Commit message suggested: `feat(forge): publish <name>@<version>`

**Marketplace entry format:**
```json
{
  "name": "forge",
  "version": "0.1.0",
  "description": "Build and package creator engine skill artifacts",
  "author": "myclaude-creator-engine",
  "license": "MIT",
  "tags": ["build", "compile", "package"],
  "depends_on": ["scout", "aegis"],
  "checksum": "sha256:<hash>",
  "published_at": "2025-01-01T00:00:00Z"
}
```

---

## Dependency Resolution

Forge delegates dependency resolution to the **Scout** skill. Before any build, Scout performs a full graph traversal to:

- Detect missing skills referenced in `depends_on`
- Identify version mismatches between declared and installed skills
- Flag circular dependency chains

If Scout reports unresolved dependencies, Forge halts and surfaces a remediation plan.

---

## Security Integration

Forge integrates with **Aegis** for:

- Checksum verification of all input skill files before bundling
- Signature validation when pulling remote skill sources
- Audit log entry written to `.aegis/audit.log` on every publish

Aegis violations block publish but do not block local builds unless `--strict` is set.

---

## Configuration

Forge reads optional configuration from `.forge/config.yaml`:

```yaml
# .forge/config.yaml
output_dir: .forge/dist
strict_lint: false
auto_publish: false
checksum_algo: sha256
include_readme: true
include_changelog: true
```

---

## Error Reference

| Code | Message | Resolution |
|------|---------|------------|
| `F001` | Missing required metadata field | Add field to SKILL.md metadata block |
| `F002` | Dependency not found | Install missing skill or update `depends_on` |
| `F003` | Circular dependency detected | Refactor skill dependency graph |
| `F004` | Checksum mismatch | Re-run `@forge build --clean` |
| `F005` | Version already published | Bump version in SKILL.md metadata |
| `F006` | Aegis security violation | Review `.aegis/audit.log` for details |

---

## Changelog

### 0.1.0
- Initial Forge skill implementation
- Lint, build, and publish pipeline
- Scout and Aegis integration hooks
- Marketplace.json publish support
