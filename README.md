<!--
@name: MyClaude Studio Engine
@version: 2.2.0
@description: Creation pipeline for Claude Code products — research, create, validate, and publish skills, agents, squads, minds, and 9 more product types with 20 structural quality patterns.
@install: myclaude studio
@install-alt: git clone https://github.com/myclaude-sh/myclaude-creator-engine
@types: skill, agent, squad, workflow, minds, system, claude-md, hooks, statusline, output-style, design-system, application, bundle
@commands: /onboard, /scout, /create, /fill, /validate, /test, /package, /publish, /import, /status, /help, /map, /think, /explore, /aegis
@audience: developers, domain-experts, consultants, researchers, writers, marketers, teams
@marketplace: https://myclaude.sh
@cli: npm i -g @myclaude-cli/cli
@license: MIT
@plugin: .claude-plugin/marketplace.json
@llms-txt: llms.txt
@agent-skills: compatible with agentskills.io specification
-->

<p align="center">
  <img src="assets/myclaude-logo.png" alt="myClaude" width="80">
</p>

<h1 align="center">MyClaude Studio Engine</h1>

<p align="center">
  <strong>The creation pipeline for Claude Code products.</strong><br>
  <sub>Research what to build. Create it with structure. Validate quality. Publish to a marketplace.<br>One engine. Any expertise. No coding required.</sub>
</p>

<p align="center">
  <a href="https://github.com/myclaude-sh/myclaude-creator-engine/releases"><img src="https://img.shields.io/badge/version-2.2.0-c97632?style=flat-square" alt="Version"></a>
  <a href="https://myclaude.sh"><img src="https://img.shields.io/badge/marketplace-39_products-d4956b?style=flat-square" alt="Marketplace"></a>
  <a href="#quality-you-can-measure"><img src="https://img.shields.io/badge/quality_patterns-20-e8c4a0?style=flat-square" alt="Quality Patterns"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-f5f0eb?style=flat-square" alt="License"></a>
</p>

<p align="center">
  <a href="#install-in-30-seconds">Install</a> ·
  <a href="#see-it-in-action">Example</a> ·
  <a href="#what-you-can-build">Build</a> ·
  <a href="docs/getting-started.md">Guides</a> ·
  <a href="https://myclaude.sh">Marketplace</a> ·
  <a href="docs/faq.md">FAQ</a>
</p>

---

Thousands of Claude Code users build custom skills, agents, and tools every day.
But there is no standard for quality — no way to know if what you built is robust, no guided process to follow, and no easy way to share your work with others.

**The Studio Engine is the missing creation pipeline.**
It walks you from idea to published product: researching your domain, generating structure, guiding you through content, scoring quality against 20 structural patterns, and publishing to a [marketplace](https://myclaude.sh) where anyone can install your work with one command.

You don't need to write code. You need expertise worth packaging.

<p align="center">
  <br>
  <img src="assets/marketplace-preview.png" alt="myClaude Marketplace — browse and install products" width="720">
  <br>
  <sub>The <a href="https://myclaude.sh">myClaude Marketplace</a> — where your products live.</sub>
</p>

---

## Install in 30 Seconds

```bash
myclaude studio
```

> Don't have the CLI yet? `npm i -g @myclaude-cli/cli` — then run the command above.
>
> Or clone directly: `git clone https://github.com/myclaude-sh/myclaude-creator-engine && cd myclaude-creator-engine && claude`

That's it. Open the folder in Claude Code and run `/onboard` — the engine adapts to you.

---

## See It in Action

A Kubernetes security consultant used the engine to turn 15 years of expertise into an installable advisor — in one sitting:

```
/scout kubernetes-security
```
> The engine tested what Claude already knows about K8s security, found 11 gaps
> it can't cover alone, scanned the marketplace for existing tools, and
> recommended building a cognitive mind.

```
/create minds
```
> Generated a product structure with guided annotations — 7 sections,
> each with context about what belongs there and why.

```
/fill
```
> The engine asked targeted questions: "What's the first thing you check
> in a cluster audit?" "Walk me through an attack path from exposed etcd."
> The consultant answered. The engine wrote the structure.

```
/validate
```
> Scored 100% — Elite quality. 20/20 structural patterns passing.
> Attack-path reasoning, CIS benchmarks, hardening checklists — all verified.

```
/publish
```
> Live on myclaude.sh. Anyone in the world can now run:
> `myclaude install k8s-security-advisor`
> and Claude Code gains deep K8s security expertise it doesn't have natively.

**The consultant provided the expertise. The engine handled everything else.**

---

## What You Can Build

| You are a... | You build... | Start with |
|:--|:--|:--|
| **Developer** | Skills, agents, hooks, multi-agent squads | `/create skill` |
| **Consultant / Coach** | Methodology frameworks anyone can install and use | `/create workflow` |
| **Domain expert** | Installable knowledge advisors with deep reasoning | `/create minds` |
| **Team lead** | Shared multi-agent teams with quality standards | `/create squad` |
| **Writer / Researcher** | Knowledge tools that augment Claude's capabilities | `/scout your-domain` |
| **Anyone with expertise** | Whatever Claude Code can't do alone | `/scout` then `/create` |

Every product is **self-contained** — no engine dependency after install. Portable, yours, forever.

> **See more scenarios:** [Use Cases](docs/use-cases.md) — lawyers, marketers, consultants, solo businesses, researchers.

> **Not sure what to build?** Run `/scout marketing-strategy` (or any domain). The engine tests what Claude already knows, finds the gaps, and recommends exactly what to build. You start with intelligence, not guesswork.

---

## How It Works

```
  research       create       refine       verify       ship
  /scout    →   /create  →   /fill   →  /validate →  /publish
                   │                        │
                   │    AI-guided filling    │  20 structural
                   │    with your expertise  │  quality patterns
                   └────────────────────────┘
```

The engine asks the right questions. You provide the expertise. Each step feeds the next — scout research flows into `/create`, which generates structure for `/fill`, which produces content scored by `/validate`. Nothing is disconnected.

<details>
<summary><strong>All 15 commands</strong></summary>
<br>

| Phase | Command | What It Does |
|:------|:--------|:-------------|
| **Profile** | `/onboard` | Set up your creator profile — the engine adapts to you |
| **Research** | `/scout [domain]` | Test Claude's knowledge, find gaps, scan competition, recommend what to build |
| **Knowledge** | `/map [topic]` | Extract and structure your domain expertise into a reusable map |
| **Create** | `/create [type]` | Generate a product with structural DNA and guided annotations |
| **Fill** | `/fill` | AI-guided content filling — the engine asks, you answer, it writes |
| **Quality** | `/validate` | Score against 20 structural patterns (Verified / Premium / Elite) |
| **Test** | `/test` | Behavioral validation in an isolated sandbox — 3 scenarios |
| **Package** | `/package` | Strip annotations, generate manifests, prepare for distribution |
| **Publish** | `/publish` | Ship to [myclaude.sh](https://myclaude.sh) with one command |
| **Import** | `/import` | Bring existing skills into the pipeline for validation and publishing |
| **Status** | `/status` | Dashboard — scores, next steps, portfolio overview |
| **Help** | `/help` | Command reference with personalized recommendations |
| **Think** | `/think` | Brainstorm and compare approaches before committing |
| **Explore** | `/explore` | Search the marketplace for existing tools and inspiration |
| **Security** | `/aegis` | Security audit for any codebase — works independently |

</details>

---

## What Makes This Different

Other tools in the Claude Code ecosystem give you **pre-built configurations** — collections of skills, agents, and rules to install. They are warehouses of ready-made parts.

The Studio Engine is a **factory**. It helps you create your own.

| | Pre-built config tools | Studio Engine |
|---|---|---|
| **What you get** | Someone else's skills | Your own products |
| **Quality** | Trust the author | Scored against 20 patterns |
| **Process** | Copy and install | Research → create → validate → publish |
| **Audience** | Developers only | Anyone with expertise |
| **Distribution** | GitHub repo | Marketplace with one-command install |
| **After install** | Depends on the repo | Self-contained, no dependency |

**No other tool in the ecosystem validates quality before publishing.** MCS scoring is unique — your products are verified, not just functional.

---

## Quality You Can Measure

Every product is scored: `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`

| Tier | Score | What It Means |
|:-----|:------|:-------------|
| **Verified** | >= 75% | Functional, documented, core patterns present |
| **Premium** | >= 85% | Professional craft — advanced structural patterns |
| **Elite** | >= 92% | State-of-the-art — deep structural quality |

20 structural patterns check for: activation protocols, error handling, anti-pattern guards, progressive disclosure, quality gates, graceful degradation, cache-friendly design, and more.

Run `/validate` at any time. The engine shows exactly what passes, what needs work, and how to fix it — with specific instructions, not vague suggestions.

---

## The Ecosystem

```
         YOU                          ANYONE
          │                             │
     ┌────┴────┐                   ┌────┴────┐
     │  BUILD  │                   │ INSTALL  │
     │ Engine  │  ──── publish ──→ │   CLI    │
     │ /create │                   │ myclaude │
     │ /fill   │                   │ install  │
     │/validate│                   │          │
     └─────────┘                   └──────────┘
          │                             │
          └──── myclaude.sh ────────────┘
                marketplace
```

| Component | What It Is | Link |
|:----------|:-----------|:-----|
| **Engine** (this repo) | Create and validate products | MIT, open source |
| **CLI** (`@myclaude-cli/cli`) | Search, install, publish from the terminal | [myclaude.sh](https://myclaude.sh) |
| **Marketplace** | Browse and install with one command | [myclaude.sh](https://myclaude.sh) |

Products created by the engine follow the [Agent Skills specification](https://agentskills.io/specification) — the open standard published by Anthropic and adopted by platforms like Codex, VS Code/Copilot, Cursor, and others. Your products work anywhere the standard is supported.

---

<details>
<summary><h2>13 Product Types</h2></summary>
<br>

Each type has specific structural DNA — patterns that ensure it works correctly, handles edge cases, and activates reliably.

| Type | What It Is | Best For |
|:-----|:-----------|:---------|
| **skill** | Single-purpose tool with focused capability | Code review, docs generation, audits, analysis |
| **agent** | Autonomous multi-step task runner | Complex automation with decision-making |
| **squad** | Multi-agent team with intelligent routing | Multi-domain tasks where agents coordinate |
| **workflow** | Orchestrated process automation | Standardized team processes and methodologies |
| **minds** | Domain expert advisor (advisory or cognitive depth) | Packaging deep knowledge as installable intelligence |
| **system** | Complex multi-component tool | When a single skill isn't enough |
| **claude-md** | Behavioral rules and coding standards | Team-wide coding standards, review criteria |
| **hooks** | Lifecycle automation scripts | Run actions on Claude Code events |
| **statusline** | Terminal status widgets | Custom information in the status bar |
| **output-style** | Response formatting rules | Control how Claude structures its answers |
| **design-system** | Design token systems | Shared design language across projects |
| **application** | Full standalone applications | Tools built with Claude Code |
| **bundle** | Meta-packages combining products | Installable suites for specific domains |

</details>

---

## Built on the Marketplace

Products created with the Studio Engine and published to [myclaude.sh](https://myclaude.sh):

| Product | Type | What It Does |
|:--------|:-----|:-------------|
| K8s Security Advisor | minds | Deep Kubernetes security expertise — attack paths, CIS benchmarks, hardening |
| AEGIS Security Auditor | skill | STRIDE threat modeling, 300+ vulnerability patterns, 8 compliance frameworks |
| Noctis Terminal Themes | system | Terminal theme creation engine — 5 skills, 8 terminal exports |
| Context Surgeon | skill | Precision context window optimization for Claude Code |
| BSI Shopping Intelligence | skill | Buyer intelligence with comparison matrices and deal scoring |

> Browse all 39 products at [myclaude.sh](https://myclaude.sh), or run `/explore` inside the engine.

---

## Documentation

| Guide | Audience | Type |
|:------|:---------|:-----|
| **[Use Cases](docs/use-cases.md)** | Everyone | Scenarios — lawyers, marketers, consultants, solo businesses |
| **[Getting Started](docs/getting-started.md)** | Everyone | Tutorial — create your first product, step by step |
| **[For Developers](docs/guides/for-developers.md)** | Developers | How-to — skills, agents, hooks, squads |
| **[For Domain Experts](docs/guides/for-domain-experts.md)** | Non-developers | How-to — package knowledge as tools |
| **[For Teams](docs/guides/for-teams.md)** | Team leads | How-to — shared workflows and squads |
| **[Commands Reference](docs/reference/commands.md)** | Everyone | Reference — all 15 commands |
| **[Product Types](docs/reference/product-types.md)** | Everyone | Reference — the 13 types in detail |
| **[Quality System](docs/reference/quality-system.md)** | Everyone | Reference — scoring, tiers, patterns |
| **[Architecture](docs/reference/architecture.md)** | Developers | Reference — how Engine, CLI, Marketplace, and CC connect |
| **[FAQ](docs/faq.md)** | Everyone | Common questions answered |
| **[Install Guide](docs/install-guide.md)** | Everyone | Detailed installation options |
| **[Changelog](CHANGELOG.md)** | Everyone | Version history — v1.0 through v2.2.0 |

---

## Requirements

- **[Claude Code](https://claude.ai/download)** — CLI, desktop app, or IDE extension
- **[MyClaude CLI](https://myclaude.sh)** — for publishing and marketplace access (`npm i -g @myclaude-cli/cli`)

---

## Contributing

The engine improves through use. If something feels off — friction, confusion, a missing feature — that is valuable signal.

**Contributions are welcome.** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ways to contribute:
- **Friction reports** from real usage — the most valuable contribution
- **New product types** with DNA spec, template, and exemplar
- **New structural patterns** with validation logic
- **Documentation** improvements and translations
- **Bug fixes** and quality improvements

---

## License

MIT. See [LICENSE](LICENSE).

---

## Why This Exists

Every Claude Code user has a setup. Skills you've refined. Workflows you repeat. Knowledge you've encoded into prompts and rules over weeks of real work. That setup makes you powerful.

But it's trapped. In your machine, in your project, in your head. You can't score it. You can't share it. You can't install it somewhere else with one command. And the person next to you — the consultant, the researcher, the developer on another continent — is solving the same problem from scratch because your solution is invisible to them.

The Studio Engine exists to change that equation. To make every Claude Code setup shareable, every piece of expertise installable, every tool scorable before it ships. Not as a platform that owns your work — as a pipeline that packages it and gets out of the way.

The vision is simple: a world where Claude Code gets better every time someone publishes a product. Where a lawyer's contract review methodology becomes a tool any lawyer can install. Where a solo founder's operational playbook becomes a bundle that saves the next founder 10 hours a week. Where quality isn't a guess — it's a number.

Every feature came from a real need. The scoring exists because shipping without knowing if it's solid isn't shipping — it's hoping. The guided pipeline exists because a blank file is where good ideas go to die. The non-developer support exists because the deepest expertise doesn't come from people who write code — it comes from people who solve real problems every day and never had a way to package that.

This is built by a Claude Code user, with Claude Code, for Claude Code users. The entire engine was created using the same pipeline it teaches you to use. Dogfooding isn't a buzzword here — it's the architecture.

**The marketplace is the multiplier.** Every product published makes the ecosystem smarter. Every install makes someone's Claude Code more capable. Every creator who packages their expertise raises the floor for everyone. That's the game we're playing.

The name says it. **myClaude** — not *the* Claude, not *a* Claude. *Yours.* The moment you install a product that carries someone's real expertise, Claude stops being a generic AI and becomes something personal. Shaped by what you need. Augmented by what others know. That's the thesis: Claude is powerful out of the box, but *your* Claude — configured, specialized, extended with tools built by people who understand your domain — that's something else entirely.

---

## Acknowledgments

This is an independent, community-driven project. It is **not affiliated with or endorsed by Anthropic**. The engine creates products that work with [Claude Code](https://claude.ai/download) — Anthropic's official coding tool — but is not made by Anthropic.

Built with respect for the ecosystem and the developers, researchers, consultants, and creators who push Claude Code further every day.

---

<p align="center">
  <sub>Every Claude Code user deserves to operate at the apex of what the tool can do.<br>Some build tools, some install tools, most do both. The marketplace is the bridge.</sub>
</p>

<p align="center">
  <a href="https://myclaude.sh">myclaude.sh</a>
</p>
