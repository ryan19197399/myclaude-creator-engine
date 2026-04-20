# Scout Skill

## Metadata

```yaml
name: scout
version: 1.0.0
author: myclaude-creator-engine
description: Autonomous research and discovery skill for scanning repositories, dependencies, and ecosystems
tags: [research, discovery, analysis, dependencies, ecosystem]
requires: []
compatible_agents: [scout-agent]
```

## Overview

The **Scout** skill enables Claude to perform deep research and discovery tasks across codebases, package ecosystems, and external resources. It is the primary skill used by `scout-agent` to gather intelligence before planning or execution phases.

Scout operates in three modes:
- **Passive**: Read-only scanning of existing files and structures
- **Active**: Fetching remote data (npm registry, GitHub API, PyPI, etc.)
- **Comparative**: Diffing two states (before/after, local/remote, fork/upstream)

---

## Capabilities

### 1. Repository Scanning

Scout can recursively analyze a project directory and produce a structured report:

```
scout.scan(path=".", depth=3)
```

**Output includes:**
- File tree with line counts
- Detected languages and frameworks
- Entry points (main files, index files, CLI definitions)
- Dependency manifests found (`package.json`, `pyproject.toml`, `requirements.txt`, etc.)
- Presence of config files (`.env`, `Dockerfile`, CI configs)
- Git metadata (current branch, last commit, remotes)

---

### 2. Dependency Analysis

Scout resolves and audits declared dependencies:

```
scout.deps(manifest="package.json", mode="audit")
```

**Modes:**
- `list` — enumerate all direct and transitive dependencies
- `audit` — flag known vulnerabilities (uses OSV / npm audit data)
- `outdated` — compare installed vs latest versions
- `unused` — detect declared but unreferenced packages (static analysis)

**Example output (audit mode):**
```json
{
  "total": 142,
  "direct": 18,
  "vulnerabilities": [
    {
      "package": "lodash",
      "installed": "4.17.15",
      "severity": "high",
      "cve": "CVE-2021-23337",
      "fix": "4.17.21"
    }
  ],
  "outdated": 7
}
```

---

### 3. Ecosystem Discovery

Scout can search external package registries to find alternatives, similar tools, or newer patterns:

```
scout.discover(query="markdown parser", ecosystem="npm", limit=5)
```

**Supported ecosystems:**
- `npm` — Node Package Registry
- `pypi` — Python Package Index
- `crates` — Rust crates.io
- `github` — GitHub repository search

**Filters:**
- `min_stars` — minimum GitHub stars
- `updated_within` — e.g. `"6months"`
- `license` — e.g. `"MIT"`, `"Apache-2.0"`
- `exclude` — list of package names to ignore

---

### 4. Fork Comparison

Scout is purpose-built for fork workflows. It compares a fork against its upstream:

```
scout.fork_diff(fork="myclaude-creator-engine", upstream="myclaude-sh/myclaude-creator-engine")
```

**Output includes:**
- Files added in fork
- Files modified (with diff summary)
- Files deleted
- Commits ahead / behind
- Divergence score (0–100)

---

### 5. Skill Marketplace Scan

Scout integrates with `.claude-plugin/marketplace.json` to identify installable skills and check for updates:

```
scout.marketplace(action="check-updates")
```

**Actions:**
- `list` — show all available skills
- `check-updates` — compare installed skill versions against marketplace
- `suggest` — recommend skills based on current project type

---

## Invocation Protocol

When scout-agent invokes this skill, it follows this sequence:

1. **Initialize context** — load project root, detect VCS, read `.claude/rules/`
2. **Select scan targets** — based on agent task description
3. **Execute scan steps** — in dependency order
4. **Emit structured report** — JSON or Markdown depending on `output_format`
5. **Store to context** — results available to downstream skills (e.g. `create`, `aegis`)

---

## Output Formats

| Format | Use Case |
|--------|----------|
| `json` | Machine-readable, for piping into other skills |
| `markdown` | Human-readable summary for PR descriptions or reports |
| `diff` | For fork comparison and change detection |
| `table` | For dependency lists and audit results |

---

## Integration with Other Skills

### → `create`
Scout findings feed into `create` skill to avoid regenerating existing functionality and to respect existing patterns.

### → `aegis`
Scout's vulnerability audit output is consumed by `aegis` to prioritize security remediation tasks.

---

## Governance

This skill operates under `.claude/rules/engine-governance.md`. Key constraints:

- Scout **never writes files** — it is strictly read/fetch only
- External API calls are rate-limited and cached for 1 hour
- Sensitive files (`.env`, secrets) are detected but **contents are never surfaced**
- All scan results are scoped to the current project context

---

## Changelog

### v1.0.0
- Initial release
- Repository scanning, dependency analysis, ecosystem discovery
- Fork comparison support
- Marketplace integration
