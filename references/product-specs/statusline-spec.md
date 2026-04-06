# Product Spec: Status Lines

## Definition

Status lines are **shell scripts** that display real-time information in the Claude Code
terminal bar. They read JSON from stdin and output ANSI-formatted text to stdout.

A status line is NOT:
- A YAML configuration file
- A skill with execution logic
- A visual theme or color scheme
- A dashboard or monitoring tool

A status line IS:
- A shell script (`statusline.sh`) that reads JSON input and writes formatted output
- Configured via `settings.json` `statusLine` object pointing to the script
- Refreshed after each assistant message (debounced 300ms)
- Capable of ANSI colors, OSC 8 hyperlinks, and multi-line output

---

## Canonical File Structure

```
statusline-name/
├── statusline.sh             # Shell script — reads JSON stdin, outputs ANSI stdout (REQUIRED)
├── settings-fragment.json    # settings.json merge fragment for activation (REQUIRED)
├── README.md                 # Marketplace documentation (REQUIRED)
├── examples/
│   └── .gitkeep              # Sample stdin JSON + expected stdout output
└── .meta.yaml                # Engine state (auto-generated)
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `statusline.sh` | Shell script — parses JSON stdin, outputs ANSI stdout | MCS-1 |
| `settings-fragment.json` | settings.json merge fragment to activate | MCS-1 |
| `README.md` | What it shows, install, preview output | MCS-1 |

---

## Input Contract (JSON on stdin)

Claude Code passes a JSON object to stdin on each refresh. Fields available:

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | Current model name (e.g., `"claude-opus-4-6"`) |
| `cwd` | string | Current working directory |
| `workspace` | string | Workspace root path |
| `cost` | string | Session cost in dollars |
| `context_window` | object | Context window usage info |
| `rate_limits` | object | Rate limit status |
| `session` | object | Session metadata (id, duration, etc.) |
| `vim_mode` | string | Current vim mode if enabled |

---

## Output Contract (stdout)

The script writes to stdout. Claude Code renders it in the terminal status bar.

- **ANSI colors:** Supported via escape codes (`\033[0;32m` etc.)
- **OSC 8 hyperlinks:** Supported (`\033]8;;URL\033\\TEXT\033]8;;\033\\`)
- **Multi-line:** Supported — each `\n` creates a new status bar line
- **Reset:** Always end segments with `\033[0m` to avoid color bleed

---

## Refresh Behavior

- Triggered: after each assistant message completes
- Debounce: 300ms (rapid messages won't spam the script)
- Timeout: if the script takes >500ms, Claude Code shows the previous output
- Only ONE status line active at a time (last `statusLine` key in settings wins)

---

## Activation via settings-fragment.json

The `settings-fragment.json` file must be merged into `.claude/settings.local.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-scripts/{slug}.sh",
    "padding": 2
  }
}
```

Installing a new status line replaces any previously active one.

---

## Install Path

```
~/.claude/statusline-scripts/{slug}.sh
```

The script must be executable. The CLI install command runs:
```bash
chmod +x ~/.claude/statusline-scripts/{slug}.sh
```

**Cross-platform note:** On Windows with Git Bash or WSL, `chmod` works normally.
On native Windows without bash, the script is invoked via `bash` prefix in the
settings.json command, which handles execution permission internally.

---

## MCS Requirements

### MCS-1: Publishable
- [ ] `statusline.sh` starts with a shebang (`#!/usr/bin/env bash`)
- [ ] `statusline.sh` reads from stdin (`INPUT=$(cat)`)
- [ ] `statusline.sh` outputs to stdout (`printf` or `echo`)
- [ ] Fallback output defined for when jq is unavailable or fields are missing
- [ ] `settings-fragment.json` is valid JSON with correct `statusLine` structure
- [ ] README.md with preview of output and install instructions

### MCS-2: Quality
- [ ] jq availability check with graceful fallback (D7)
- [ ] All parsed fields have `// "fallback"` defaults in jq expressions
- [ ] 3+ examples in `examples/` showing different input states and expected output
- [ ] Anti-patterns documented (D2)

---

## DNA Requirements

See `product-dna/statusline.yaml`.
