# Hooks Exemplar: Auto-Lint on Save

**MCS Level:** 2 (Quality)
**Demonstrates:** settings.json format, PostToolUse event, idempotent handlers, security
transparency, exit codes, timeout, anti-patterns, install merge logic.

---

## File: `hooks.json`

```json
{
  "_comment": "auto-lint-on-save — Claude Code Hooks",
  "_why": "Automatically lint and format every file Claude writes or edits.",
  "_why_format": "This is a settings.json fragment. Install merges into .claude/settings.local.json.",

  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/auto-lint-on-save/scripts/lint-and-format.sh",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

---

## File: `scripts/lint-and-format.sh`

```bash
#!/usr/bin/env bash
# auto-lint-on-save — Hook Handler Script
# WHY: Runs when PostToolUse fires with matcher "Write|Edit"
# WHY: Exit code 0 = allow, 2 = block (stderr becomes feedback), other = non-blocking error
# WHY: SECURITY: Modifies only the file Claude just wrote. No network calls. No data exfiltration.

set -euo pipefail

# Read event payload from stdin
EVENT_PAYLOAD=$(cat)

# Extract the file path from the event payload
FILE_PATH=$(echo "$EVENT_PAYLOAD" | grep -o '"path":"[^"]*"' | cut -d'"' -f4 || true)

if [ -z "$FILE_PATH" ]; then
  # No file path in payload — skip silently (non-blocking)
  exit 0
fi

# Run ESLint with --fix first (linter before formatter)
# WHY: --fix converges — running twice produces the same output (idempotent)
# WHY: || true silences errors on non-JS files (e.g., .md, .yaml)
npx eslint --fix --quiet "$FILE_PATH" 2>/dev/null || true

# Then run Prettier to format the result
# WHY: Prettier runs after ESLint so it gets the last word on formatting
npx prettier --write --log-level silent "$FILE_PATH" 2>/dev/null || true

# Exit 0 — allow Claude to continue after linting
exit 0
```

---

## File: `README.md`

```markdown
# Auto-Lint on Save

> Automatically lint and format every file Claude modifies.

## What It Does

When Claude writes or edits a file, this hook:
1. Runs ESLint with `--fix` on the modified file
2. Runs Prettier to format the result

Both are silent — they won't interrupt your Claude session.

## Installation

\`\`\`bash
myclaude install auto-lint-on-save
\`\`\`

This merges the hook configuration into `.claude/settings.local.json` and copies
`scripts/lint-and-format.sh` to your project.

## Security Notice

This hook executes the following shell commands:

\`\`\`bash
npx eslint --fix --quiet "$FILE_PATH"
npx prettier --write --log-level silent "$FILE_PATH"
\`\`\`

Both commands modify **only the file Claude just edited**. No network calls. No data
exfiltration. No access outside the current project directory.

**Review `scripts/lint-and-format.sh` before installing on sensitive projects.**

## Requirements

- Claude Code >= 1.0.0
- Node.js with `eslint` and `prettier` installed (`npm install -D eslint prettier`)

## Anti-Patterns

| Anti-Pattern | Prevention |
|---|---|
| Non-idempotent linting | Use `--fix` which converges. Verify by running twice. |
| Matching all PostToolUse events | Only match `Write\|Edit` — tools that modify files. |
| No timeout | Always set `timeout`. 15s covers large files. |
| Failing loudly on non-JS files | Use `\|\| true` to silently skip unsupported extensions. |
| Running formatter before linter | ESLint `--fix` first, then Prettier. Prevents re-formatting. |
```

---

## Install Merge Logic

Before install, `.claude/settings.local.json` might look like:

```json
{
  "permissions": {
    "allow": ["Bash(git:*)"]
  }
}
```

After `myclaude install auto-lint-on-save`, it becomes:

```json
{
  "permissions": {
    "allow": ["Bash(git:*)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/auto-lint-on-save/scripts/lint-and-format.sh",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

The `"hooks"` key is merged in. Existing keys (`"permissions"`) are untouched.
Multiple hook products merge their events together — no conflicts.

---

## Quality Verification

- [x] `hooks.json` is valid settings.json fragment with correct structure
- [x] `PostToolUse` event with `Write|Edit` matcher (not all tools)
- [x] Handler script is idempotent (`--fix` converges, `|| true` guards)
- [x] Exit codes documented: 0=allow, no blocking (error uses non-blocking exit)
- [x] Timeout defined (15s)
- [x] Security notice in README lists exact commands
- [x] 5 anti-patterns documented
- [x] No shell injection patterns
- [x] `set -euo pipefail` — fail-fast script
- [x] MCS-2 criteria met
