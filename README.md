# MyClaude Creator Engine

> The official creation studio for producing, validating, packaging, and publishing
> products to the [MyClaude marketplace](https://myclaude.sh).
>
> **Mental model:** Unity Editor for the Claude Code Asset Store.

---

## What It Is

The MyClaude Creator Engine is a **standalone Claude Code-native system** — a repo you open
in Claude Code that transforms your session into a full-powered creation studio.

It is the official toolchain for producing, validating, packaging, and publishing products
to the MyClaude marketplace. It adapts to your creator type (developer, prompt engineer,
domain expert, marketer, or agency) and enforces quality standards through the MyClaude
Creator Spec (MCS) tier system.

**What it covers:**

- Scaffolding for all 9 product categories (skills, agents, squads, workflows, design
  systems, prompts, CLAUDE.md configs, applications, systems)
- MCS validation in 3 tiers (Bronze / Silver / Gold)
- Packaging products into distribution-ready `.publish/` directories with `vault.yaml` metadata
- Publishing workflow integrated with the MyClaude CLI (`myclaude publish`)

**What it is NOT:**

- Not a standalone CLI binary — it runs inside Claude Code
- Not limited to developers — adapts to any creator persona
- Not a replacement for the MyClaude CLI — the Engine creates, the CLI distributes

---

## Prerequisites

| Requirement | Install |
|-------------|---------|
| Claude Code | [claude.ai/download](https://claude.ai/download) |
| MyClaude CLI | `npm i -g @myclaude/cli` |
| MyClaude account | [myclaude.sh](https://myclaude.sh) |
| Git | [git-scm.com](https://git-scm.com) |

---

## Quick Start

```bash
# 1. Clone the Engine
git clone https://github.com/l0z4n0-a1/myclaude-creator-engine.git
cd myclaude-creator-engine

# 2. Open in Claude Code
claude   # or open in VS Code / JetBrains with Claude Code extension

# 3. Set up your creator profile (~3 minutes, conversational)
/onboard

# 4. Create your first product
/create skill

# 5. Validate quality
/validate

# 6. Package and publish
/publish
```

---

## Command Reference

### Core Creation (P0)

| Command | Description |
|---------|-------------|
| `/onboard` | Set up your creator profile — runs once, adapts everything |
| `/create skill` | Scaffold a new skill |
| `/create agent` | Scaffold a new agent |
| `/create squad` | Scaffold a new squad |
| `/create workflow` | Scaffold a new workflow |
| `/create ds` | Scaffold a new design system |
| `/create prompt` | Scaffold a new prompt |
| `/create claude-md` | Scaffold a new CLAUDE.md configuration |
| `/create app` | Scaffold a new application |
| `/create system` | Scaffold a new system |

### Quality and Publishing (P0)

| Command | Description |
|---------|-------------|
| `/validate` | Run MCS validation (defaults to MCS-1) |
| `/validate --level=N` | Validate at specific MCS level (1, 2, or 3) |
| `/validate --fix` | Auto-fix structural issues that can be safely resolved |
| `/validate --batch` | Validate all products in workspace |
| `/test` | Sandbox test your product against sample inputs |
| `/package` | Strip guidance comments, generate `vault.yaml`, stage `.publish/` directory |
| `/publish` | Full publish workflow — validate, package, invoke `myclaude publish` |

### Shortcuts

| Shortcut | What It Does |
|----------|-------------|
| `/quick-skill` | Create, Validate, Package, Publish in one flow |
| `/quick-publish` | Validate, Package, Publish for an existing product |

### Utility

| Command | Description |
|---------|-------------|
| `/engine-status` | Engine version, profile loaded, active workspace, stale builds |
| `/engine-help` | All available commands with descriptions |
| `/differentiate` | Anti-commodity coaching session — make your product stand out |

---

## Architecture

```
CLAUDE.md (System Brain)
  Routes commands, loads creator profile, enforces MCS rules
              |
    +---------+-----------+
    |         |           |
 SKILLS    AGENTS     REFERENCES
    |         |           |
 /create   quality    product-specs/
 /validate market     exemplars/
 /package  packaging  mcs-spec
 /publish  coaching   best-practices/
    |
    v
 workspace/
 (active builds -- gitignored)
    |
    v
 .publish/                    <-- staged output with vault.yaml
    |
    v
 MyClaude CLI
 myclaude publish (ships to marketplace)
```

### Key Design Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| CE-D28 | Engine invokes CLI, never reimplements | Single responsibility — Engine creates, CLI distributes |
| CE-D12 | Guidance comments stripped during `/package` | Buyers receive clean files, originals untouched |
| CE-D13 | Validation is non-destructive by default | `--fix` has conservative scope: structural/formatting only |
| CE-D9 | Anti-Commodity Gate at MCS-2+ | MCS-1 allows commodity products; MCS-2+ demands differentiation |
| WP-3 | Unified `vault.yaml` manifest | One schema across Engine, CLI, and Marketplace (CONDUIT) |
| WP-20 | CLI publish is available | Engine invokes `myclaude publish` directly from `.publish/` |

---

## Ecosystem Integration (CONDUIT)

The Engine is one part of a three-system pipeline:

```
  CREATOR ENGINE          CLI              MARKETPLACE
  (this repo)         (myclaude)          (myclaude.sh)
       |                  |                    |
  /create             reads               displays
  /validate           vault.yaml           product
  /package  ------>   packs + uploads  --> with MCS badge,
  /publish            to R2 + API          enrichment fields
       |                  |                    |
   vault.yaml v2      vault.yaml v2       Firestore
   in .publish/        from CWD            (persisted)
```

The **CONDUIT Wiring Protocol** (see `docs/frameworks/conduit-wiring-protocol.md` in vault-marketplace) ensures every field the Engine generates flows unbroken to the buyer's eyes.

### vault.yaml (Unified Manifest)

The Engine generates `vault.yaml` during `/package`. The CLI reads it during `myclaude publish`. One schema, zero translation:

```yaml
name: "my-product"
display_name: "My Product"
version: "1.0.0"
type: "skill"
description: "One-line value proposition"
license: "MIT"
entry: "SKILL.md"
readme: "README.md"

# Enrichment (optional, CLI applies defaults)
mcs_level: 2
language: "en"
tags: ["security", "audit"]
price: 0
install_target: ".claude/skills/my-product/"
compatibility:
  claude_code: ">=1.0.0"
dependencies:
  myclaude: []
```

---

## Quality Tiers (MCS)

| Tier | Name | Criteria | Badge |
|------|------|----------|-------|
| **MCS-1** | Publishable | Structure complete, no broken references, README exists | Muted |
| **MCS-2** | Quality | Anti-Commodity Gate passed, unique value prop documented | Cyan |
| **MCS-3** | State-of-the-Art | Agent quality review, exemplar comparison, full coverage | Gold |

Every product must pass MCS-1 before it can be published. MCS level is persisted in `vault.yaml` and displayed as a badge on the marketplace.

---

## Product Categories

The Engine supports all 9 MyClaude product categories:

| Category | Type Key | Install Target |
|----------|----------|---------------|
| Skills | `skill` | `.claude/skills/{slug}/` |
| Agents | `agent` | `.claude/skills/{slug}/` |
| Squads | `squad` | `.claude/skills/{slug}/` |
| Workflows | `workflow` | `.claude/skills/{slug}/` |
| Design Systems | `design-system` | `myclaude-products/{slug}/` |
| Prompts | `prompt` | `.claude/skills/{slug}/` |
| CLAUDE.md | `claude-md` | `.claude/rules/{slug}.md` |
| Applications | `application` | `myclaude-products/{slug}/` |
| Systems | `system` | `.claude/skills/{slug}/` |

---

## Project Structure

```
myclaude-creator-engine/
  CLAUDE.md                    # System brain — boot sequence, routing, rules
  creator.yaml                 # Creator profile (generated by /onboard)
  .engine-meta.yaml            # Engine state tracking
  skills/
    onboarder/SKILL.md         # Creator onboarding flow
    scaffolder/SKILL.md        # Product scaffolding (all 9 types)
    validator/SKILL.md         # MCS validation pipeline
    publisher/SKILL.md         # Packaging and publishing
  agents/
    quality-reviewer.md        # MCS-3 deep quality review
    market-analyst.md          # Market opportunity scanning
    packaging-specialist.md    # README/tag/metadata optimization
    domain-expert.md           # Category-specific guidance
    differentiation-coach.md   # Anti-commodity coaching
  references/
    product-specs/             # Spec per product type
    exemplars/                 # Gold-standard examples
    quality/                   # MCS spec, anti-patterns
    best-practices/            # Naming, skill design
    market/                    # Pricing benchmarks
  templates/                   # Scaffold templates per category
  workspace/                   # Active builds (gitignored)
```

---

## Creator Types

The Engine adapts its behavior based on your creator profile:

| Type | Engine Behavior |
|------|-----------------|
| **Developer** | Lead with scaffolding, show CLI integration, expose architecture docs |
| **Prompt Engineer** | Focus on prompt structure, context engineering, exemplar references |
| **Domain Expert** | Emphasize AI-assisted creation, packaging, market positioning |
| **Marketer** | Lead with market opportunities, pricing benchmarks, competitive positioning |
| **Agency** | Show batch operations, multi-product workspace management |
| **Hybrid** | Ask which mode per session |

---

## Development

### Related Repositories

| Repository | Description |
|------------|-------------|
| [vault-marketplace](https://github.com/darwimmusic/vault-marketplace) | VAULT Marketplace web app (Next.js + Firebase + Stripe) |
| [@myclaude/cli](https://github.com/darwimmusic/vault-marketplace/tree/master/packages/cli) | MyClaude CLI (`myclaude publish`, `myclaude install`) |

### Decisions Log

All architectural decisions are tracked with `CE-D` prefix in `CLAUDE.md` and the framework document at `docs/frameworks/myclaude-creator-engine.md` in the vault-marketplace repo. The CONDUIT wiring decisions use `WP-` prefix.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

*MyClaude Creator Engine v1.0.0 — The Engine is itself a MyClaude product (category: system).*
