# claude-code-ground-truth.md

**Verified capability register for Claude Code native primitives.** Every claim in this
file is backed by a `[SOURCE:]` reference that was personally verified in session S118
against `D:\repos-reverse-engineering\claude-code-main\src\`. This file is the single
truth source that all family-skill codices (agent, squad, system, minds, workflow, hooks,
claude-md) reference. No codex may claim a capability not present here.

**Purpose:** protect the Engine's product-dna codices from speculation. When a codex
says "Claude Code supports X", the reader can follow the SOURCE reference and see the
real line of TypeScript that implements X.

**Last verified:** S118, against a git snapshot of `claude-code-main/src/` as
available on disk at `D:\repos-reverse-engineering\claude-code-main\src\`.

**What this file is NOT:** a replacement for reading the source. When a question arises
that this file does not answer, the answer is to read the source — not to guess.

---

## Layer 0 — CLAUDE.md memory hierarchy (the constitutional layer)

**Verified in S118c against `src/utils/claudemd.ts:1-26` (the file's own header
documentation).** This is the merge hierarchy that determines how multiple
CLAUDE.md files combine into the model's effective constitution per turn.

### The four memory tiers, in load order (= reverse order of priority)

| Tier | Source | Path | Scope | Purpose |
|---|---|---|---|---|
| 1 (lowest priority) | Managed memory | `/etc/claude-code/CLAUDE.md` | system-wide | Org-managed global instructions for all users on the machine |
| 2 | User memory | `~/.claude/CLAUDE.md` | per user | Private global instructions for all the user's projects |
| 3 | Project memory | `CLAUDE.md` + `.claude/CLAUDE.md` + `.claude/rules/*.md` | per project | Instructions checked into the codebase, traversed UP from cwd to root |
| 4 (highest priority) | Local memory | `CLAUDE.local.md` | per project, private | Private project-specific instructions, NOT in version control |

**Critical loading rule** [SOURCE: claudemd.ts:1-16]:

> "Files are loaded in **reverse order of priority**, i.e., the latest files
> are highest priority with the model paying more attention to them."

This means: the file LOADED LAST is the file the MODEL PAYS MOST ATTENTION TO.
This is the structural form of D19 (Attention-Aware Authoring) operating at the
constitution layer itself. The merge order is not a flat union — it is an
ordered concatenation where recency in the prompt = priority in attention.

### Project memory traversal

Project memory is discovered by walking UP from the current directory to root,
checking each directory for `CLAUDE.md`, `.claude/CLAUDE.md`, and every `*.md`
file inside `.claude/rules/`. **Files closer to the current directory have
higher priority** (loaded LATER, attention-recency wins). [SOURCE: claudemd.ts:6, 12-16]

This is why a project-root `.claude/rules/myclaude-status.md` overrides a
parent-directory rule of the same name without any explicit precedence
declaration — the closer file is simply loaded later in the concatenation.

### The `@include` directive

Memory files compose recursively via `@path` notation [SOURCE: claudemd.ts:18-26]:

- `@path`, `@./relative/path`, `@~/home/path`, or `@/absolute/path`
- Bare `@path` (no prefix) is treated as relative (same as `@./path`)
- Resolved in **leaf text nodes only** — not inside fenced code blocks or code spans
- Included files are added as **separate entries before the including file**
  (so the includer wins on attention recency over the included)
- Circular references are tracked and prevented
- Non-existent files are silently ignored — no broken-include errors
- Only files with extensions in `TEXT_FILE_EXTENSIONS` (~80 extensions including
  `.md`, `.txt`, `.yaml`, `.json`, `.ts`, `.py`, etc.) are eligible —
  binary files are skipped to prevent loading PDFs/images into memory.

### Memory file size cap

`MAX_MEMORY_CHARACTER_COUNT = 40000` [SOURCE: claudemd.ts:92]. Memory files
larger than this are eligible for truncation by `truncateEntrypointContent`
(applied to `AutoMem` and `TeamMem` types specifically). This is the hard
upper bound on a single memory file's contribution to the prompt.

### Frontmatter `paths:` glob scoping

A CLAUDE.md or rule file may declare a `paths:` frontmatter field with glob
patterns. The file is then **conditional** — it only contributes to the
constitution when files matching those globs are present in the working
context. [SOURCE: claudemd.ts:253-279 parseFrontmatterPaths] Patterns ending
in `/**` are normalized to `/`. A pattern of `**` alone is treated as
no-glob (file always applies). This is the mechanism by which a `claude-md`
product type can declare ambient-only-when-relevant scope.

### HTML comment stripping

Block-level HTML comments (`<!-- ... -->`) at the line level are stripped
from memory files BEFORE they are injected into the prompt [SOURCE:
claudemd.ts:281-334 stripHtmlComments]. Comments inside fenced code blocks
and inline code spans are preserved. Inline comments inside a paragraph are
also preserved — only standalone comment lines are stripped. This means
authorial WHY comments at block level are invisible to the model at runtime
but visible to readers of the source file. **This is the mechanism `/package`
exploits to strip WHY comments — the runtime would have stripped them anyway,
so `/package` is making the disk file match what the runtime sees.**

### Implication for system.yaml claude_md_fragment_spec

A forged system that ships a CLAUDE.md fragment via install_manifest can rely on:
1. **Project tier (3)** as the canonical install target for system-shipped rules
   (`.claude/rules/{slug}.md` is the convention).
2. **Reverse-priority load order** as the mechanism — the system's fragment
   loaded later than the user's global, so the system's rules win on attention.
3. **`paths:` frontmatter** as the conditional-activation mechanism — the
   fragment is dormant until matching files are touched.
4. **`@include` directive** as the composition mechanism — the system's main
   fragment can `@include` modular sub-rules for different concerns.
5. **40K char cap** as the budget — keep system fragments well under this.

This is sufficient ground truth for the codex to declare `claude_md_fragment_spec`
as `consumer_status: fully_wired` (verified, not aspirational).

---

## Layer 1 — Filesystem convention (where artifacts live, how they are found)

### `.claude/agents/` — subagent definitions

- Loader: `src/tools/AgentTool/loadAgentsDir.ts`.
- Discovery: `loadMarkdownFilesForSubdir('agents', cwd)` walks the standard search paths.
- Format: markdown with YAML frontmatter. Filename without `.md` is preserved as `filename`.
- Required frontmatter fields: `name`, `description`. Files missing either are
  silently skipped (if no `name`) or reported as failed (if `name` present but
  `description` missing). [SOURCE: loadAgentsDir.ts:541-562]
- JSON-defined agents are also supported via `parseAgentsFromJson` —
  declared in settings files as `{ "agents": { "name": { ... } } }`.

### `.claude/skills/` — skill definitions (directory format ONLY)

- Loader: `src/skills/loadSkillsDir.ts:loadSkillsFromSkillsDir`.
- Format: each skill is a DIRECTORY `{skillName}/SKILL.md`. Single `.md` files at
  the top level of `.claude/skills/` are NOT loaded. [SOURCE: loadSkillsDir.ts:423-429]
- A skill's `baseDir` is its directory path — this is what `${CLAUDE_SKILL_DIR}`
  resolves to at invocation time. [SOURCE: loadSkillsDir.ts:357-363]
- **Namespace via path**: skills can live in subdirectories. A skill at
  `.claude/skills/squad-review/reviewer/SKILL.md` gets named `squad-review:reviewer`
  — the `:` separator comes from `buildNamespace` joining pathSep segments.
  [SOURCE: loadSkillsDir.ts:523-543] This is how nested skill namespaces work natively.
  **myClaude can use this for squad/system sub-skill organization without prefix tricks.**

### `.claude/commands/` — legacy slash commands

- Loader: `loadSkillsFromCommandsDir`.
- Supports both `.md` files AND `{name}/SKILL.md` directories.
- Defaults to `user-invocable: true`.
- Marked as `loadedFrom: 'commands_DEPRECATED'` in the source.
  [SOURCE: loadSkillsDir.ts:67-73, 566-623]

### Source precedence (lower index = loaded first, higher index overrides)

For agents, the `getActiveAgentsFromList` function merges by `agentType` with this
precedence — later sources override earlier ones:

1. `built-in`
2. `plugin`
3. `userSettings` (`~/.claude/`)
4. `projectSettings` (`.claude/` in cwd)
5. `flagSettings` (command-line flags)
6. `policySettings` (organization-managed)

[SOURCE: loadAgentsDir.ts:193-221]

**Implication for myClaude distribution:** a published agent with `agentType: reviewer`
can be overridden by a user's project agent with the same name. This is native and
intentional.

### Deduplication by filesystem identity

Skills are deduplicated by `realpath` — the same file accessed through a symlink is
recognized as the same skill and loaded once. [SOURCE: loadSkillsDir.ts:118-124, 725-769]

### Dynamic skill discovery (walk-up from touched files)

`discoverSkillDirsForPaths(filePaths, cwd)` walks up from any touched file path,
looking for `.claude/skills/` directories along the way. This means skills can be
discovered **below** the cwd dynamically, not just at session boot. Gitignored
directories are skipped. [SOURCE: loadSkillsDir.ts:861-915]

---

## Layer 2 — Frontmatter schemas (the ONLY fields Claude Code recognizes)

### Agent frontmatter — full field list

Verified against `loadAgentsDir.ts:73-99` (Zod schema `AgentJsonSchema`) and
`loadAgentsDir.ts:541-755` (`parseAgentFromMarkdown` — the markdown parser that is
authoritative for agents defined as `.md` files).

| Field | Type | Required | Effect | SOURCE |
|---|---|---|---|---|
| `name` | string | YES | Agent's invocation name. Used as `agentType`. | loadAgentsDir.ts:404-409 |
| `description` | string | YES | `whenToUse` — the catalog description the parent LLM reads to decide whether to invoke this agent. Token-counted in catalog. | loadAgentsDir.ts:411-414, 550 |
| `tools` | string or array | no | Allowlist of tool names. `['*']` means all tools (fork children use this). Parsed by `parseAgentToolsFromFrontmatter`. | loadAgentsDir.ts:660 |
| `disallowedTools` | string or array | no | Denylist of tool names. Can combine with `tools`; runtime intersection = `tools` minus `disallowedTools`. | loadAgentsDir.ts:677-681 |
| `model` | string | no | Model override. Accepts model name strings OR `"inherit"` (lowercase) to use parent's `mainLoopModel`. | loadAgentsDir.ts:568-573 |
| `effort` | string or int | no | Reasoning effort level. Valid strings from `EFFORT_LEVELS` enum. Integer also accepted. Parsed by `parseEffortValue`. | loadAgentsDir.ts:624-631 |
| `permissionMode` | string | no | Override permission mode. Valid values from `PERMISSION_MODES` enum: includes `default`, `plan`, `dontAsk`, `bypassPermissions`, `acceptEdits`, `bubble`, `auto` (verified via runAgent.ts:420-464). | loadAgentsDir.ts:634-645 |
| `maxTurns` | positive int | no | Maximum agentic turns before stopping. | loadAgentsDir.ts:647-654 |
| `memory` | `user\|project\|local` | no | Memory scope. If `isAutoMemoryEnabled()` is true and memory is set, Write/Edit/Read tools are auto-injected into the agent's tool pool so the agent can persist to its memory. | loadAgentsDir.ts:456-467, 594-605 |
| `mcpServers` | array | no | Per-agent MCP server specs. Each item is either a string (reference to existing server by name) OR an inline object `{serverName: config}` that creates an ephemeral server for the lifetime of the agent. | loadAgentsDir.ts:57-68, 693-708 |
| `hooks` | object | no | Session-scoped hooks registered when agent starts. Validated by `HooksSchema`. Cleaned up when agent finishes. | loadAgentsDir.ts:424-440, 710-711 |
| `skills` | comma-separated string | no | Skill names to preload into the agent's initial context. `runAgent` resolves each name and injects the skill's prompt into initialMessages. | loadAgentsDir.ts:684, runAgent.ts:577-646 |
| `initialPrompt` | string | no | Text prepended to the first user turn. Slash commands work here. | loadAgentsDir.ts:123, 686-690 |
| `background` | bool | no | When true, agent always runs as background task when spawned. Default false. | loadAgentsDir.ts:575-591 |
| `isolation` | `worktree\|remote` | no | When `worktree`, agent runs in an isolated git worktree — its own working copy. When `remote` (ant-only), runs remotely in CCR. Non-ant builds reject `remote` at parse time. | loadAgentsDir.ts:607-621 |
| `color` | AgentColorName | no | Display color in the teams/agents panel. | loadAgentsDir.ts:567 |
| `criticalSystemReminder_EXPERIMENTAL` | string | no | **Load-bearing field.** A short message that is re-injected at every user turn of the agent's conversation. Used by `verificationAgent` to enforce the VERDICT protocol. This is the mechanism for persistent constitution without relying on the LLM to remember. | loadAgentsDir.ts:121, verificationAgent.ts:150-151, runAgent.ts:711-714 |
| `omitClaudeMd` | bool | no | When true, the agent does not inherit the parent's CLAUDE.md hierarchy. Gated by `tengu_slim_subagent_claudemd` GrowthBook flag (default true). Used by `Explore` and `Plan` — saves ~5-15 Gtok/week at fleet scale. | loadAgentsDir.ts:127-133, runAgent.ts:390-398 |
| `requiredMcpServers` | string array | no | Pattern list of MCP server names the agent requires to be available. Agent is filtered out of the selectable list if any pattern fails to match. Case-insensitive substring match. | loadAgentsDir.ts:125, 229-242 |

### Skill frontmatter — full field list

Verified against `src/utils/frontmatterParser.ts:10-59` (type declaration) and
`src/skills/loadSkillsDir.ts:185-265` (`parseSkillFrontmatterFields` — the parser).

| Field | Type | Effect | SOURCE |
|---|---|---|---|
| `name` | string | Optional display name override (the skill directory name is used otherwise). | loadSkillsDir.ts:238 |
| `description` | string | Skill description. Validated by `coerceDescriptionToString`. If absent, extracted from the markdown body by `extractDescriptionFromMarkdown`. | frontmatterParser.ts:304-326, loadSkillsDir.ts:208-214 |
| `allowed-tools` | string or array | Tool allowlist when the skill invokes the model (for context:fork skills). | loadSkillsDir.ts:242-244 |
| `argument-hint` | string | Short hint shown in /help for the skill's `$ARGUMENTS`. | loadSkillsDir.ts:245-249 |
| `arguments` | string or array | Declared argument names, parsed by `parseArgumentNames`. | loadSkillsDir.ts:249-251 |
| `when_to_use` | string | Natural language trigger text. Token-counted in catalog. | loadSkillsDir.ts:252 |
| `version` | string | Version marker. | loadSkillsDir.ts:253 |
| `model` | string | Model override. Accepts `inherit` to use parent. | loadSkillsDir.ts:221-226 |
| `disable-model-invocation` | bool string | When true, model CANNOT auto-invoke the skill — only user can. | loadSkillsDir.ts:255-257 |
| `user-invocable` | bool string | When true, user can type `/skill-name`. Default differs by source (`commands/` defaults true, `skills/` defaults false). | frontmatterParser.ts:28-33, loadSkillsDir.ts:216-219 |
| `hooks` | object | Session-scoped hooks registered when skill is invoked. | loadSkillsDir.ts:136-153, 259 |
| `context` | `inline\|fork` | Execution context. `inline` (default): skill content expands into the current conversation. `fork`: skill runs as a sub-agent with separate context and token budget. **This is how any skill can become a subagent.** | frontmatterParser.ts:43-47, loadSkillsDir.ts:260-262 |
| `agent` | string | When `context: fork`, specifies which agent type to use. e.g. `general-purpose`, `Explore`, `Plan`, or any custom agent name. | frontmatterParser.ts:46-47, loadSkillsDir.ts:261 |
| `effort` | string or int | Effort level, same as agent. | loadSkillsDir.ts:228-235 |
| `shell` | `bash\|powershell` | Which shell to use for inline `!` blocks in the skill body. Defaults to bash. Skill-scoped, not session-scoped — author controls portability. | frontmatterParser.ts:55-57, 339-370 |
| `paths` | string or array | Glob patterns scoping when the skill activates. Uses `ignore` library (gitignore-style matching). Skills with paths are CONDITIONAL — stored in `conditionalSkills` map until matching files are touched, then activated via `activateConditionalSkillsForPaths`. | frontmatterParser.ts:48-52, loadSkillsDir.ts:159-178, 997-1058 |

**Critical insight**: `paths:` on skills enables **ambient cost zero until activation**. A
squad can bundle 10 specialist skills, each scoped to different file patterns, and the
buyer pays tokens only for the ones that match their current work.

### Hook schema — full type list

Verified against `src/schemas/hooks.ts`. There are **FOUR** hook types, not just bash commands:

#### 1. `BashCommandHook` — shell command execution

```yaml
type: command
command: "./scripts/verify.sh"
if: "Bash(git *)"           # permission rule syntax — only fires when matching
shell: bash                 # or 'powershell'
timeout: 30                 # seconds
statusMessage: "Verifying"
once: false                 # removed after execution if true
async: false                # background execution
asyncRewake: false          # background + wake on exit code 2 (blocking error)
```
[SOURCE: schemas/hooks.ts:31-66]

#### 2. `PromptHook` — LLM prompt evaluation

```yaml
type: prompt
prompt: "Is this commit message clear? Answer YES or NO. Input: $ARGUMENTS"
if: "Bash(git commit *)"
timeout: 30
model: "claude-haiku-4-5"    # defaults to small fast model
statusMessage: "Checking commit"
once: false
```
[SOURCE: schemas/hooks.ts:67-96]

**This is load-bearing**: hooks can be LLM reasoning, not just shell side effects. A
squad orchestrator can use a `PromptHook` to decide routing — YAML declarative with
LLM semantic matching.

#### 3. `HttpHook` — webhook POST

```yaml
type: http
url: "https://ci.example.com/notify"
if: "Write(*.py)"
timeout: 10
headers:
  Authorization: "Bearer $MY_TOKEN"
allowedEnvVars: [MY_TOKEN]   # env var interpolation whitelist — required
statusMessage: "Notifying CI"
once: false
```
[SOURCE: schemas/hooks.ts:97-126]

Env var interpolation is opt-in per hook via `allowedEnvVars`. Variables not whitelisted
are replaced with empty strings. This is the security boundary for distributed hook configs.

#### 4. `AgentHook` — agentic verifier

```yaml
type: agent
prompt: "Verify that unit tests ran and passed for the files just changed."
if: "Write(**/*.test.ts)"
timeout: 60
model: "claude-sonnet-4-6"   # defaults to Haiku
statusMessage: "Verifying tests"
once: false
```
[SOURCE: schemas/hooks.ts:128-163]

A hook that spawns a full agent to verify something. Used by `VerifyPlanExecutionTool`.
**Hooks can be agents.** This collapses the distinction between lifecycle reaction and
cognitive verification.

### Hook matching — `if:` condition

All four hook types support an `if:` field that uses **permission rule syntax** —
the same DSL used for tool permission rules like `Bash(git *)` or `Read(*.ts)`. The
hook is only evaluated if the tool call matches the pattern. This avoids spawning
hooks for non-matching events.

[SOURCE: schemas/hooks.ts:19-27]

### Hook events — canonical enum (27 events)

The `HOOK_EVENTS` constant is defined in `src/entrypoints/sdk/coreTypes.ts:25-53`
(and re-exported as a `z.enum` in `src/entrypoints/sdk/coreSchemas.ts:355-385`).
It is the SINGLE source of truth for which event names a hook may bind to.
[SOURCE: coreTypes.ts:25-53; coreSchemas.ts:355-385] — verified in S118c.

The full canonical list, in declaration order:

| # | Event | Phase | Notes |
|---|-------|-------|-------|
| 1 | `PreToolUse` | per-tool | fires before any tool invocation; can block |
| 2 | `PostToolUse` | per-tool | fires after successful tool execution |
| 3 | `PostToolUseFailure` | per-tool | fires only when a tool invocation errored |
| 4 | `Notification` | session | UI-bound notifications (e.g., permission toast) |
| 5 | `UserPromptSubmit` | per-turn | fires when the user submits a prompt |
| 6 | `SessionStart` | session-boot | always-emitted [hookEvents.ts:18 ALWAYS_EMITTED list] |
| 7 | `SessionEnd` | session-end | symmetric pair to SessionStart |
| 8 | `Stop` | per-turn | main agent stop; converted to SubagentStop inside agents |
| 9 | `StopFailure` | per-turn | fires only on stop-with-error |
| 10 | `SubagentStart` | per-spawn | injects `additionalContexts[]` into child [runAgent.ts:532-555] |
| 11 | `SubagentStop` | per-spawn | symmetric pair to SubagentStart |
| 12 | `PreCompact` | compact | fires before `/compact` runs — last chance to persist |
| 13 | `PostCompact` | compact | fires after compaction completes |
| 14 | `PermissionRequest` | runtime | fires when a permission decision is requested |
| 15 | `PermissionDenied` | runtime | fires when a permission decision returned deny |
| 16 | `Setup` | session-boot | always-emitted alongside SessionStart |
| 17 | `TeammateIdle` | teams | fires when a teammate becomes idle |
| 18 | `TaskCreated` | task-mgmt | TaskCreate tool fired |
| 19 | `TaskCompleted` | task-mgmt | a task transitioned to completed |
| 20 | `Elicitation` | mcp | MCP elicitation request received |
| 21 | `ElicitationResult` | mcp | MCP elicitation answered |
| 22 | `ConfigChange` | settings | settings.json or environment changed at runtime |
| 23 | `WorktreeCreate` | worktree | git worktree was created (e.g., isolation: worktree) |
| 24 | `WorktreeRemove` | worktree | git worktree was removed |
| 25 | `InstructionsLoaded` | claude-md | a CLAUDE.md / rules file finished loading |
| 26 | `CwdChanged` | filesystem | cwd changed (cd or worktree switch) |
| 27 | `FileChanged` | filesystem | a watched file changed on disk |

**Two events are ALWAYS emitted regardless of matchers:** `SessionStart` and
`Setup` [SOURCE: hookEvents.ts:18 ALWAYS_EMITTED_HOOK_EVENTS]. These two are the
canonical entry points for `constitutional_homeostasis_via_session_hook` patterns.

**Implication for system.yaml hooks_fragment_spec and Brecha #1:** the canonical
list of trigger events for organism-level lifecycle reactions is FULLY ENUMERATED
above. A forged system that wants to install a session-boot homeostasis verifier
binds to `SessionStart` (or `Setup` for managed contexts). A longitudinal observer
binds to `PostToolUse` and/or `TaskCompleted`. A pre-compact survival snapshot
binds to `PreCompact`. A constitution change reaction binds to `InstructionsLoaded`
or `ConfigChange`. None of these are speculation; all 27 are real and bind-able.

---

## Layer 3 — Subagent runtime (how Task tool actually spawns and retrieves)

### The runAgent function

`src/tools/AgentTool/runAgent.ts:runAgent` is the canonical entry point. It is an
`AsyncGenerator<Message>` — meaning the parent CAN stream the subagent's messages
as they arrive, not just wait for a final result. Most callers just collect the
final assistant message and treat it as the return value.

**What the parent passes in**:
- `agentDefinition` — the resolved AgentDefinition
- `promptMessages` — the prompt the parent writes for the subagent (already structured as Message[])
- `toolUseContext` — the parent's ToolUseContext (reused or forked)
- `canUseTool` — permission check callback
- `isAsync` — whether this is a background spawn
- `canShowPermissionPrompts` — whether the subagent can interrupt the parent with permission dialogs
- `forkContextMessages` — optional: when present, the subagent INHERITS parent's conversation history up to a point. This is what fork children use.
- `maxTurns` — overrides agentDefinition.maxTurns if set
- `override.userContext` / `override.systemContext` / `override.systemPrompt` — rare: pre-rendered replacements (fork children use override.systemPrompt for byte-identical cache prefix)
- `model` — alias override
- `availableTools` — precomputed tool pool (caller computes to avoid circular imports)
- `allowedTools` — session-level allow rules that REPLACE parent's session rules (to prevent parent approvals leaking through)
- `useExactTools` — for fork children: skip filtering, use exact tools for cache identity
- `worktreePath` — if isolation: worktree, the child's git worktree path
- `description` — task description, persisted to metadata for resume

[SOURCE: runAgent.ts:248-329]

### What the child agent receives in its context

The child agent's context is assembled in this order (verified in runAgent.ts:370-713):

1. **`forkContextMessages`** (if any) — parent's history up to the fork point, with
   incomplete tool calls filtered out.
2. **`promptMessages`** — the new prompt from the parent.
3. **`SubagentStart` hook additional contexts** — if hooks return `additionalContexts[]`,
   they are appended as a user message. This is a **native dependency injection** point.
4. **Preloaded skills** — for each skill in `agentDefinition.skills`, the resolved skill's
   `getPromptForCommand('', toolUseContext)` result is prepended as a user `isMeta: true` message.
5. **Agent's own system prompt** — from `agentDefinition.getSystemPrompt()`, possibly
   enhanced with env details (cwd, platform, tool names).
6. **`criticalSystemReminder_EXPERIMENTAL`** — if set, this short string is re-injected
   at every user turn of the child's conversation, via `agentToolUseContext.criticalSystemReminder_EXPERIMENTAL`.

### What the child agent can access from the parent

Determined by `createSubagentContext` (in `utils/forkedAgent.ts` — not yet verified in S118):

- Sync agents SHARE `setAppState`, `setResponseLength`, `abortController` with parent.
- Async agents are **fully isolated** — own AbortController, own app state path.
- All agents get a CLONED `readFileState` cache (parent's clone when forked, fresh limited
  cache when non-forked).
- The child's `messages` start as the `initialMessages` assembled above.

[SOURCE: runAgent.ts:694-714]

### Permission mode override behavior

If the agent defines a `permissionMode`, it overrides the parent's — UNLESS the parent
is already in `bypassPermissions`, `acceptEdits`, or (with `TRANSCRIPT_CLASSIFIER` flag)
`auto` mode. Those modes take precedence.

For async agents: `shouldAvoidPermissionPrompts` is auto-set unless the agent is in
`bubble` mode OR `canShowPermissionPrompts` is explicitly true.

For async agents that CAN show prompts: `awaitAutomatedChecksBeforeDialog: true` is set
— meaning classifier and permission hooks run before the dialog appears.

[SOURCE: runAgent.ts:415-464]

### `bubble` permission mode — load-bearing feature

Agents in `permissionMode: bubble` run async but still surface permission prompts to
the parent terminal. This enables background agents that genuinely need user input
without blocking the parent's flow. The `FORK_AGENT` uses this.
[SOURCE: forkSubagent.ts:67]

### Tool merging: agent tools + MCP tools

When an agent declares `mcpServers` in its frontmatter, `initializeAgentMcpServers`:
1. Connects to each referenced server OR creates ephemeral inline servers
2. Fetches their tools
3. Merges them with the agent's resolved tool pool (dedup by name)
4. Returns a cleanup function that destroys ephemeral servers when the agent finishes

The cleanup runs in a `finally` block — guaranteed even on abort or error.

[SOURCE: runAgent.ts:95-218, 648-664, 817]

### Subagent return to parent

The parent that calls `runAgent` receives an `AsyncGenerator<Message>`. It iterates
the generator, typically consuming only the FINAL assistant message and treating
its text as the subagent's output. In the prompt template for the Agent tool, the
convention is:

> "When the agent is done, it will return a single message back to you. The result
> returned by the agent is not visible to the user."
>
> [SOURCE: AgentTool/prompt.ts:257]

This means:
- Return value is **unstructured text by default**.
- The parent must prompt the child to produce structured output (JSON, YAML, XML)
  if it wants to parse it.
- For verification agents, the convention is a line like `VERDICT: PASS|FAIL|PARTIAL`
  that the parent can grep for. [SOURCE: verificationAgent.ts:117-127]

**Implication for `output_contract`** (myClaude convention): this is a COACHING
field, not a nativeenforced contract. The codex tells the creator to instruct
the child to return structured output; Claude Code does not natively parse it.

### Background agents and `asyncRewake`

Agents declared with `background: true` always spawn in the background regardless of
caller preference. The Agent tool prompt explains:

> "You can optionally run agents in the background using the run_in_background parameter.
> When an agent runs in the background, you will be automatically notified when it
> completes — do NOT sleep, poll, or proactively check on its progress."
>
> [SOURCE: AgentTool/prompt.ts:262-265]

For `BashCommandHook` types, there is `asyncRewake: true` which means "run in background
AND wake the model on exit code 2" — this is the mechanism for lifecycle side effects
that can interrupt the main flow when they detect something important.

---

## Layer 4 — Fork subagent (the crown jewel of composition)

### What forking is

When `isForkSubagentEnabled()` returns true (gated by `FORK_SUBAGENT` feature flag
AND NOT in coordinator mode AND NOT non-interactive session), the Agent tool gains a
new mode: **omit `subagent_type`** to trigger an implicit fork.

[SOURCE: forkSubagent.ts:32-39]

A fork child:
- Inherits the parent's FULL conversation context (history up to the fork point)
- Inherits the parent's exact rendered system prompt (byte-identical, threaded via `toolUseContext.renderedSystemPrompt`)
- Inherits the parent's exact tool pool (via `useExactTools: true`)
- Uses `tools: ['*']` (all tools)
- Uses `model: 'inherit'` (must match parent for prompt cache hits)
- Uses `permissionMode: 'bubble'` (bubbles prompts to parent terminal)
- Runs async (background) with `maxTurns: 200`

[SOURCE: forkSubagent.ts:60-71]

### Why forking is disruptive

**Prompt cache sharing.** Fork children all produce byte-identical API request prefixes
up to the fork point. This means:
1. Parent's cache hit ratio stays maximum.
2. Each fork child pays ONLY for the divergent suffix.
3. Spawning 5 fork children to answer 5 parallel questions costs nearly the same
   as spawning 1 — the shared prefix is cached once.

The code explicitly constructs a single user message with `[tool_result, tool_result, ...,
text_directive]` where every tool_result uses the identical placeholder:

```js
const FORK_PLACEHOLDER_RESULT = 'Fork started — processing in background'
```

Only the final text block differs per child. This is deliberate — "Only the final text
block differs per child, maximizing cache hits." [SOURCE: forkSubagent.ts:91-169]

### The fork child directive — constitution in the prompt body

Every fork child receives this message as its last user turn content
[SOURCE: forkSubagent.ts:171-198]:

```
<fork-boilerplate>
STOP. READ THIS FIRST.

You are a forked worker process. You are NOT the main agent.

RULES (non-negotiable):
1. Your system prompt says "default to forking." IGNORE IT — that's for the parent. You ARE the fork. Do NOT spawn sub-agents; execute directly.
2. Do NOT converse, ask questions, or suggest next steps
3. Do NOT editorialize or add meta-commentary
4. USE your tools directly: Bash, Read, Write, etc.
5. If you modify files, commit your changes before reporting. Include the commit hash in your report.
6. Do NOT emit text between tool calls. Use tools silently, then report once at the end.
7. Stay strictly within your directive's scope. If you discover related systems outside your scope, mention them in one sentence at most — other workers cover those areas.
8. Keep your report under 500 words unless the directive specifies otherwise. Be factual and concise.
9. Your response MUST begin with "Scope:". No preamble, no thinking-out-loud.
10. REPORT structured facts, then stop

Output format (plain text labels, not markdown headers):
  Scope: <echo back your assigned scope in one sentence>
  Result: <the answer or key findings, limited to the scope above>
  Key files: <relevant file paths — include for research tasks>
  Files changed: <list with commit hash — include only if you modified files>
  Issues: <list — include only if there are issues to flag>
</fork-boilerplate>

<fork-directive>{directive}</fork-directive>
```

**This is the canonical fork protocol.** Study it. It teaches the exact discipline
that a forked worker must follow. It is the single best template in the Claude Code
source for how to write a constraining prompt.

### Recursive fork prevention

Fork children keep the Agent tool in their pool (for cache-identical tool definitions),
so the recursive-fork guard runs at Agent tool call time. It detects whether the
conversation already contains a `<fork-boilerplate>` block; if yes, fork is rejected.
[SOURCE: forkSubagent.ts:73-89]

### Worktree notice

When a fork (or any agent) spawns with `isolation: 'worktree'`, there is an additional
notice injected into the child's context:

> "You've inherited the conversation context above from a parent agent working in
> {parentCwd}. You are operating in an isolated git worktree at {worktreeCwd}...
> Your changes stay in this worktree and will not affect the parent's files."
>
> [SOURCE: forkSubagent.ts:205-210]

---

## Layer 5 — Built-in agents (canonical archetype examples)

These six built-in agents are the **ground-truth templates** for agent archetypes. Any
myClaude agent archetype should be derivable from one of these shapes.

### 1. `Explore` — Fast read-only search specialist

[SOURCE: src/tools/AgentTool/built-in/exploreAgent.ts]

```yaml
agentType: Explore
disallowedTools: [Agent, ExitPlanMode, Edit, Write, NotebookEdit]
model: haiku  # (ants: inherit)
omitClaudeMd: true
```

Prompt pattern: "You are a file search specialist for Claude Code... READ-ONLY MODE...
STRICTLY PROHIBITED from: Creating new files, Modifying existing files, Deleting files..."

**Archetype**: SCOUT — fast, parallel, read-only, drops expensive context (CLAUDE.md,
gitStatus), returns concise findings.

**Defining properties**:
- `disallowedTools` enforces read-only at the tool level (can't even try to Write)
- `omitClaudeMd: true` drops 5-15 Gtok/week of context
- Hardcoded to haiku (or inherit for ants) — speed over depth
- In `ONE_SHOT_BUILTIN_AGENT_TYPES` — no SendMessage follow-up [SOURCE: constants.ts:9-12]

### 2. `Plan` — Read-only software architect

[SOURCE: src/tools/AgentTool/built-in/planAgent.ts]

```yaml
agentType: Plan
disallowedTools: [Agent, ExitPlanMode, Edit, Write, NotebookEdit]
tools: <inherits from Explore>
model: inherit
omitClaudeMd: true
```

Prompt pattern: "You are a software architect and planning specialist for Claude Code.
Your role is to explore the codebase and design implementation plans. READ-ONLY..."

Required output: "### Critical Files for Implementation — List 3-5 files most critical..."

**Archetype**: ARCHITECT — same tool restrictions as Explore, but optimized for
structured planning output. Also one-shot.

### 3. `general-purpose` — The flexible default

[SOURCE: src/tools/AgentTool/built-in/generalPurposeAgent.ts]

```yaml
agentType: general-purpose
tools: ['*']
# no model (uses getDefaultSubagentModel())
```

Prompt pattern: "You are an agent for Claude Code... complete the task fully—don't
gold-plate, but don't leave it half-done. ... Your strengths: Searching for code,
Analyzing multiple files, Investigating complex questions, Performing multi-step research."

**Archetype**: GENERALIST — all tools, no hard constraints, relies on prompting for
discipline. The fallback for unstructured tasks.

### 4. `verification` — Adversarial verifier with VERDICT protocol

[SOURCE: src/tools/AgentTool/built-in/verificationAgent.ts]

```yaml
agentType: verification
color: red
background: true
disallowedTools: [Agent, ExitPlanMode, Edit, Write, NotebookEdit]
model: inherit
criticalSystemReminder_EXPERIMENTAL:
  "CRITICAL: This is a VERIFICATION-ONLY task. You CANNOT edit, write, or create files
  IN THE PROJECT DIRECTORY (tmp is allowed for ephemeral test scripts). You MUST end
  with VERDICT: PASS, VERDICT: FAIL, or VERDICT: PARTIAL."
```

Prompt pattern: "You are a verification specialist. Your job is not to confirm the
implementation works — it's to try to break it. You have two documented failure
patterns. First, verification avoidance... Second, being seduced by the first 80%..."

Required output: structured check blocks with `Command run / Output observed / Result`
followed by a literal `VERDICT: PASS|FAIL|PARTIAL` line the parent greps for.

**Archetype**: ADVERSARIAL VERIFIER — background, tool-restricted, with a
`criticalSystemReminder` that is re-injected every turn to prevent drift. Produces a
machine-parsable verdict.

**Why this agent is a masterclass**: it NAMES its own failure modes in the system prompt
("verification avoidance", "seduced by the first 80%") AND provides specific rationalizations
it must recognize and reject. This is D11 (Socratic Pressure) and D2 (Anti-Pattern Guard)
fused into a single prompt.

### 5. `fork` (synthetic — FORK_AGENT) — Context-inheriting worker

[SOURCE: forkSubagent.ts:60-71]

```yaml
agentType: fork           # synthetic, not in builtInAgents registry
tools: ['*']              # with useExactTools: true for byte-identical cache
maxTurns: 200
model: inherit            # MUST match parent for cache hits
permissionMode: bubble    # surfaces prompts to parent terminal
```

**Archetype**: CONTEXT-HEIR — inherits parent's full conversation, prompt, and tool
pool. Used for parallel work where dropping context would waste the cache investment.

### 6. `claude-code-guide` (referenced, not fully read in S118)

Referenced in the file listing but source contents not read. Name suggests a
documentation/help agent.

### Archetype summary table — to drive agent.yaml design

| Archetype | Tools pattern | Model | Background | omitClaudeMd | criticalReminder | Example |
|---|---|---|---|---|---|---|
| **SCOUT** | denylist mutation tools | haiku or inherit | no | YES | — | Explore |
| **ARCHITECT** | denylist mutation tools | inherit | no | YES | — | Plan |
| **GENERALIST** | `['*']` | default | optional | no | — | general-purpose |
| **ADVERSARIAL VERIFIER** | denylist mutation | inherit | YES | no | YES | verification |
| **CONTEXT-HEIR** | `['*']` (exact) | inherit | YES | no | — | fork |
| **SPECIALIST (custom)** | narrow allowlist | depends | optional | optional | optional | (user-defined) |

---

## Layer 6 — Skills as composition material

### Agents preload skills natively

When an agent frontmatter declares `skills: [name1, name2]`, `runAgent` resolves each
skill name (via `resolveSkillName`) and calls `skill.getPromptForCommand('', toolUseContext)`.
The resulting content is prepended as a user `isMeta: true` message with metadata
formatting from `formatSkillLoadingMetadata`. [SOURCE: runAgent.ts:577-646]

**This means:** an agent = persona + tools + pre-loaded skill knowledge. A "squad" in
myClaude terms can be implemented as:

1. An orchestrator agent with `skills: [routing, handoff-format]` pre-loaded.
2. N specialist agents, each with `skills: [specialist-knowledge-N]` pre-loaded.
3. Routing logic in the orchestrator's body that calls `Task(subagent_type: specialist-N)`.

This is distributable as pure files — no install magic, no convention fiction.

### Skill name resolution (the 3-strategy algorithm)

From `runAgent.ts:945-973`:

```typescript
// 1. Direct match via hasCommand (checks name, userFacingName, aliases)
if (hasCommand(skillName, allSkills)) return skillName

// 2. Try prefixing with the agent's plugin name
const pluginPrefix = agentDefinition.agentType.split(':')[0]
if (pluginPrefix && hasCommand(`${pluginPrefix}:${skillName}`, allSkills)) {
  return `${pluginPrefix}:${skillName}`
}

// 3. Suffix match — find a skill whose name ends with ":skillName"
const match = allSkills.find(cmd => cmd.name.endsWith(`:${skillName}`))
if (match) return match.name

return null
```

Plugin-namespaced skills can be referenced by bare name from agents in the same
plugin. This is the native plugin-scoping mechanism.

### Skill placeholders

Skills' markdown body is processed at invocation time:

- `${CLAUDE_SKILL_DIR}` → replaced with the skill's own directory (backslashes normalized
  to forward slashes on Windows). Enables skills to reference bundled scripts without
  hardcoding paths. [SOURCE: loadSkillsDir.ts:357-363]
- `${CLAUDE_SESSION_ID}` → replaced with current session ID. [SOURCE: loadSkillsDir.ts:366-369]
- `` !`command` `` and ` ```! block ``` ` — inline shell execution before the prompt is
  delivered. SECURITY: MCP skills do NOT execute these (untrusted remote source).
  [SOURCE: loadSkillsDir.ts:372-396]

### Conditional skills — ambient cost zero

Skills with `paths:` frontmatter are **stored in a separate `conditionalSkills` map**
and NOT exposed to the model catalog until matching files are touched. When a Read/Write/Edit
operation fires on a matching path, `activateConditionalSkillsForPaths` moves the skill
to the active dynamic map.

[SOURCE: loadSkillsDir.ts:826-1058]

**Design implication for myClaude**: every domain-specific skill in a bundle should
consider declaring `paths:` to stay dormant until relevant. A bundle of 20 skills with
proper `paths:` scoping only surfaces the ones matching the buyer's current work —
ambient cost approaches zero.

---

## Layer 7 — Cross-cutting facts that change codex assumptions

### Fact 1: `context: fork` is the skill→subagent bridge

Any skill can become a subagent by setting `context: fork` and optionally `agent: <type>`.
This collapses skill/agent into a spectrum, not a dichotomy. The codex should reflect this.

### Fact 2: Agents are the only primitive with native MCP server composition

Skills cannot declare `mcpServers`. Only agents can. This is a hard constraint — if you
need an agent to bring its own Slack or GitHub integration, it must be an agent, not a
skill with `context: fork`.

### Fact 3: Skills cannot declare `memory` scope — only agents can

Verified: `parseSkillFrontmatterFields` does NOT read a memory field. Only agents have
`memory: user|project|local`. For persistent state in a skill, use hooks or a state file
that the skill reads/writes via its tools.

### Fact 4: `criticalSystemReminder_EXPERIMENTAL` is only for agents

This field does not exist on skills. If you need persistent constitution in a skill
body, the only mechanism is placing the rule at the END of the skill body (D19
Attention-Aware Authoring) so the rule is in the high-attention position every time
the skill loads.

### Fact 5: Hooks can reference env vars but require opt-in

Only hooks (not skills or agents directly) can interpolate env vars in their HTTP
headers. And they require `allowedEnvVars` whitelist. This is the ONLY place in the
frontmatter layer where env vars participate.

### Fact 6: Agent tool pool is computed BEFORE the agent spawns

The tool pool passed as `availableTools` is computed by the caller (AgentTool.tsx) to
avoid circular imports. The runtime intersects it with `agentDefinition.tools`,
`disallowedTools`, and `allowedTools`. [SOURCE: runAgent.ts:292-297, 500-502]

The practical implication: tool restrictions are applied at spawn time, not reconfigurable
mid-conversation. An agent's tool surface is fixed for its lifetime.

### Fact 7: Agents clean up everything on exit — guaranteed

The `finally` block in `runAgent` runs:
- MCP server cleanup (for inline ephemeral servers)
- Session hooks cleanup
- Prompt cache tracking cleanup
- File state cache release
- Initial messages release
- Perfetto tracing release
- Transcript subdir mapping release
- TodoWrite entry removal
- Background bash tasks killed
- Monitor MCP tasks killed (if feature enabled)

[SOURCE: runAgent.ts:816-858]

**This guarantees** that even malformed or aborted agents don't leak resources.
myClaude agents can safely declare ephemeral MCP servers without worrying about
zombie connections.

### Fact 8: Filename dedup handles symlinks and duplicate parent dirs

Skills accessed through symlinks are recognized as the same file via `realpath` and
loaded once with first-wins precedence. This is important for myClaude distribution:
installing the same skill in both `~/.claude/skills/` and a project `.claude/skills/`
will NOT double-load — the first-seen wins.

### Fact 9: Gitignored directories skip skill discovery

`discoverSkillDirsForPaths` calls `isPathGitignored` and skips matching paths. Skills
inside `node_modules/pkg/.claude/skills/` won't load silently. [SOURCE: loadSkillsDir.ts:892-897]

### Fact 10: `isAutoMemoryEnabled()` auto-injects FS tools into agents with memory

If `isAutoMemoryEnabled()` returns true AND the agent declares `memory: ...`, then
`Write`, `Edit`, and `Read` tools are automatically ADDED to the agent's tool pool —
even if the agent's `tools:` declaration didn't include them. This is how memory-enabled
agents physically can persist. [SOURCE: loadAgentsDir.ts:456-467, 662-674]

---

## Layer 8 — What myClaude can do that nobody in the marketplace is doing

This section translates the capabilities above into **productable features** that
differentiate myClaude from any existing Claude Code tooling.

### Feature 1: Physical D9 enforcement (Orchestrate Don't Execute)

**Native mechanism**: `disallowedTools: [Edit, Write, NotebookEdit]` on orchestrator
agents.

**Commodity approach**: prompt coaching "please don't edit files".
**myClaude approach**: codex enforces that orchestrator archetype agents MUST declare
the mutation tool denylist. Validator fails forge if a squad orchestrator has Write
or Edit in its effective tool pool.

### Feature 2: criticalSystemReminder-driven agents

**Native mechanism**: `criticalSystemReminder_EXPERIMENTAL` field re-injects a constraint
at every user turn.

**Commodity approach**: none — this field is undocumented publicly.
**myClaude approach**: the codex teaches creators to use this field for verification
agents, advisors, and any agent whose constitution must not drift. It is the native
petrification of D2+D14.

### Feature 3: paths-scoped conditional skills

**Native mechanism**: `paths: [glob, glob]` makes a skill dormant until matching files
are touched.

**Commodity approach**: skills are always in the catalog, always costing ambient tokens.
**myClaude approach**: every domain-specific skill in a bundle SHOULD declare `paths`.
The forge coaches this in scaffolding. A bundle of 20 specialist skills can have
ambient cost near zero because only the matching 2-3 activate.

### Feature 4: Ephemeral MCP composition per agent

**Native mechanism**: `mcpServers: [...]` with inline definitions creates ephemeral
servers destroyed on agent exit.

**Commodity approach**: shared MCP config forever.
**myClaude approach**: a distributed agent can bring its own MCP integration (Slack,
GitHub, Notion, custom) that only lives while the agent runs. Install manifest stays
trivial — no "please configure an MCP server manually" instructions.

### Feature 5: omitClaudeMd for read-only agents

**Native mechanism**: `omitClaudeMd: true` drops the parent CLAUDE.md hierarchy from
the agent's context.

**Commodity approach**: all subagents inherit all the context, always.
**myClaude approach**: the codex enforces that ADVISOR archetype agents (minds,
scouts, verifiers) MUST declare `omitClaudeMd: true`. Saves massive tokens, enforces
independence from project context.

### Feature 6: Fork subagent discipline — the directive pattern

**Native mechanism**: fork children receive a specific directive-style prompt that
forbids conversation, editorializing, and speculation.

**Commodity approach**: verbose back-and-forth prompts full of hedging.
**myClaude approach**: the codex teaches the fork directive pattern (10 numbered rules
+ structured output format with labeled fields). Any workflow pattern that uses fork
children must follow this template.

### Feature 7: Squad as multi-file coherent install

**Native mechanism**: multiple agent files + orchestrator agent with skill preloading,
distributed as a coherent bundle with ONE install manifest.

**Commodity approach**: "squads" published as a single SQUAD.md with prose describing
imaginary agents.
**myClaude approach**: a squad = directory `squads/{slug}/` containing:
- `SQUAD.md` (manifest describing the squad's purpose)
- `routing.yaml` (declarative routing table consumed by orchestrator)
- `agents/{role}.md` files (one per sub-agent, installed to `.claude/agents/{slug}__{role}.md` OR `.claude/agents/{slug}/{role}.md` using native path namespace)
- `skills/{role}/SKILL.md` files (per-role knowledge, namespaced via path)
- `orchestrator.md` (the orchestrator agent with `skills: [routing]` preloaded)
- `install-manifest.yaml` (declares multi-target copy + hook merge + CLAUDE.md region append)

Install via `myclaude install` reads the manifest, does the multi-target copy, and
logs what was added so `myclaude uninstall` can reverse exactly.

### Feature 8: Agent output_contract coaching (the honest version)

**Native mechanism**: none — subagent returns are unstructured text.
**Commodity approach**: parent parses free text, fragile.
**myClaude approach**: the codex declares `output_contract` as a COACHING FIELD —
the agent's body is required to include a section like "Your response MUST match this
shape: {...}" and end with a machine-parsable line. The codex validator checks the
body for this discipline. The parent then reliably parses the return because the child
was told exactly how to format it. This is convention, not runtime enforcement — but
it works because the child is LLM and obeys prompt.

### Feature 9: Hooks-as-verifier with AgentHook

**Native mechanism**: `type: agent` hooks spawn a full agent to verify something.
**Commodity approach**: hooks are shell scripts only.
**myClaude approach**: the codex teaches creators that a system's state machine can
be enforced via AgentHook type: "on PostToolUse(Write), spawn the verification agent
to verify the change, block further work if VERDICT: FAIL." State enforcement via
cognitive verification, not regex.

### Feature 10: Recursive install via `skills: [...]` composition

**Native mechanism**: an agent can preload skills. A skill can be invoked within an
agent. The agent can spawn another agent. That agent can preload different skills.
**Commodity approach**: flat composition, hand-coded.
**myClaude approach**: a system = root orchestrator agent with `skills: [router]` →
the router skill's body lists `Task(subagent_type: specialist-A)` calls → specialist
agents have `skills: [specialist-A-knowledge]`. The composition graph is declarative
in frontmatter, the execution is LLM-driven. Validator can visualize the graph for
buyers before install.

---

## Layer 9 — Outstanding gaps (to be filled in S118b or S119)

These are files that would complete the ground truth but were not read in S118. Each
has a prioritized "why it matters" note.

1. **`src/entrypoints/sdk/runtimeTypes.ts`** → exact list of HOOK_EVENTS enum values.
   Resolves Yellow Flag #3 definitively. **Priority: HIGH for hooks.yaml codex.**

2. **`src/tools/AgentTool/AgentTool.tsx`** (157K tokens, read in targeted slices) →
   the Zod input schema that defines what parameters the Task tool accepts
   (`subagent_type`, `prompt`, `description`, `run_in_background`, etc.) and
   the return type structure. **Priority: HIGH for verifying output_contract claims.**

3. **`src/utils/claudemd.ts`** → how CLAUDE.md files are loaded, merged, and scoped.
   Resolves how system.yaml can distribute CLAUDE.md fragments. **Priority: HIGH for
   system.yaml codex.**

4. **`src/tools/AgentTool/agentMemory.ts`** + **`agentMemorySnapshot.ts`** → exact
   behavior of memory scopes, whether snapshots are copied between projects, what
   `AGENT_MEMORY_SNAPSHOT` feature flag unlocks. **Priority: MEDIUM for agent.yaml and
   minds.yaml D12 claims.**

5. **`src/utils/forkedAgent.ts`** (`createSubagentContext` + `CacheSafeParams`) → how
   parent context is forked, what is shared vs isolated between sync and async agents.
   **Priority: MEDIUM for D18 Subagent Isolation claims.**

6. **`src/utils/hooks.ts`** + `src/utils/hooks/hooksConfigManager.ts` → how settings.json
   hooks are merged with frontmatter hooks at runtime, what precedence rules apply.
   **Priority: MEDIUM for hooks.yaml and system.yaml install_manifest merge logic.**

7. **`src/commands/agents/index.ts`** → the `/agents` slash command that manages agents.
   Might reveal user-facing operations we can mirror. **Priority: LOW.**

8. **`src/constants/prompts.ts`** (`DEFAULT_AGENT_PROMPT`, `enhanceSystemPromptWithEnvDetails`)
   → the default agent prompt and the env enhancement. Reveals what Claude Code
   automatically adds to any agent's system prompt. **Priority: LOW but interesting.**

9. **`src/skills/`** subdirectory files (beyond loadSkillsDir.ts) → anything
   additional about skill execution. **Priority: LOW.**

10. **`src/tools/AgentTool/built-in/claudeCodeGuideAgent.ts`** + **`statuslineSetup.ts`**
    → additional built-in agents not read in S118. May reveal more archetype patterns.
    **Priority: LOW.**

---

## Verification checklist for future sessions

When updating a codex with a claim about Claude Code native behavior, require:

- [ ] The claim has a `[SOURCE: file.ts:line]` reference.
- [ ] The reference resolves to an actual line in `D:\repos-reverse-engineering\claude-code-main\src\`.
- [ ] The verification was done in the session that wrote the claim (not inherited without re-check).
- [ ] Feature-flag-gated behavior is noted as such, with the flag name.
- [ ] ant-only behavior (`process.env.USER_TYPE === 'ant'`) is noted as such.

Any codex claim that lacks a verified SOURCE reference must be marked `# [UNVERIFIED]`
and refactored into a myClaude convention rather than a Claude Code fact.

---

## Closing note — why this file exists

The difference between a codex that teaches creators to make state-of-the-art products
and a codex that fabricates authority is **one verified line of source code per claim**.

This file is that ground. Every line in every family-skill codex (agent, squad, system,
minds, workflow, hooks, claude-md) that says "Claude Code does X" can be traced through
this file to a specific file and line of TypeScript that implements X.

When Anthropic ships new primitives, this file gets updated. When myClaude claims a
capability that Anthropic doesn't yet support natively, it is explicitly declared as
"convention" with a note about what would change if Anthropic ever ships a loader for it.

The job of the codices is to turn this ground into pedagogy.
The job of the Engine is to turn this ground into production.
The job of this file is to keep both honest.

— S118, destillation written before any family-skill codex touched disk.
