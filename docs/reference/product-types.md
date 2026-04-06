# Product Types

13 ways to package expertise. Each type has specific structural DNA, its own installation slot, and quality patterns the engine validates automatically.

---

## Overview

| Type | What It Is | Installs To | Best For |
|:-----|:-----------|:------------|:---------|
| **skill** | Single-purpose tool | `.claude/skills/` | Developers, prompt engineers |
| **agent** | Autonomous multi-step task runner | `.claude/skills/` | Complex automation |
| **squad** | Multi-agent team with routing | `.claude/skills/` | Teams, multi-domain tasks |
| **workflow** | Orchestrated process automation | `.claude/skills/` | Operators, agencies |
| **minds** | Domain expert advisor | `.claude/agents/` | Domain experts, consultants |
| **system** | Complex multi-component tool | `.claude/skills/` | Advanced tooling |
| **claude-md** | Behavioral rules and instructions | `.claude/rules/` | Team standards |
| **hooks** | Lifecycle automation scripts | `~/.claude/hooks/` | Automation, CI/CD |
| **statusline** | Terminal status widgets | `~/.claude/statusline-scripts/` | Productivity |
| **output-style** | Response formatting rules | *(experimental — not yet in CLI)* | Output customization |
| **design-system** | Design token systems | `myclaude-products/{slug}/` | Frontend teams |
| **application** | Full applications | `myclaude-products/{slug}/` | Standalone tools |
| **bundle** | Meta-packages combining products | N/A | Product suites |

---

## Details

### skill
The most common type. A focused tool that does one thing well — code review, security audit, documentation generation, test creation. Skills have a clear activation trigger, structured references, and quality gates.

**Create:** `/create skill`

### agent
Like a skill, but with autonomy. Agents have goals, tool access, decision-making logic, and can run multi-step tasks without human intervention. They report results when done.

**Create:** `/create agent`

### squad
A team of agents coordinated by routing logic. Each agent has a role (security reviewer, architecture analyst, performance auditor). The squad decides which agents to activate based on the task.

**Create:** `/create squad`

### workflow
Step-by-step process automation. Workflows define a sequence of actions with decision points, quality checks, and handoff protocols. Think of it as a documented process that Claude follows.

**Create:** `/create workflow`

### minds
An installable knowledge advisor. Minds come in two depths:

- **Advisory** (~200 lines) — Focused guidance in one area. Quick to build.
- **Cognitive** (~1000 lines) — Deep multi-layered expertise with reasoning patterns, decision frameworks, and anti-patterns. Built from the genius library.

**Create:** `/create minds`

### system
When a single skill isn't enough. Systems combine multiple components — skills, agents, and configuration — into a cohesive tool.

**Create:** `/create system`

### claude-md
Behavioral rules written as markdown. When installed in `.claude/rules/`, they shape how Claude Code behaves in a project — coding standards, review criteria, communication style.

**Create:** `/create claude-md`

### hooks
Scripts that run on Claude Code lifecycle events: session start, before/after tool calls, permission prompts. Hooks automate recurring tasks without manual invocation.

**Create:** `/create hooks`

### statusline
Terminal status widgets that display information in Claude Code's status bar — git status, build health, deployment state, custom metrics.

**Create:** `/create statusline`

### output-style
Rules that control how Claude formats its responses — markdown conventions, code style preferences, verbosity levels, language choices.

> *Engine-only — you can create and use output-style products locally, but CLI publish/install is not yet available. For now, share via git or manual copy.*

**Create:** `/create output-style`

### design-system
Design token systems with color palettes, typography scales, spacing rules. Exported to CSS, Tailwind, JSON, or framework-specific formats.

> **Actionability note:** Design systems install to a project folder — Claude Code does not auto-discover them as slash commands. For full actionability, pair your design system with a companion **skill** that reads the tokens and generates code. The engine will prompt you to create one during `/fill`.

**Create:** `/create design-system`

### application
Full standalone applications built with Claude Code. The product lives as a project directory.

> **Actionability note:** Applications install to a project folder. For the best user experience, include a clear README with setup instructions, or pair with a companion **skill** that bootstraps the application.

**Create:** `/create application`

### bundle
Meta-packages that combine multiple products into a suite. A security bundle might include a security skill, a security squad, and a security mind.

**Create:** `/create bundle`

---

## How Installation Works

When someone runs `myclaude install your-product`, the CLI downloads the product files from the marketplace and copies them to the correct slot in Claude Code:

| Slot | Path | What Goes There |
|:-----|:-----|:----------------|
| Skills | `.claude/skills/{slug}/` | Skills, agents, squads, workflows, systems |
| Agents | `.claude/agents/{slug}.md` | Minds (domain advisors) |
| Rules | `.claude/rules/{slug}.md` | claude-md behavioral rules |
| Hooks | `~/.claude/hooks/{slug}/scripts/` | Lifecycle automation scripts |
| Statusline | `~/.claude/statusline-scripts/{slug}.sh` | Terminal status widgets |
| Project files | `myclaude-products/{slug}/` | Design systems, applications |

Claude Code discovers installed products automatically on session start. Skills and agents appear in the command catalog. Rules become active immediately. Hooks fire on their configured events. No manual wiring needed.

**Updates:** When a creator publishes a new version, users update with `myclaude update product-name`.

**Uninstall:** `myclaude uninstall product-name` removes the files cleanly.

---

## How Products Load in Claude Code

Not all products are active at the same time. Claude Code loads them at different moments, which affects their behavior and token cost.

```
ALWAYS ACTIVE (loaded every turn):
  claude-md     → behavioral rules, always governing

ON-DEMAND (zero cost until invoked):
  skill         → loaded when you type /skill-name
  minds         → loaded when referenced via Agent tool
  workflow      → loaded when you type /workflow-name

ON-SPAWN (isolated context):
  agent         → spawned in its own context, cannot see parent conversation
  squad agents  → each agent operates behind a context firewall

EVENT-TRIGGERED (invisible, reactive):
  hooks         → fires on lifecycle events (tool calls, session start, etc.)
  statusline    → updates in the terminal render loop

REFERENCE (project files, not auto-discovered):
  design-system → token files in project folder, pair with a skill for actionability
  application   → project files, include README with setup instructions
```

**Why this matters:** Products that are always active (claude-md) consume tokens every turn — keep them short. Products that are on-demand (skills, minds) have zero cost until invoked — they can be as deep as needed.

---

## The Intelligence Gradient

Products exist on a spectrum from fully deterministic to fully autonomous:

```
Deterministic ──────────────────────────────────→ Autonomous
hooks → skills → workflows → agents → squads → systems
│       │         │           │         │        │
always  no        fixed       uses      multi-   everything
fires   judgment  sequence    judgment  agent    combined
```

When deciding what to build:
- **Needs zero judgment, same every time?** → hooks or skill
- **Fixed sequence of steps with gates?** → workflow
- **Requires decisions based on context?** → agent
- **Needs multiple perspectives coordinating?** → squad

---

## How Products Compose

Products are designed to work together. Here is how they relate.

**Composition** (what contains what):

```
system  → can include skills, agents, minds, squads, hooks, workflows
bundle  → aggregates any combination for joint install
squad   → contains 2+ agents, may include skills and workflows
```

**Usage** (what uses what):

```
agents  → can invoke skills as instruments
agents  → can consult minds for domain expertise
agents  → can spawn sub-agents for parallel work
squads  → route work to agents based on rules
workflows → orchestrate skills in sequence
```

**Governance** (what governs what):

```
claude-md → governs ALL products (always in context, constitutional)
hooks     → guard tool execution (can block writes, edits, etc.)
```

**Powerful combinations:**
- `minds + skill` = an advisor that can also analyze data
- `hooks + claude-md` = automatic enforcement of team rules
- `squad + workflows` = a team with formal processes
- `bundle` = everything your team needs in one install

---

## Choosing the Right Type

### Quick Decision Heuristics

These rules of thumb help you recognize which type fits without reading specs:

- **If what you want to package fits in an email** → `skill`
- **If it would take a 1-hour meeting to explain** → `minds`
- **If it needs a team to execute** → `squad`
- **If you catch yourself explaining the same concept for the 5th time** → that's a `minds` waiting to be built
- **If your process has 5+ sequential steps with decisions between them** → `workflow`, not a skill
- **If the right answer depends on context and requires judgment** → `agent`. If it's always the same answer → `skill`
- **If a single skill keeps growing past 800 lines** → it wants to be an `agent`
- **If you built 3+ products in the same domain** → time for a `bundle`

### Decision Tree

For a more systematic choice:

- **You want Claude to do one focused task** → `skill`
- **You want Claude to run multi-step tasks autonomously** → `agent`
- **You want multiple agents to coordinate** → `squad`
- **You want to standardize a team process** → `workflow`
- **You want to package domain expertise** → `minds`
- **You want to set team-wide coding rules** → `claude-md`
- **You want automation on Claude Code events** → `hooks`
- **You want to combine multiple products** → `bundle`

Still unsure? Run `/scout your-domain` — the engine will recommend the best type based on your domain analysis. Or `/think` to brainstorm before committing.

---

## What `/package` Produces

When you run `/package`, the engine generates distribution-ready files in `.publish/`:

```
.publish/
├── SKILL.md              ← Primary product file (annotations stripped)
├── references/            ← Supporting knowledge files
├── vault.yaml             ← Marketplace manifest (name, version, description, install target)
├── plugin.json            ← Plugin metadata (Anthropic plugin format)
└── agentskills.yaml       ← Agent Skills spec manifest (cross-platform compatibility)
```

The `SKILL.md` uses the Agent Skills format — YAML frontmatter with name, description, and optional tool/model constraints, followed by markdown instructions. This is the native format recognized by Claude Code.

Example frontmatter from a packaged product:

```yaml
---
name: k8s-security-advisor
description: Deep Kubernetes security expertise — attack paths, CIS benchmarks, hardening checklists, compliance mapping.
---
```

### Agent Skills Spec Constraints

The `/package` output follows the Agent Skills format used by Claude Code. Key constraints the engine enforces automatically:

| Field | Constraint |
|:------|:-----------|
| `name` | Lowercase letters, numbers, hyphens only. Max 64 chars. No leading/trailing hyphens. |
| `description` | Max 1024 chars. Must describe what the skill does AND when to use it. |
| Body | Recommended under 5000 tokens (~500 lines). Move reference material to `references/`. |

Products packaged by the engine are compatible with any platform that supports the Agent Skills standard — including Claude Code and other tools that have adopted the specification.

---

> ✦ Every product is self-contained after install — no engine dependency, no lock-in. The work is yours. The quality verification is ours.

**Next:** [Architecture](architecture.md) · [Commands Reference](commands.md) · [Quality System](quality-system.md) · [Getting Started](../getting-started.md)
