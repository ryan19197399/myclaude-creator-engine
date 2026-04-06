# Product Spec: Hooks

## Definition

Hooks are Claude Code event handlers defined as JSON in `settings.json`. They bind to
lifecycle events and execute commands (shell, LLM prompt, subagent, or HTTP) when triggered.
Hooks are security-sensitive — they execute with the user's full permissions.

A hook is NOT:
- A skill invoked by the user
- A background service or daemon
- A monitoring tool
- A YAML configuration file

A hook IS:
- An event-driven automation triggered by Claude Code lifecycle events
- A JSON fragment merged into `.claude/settings.local.json` at install time
- Idempotent (safe to run multiple times on the same event)
- Security-transparent (documents all shell commands in README)

---

## Canonical File Structure

```
hooks-name/
├── hooks.json            # settings.json fragment — event bindings (REQUIRED)
├── scripts/              # Handler scripts executed by hooks (REQUIRED)
│   └── handler.sh        # At least one handler for each command hook
├── README.md             # Documentation with security notice (REQUIRED)
├── examples/
│   └── .gitkeep          # Test scenarios per event (MCS-2)
└── .meta.yaml            # Engine state (auto-generated)
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `hooks.json` | Event bindings in settings.json format | MCS-1 |
| `scripts/` | Handler scripts for command-type hooks | MCS-1 |
| `README.md` | What it does, security notice with command list, install | MCS-1 |

---

## hooks.json Structure

`hooks.json` is a **settings.json fragment** — it is merged (not replaced) into
`.claude/settings.local.json` on install.

```json
{
  "hooks": {
    "{EventType}": [
      {
        "matcher": "{pattern}",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/{slug}/scripts/handler.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

The top-level key is always `"hooks"`. No other keys are merged into settings.json.

---

## 15 Hook Events (CC Source-Verified)

| Group | Events | Can Block? |
|-------|--------|------------|
| Tool | `PreToolUse`, `PostToolUse`, `PostToolUseFailure` | PreToolUse: YES (deny) |
| Prompt | `UserPromptSubmit` | YES (continue=false) |
| Session | `SessionStart`, `Setup` | No |
| Permission | `PermissionRequest`, `PermissionDenied` | PermissionRequest: YES |
| Subagent | `SubagentStart` | No |
| Lifecycle | `Notification` | No |
| Filesystem | `CwdChanged`, `FileChanged` | No (can set watchPaths) |
| Worktree | `WorktreeCreate` | No |
| Elicitation | `Elicitation`, `ElicitationResult` | Elicitation: YES |

Common response fields: `continue`, `suppressOutput`, `stopReason`, `decision`, `reason`, `systemMessage`, `additionalContext`.

**Note:** Earlier documentation listed 25-26 events. CC source code (verified April 2026) confirms exactly 15 named hook events in the schema.

### Security Implications by Event

| Risk | Events | Why |
|------|--------|-----|
| **HIGH** | `PreToolUse`, `UserPromptSubmit`, `PermissionRequest`, `Elicitation` | Can block or alter Claude's actions — a malicious hook can silently veto operations or inject prompts |
| **MEDIUM** | `SessionStart`, `PostToolUse`, `Setup` | Execute at startup or after tool use — can exfiltrate data or modify context |
| **LOW** | `Notification`, `ElicitationResult`, `PostToolUseFailure` | Fire after the fact — limited ability to influence behavior |
| **CONTEXT** | `SubagentStart`, `WorktreeCreate`, `CwdChanged`, `FileChanged`, `PermissionDenied` | Informational — could leak workspace structure to external endpoints |

**Rule:** HIGH-risk events MUST document every shell command in README. MEDIUM-risk events SHOULD document. README security notice is REQUIRED for all hooks regardless of risk level.

---

## Settings Merge Behavior (CC Source-Verified)

Hooks install into `.claude/settings.local.json` (4th priority level). CC settings hierarchy (low→high priority):

1. **Plugin** — allowlisted keys only (security restricted)
2. **User** — `~/.claude/settings.json`
3. **Project** — `.claude/settings.json`
4. **Local** — `.claude/settings.local.json` ← hooks install here
5. **Flag/SDK** — CLI `--settings` or SDK inline
6. **Policy** — Enterprise managed (first-source-wins: Remote > MDM > File > Registry)

**Merge rules differ by type:**
- General settings: last wins (override)
- Nested objects: deep merge recursively
- **Hooks: ACCUMULATE uniquely** (extend, never replace — your hook ADDS to existing hooks)
- MCP servers: replace entirely (no merge)

This means hook products are additive — installing multiple hook products is safe. Each adds its handlers without overwriting others.

---

## 4 Hook Types

| Type | Description | Use When |
|------|-------------|----------|
| `command` | Execute a shell script | Running linters, formatters, validators |
| `prompt` | Single LLM call injected into context | Adding instructions at event time |
| `agent` | Multi-turn subagent launch | Complex autonomous handling |
| `http` | POST event payload to a URL | External integrations, webhooks |

### Hook Type Security Differences

| Type | Risk Level | Validation Focus |
|------|-----------|-----------------|
| `command` | **HIGHEST** — executes shell with user permissions | Scan for injection, eval, source, pipe, base64, curl\|sh. Require timeout. |
| `prompt` | **MEDIUM** — injects text into LLM context | Check for prompt injection patterns, instruction override attempts. No shell risk. |
| `agent` | **HIGH** — spawns autonomous subagent | Verify agent has tool restrictions. Subagent inherits user permissions unless isolated. |
| `http` | **HIGH** — sends data to external URL | Verify URL is documented in README. Check for credential/secret exfiltration in payload. No localhost-only guarantee. |

**Validation rule:** `command` and `http` hooks require the strictest security scan. `prompt` hooks require injection review. `agent` hooks require tool restriction verification.

---

## Exit Codes (command type only)

| Code | Meaning |
|------|---------|
| `0` | Allow — operation proceeds normally |
| `2` | Block — stderr content becomes feedback to Claude |
| other | Non-blocking error — logged, operation proceeds |

---

## Security Validation (Stage 2)

Hooks execute shell commands with user permissions. Stage 2 MUST check for:

- Shell injection patterns: `;`, `&&`, `||`, backticks, `$()`
- `eval` — arbitrary code execution
- `source` or `.` commands — executes external scripts without review
- Unquoted single `|` — potential injection vector
- `base64` decode-and-execute patterns
- `curl|sh` or `wget|sh` — remote code execution
- `python -c` or `node -e` — inline code execution
- File system access outside project scope
- Network calls without documentation in README
- Missing timeout (runaway handler protection)

---

## MCS Requirements

### MCS-1: Publishable
- [ ] `hooks.json` valid JSON with correct settings.json fragment structure
- [ ] `scripts/` directory with at least one handler script
- [ ] README.md with security notice listing all shell commands
- [ ] Handler scripts are idempotent
- [ ] Exit codes documented (0=allow, 2=block)
- [ ] Timeout defined in each hook binding

### MCS-2: Quality
- [ ] All handler scripts pass security scan (no injection patterns)
- [ ] 3+ test scenarios in examples/
- [ ] Anti-patterns section with >=5 items (D2 — critical for hooks)
- [ ] Testability: each hook can be triggered in isolation
- [ ] Event types are valid (from the 25-event reference)

---

## Install Mechanism

Install performs two operations:

1. **Merge hooks:** Deep-merge the `"hooks"` key from `hooks.json` into
   `.claude/settings.local.json`. Existing hooks for other events are preserved.
   If the same event+matcher already exists, the new hooks APPEND to the array.

2. **Copy scripts:** Copy `scripts/` directory to `~/.claude/hooks/{slug}/scripts/`.
   All `.sh` files are made executable:
   ```bash
   chmod +x ~/.claude/hooks/{slug}/scripts/*.sh
   ```
   On Windows with Git Bash/WSL, `chmod` works normally. The `bash` prefix
   in the command field handles execution permission on native Windows.

The `command` fields in hooks.json use absolute paths with tilde:
`bash ~/.claude/hooks/{slug}/scripts/handler.sh`

This matches the proven pattern used by existing Claude Code hooks (tilde expansion
works because commands are invoked via `bash`).

The CLI command:
```bash
myclaude install {slug}
```

---

## DNA Requirements

See `product-dna/hooks.yaml`.
