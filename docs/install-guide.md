# Installation Guide

**Version:** 2.2.0

---

## Quick Install (recommended)

```bash
myclaude studio
```

Or clone manually:

```bash
git clone https://github.com/myclaude-sh/myclaude-creator-engine
cd myclaude-creator-engine && claude
```

The engine activates automatically. Run `/help` to see all commands.

> **Need the CLI?** `npm i -g @myclaude-cli/cli` — [myclaude.sh](https://myclaude.sh)

---

## Manual Install (into an existing project)

### 1. Clone the repository

```bash
git clone https://github.com/myclaude-sh/myclaude-creator-engine
```

### 2. Copy skills and engine files

From the cloned repo, copy the engine's skills and reference files into your target project:

```bash
TARGET="path/to/your-project"

# Copy all 15 skills
cp -r .claude/skills/* "$TARGET/.claude/skills/"

# Copy engine infrastructure
for dir in templates product-dna references; do
  cp -r "$dir" "$TARGET/myclaude-engine/$dir"
done
```

### 3. Initialize

Open Claude Code in your project and run `/onboard` to set up your creator profile.

---

## All 15 Commands

| Command | Purpose |
|:--------|:--------|
| `/onboard` | Creator profile setup |
| `/scout [domain]` | Research before building |
| `/create [type]` | Scaffold new product |
| `/fill` | Guided content filling |
| `/validate` | Quality scoring (20 patterns) |
| `/test` | Behavioral sandbox testing |
| `/package` | Prepare for distribution |
| `/publish` | Ship to marketplace |
| `/import` | Import existing skills |
| `/status` | Dashboard overview |
| `/help` | Command reference |
| `/map [topic]` | Domain knowledge extraction |
| `/think [topic]` | Brainstorm and evaluate |
| `/explore [query]` | Search marketplace |
| `/aegis` | Security audit |

---

## Verify

Run `/status` in Claude Code. Expected:

```
Engine v2.2.0 [LITE] | Creator: {name} | Products: 0
```

---

## Troubleshooting

**"myclaude: command not found"**
The CLI is not installed. Run `npm i -g @myclaude-cli/cli` first.

**"Authentication required"**
Run `myclaude login` to authenticate with the marketplace.

**"Engine doesn't load in Claude Code"**
Make sure you opened Claude Code in the engine directory (the folder with `CLAUDE.md`). The engine activates from this file.

**"/onboard says creator.yaml not found"**
This is expected on first run — `/onboard` creates it. Just answer the questions.

**Products I installed aren't showing up**
Claude Code discovers products on session start. If you installed mid-session, restart Claude Code. Products should appear in `.claude/skills/` or `.claude/agents/` depending on type.

---

## Requirements

- [Claude Code](https://claude.ai/download) — CLI, desktop app, or IDE extension
- [MyClaude CLI](https://myclaude.sh) — for publishing and marketplace access (`npm i -g @myclaude-cli/cli`)

---

**Next:** [Getting Started](getting-started.md) · [FAQ](faq.md) · [Architecture](reference/architecture.md)
