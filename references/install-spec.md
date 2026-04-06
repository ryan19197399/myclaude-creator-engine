# Engine Install Specification
**Status:** Design complete | **Blocks:** F-007 | **Priority:** P0

---

## The Problem

The Engine lives in a git repo. To use it, a creator needs to:
1. Clone the repo
2. Understand 15+ file structure
3. Manually navigate CLAUDE.md, STATE.yaml, workspace/
4. Know about /onboard, /create, etc.

This is a cliff, not a ramp. **Time to first value: ~30 minutes.** Target: **60 seconds.**

---

## The Solution: Two-Phase Install

### Phase 1: CLI Install (requires myclaude CLI >=0.9.0)

```bash
myclaude install studio-engine
```

**What happens:**
1. Downloads the latest release package from myclaude.sh
2. Installs 15 Engine skills to `.claude/skills/` (each skill is a directory with SKILL.md + references/)
3. Creates `workspace/` in the current project root (gitignored)
4. Copies foundational files to project root:
   - `structural-dna.md` → immutable reference, skills read this
   - `config.yaml` → Engine configuration, creator can customize
   - `quality-gates.yaml` → state machine rules
   - `STATE.yaml` → session state (auto-managed)
5. Copies supporting infrastructure:
   - `product-dna/` → DNA definitions per type (13 files)
   - `templates/` → scaffold templates per type
   - `references/` → product specs, quality, best practices, market intel
   - `meta/pitfalls/pitfalls.json` → institutional memory
6. Runs implicit micro-onboard (scans environment, asks 1 question) if no `creator.yaml`
7. Shows: "Studio Engine v{ver} installed. Run `/create {type}` to build your first product."

**Idempotent:** Re-running doesn't break existing workspace/ or creator.yaml.
**Non-destructive:** Never overwrites files the creator modified. Uses hash comparison.

### Phase 2: Upgrade

```bash
myclaude upgrade studio-engine
```

**What happens:**
1. Downloads latest release
2. Updates skills in `.claude/skills/` (overwrite — skills are Engine code, not creator content)
3. Updates `product-dna/`, `templates/`, `references/` (overwrite)
4. Updates `structural-dna.md`, `quality-gates.yaml` (overwrite — these are Engine definitions)
5. **PRESERVES**: `workspace/`, `creator.yaml`, `config.yaml`, `STATE.yaml`, `meta/` (creator data)
6. Shows changelog: "Upgraded v{old} → v{new}. Changes: {summary}"

### Phase 3: Manual Install (no CLI required)

For creators who can't or don't want to use the CLI:

```bash
git clone https://github.com/myclaude-sh/myclaude-creator-engine.git
cd myclaude-creator-engine
# Everything is already in place — just start using it
```

The repo IS the Engine. This is the current path and remains valid forever.

---

## File Ownership Model

| Category | Who Owns | Install Behavior | Upgrade Behavior |
|----------|----------|-----------------|-----------------|
| Skills (`.claude/skills/engine-*`) | Engine | Create | Overwrite |
| DNA (`product-dna/`) | Engine | Create | Overwrite |
| Templates (`templates/`) | Engine | Create | Overwrite |
| References (`references/`) | Engine | Create | Overwrite |
| Structural DNA (`structural-dna.md`) | Engine | Create | Overwrite |
| Quality Gates (`quality-gates.yaml`) | Engine | Create | Overwrite |
| Pitfalls (`meta/pitfalls/`) | Shared | Create with seed | Merge (add new, keep creator's) |
| Config (`config.yaml`) | Creator | Create with defaults | Preserve |
| State (`STATE.yaml`) | Creator | Create with defaults | Preserve |
| Profile (`creator.yaml`) | Creator | Create via micro-onboard | Preserve |
| Workspace (`workspace/`) | Creator | Create empty | Preserve |
| Frictions (`meta/frictions/`) | Creator | Skip | Preserve |

---

## Package Structure (what gets published to myclaude.sh)

```
studio-engine/
├── vault.yaml                    # Marketplace manifest
├── SYSTEM.md                     # Engine identity + boot sequence
├── STATE.yaml.template           # Template for creator's state
├── config.yaml                   # Default configuration
├── structural-dna.md             # 20 DNA patterns
├── quality-gates.yaml            # State machine rules
├── product-dna/                  # DNA per type (13 files)
├── templates/                    # Scaffold templates
│   ├── skill/
│   ├── agent/
│   ├── squad/
│   ├── minds/
│   │   ├── cognitive/
│   │   └── (advisory is default)
│   ├── genius-library/
│   └── ... (13 types)
├── references/                   # Product specs, quality, market
│   ├── product-specs/
│   ├── quality/
│   ├── best-practices/
│   ├── market/
│   ├── cc-platform-contract.md
│   └── shared-vocabulary.md
├── meta/
│   └── pitfalls/
│       └── pitfalls.json         # Seed institutional memory
├── skills/                       # 15 Engine skills (installed to .claude/skills/)
│   ├── create/
│   ├── fill/
│   ├── validate/
│   ├── package/
│   ├── publish/
│   ├── scout/
│   ├── onboard/
│   ├── import/
│   ├── status/
│   ├── help/
│   ├── think/
│   ├── explore/
│   ├── map/
│   ├── test/
│   └── aegis/
├── agents/                       # 1 Engine agent
│   └── scout-agent.md
└── README.md                     # Installation guide + quick start
```

---

## The Meta-Bootstrap

The Engine should be publishable through its own pipeline:

```
/create system studio-engine
/fill (all the Engine content)
/validate --level=3
/package
/publish
→ myclaude install studio-engine  # anyone can use it
```

This is the ultimate dogfood test. The Engine validates itself.

---

## Implementation Dependencies

1. **myclaude CLI** must support `install` command for system-type products
2. **myclaude CLI** must support idempotent file distribution (hash-based skip)
3. **Engine** must be packagable as a system product via its own /package
4. **F-010** (publish directory structure mismatch) must be resolved

## Timeline Estimate

- Install spec (this document): DONE
- Package Engine as system product: 1 session
- Test install flow: 1 session
- CLI `install` command: depends on myclaude CLI team
