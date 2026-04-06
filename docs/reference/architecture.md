# Architecture

How the Engine, CLI, Marketplace, and Claude Code work together.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR MACHINE                             │
│                                                                 │
│  ┌───────────────────┐         ┌─────────────────────────────┐  │
│  │   Studio Engine    │         │       Claude Code            │  │
│  │                   │         │                             │  │
│  │  /scout           │         │  .claude/skills/{slug}/     │  │
│  │  /create          │         │  .claude/agents/{slug}.md   │  │
│  │  /fill    ─────────── /package ──→  .claude/rules/        │  │
│  │  /validate        │         │  ~/.claude/hooks/           │  │
│  │  /test            │         │  ~/.claude/statusline-*/    │  │
│  │                   │         │                             │  │
│  │  workspace/       │         │  Session loads products     │  │
│  │  .publish/        │         │  from these directories     │  │
│  └───────────────────┘         └─────────────────────────────┘  │
│           │                                 ▲                    │
│           │ /publish                        │ myclaude install   │
│           ▼                                 │                    │
│  ┌───────────────────┐         ┌────────────┴──────────────┐    │
│  │   MyClaude CLI     │         │      MyClaude CLI          │    │
│  │  myclaude publish  │────────→│   myclaude install {slug}  │    │
│  └───────────────────┘         └────────────────────────────┘    │
│           │                                 ▲                    │
└───────────┼─────────────────────────────────┼────────────────────┘
            │                                 │
            ▼              INTERNET            │
     ┌──────────────────────────────────────────┐
     │           myclaude.sh                    │
     │          Marketplace                     │
     │                                          │
     │  Browse · Search · Install · Stats       │
     │  Product registry · User profiles        │
     │  Quality badges · Install tracking       │
     └──────────────────────────────────────────┘
```

---

## The Publish Flow

What happens when you run `/publish` inside the Engine:

```
   Engine workspace/                     CLI                     Marketplace
   ═══════════════                    ════════                  ═══════════
        │                                │                          │
   1. /validate passes                   │                          │
        │                                │                          │
   2. /package generates:                │                          │
      .publish/                          │                          │
      ├── SKILL.md (cleaned)             │                          │
      ├── references/                    │                          │
      ├── vault.yaml (manifest)          │                          │
      └── plugin.json                    │                          │
        │                                │                          │
   3. /publish invokes CLI ──────→  myclaude publish               │
                                    │                              │
                                    4. Reads vault.yaml            │
                                    5. Validates manifest          │
                                    6. Scans for secrets           │
                                    7. Packs files ────────→  8. API receives
                                                              9. Stores files
                                                             10. Indexes product
                                                             11. Available for
                                                                 search/install
```

---

## The Install Flow

What happens when someone runs `myclaude install {slug}`:

```
   CLI                          Marketplace API              Your filesystem
   ════                         ════════════════              ═══════════════
    │                                │                            │
    1. Validate slug                 │                            │
    2. Check auth                    │                            │
    3. Check lockfile                │                            │
       (already installed?)          │                            │
    │                                │                            │
    4. Request product ──────→  5. Resolve slug                   │
                                6. Return download URL            │
                                   + metadata (type,              │
                                     version, files)              │
    │                                │                            │
    7. Download files (HTTPS)        │                            │
    8. Validate checksums            │                            │
    9. Resolve install path ─────────────────────────────→  10. Write files
       based on product type                                     to correct
                                                                 slot (below)
    │                                                            │
   11. Update lockfile                                           │
   12. Show post-install hint                                    │
```

---

## Where Products Install

The CLI places files in different directories based on product type. Claude Code discovers them automatically on session start.

```
Product Type        Install Path                        Discovery
══════════════      ════════════════════════════════     ═══════════════════
skill               .claude/skills/{slug}/              On /slash-command
agent               .claude/skills/{slug}/              On Agent tool spawn
squad               .claude/skills/{slug}/              On /slash-command
workflow            .claude/skills/{slug}/              On /slash-command
system              .claude/skills/{slug}/              On /slash-command

minds               .claude/agents/{slug}.md            On Agent tool spawn
                    (advisory-only, denied write tools)

claude-md           .claude/rules/{slug}.md             Always (every turn)

hooks               ~/.claude/hooks/{slug}/scripts/     On lifecycle events
                    (+ settings.local.json merge)

statusline          ~/.claude/statusline-scripts/       Terminal render loop
                    {slug}.sh

design-system       ./myclaude-products/{slug}/         On reference
application         ./myclaude-products/{slug}/         On reference
```

**Key architectural points:**
- Skills, agents, squads, workflows, and systems share the same `.claude/skills/` directory. Claude Code treats them identically at the discovery level — the product's internal structure determines behavior.
- Minds install as `.claude/agents/{slug}.md` — they are native Claude Code agents with advisory-only permissions (write tools denied). This means minds can think and advise but cannot modify files.
- claude-md products install as rules — they load every turn and govern all behavior. Keep them concise (ambient token cost).
- Hooks and statusline install globally (`~/.claude/`) because they apply across all projects.

---

## How Claude Code Loads Products

Products are loaded at different moments, with different token costs:

```
ALWAYS IN CONTEXT (ambient cost — tokens consumed every turn):
  ┌──────────────────────────────────────────────────┐
  │  .claude/rules/*.md          ← claude-md         │
  │  Skill/agent catalog         ← name + description│
  │     (all installed skills)      only, not body    │
  └──────────────────────────────────────────────────┘

ON-DEMAND (zero cost until invoked):
  ┌──────────────────────────────────────────────────┐
  │  /skill-name invoked     → full SKILL.md loaded  │
  │  skill reads references/ → additional files load │
  └──────────────────────────────────────────────────┘

ON-SPAWN (isolated context — behind firewall):
  ┌──────────────────────────────────────────────────┐
  │  Agent tool spawns agent  → AGENT.md loaded      │
  │  Agent gets its own context window               │
  │  Agent CANNOT see parent conversation            │
  │  Agent returns TEXT only (cross-firewall)         │
  └──────────────────────────────────────────────────┘

EVENT-TRIGGERED (invisible, reactive):
  ┌──────────────────────────────────────────────────┐
  │  Hook fires on event      → runs shell command   │
  │  PreToolUse hooks can BLOCK tool execution       │
  │  Other hooks observe only                        │
  │  Statusline renders after each assistant message  │
  └──────────────────────────────────────────────────┘
```

**Design implication:** Products that are always in context (claude-md) should be minimal — every token counts. Products that are on-demand (skills, minds) can be as deep as needed because they cost nothing until activated.

---

## The Engine Pipeline Internally

How the Engine transforms expertise into a published product:

```
  /onboard                /scout                 /create
  ════════               ════════               ════════
  creator.yaml    →    scout-{domain}.md   →   workspace/{slug}/
  (profile)            (gap analysis)           ├── SKILL.md (scaffold)
                       (baseline %)             ├── references/
                       (recommendation)         └── .meta.yaml (state)
       │                     │                        │
       └─────────────────────┘                        │
         Profile + research                           │
         inform the scaffold                          ▼

  /fill                    /validate               /test
  ════════                ════════                ════════
  Engine interviews  →   20 structural     →   3 behavioral
  you section by         patterns scored        scenarios in
  section. Writes        across 3 tiers.        isolated sandbox.
  content from           Formula:               Happy path,
  your answers.          DNA × 0.50 +           edge case,
                         Structural × 0.30 +    adversarial.
  .meta.yaml tracks      Integrity × 0.20
  fill progress.         
       │                      │                      │
       ▼                      ▼                      ▼

  /package                                    /publish
  ════════                                   ════════
  Strip WHY comments                         Invoke CLI:
  Generate manifests:                        myclaude publish
  ├── vault.yaml                             
  ├── plugin.json           ──────────→     Product live on
  └── agentskills.yaml                      myclaude.sh
  Stage in .publish/
```

---

## Security Boundaries

The system enforces security at multiple layers:

| Layer | What It Protects | How |
|:------|:----------------|:----|
| **Slug validation** | Prevents path traversal | Regex: lowercase alphanumeric + hyphens only |
| **File name validation** | Prevents malicious filenames from server | No path separators, no `..`, max 255 chars |
| **Download validation** | Prevents non-HTTPS downloads | URL must start with `https://` |
| **Size limit** | Prevents resource exhaustion | Max 50 MB per product download |
| **Type validation** | Prevents unknown install targets | Must match known product type set |
| **Secret scanning** | Prevents credential leaks on publish | CLI scans for secrets before upload |
| **Manifest validation** | Prevents incomplete products | Required fields checked before publish |
| **Checksum verification** | Prevents tampering | SHA-256 integrity check on install |
| **Context firewall** | Isolates agent execution | Spawned agents cannot see parent conversation |
| **Denied tools** | Restricts mind permissions | Minds cannot write/edit/execute — advisory only |

---

**Next:** [Product Types](product-types.md) · [Quality System](quality-system.md) · [Commands](commands.md)
