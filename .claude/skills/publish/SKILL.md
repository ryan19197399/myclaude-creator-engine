# Skill: Publish

## Overview

The **Publish** skill enables the myclaude-creator-engine to package, validate, and publish skills to the marketplace. It handles versioning, manifest generation, dependency resolution, and submission to the `.claude-plugin/marketplace.json` registry.

---

## Metadata

```yaml
name: publish
version: 1.0.0
author: myclaude-creator-engine
category: tooling
tags: [publish, marketplace, registry, packaging, versioning]
dependencies:
  - aegis >= 1.0.0
license: MIT
```

---

## Purpose

When a skill is ready for distribution, the Publish skill automates the full release pipeline:

1. **Validate** the skill's `SKILL.md`, `README.md`, `LICENSE.md`, and `CHANGELOG.md`
2. **Lint** metadata fields for completeness and correctness
3. **Bump** the version according to semver rules
4. **Generate** or update the marketplace manifest entry
5. **Sign** the package using Aegis for integrity verification
6. **Submit** the entry to the marketplace registry

---

## Trigger Phrases

- `publish skill <name>`
- `release <name> as <version>`
- `submit <name> to marketplace`
- `package skill <name>`
- `bump version of <name> [major|minor|patch]`

---

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skill_name` | string | ✅ | The directory name under `.claude/skills/` |
| `bump_type` | enum | ❌ | `major`, `minor`, or `patch` (default: `patch`) |
| `dry_run` | boolean | ❌ | Preview changes without writing to registry |
| `sign` | boolean | ❌ | Whether to invoke Aegis signing (default: `true`) |
| `changelog_entry` | string | ❌ | Text to prepend to `CHANGELOG.md` for this release |

---

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `published_version` | string | The semver string of the published release |
| `manifest_entry` | object | The JSON object written to `marketplace.json` |
| `signature` | string | Aegis-generated SHA-256 signature (if signing enabled) |
| `dry_run_report` | string | Human-readable preview (only when `dry_run: true`) |

---

## Execution Steps

### Step 1 — Preflight Validation

```python
def preflight(skill_name: str) -> ValidationResult:
    """
    Ensure all required skill files exist and contain mandatory fields.
    Required files: SKILL.md, README.md, LICENSE.md, CHANGELOG.md
    """
    base = f".claude/skills/{skill_name}"
    required_files = ["SKILL.md", "README.md", "LICENSE.md", "CHANGELOG.md"]
    missing = [f for f in required_files if not path_exists(f"{base}/{f}")]
    if missing:
        raise PublishError(f"Missing required files: {missing}")
    return ValidationResult(ok=True)
```

### Step 2 — Parse Current Version

Extract the current version from the `SKILL.md` metadata block:

```yaml
# Pattern to match inside SKILL.md
version: X.Y.Z
```

If no version is found, default to `0.0.0` and apply the bump.

### Step 3 — Semver Bump

```python
def bump_version(current: str, bump_type: str) -> str:
    major, minor, patch = map(int, current.split("."))
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"
```

### Step 4 — Update CHANGELOG.md

Prepend a new entry in the format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

- <changelog_entry or auto-generated summary>
```

### Step 5 — Aegis Signing

Invoke the **Aegis** skill to compute an integrity signature over the skill directory:

```python
def sign_skill(skill_name: str, version: str) -> str:
    """
    Delegates to the Aegis skill to produce a SHA-256 content hash
    of all files under .claude/skills/<skill_name>/.
    Returns the hex digest string.
    """
    return aegis.sign(target=f".claude/skills/{skill_name}", version=version)
```

### Step 6 — Marketplace Manifest Entry

Write or update the entry in `.claude-plugin/marketplace.json`:

```json
{
  "name": "<skill_name>",
  "version": "<new_version>",
  "description": "<extracted from README.md first paragraph>",
  "author": "<extracted from SKILL.md metadata>",
  "license": "<extracted from LICENSE.md>",
  "tags": ["<from SKILL.md metadata>"],
  "signature": "<aegis sha256 hex>",
  "published_at": "<ISO 8601 timestamp>",
  "path": ".claude/skills/<skill_name>"
}
```

---

## Error Handling

| Error Code | Cause | Resolution |
|------------|-------|------------|
| `PUBLISH_001` | Missing required files | Add missing `SKILL.md`, `README.md`, `LICENSE.md`, or `CHANGELOG.md` |
| `PUBLISH_002` | Invalid semver in SKILL.md | Correct the `version:` field to `X.Y.Z` format |
| `PUBLISH_003` | Aegis signing failed | Check Aegis skill installation and permissions |
| `PUBLISH_004` | Marketplace registry write failed | Verify `.claude-plugin/marketplace.json` is writable |
| `PUBLISH_005` | Duplicate version detected | Bump the version before re-publishing |

---

## Dry Run Example

```
> publish skill forge --dry-run

[DRY RUN] Publish Skill: forge
  Current version : 1.2.1
  Bump type       : patch
  New version     : 1.2.2
  Files validated : SKILL.md, README.md, LICENSE.md, CHANGELOG.md ✅
  Aegis signature : (would be computed)
  Registry entry  : (would be written to .claude-plugin/marketplace.json)
  Changelog entry : (would prepend to .claude/skills/forge/CHANGELOG.md)

No changes written. Pass --no-dry-run to publish.
```

---

## Governance

This skill operates under `.claude/rules/engine-governance.md`. All marketplace submissions must:

- Pass preflight validation
- Include a valid OSI-approved license
- Be signed by Aegis before registry submission
- Not overwrite an existing version (versions are immutable once published)

---

## Changelog

## [1.0.0] - 2025-01-01

- Initial release of the Publish skill
- Preflight validation, semver bumping, Aegis signing, and marketplace submission
