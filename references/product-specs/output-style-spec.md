# Product Spec: Output Style

## Definition

Output styles are markdown files that customize how Claude formats and communicates its responses. They install to `.claude/output-styles/` and are activated via the `/output-style` slash command.

An output style is NOT:
- A skill (it doesn't execute logic)
- A rule (it doesn't constrain behavior, just format)
- A prompt injection (it works through CC's native output style system)

An output style IS:
- A single markdown file with optional YAML frontmatter
- Instructions for Claude's response formatting, voice, and structure
- Composable with Claude's default coding instructions (via `keep-coding-instructions`)

---

## Canonical File Structure

```
output-style-name/
├── OUTPUT-STYLE.md       # The style definition (REQUIRED)
├── README.md             # Documentation (REQUIRED)
├── examples/             # Before/after output samples (MCS-2)
│   └── .gitkeep
└── .meta.yaml            # Engine state (auto-generated)
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| OUTPUT-STYLE.md | Style definition with frontmatter | MCS-1+ |
| README.md | Installation and usage docs | MCS-1+ |
| examples/ | Before/after comparisons | MCS-2+ |

---

## Frontmatter Schema (CC Source-Verified)

```yaml
---
name: "my-style"                    # display name (required)
description: "Concise technical prose"  # when to use (required)
keep-coding-instructions: true      # keep Claude's default coding behavior (optional, default: true)
---
```

**Note:** `keep-coding-instructions` is the key differentiation:
- `true` (default): Your style ADDS to Claude's existing behavior
- `false`: Your style REPLACES Claude's default output formatting entirely

---

## Install Target

```
.claude/output-styles/{slug}.md
```

The file is renamed during /package: `OUTPUT-STYLE.md` → `{slug}.md`.

---

## Activation

Users activate via: `/output-style {slug}`
Users deactivate via: `/output-style default`

The active output style is injected into the system prompt's intro section (see CC source: SystemPromptBuilder section 2).

---

## Quality Criteria

| Level | Criteria |
|-------|---------|
| MCS-1 | Frontmatter valid, anti-patterns defined, quality criteria stated |
| MCS-2 | Before/after examples, works across project types |
| MCS-3 | Not typically applicable to output styles |
