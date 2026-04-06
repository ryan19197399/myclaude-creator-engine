# Create Router — Decision Tree, Scaffold Structures, Prefilling

Full routing logic and scaffold details for the `/create` skill.
Load this file when: routing a creator through type selection, generating a scaffold structure, or building prefill content.

---

## SECTION 1: DECISION TREE

### Scout-Aware Routing (check FIRST, before any menu)

1. Glob `workspace/scout-*.md` for existing scout reports
2. If one or more reports exist, read the most recent and extract Section 5 (Setup Recommendation)
3. Present scout-informed options:
   ```
   I found a scout report for "{domain}" ({date}).
   It recommends {N} products:

     1. {name} ({type}) — {purpose}
     2. {name} ({type}) — {purpose}
     ...

   Build from this recommendation? Pick a number, or:
   - "all" → scaffold all recommended products in sequence
   - "skip" → ignore scout and choose manually
   - "/scout {new-domain}" → research a different domain first
   ```
4. If creator picks a product from the recommendation:
   - Pre-populate slug, type, description, and MCS target from scout report
   - Load scout report as context during discovery questions (Step 2)
   - Note in `.meta.yaml`: `scout_source: "scout-{slug}.md"` for traceability
5. If "all" → scaffold each product sequentially, pausing after each for confirmation.
   **Each** scaffold gets `scout_source: "scout-{slug}.md"` in its `.meta.yaml` — traceability must be per-product, not just the first.

### No Scout Report + No Argument: Level-Based Menu

**If creator.yaml exists AND technical_level is advanced/expert**, show the direct menu.

**CRITICAL:** Load `references/ux-vocabulary.md` → Product Types table. If `creator.profile.type` is NOT `developer`, use the user-facing names and one-liners from ux-vocabulary.md instead of the internal names below. The menu adapts to who is reading it.

**Developer menu** (profile.type = developer):
```
What do you want to create?

  1. skill        — A reusable capability Claude can run
  2. agent        — A specialized persona with domain expertise
  3. squad        — A team of coordinated agents
  4. workflow     — An automated multi-step process
  5. ds           — A design system (tokens, components, exports)
  6. claude-md    — A project-specific CLAUDE.md configuration
  7. app          — A deployable application
  8. system       — A composite system (skills + agents + workflows)
  9. bundle       — A curated collection of products
  10. statusline  — A Claude Code status bar configuration
  11. hooks       — Event-driven automations for Claude Code
  12. minds        — A domain expertise profile
  13. output-style — Custom output formatting and rendering rules

Enter number or name:
```

**Non-developer menu** (all other profile.type values):
```
What do you want to create?

  1. Tool              — Adds a new capability to Claude Code
  2. Agent             — A specialized persona with domain expertise
  3. Team              — Multiple agents working together
  4. Guided Process    — Step-by-step automation
  5. Design Kit        — Visual design language and components
  6. Project Rules     — Smart defaults for your project type
  7. Application       — Deployable software
  8. Complete Setup    — Full working environment
  9. Collection        — Curated set of tools that work together
  10. Status Bar       — Live info at the bottom of your screen
  11. Auto-Actions     — Things that happen automatically
  12. Advisor / Mind   — An expert you can consult
  13. Response Style   — Changes how Claude communicates

Pick a number:
```

**If creator is beginner/intermediate OR type is domain-expert/operator/marketer**, use the Decision Tree below.

### Decision Tree: Q1 → Q2 → Q3 Routing

Ask via AskUserQuestion (single select):

```
Q1: What does your product need to do?

  1. DO something        — execute tasks, run processes, produce output
  2. THINK about something — advise, analyze, reason, consult
  3. GOVERN something    — enforce rules, react to events, set standards
  4. EVERYTHING          — full domain infrastructure or an app
  5. LOOK / FORMAT       — visual design, output formatting, status display
  6. I don't know yet    — help me figure it out
```

**DO →** Ask Q2:
```
Q2: Is it a single action or a sequence of steps?

  1. Single action
  2. Sequence of steps
  3. Automatic reaction to an event
```
- Single action → Q3: "Does it need judgment to decide WHAT to do, or just execution?"
  - Needs judgment → **agent** ("An agent can assess context and decide how to act.")
  - Just execution → **skill** ("A skill runs the same way every time — focused and reliable.")
- Sequence → **workflow** ("A workflow orchestrates steps in order — like a recipe.")
- Automatic reaction → **hooks** ("Hooks fire automatically when Claude does something.")

**THINK →** Ask Q2:
```
Q2: How many perspectives does it need?

  1. One deep perspective (a specialist advisor)
  2. Multiple perspectives that collaborate
```
- One → Q3: "Does it also need to ACT (do things), or just advise?"
  - Also acts → **agent** ("An agent thinks AND does — judgment plus action.")
  - Just advises → **minds** (depth: advisory by default — fast, ~200 lines)

    **Depth upsell (post-scaffold, not pre-scaffold):** After advisory scaffold is generated, offer. **CRITICAL:** Adapt language to profile.type.

    For developers:
    ```
    Scaffold ready. Want to upgrade this to a deeper cognitive mind?

      1. Keep as advisory mind (done — run /fill to add content)
      2. Upgrade to cognitive mind (5 layers, ~1000 lines, full reasoning engine)
      3. Build from genius profile (da-vinci, etc. — pre-populated cognitive architecture)
    ```

    For non-developers:
    ```
    Your advisor is ready. How deep should it go?

      1. Keep it simple — a quick expert you can ask questions (done — /fill to add your expertise)
      2. Make it deep — a specialist that reasons through problems step by step (more setup, much more powerful)
      3. Start from a famous thinker — pre-built expert personality you customize (da Vinci, etc.)
    ```
    - Option 1: proceed with advisory scaffold as-is
    - Option 2: replace scaffold with cognitive template from `templates/minds/cognitive/`, update .meta.yaml `minds_depth: cognitive`
      - Then ask sub-type: "What's the source?" → Self (scan environment) or Domain (suggest /scout)
    - Option 3: load from genius library `templates/genius-library/{name}/profile.yaml`, pre-populate C1-C7 strands, update .meta.yaml `minds_depth: cognitive, minds_sub_type: genius, genius_profile: "{name}"`

    **Direct shortcuts (skip decision tree entirely):**
    - `/create minds --cognitive` → scaffold cognitive directly
    - `/create minds --genius` → show genius library directly
    - `/create minds --genius da-vinci` → load da-vinci profile directly
    - If creator says "cognitive mind", "genius mind", "da-vinci mind", "self mind" → route directly without Q4

- Multiple → **squad** ("A squad is a team of specialists that collaborate on complex problems.")

**GOVERN →** Ask Q2:
```
Q2: Should the rules be always active or triggered by events?

  1. Always active — every session, no exception
  2. Triggered by specific events
```
- Always active → **claude-md** ("A CLAUDE.md is constitutional — rules that apply every single time.")
- Event-triggered → **hooks** ("Hooks watch for events and react automatically.")

**EVERYTHING →** Ask Q2:
```
Q2: Does this need a dedicated project, or are you extending your current setup?

  1. Dedicated project (its own directory, config, infrastructure)
  2. Extensions to my current setup (add capabilities)
  3. An application (deployable software, not a Claude product)
```
- Dedicated → **system** ("A system is a complete organism — skills, agents, rules, all composed.")
- Extensions → **bundle** ("A bundle packages products together for joint install.")
- Application → **application** ("An application is deployable software — code, not prompts.")

**APPEARANCE / FORMAT →**
```
Q2: What aspect of appearance or formatting?

  1. Visual consistency across UIs (colors, typography, components)
  2. How Claude formats its output (tone, structure, rendering)
  3. Always-visible info in the status bar
```
- Visual consistency → **design-system** ("A design system defines visual DNA — tokens, components, exports.")
- Output formatting → **output-style** ("An output style controls how Claude presents its responses.")
- Status bar → **statusline** ("A statusline shows ambient info without asking — always visible.")

**DON'T KNOW →**
```
No problem. Let me help:

  1. Describe what you're trying to achieve → I'll recommend a type
  2. /scout {domain} → I'll research the domain and recommend products
  3. /explore → Browse what others have built for inspiration
```
If creator describes their goal: parse intent using these patterns:
- "do X" / "automate X" → route to DO branch
- "think about X" / "advise on X" → route to THINK branch
- "enforce X" / "rules for X" → route to GOVERN branch
- Still unclear → suggest `/scout` as next step

After the tree resolves to a type, explain in one sentence why it fits, then proceed to the standard flow (exemplar preview → discovery questions → scaffold).

---

## SECTION 2: PER-CATEGORY SCAFFOLD STRUCTURES

**skill:**
```
workspace/{slug}/
├── SKILL.md              # Main skill definition
├── references/           # Domain knowledge
│   └── .gitkeep
├── examples/             # Usage examples (3+ for MCS-2)
│   └── .gitkeep
└── README.md             # Installation and usage
```

**agent:**
```
workspace/{slug}/
├── AGENT.md              # Agent definition + persona
├── identity/             # Persona detail files
│   └── .gitkeep
├── architecture/         # Cognitive architecture docs
│   └── .gitkeep
└── README.md
```

**squad:**
```
workspace/{slug}/
├── SQUAD.md              # Squad definition + routing
├── agents/               # Individual agent definitions
│   └── .gitkeep
├── config/               # Routing and handoff config
│   └── routing.yaml
└── README.md
```

**workflow:**
```
workspace/{slug}/
├── WORKFLOW.md           # Workflow definition
├── steps/                # Individual step definitions
│   └── .gitkeep
├── config/               # Triggers and error handling
│   └── config.yaml
└── README.md
```

**ds (design system):**
```
workspace/{slug}/
├── DESIGN-SYSTEM.md      # Design system definition
├── tokens/               # Design tokens
│   └── .gitkeep
├── components/           # Component definitions
│   └── .gitkeep
├── exports/              # Export format configs
│   └── .gitkeep
└── README.md
```

**claude-md:**
```
workspace/{slug}/
├── CLAUDE.md             # The CLAUDE.md itself
├── rules/                # Modular rule files
│   └── .gitkeep
└── README.md
```

**app:**
```
workspace/{slug}/
├── APPLICATION.md        # Application definition
├── src/                  # Application source
│   └── .gitkeep
├── CLAUDE.md             # AI pair-programming instructions
├── package.json          # or equivalent manifest
└── README.md
```

**system:**
```
workspace/{slug}/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest — components, routing, install target
├── SYSTEM.md             # System definition + composition + routing
├── skills/               # Included skills
│   └── .gitkeep
├── agents/               # Included agents
│   └── .gitkeep
├── hooks/                # Lifecycle hooks (optional)
│   └── .gitkeep
├── references/           # Shared knowledge base
│   └── .gitkeep
├── config/
│   └── routing.yaml      # Component routing rules
└── README.md
```

**bundle:**
```
workspace/{slug}/
├── vault.yaml            # Bundle manifest with includes[] (IS the product)
└── README.md             # What's included, curation rationale
```

**statusline:**
```
workspace/{slug}/
├── statusline.sh             # Shell script (reads JSON stdin, outputs ANSI stdout)
├── settings-fragment.json    # settings.json merge fragment for activation
├── examples/                 # Sample stdin JSON + expected stdout output
│   └── .gitkeep
└── README.md
```

**hooks:**
```
workspace/{slug}/
├── hooks.json            # settings.json fragment (event bindings)
├── scripts/              # Handler scripts
│   └── handler.sh
├── examples/
│   └── .gitkeep
└── README.md
```

**minds (advisory depth):**
```
workspace/{slug}/
├── AGENT.md              # Mind definition (YAML frontmatter + advisory persona)
├── references/           # Domain knowledge
│   └── .gitkeep
├── examples/             # Conversation examples
│   └── .gitkeep
└── README.md
```

**minds (cognitive depth):**
```
workspace/{slug}/
├── AGENT.md                          # Layer 1: Boot (identity, principles, cognitive patterns)
├── references/
│   ├── cognitive-core.md             # Layer 2: Biography, architecture, singularity
│   ├── personality.md                # Layer 3: Behavioral matrix, style, interaction
│   ├── knowledge-base.md            # Layer 4: Domain depth + explicit boundaries
│   └── reasoning-engine.md          # Layer 5: Patterns, models, triggers
├── examples/
│   └── examples.md                   # 3+ interaction examples
└── README.md
```

When scaffolding cognitive depth: load template from `templates/minds/cognitive/` instead of `templates/minds/`. If genius sub-type: also load `templates/genius-library/{name}/profile.yaml` and pre-populate C1-C7 strands in the scaffold. Record in `.meta.yaml`: `minds_depth: cognitive`, `minds_sub_type: self|genius|domain`, and if genius: `genius_profile: "{name}"`.

**output-style:**
```
workspace/{slug}/
├── OUTPUT-STYLE.md       # Style definition (tone, structure, rendering rules)
├── examples/             # Before/after examples of styled output
│   └── .gitkeep
└── README.md
```

---

## SECTION 3: PREFILLING STRATEGY

When generating scaffold files, prefill key sections to give creators a running start:

**SKILL.md prefill:**
```markdown
# {Product Name}

> {One-liner from discovery answer}

**Version:** 1.0.0
**Category:** Skills
**Author:** {from creator.yaml}

---

## When to Use

- {Prefilled from discovery question "What problem does this skill solve?"}

## When NOT to Use

- General-purpose tasks that don't require specialized knowledge (use direct prompting instead)

---

## Activation Protocol

Before responding to any invocation:

1. **Load domain knowledge:** Read `references/domain-knowledge.md`
2. **Load exemplars:** Read `examples/examples.md`
3. **Identify user intent:** Parse input for specific request type
```

**README.md prefill:**
```markdown
# {Product Name}

{One-liner from discovery}

## Install

```bash
myclaude install {slug}
```

## Usage

```
/{slug} {example input}
```

## Requirements

- Claude Code >= 1.0.0
```

Prefilling reduces blank-page paralysis and ensures MCS-1 structural compliance from the first moment.
