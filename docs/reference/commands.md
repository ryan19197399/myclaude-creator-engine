# Commands Reference

All 15 commands. Organized by pipeline phase, with usage examples and expected output.

```
  research       create       refine       verify       ship
  /scout    →   /create  →   /fill   →  /validate →  /publish
```

> ✦ Each step feeds the next. Scout research flows into creation. Creation generates structure for filling. Filling produces content that validation scores. Nothing is disconnected.

---

## Pipeline Commands

These commands follow a natural sequence.

```
/onboard → /scout → /create → /fill → /validate → /test → /package → /publish
              ↑                                              ↑
           optional                                    required for
           but recommended                             Premium/Elite
```

---

### `/onboard` — Set Up Your Profile

Set up or update your creator profile. The engine adapts language, guidance depth, and workflow to your answers.

```
/onboard              # first-time setup (60 seconds)
/onboard              # run again to update anytime
```

**Creates:** `creator.yaml` — your profile, read by every other command.

**What it asks:** Your expertise areas, goals (share knowledge? automate workflows? build a portfolio?), technical level, and preferred workflow style (guided or autonomous).

---

### `/scout [domain]` — Research Before Building

Test what Claude already knows about a domain, find the gaps, scan the marketplace, and get a recommendation for what to build.

```
/scout kubernetes-security
/scout brand-strategy
/scout financial-modeling
```

**Output example:**

```
Scout Report: kubernetes-security
─────────────────────────────────
Claude baseline: 67% coverage
Gaps found: 11
Marketplace: 0 existing products
Recommendation: cognitive mind (+33 points vs vanilla)
```

**Creates:** `workspace/scout-{domain}.md` — consumed automatically by `/create` and `/fill`.

---

### `/create [type]` — Generate Product Structure

Generate a new product with structural DNA and guided annotations.

```
/create skill         # focused tool
/create minds         # knowledge advisor
/create squad         # multi-agent team
/create workflow      # methodology framework
/create agent         # autonomous task runner
/create claude-md     # behavioral rules
/create hooks         # lifecycle automation
/create system        # multi-component tool
/create bundle        # meta-package
```

**All 13 types:** skill, agent, squad, workflow, minds, system, claude-md, hooks, statusline, output-style, design-system, application, bundle

**What happens:** The engine asks discovery questions (name, purpose, audience, differentiation), then generates a complete structure with `<!-- WHY -->` annotations explaining what goes in each section.

**Creates:** `workspace/{slug}/` with product files and `.meta.yaml` state tracker.

---

### `/fill` — Add Your Expertise

AI-guided content filling. The engine walks through each section, asks domain-specific questions, and writes structured content from your answers.

```
/fill                 # continues active product
/fill my-product      # target a specific product
```

**What it looks like:**

```
── Section 3/7: Reasoning Engine ──
Walk me through how you approach a K8s security audit.
What's the first thing you check?
```

You answer in plain language. The engine converts your expertise into structured, activatable content.

When all sections are filled, the engine automatically runs a quick quality check.

---

### `/validate` — Score Quality

Score your product against 20 structural patterns across three tiers.

```
/validate             # validate active product (default: MCS-1)
/validate --level=2   # deeper review (Premium patterns)
/validate --fix       # auto-fix what can be fixed
/validate --batch     # validate all products in workspace
```

**Tiers:**

| Tier | Score | Gate |
|:-----|:------|:-----|
| Verified | >= 75% | Core patterns: activation, documentation, error handling |
| Premium | >= 85% | Advanced: anti-patterns, progressive disclosure, quality gates |
| Elite | >= 92% | State-of-the-art: cache design, attention-aware authoring |

**Output when passing:**

```
READY — 100% (target: 85%)
20/20 structural patterns passing.
```

**Output when failing:**

```
NEEDS WORK — 72% (target: 85%)
Top 3 fixes:
  1. Anti-patterns: 2 found, need 5
  2. Quality gate: criteria not verifiable
  3. References: no files loaded in activation
```

---

### `/test` — Behavioral Validation

Run your product in an isolated sandbox against three scenarios: happy path, edge case, and adversarial.

```
/test                 # test active product
/test my-product      # test specific product
```

**Required** for Premium and Elite products before packaging. Optional for Verified.

---

### `/package` — Prepare for Distribution

Strip guided annotations, generate distribution manifests (vault.yaml, plugin.json, agentskills.yaml), and stage everything in `.publish/`.

```
/package              # package active product
/package my-product   # package specific product
```

**Requires:** `/validate` must pass first.

---

### `/publish` — Ship to the Marketplace

Publish to [myclaude.sh](https://myclaude.sh). Shows a summary, requires your confirmation, then runs validation and publishes.

```
/publish              # publish active product
/publish my-product   # publish specific product
```

**Requires:** `/package` must run first. You must confirm before publishing — the engine never publishes without explicit approval.

**After publishing:** Anyone can install with `myclaude install your-product`.

> ◆ The engine never publishes without your explicit confirmation. Your work, your decision, always.

---

## Utility Commands

### `/status` — Dashboard

Shows engine version, your profile, all products with scores, pipeline positions, and suggested next steps.

```
/status
```

---

### `/help` — Command Reference

Quick command listing with descriptions, organized by category. Adapts recommendations based on your profile and current state.

```
/help
```

---

### `/import` — Bring Existing Skills

Import skills you have already created in `.claude/skills/` into the engine pipeline for validation, quality scoring, and publishing.

```
/import               # interactive import
/import --scan        # scan and list all importable skills
```

---

### `/map [topic]` — Structure Domain Knowledge

Extract and structure your expertise into a reusable knowledge map. Useful before creating complex products like cognitive minds or squads.

```
/map kubernetes-security
/map brand-positioning
```

**Creates:** `workspace/domain-map.md` — consumed by `/create` and `/fill`.

---

### `/think [topic]` — Brainstorm Before Committing

Pause the pipeline to think through a problem, compare approaches, or explore ideas. Use this when you are not sure which direction to take.

```
/think should I build a skill or a mind?
/think what product type fits my use case?
```

---

### `/explore [query]` — Search the Marketplace

Search [myclaude.sh](https://myclaude.sh) for existing tools, analyze competition, and discover gaps and inspiration.

```
/explore security tools
/explore what exists for marketing
```

---

### `/aegis` — Security Audit

Security audit for any codebase. STRIDE threat modeling, 300+ vulnerability patterns, 8 compliance frameworks. Works independently — use it on any project, not just engine products.

```
/aegis
```

---

## Quick Reference

| Command | Purpose | Required? |
|:--------|:--------|:----------|
| `/onboard` | Profile setup | Yes (once) |
| `/scout` | Domain research | Recommended |
| `/create` | Generate product | Yes |
| `/fill` | Add content | Yes |
| `/validate` | Quality check | Yes |
| `/test` | Behavioral test | Premium/Elite only |
| `/package` | Prep for publish | Yes |
| `/publish` | Ship to marketplace | Yes |
| `/import` | Bring existing skills | As needed |
| `/status` | Dashboard | Anytime |
| `/help` | Command list | Anytime |
| `/map` | Knowledge mapping | As needed |
| `/think` | Brainstorm | As needed |
| `/explore` | Search marketplace | As needed |
| `/aegis` | Security audit | As needed |

---

> ✦ Not sure where to start? `/status` always knows where you are. `/think` helps when you're stuck. `/scout` shows what's worth building.

**Next:** [Product Types](product-types.md) · [Quality System](quality-system.md) · [Getting Started](../getting-started.md)
