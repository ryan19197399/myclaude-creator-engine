# Statusline Exemplar: git-cost-monitor

**MCS Level:** 2 (Quality)
**Demonstrates:** Shell script architecture, jq parsing with fallback, ANSI colors,
graceful degradation, settings-fragment.json activation, examples with stdin/stdout.

---

## File: `statusline.sh`

```bash
#!/usr/bin/env bash
# git-cost-monitor — Claude Code Status Line
# WHY: Shows model, session cost, git branch, and context usage at a glance.
# WHY: Reads JSON from stdin, outputs ANSI-formatted text to stdout.

# Read JSON from stdin
INPUT=$(cat)

# ── Parse fields with jq (fallback if jq unavailable) ────────────
if command -v jq &>/dev/null; then
  MODEL=$(echo "$INPUT" | jq -r '.model // "unknown"')
  COST=$(echo "$INPUT"  | jq -r '.cost // "0.00"')
  # context_window may be an object with .used and .total
  CTX_USED=$(echo "$INPUT"  | jq -r '.context_window.used // 0')
  CTX_TOTAL=$(echo "$INPUT" | jq -r '.context_window.total // 200000')
else
  # Fallback: no jq available — show safe defaults
  MODEL="?"
  COST="0.00"
  CTX_USED=0
  CTX_TOTAL=200000
fi

# ── Git branch (run independently — not in JSON) ──────────────────
# WHY: D7 (Pre-Execution Gate) — check git is available before calling it.
if command -v git &>/dev/null && git rev-parse --git-dir &>/dev/null 2>&1; then
  BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
else
  BRANCH="no-git"
fi

# ── Context usage percentage ──────────────────────────────────────
if [ "$CTX_TOTAL" -gt 0 ] 2>/dev/null; then
  CTX_PCT=$(( CTX_USED * 100 / CTX_TOTAL ))
else
  CTX_PCT=0
fi

# Color context bar based on usage
if [ "$CTX_PCT" -ge 80 ]; then
  CTX_COLOR='\033[0;31m'   # red — high usage
elif [ "$CTX_PCT" -ge 50 ]; then
  CTX_COLOR='\033[0;33m'   # yellow — moderate usage
else
  CTX_COLOR='\033[0;32m'   # green — healthy
fi

# ── ANSI Color Helpers ────────────────────────────────────────────
CYAN='\033[0;36m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
DIM='\033[2m'
RESET='\033[0m'

SEP="${DIM} | ${RESET}"

# ── Output ────────────────────────────────────────────────────────
# WHY: D14 (Graceful Degradation) — all variables have safe fallbacks above.
# Format: model | $cost | ⎇ branch | ctx%
printf "${CYAN}${MODEL}${RESET}${SEP}${GREEN}\$${COST}${RESET}${SEP}${BLUE}⎇ ${BRANCH}${RESET}${SEP}${CTX_COLOR}ctx ${CTX_PCT}%%${RESET}"
```

---

## File: `settings-fragment.json`

```json
{
  "_comment": "git-cost-monitor — Status Line Settings Fragment",
  "_why": "Merge this into .claude/settings.local.json to activate this status line.",
  "_why_note": "Only ONE status line can be active at a time. Installing replaces the current one.",

  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-scripts/git-cost-monitor.sh",
    "padding": 2
  }
}
```

---

## File: `README.md`

```markdown
# git-cost-monitor

> See your model, session cost, git branch, and context usage — all in the terminal bar.

## What It Shows

```
claude-opus-4-6 | $0.42 | ⎇ feature/auth | ctx 23%
```

Color coding:
- Context bar: green (< 50%), yellow (50-80%), red (>= 80%)

## Requirements

- Claude Code >= 1.0.0
- `jq` recommended (graceful fallback if absent)
- `git` for branch display (shows "no-git" in non-git directories)

## Installation

```bash
myclaude install git-cost-monitor
```

Manual install:

1. Copy the script:
   ```bash
   cp statusline.sh ~/.claude/statusline-scripts/git-cost-monitor.sh
   chmod +x ~/.claude/statusline-scripts/git-cost-monitor.sh
   ```

2. Merge into `.claude/settings.local.json`:
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "bash ~/.claude/statusline-scripts/git-cost-monitor.sh",
       "padding": 2
     }
   }
   ```

## Anti-Patterns

- Do NOT call slow external APIs in the script — it runs after every message
- Do NOT write to disk from the script — stdout only
- Do NOT omit jq fallbacks — not all environments have jq installed
- Do NOT hardcode paths — use `~/.claude/statusline-scripts/{slug}.sh` pattern
- Do NOT forget `chmod +x` — the script must be executable

## Activation Note

Only ONE status line is active at a time. Installing this will replace your current
`statusLine` configuration in `settings.local.json`.
```

---

## File: `examples/.gitkeep`

(empty placeholder — add `examples/happy-path.sh`, `examples/no-git.sh` etc. for MCS-2)

---

## Sample: examples/happy-path.txt

Input (stdin JSON):
```json
{
  "model": "claude-opus-4-6",
  "cost": "0.42",
  "cwd": "/home/user/my-project",
  "context_window": { "used": 46000, "total": 200000 }
}
```

Expected stdout (ANSI stripped for readability):
```
claude-opus-4-6 | $0.42 | ⎇ feature/auth | ctx 23%
```

---

## Quality Verification

- [x] `statusline.sh` starts with `#!/usr/bin/env bash`
- [x] Reads from stdin via `INPUT=$(cat)`
- [x] All jq fields use `// "fallback"` defaults
- [x] jq availability check with safe fallback values
- [x] git availability check before calling git
- [x] Context color changes at 50% and 80% thresholds
- [x] `settings-fragment.json` valid JSON with correct structure
- [x] README with visual preview, install, requirements, anti-patterns
- [x] MCS-2 criteria met
