# Engine Pipeline & State Machine

## PIPELINE CONTRACTS

```
/onboard → creator.yaml (Master Input: creator profile, environment scan, preferences)
/scout   ← creator.yaml + domain query | → workspace/scout-{slug}.md + STATE.yaml{last_scout}
/create  ← creator.yaml [+ scout report] | → workspace/{slug}/ + .meta.yaml{type, slug, phase:scaffold}
/fill    ← workspace/{slug}/ + .meta.yaml{phase:scaffold} | → .meta.yaml{phase:content, fill_progress:cleared}
/fill output additions to .meta.yaml:
  fill_metrics:
    sections_total: N
    sections_completed: N
    sections_without_help: N        # key signal for adaptive fading
    avg_time_per_section: seconds   # approximation from session timing
    help_invocations: N             # /think calls + "I'm not sure" signals
    abandonment_point: null | section_name
    inline_research_used: boolean
  scaffolding_level: auto | minimal | full
  # Scaffolding logic:
  # IF sections_without_help >= 3 → scaffolding_level: minimal (reduce guidance)
  # IF help_invocations > sections_completed → scaffolding_level: full (increase guidance)
  # DEFAULT: auto (Engine decides per section based on creator signals)
  # This is adaptive fading in a single interface — no "beginner/expert" toggle.
/validate← workspace/{slug}/ + .meta.yaml{phase:content} | → .meta.yaml{phase:validated, scores, trajectory, intelligence}
/test    ← workspace/{slug}/ + .meta.yaml{phase:validated} | → .meta.yaml{test_result, test_scenarios} (MANDATORY before /package for MCS-2+)
/package ← workspace/{slug}/ + .meta.yaml{phase:validated, test_result:pass} | → .publish/{vault.yaml, stripped files, manifests}
/publish ← .publish/ + myclaude auth | → marketplace listing + .meta.yaml{phase:published}
```

Note: /scout is optional but recommended. It produces intelligence that /create and /fill consume (scout-aware routing + research injection).
Scout reports are NOT products — they don't enter the state machine. They persist as `workspace/scout-{slug}.md`.
If /fill detects no scout report for MCS-2+ products, it warns the creator and offers inline WebSearch as fallback (proactive #15, #16).
After /publish, the Engine suggests feedback collection and checks install data on next session (proactive #14 — feedback loop).
Install specification: `references/install-spec.md` — defines `myclaude install studio-engine` behavior.
Intelligence layer: `references/intelligence-layer.md` — autonomous awareness (market, value, portfolio, distribution, amplification). Surfaces one insight per pipeline moment. Always suggestion, never command.

## VALIDATION

8 stages + 3 sub-stages: Structural(blocking)→Integrity(blocking)→DNA Tier1(blocking)→DNA Tier2→DNA Tier3(PRO)→CLI Preflight(blocking)→Anti-Commodity(coaching)→Cognitive Fidelity(advisory, cognitive minds only)→Baseline Delta(advisory, if scout report)→Composition Check(advisory, bundles only)→Value Intelligence(advisory, MCS-2+). Score: `(DNA×0.50)+(Structural×0.30)+(Integrity×0.20)`. Stage 8 (Value Intelligence) computes value_score from 4 factors (depth×0.35 + uniqueness×0.30 + coverage×0.20 + market×0.15), suggests pricing, determines portfolio role. Always advisory — never blocks publishing. Reference: `references/intelligence-layer.md` + `config.yaml → intelligence`. Details in `quality-gates.yaml`.

## STATE MACHINE

```
/create→scaffold → /fill→content → /validate→validated → /test→tested → /package→packaged → /publish→published
                         ↑ file edited = state regresses ←───────────────────────────────────────────┘
Note: /test is MANDATORY for MCS-2+ products (meta-learning #20). MCS-1 products may skip to /package.
```

## FILE MAP

Root: CLAUDE.md, STATE.yaml, config.yaml, structural-dna.md, quality-gates.yaml.
Product system: `product-dna/`, `templates/`, `references/` (product-specs, exemplars, quality, best-practices, market).
Skills: `.claude/skills/` (15 skills). Agents: `.claude/agents/` (scout-agent). Workspace: `workspace/` (active builds + scout reports, gitignored).

## LOAD ON DEMAND

Skills load `product-dna/{type}.yaml` + `references/product-specs/{type}` per invocation. `/scout` loads `.claude/agents/scout-agent.md` + `references/scout-methodology.md` + `templates/scout/` + `config.yaml{scout}`. `/create` adds `templates/{type}/` [+ `workspace/scout-*.md` if exists]. `/validate` adds `config.yaml` + `quality-gates.yaml`. Reference paths: quality→`references/quality/`, pricing→`references/market/`, DNA→`structural-dna.md`, platform→`references/cc-platform-contract.md`, UX→`references/ux-experience-system.md` + `references/ux-vocabulary.md` + `references/quality/engine-voice.md` (UX stack, loaded by all output-producing skills). Context: <5%.

## Context Architecture

### Loading Order (cache-optimized)

Every Engine operation loads context in this strict order:

1. **Tools/Skill definitions** [STATIC — cacheable]
   - Active skill's primary file loaded as tool definition
   - References/ loaded per skill's activation protocol

2. **System prompt** (CLAUDE.md) [STATIC — cacheable]
   - Engine identity, boot sequence, rules
   - Budget: <4K characters (platform-verified optimal)

3. **Product DNA + Templates** [SEMI-STATIC — cacheable per type]
   - product-dna/{type}.yaml loaded per /create or /validate
   - templates/{type}/ loaded per /create
   - Invalidated only when Engine version changes

4. **Dynamic state** [NEVER CACHED]
   - STATE.yaml (session state, current task)
   - .meta.yaml (active product state, scores)
   - creator.yaml (profile, preferences)
   - User messages and conversation history

### Token Budgets

| Layer | Budget | Rationale |
|-------|--------|-----------|
| Ambient (always loaded) | <4K tokens | Performance degrades non-linearly beyond this threshold |
| Per-operation (on-demand) | <15K tokens | Maintains high instruction-following accuracy |
| Total ceiling | 70% of context window | Degradation accelerates near limits; never approach the edge |

### Rules

- NEVER load all 13 product type specs simultaneously
- NEVER put timestamps, counters, or session IDs in cached blocks
- Dynamic content (STATE.yaml, .meta.yaml) ALWAYS loads AFTER all static content
- Each loaded reference should use clear section boundaries for model parsing
- The Engine already implements this as hybrid RAG: retrieve per skill, reason in context
