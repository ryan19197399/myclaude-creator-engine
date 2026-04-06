# FAQ

Answers to the questions people actually ask.

---

### Do I need to be a developer?

No. The engine adapts to your profile — consultants, coaches, researchers, writers, marketers, anyone with expertise worth packaging can use it. You provide the knowledge; the engine provides the structure, quality checks, and distribution.

### What is this, exactly?

A creation pipeline for Claude Code products. It helps you research what to build, generate a product structure, fill it with your expertise, validate quality against 20 structural patterns, and publish to a marketplace where anyone can install your work with one command.

### What is this NOT?

- **Not a runtime.** The engine creates products. It does not execute them. After installation, products run independently in Claude Code.
- **Not a hosting service.** Products are files that live on the user's filesystem, not in the cloud.
- **Not a framework.** It does not impose architecture on your products. It provides structure during creation, then gets out of the way.
- **Not a replacement for expertise.** The engine captures and structures knowledge you already have. It does not generate domain expertise.
- **Not for disposable prompts.** If you need a quick one-off prompt, just type it. The engine is for durable, reusable tools worth installing.

### How is this different from just writing a CLAUDE.md file?

A CLAUDE.md is one of 13 product types the engine supports. The engine gives you a guided creation pipeline (research, create, fill, validate, publish), quality scoring, and marketplace distribution. You can still build claude-md products through the engine — they will be structurally validated and publishable.

### Do my products depend on the engine after installation?

No. Every product is self-contained. Once installed, it runs independently with no engine dependency. The engine is a creation tool, not a runtime requirement.

### How long does it take to create a product?

A simple skill takes 15–30 minutes including validation. A deep cognitive mind or multi-agent squad takes longer depending on the breadth of your domain. The engine's guided filling (`/fill`) handles structural work — you focus on expertise.

### What is a "mind"?

An installable knowledge advisor. When someone installs your mind, Claude Code gains your expertise — your frameworks, decision patterns, domain knowledge, and reasoning approaches. Minds come in two depths: advisory (focused, ~200 lines) and cognitive (deep multi-layered, ~1000 lines).

### What does the quality scoring check?

20 structural patterns across three tiers. The patterns check things like: does your product activate correctly? Does it document anti-patterns (what NOT to do)? Does it have verifiable success criteria? Does it handle missing inputs gracefully? Does it reveal complexity progressively?

Formula: `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`. Verified >= 75%, Premium >= 85%, Elite >= 92%.

See the [Quality System reference](reference/quality-system.md) for details.

### Can I import existing skills I have already built?

Yes. `/import --scan` scans your `.claude/skills/` directory and brings existing work into the pipeline for validation and publishing. The engine auto-detects the product type and creates the state tracking file.

### What does `/scout` do?

Research before creation. `/scout kubernetes-security` tests what Claude already knows about K8s security, finds the gaps it cannot cover alone, scans the marketplace for existing tools, and recommends what to build. You start with data, not guesswork.

### Is the engine free?

Yes. The engine is MIT-licensed and open source. The marketplace ([myclaude.sh](https://myclaude.sh)) supports both free and paid products — creators set their own pricing.

### How does the engine adapt to me?

It reads your creator profile (set up via `/onboard`) and adjusts based on your role, technical level, and workflow preferences. A developer sees different vocabulary, examples, and guidance depth than a consultant or writer. The adaptation is continuous — not just in `/validate` output but in every interaction.

### What is the LITE vs PRO edition?

LITE (free, this repo): 15 commands, Verified and Premium quality tiers. PRO: adds specialized agents and Elite-tier validation. LITE is complete for most users.

### Can I sell what I build?

Yes. Products published to [myclaude.sh](https://myclaude.sh) can be free or paid. Creators set their own pricing and keep their revenue.

### Is this affiliated with Anthropic?

No. MyClaude is an independent, community-driven project. The engine creates products that work with Claude Code — Anthropic's official tool — but it is not made by or endorsed by Anthropic.

### Are products compatible with other AI coding tools?

Products created by the engine use the Agent Skills format — YAML frontmatter with name, description, and constraints, followed by markdown instructions. This is the same `SKILL.md` format used natively by Claude Code. Other AI coding tools that support structured skill definitions can also consume these files. The engine pipeline runs in Claude Code, but the output format is portable.

### What happens to my products if the engine updates?

Nothing. Published products are self-contained. Engine updates improve the creation pipeline, not existing products. You can re-validate older products with `/validate` to check them against newer quality patterns.

### Can I use this with Cursor, Windsurf, or other AI editors?

The engine pipeline itself runs in Claude Code. However, products it creates follow the Agent Skills spec — so skill and agent products may be compatible with other tools that support the standard. Product types like applications and design systems are editor-agnostic by nature.

### Where can I find products other people have built?

Browse the marketplace at [myclaude.sh](https://myclaude.sh), or run `/explore` inside the engine to search from the terminal.

### How do I update a product I already published?

Edit the product files in `workspace/your-product/`, then re-run the pipeline: `/validate` → `/package` → `/publish`. The engine tracks this as a new version. Users who already installed it can run `myclaude update your-product` to get the latest.

### What does `myclaude install` actually do?

It downloads your product from the marketplace and copies the files to the correct Claude Code slot:
- Skills, agents, squads, workflows, systems → `.claude/skills/{slug}/`
- Minds (domain advisors) → `.claude/agents/{slug}.md`
- Behavioral rules (claude-md) → `.claude/rules/{slug}.md`
- Hooks → `~/.claude/hooks/{slug}/scripts/`
- Statusline → `~/.claude/statusline-scripts/{slug}.sh`
- Design systems, applications → `myclaude-products/{slug}/`

Claude Code discovers installed products automatically on session start. No manual configuration needed.

### What if `/validate` fails and I don't understand the output?

The engine always shows the top 3 issues with specific fix instructions. If a pattern fails, the output tells you exactly what is missing and what to add. Run `/validate --fix` to auto-fix structural issues where possible. For the rest, follow the instructions — they reference specific sections in your product files.

If you are genuinely stuck, run `/think` to brainstorm the issue, or open a [friction report](https://github.com/myclaude-sh/myclaude-creator-engine/issues/new?template=friction_report.yml).

### What if `myclaude install` doesn't work?

Make sure you have the CLI installed: `npm i -g @myclaude-cli/cli`. Then verify your connection: `myclaude auth`. If the install command times out or fails, try cloning the engine directly with git as an alternative.

### How do I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md). The most valuable contribution is friction reports — tell us where the engine felt confusing or wrong. We also welcome new product types, structural patterns, documentation improvements, and translations.

---

**Next:** [Getting Started](getting-started.md) · [Commands Reference](reference/commands.md) · [Marketplace](https://myclaude.sh)
