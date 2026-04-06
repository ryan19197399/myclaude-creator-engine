---
name: validate
description: >-
  Run MCS quality validation on products in workspace/. Three-tier system: MCS-1
  structure, MCS-2 quality + anti-commodity, MCS-3 deep review. Returns scored reports
  with fix instructions. Use when: 'validate', 'check quality', or before publishing.
argument-hint: "[--level=1|2|3] [--fix] [--batch]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(myclaude *)
---

# Validator

Run MCS quality checks on any product in `workspace/` and return actionable, scored reports.

**When to use:** After building or modifying a product, before publishing, or anytime you want a quality snapshot.

**When NOT to use:** On products outside `workspace/`. Do not use to validate the Engine itself.

---

## Activation Protocol

1. Detect product type: read `.meta.yaml` → `product.type` and `state.phase`
   - Missing → infer from file structure (SKILL.md, AGENT.md, SQUAD.md, hooks.json, etc.)
   - Cannot determine → ask: "What product type is this?"
2. **Maintain creator persona**: Read `creator.yaml` → adapt to `profile.type` and `technical_level`
3. **Load voice identity**: Read `references/quality/engine-voice.md` → verdict format
4. Load DNA requirements: `product-dna/{type}.yaml`
5. Load product spec: `references/product-specs/{type}-spec.md`
6. Load config: `config.yaml` → scoring weights, thresholds, placeholder patterns
7. Load gates: `quality-gates.yaml` → state transition rules

---

## Commands

```
/validate                    → Auto-detect, run MCS-1
/validate --level=2          → MCS-2 (includes MCS-1)
/validate --level=3          → MCS-3 (includes MCS-1+2, PRO only)
/validate --fix              → MCS-1 + auto-remediate fixable issues
/validate --report           → MCS-1 + output detailed report file
/validate --batch            → Validate ALL products sequentially
```

---

## Core Instructions

### STAGE EXECUTION

Execute stages in order. Blocking stages stop on failure. Non-blocking stages report but continue.

**Load detailed stage protocols from references/ on demand:**

| Stage | Name | Blocking | Reference |
|-------|------|----------|-----------|
| 1 | Structural | YES | Read `${CLAUDE_SKILL_DIR}/references/validation-stages.md` → Stage 1 |
| 2 | Integrity | YES | Same file → Stage 2 |
| 3 | DNA Tier 1 | YES (MCS-1) | Same file → Stage 3 |
| 4 | DNA Tier 2 | no (MCS-2) | Same file → Stage 4 |
| 5 | DNA Tier 3 | no (MCS-3, PRO) | Same file → Stage 5 |
| 6 | CLI Preflight | YES | Same file → Stage 6 |
| 7 | Anti-Commodity | no (MCS-2+) | Same file → Stage 7 |
| 7b | Cognitive Fidelity | no (cognitive minds) | Same file → Stage 7b |
| 7c | Baseline Delta | no (if scout) | Same file → Stage 7c |
| 7d | Composition Check | no (bundles) | Same file → Stage 7d |
| 8 | Value Intelligence | no (MCS-2+) | Read `${CLAUDE_SKILL_DIR}/references/value-intelligence.md` |

**Stage routing by level:**
- `--level=1` (MCS-1): Stages 1, 2, 3, 6
- `--level=2` (MCS-2): Stages 1, 2, 3, 4, 6, 7, 7b-7d, 8
- `--level=3` (MCS-3): Stages 1, 2, 3, 4, 5, 6, 7, 7b-7d, 8

### UX STACK (load before rendering output)

1. `references/ux-experience-system.md` §1 Context Assembly + §2.3 Moment Awareness (pass vs fail) + §3.3 Score Trajectory
2. `references/ux-vocabulary.md` — translate tiers and terms
3. `references/quality/engine-voice.md` — Brand DNA + sfumato constraints

**Cognitive rendering:** /validate output adapts to creator journey. First validation pass = milestone moment (§4.1). Nth pass at 100% = skip celebration, surface next challenge ("Quality mastered. Distribution next?"). Failure = direct, prioritized, no sugar-coating. Score trajectory = show only when 2+ data points tell a meaningful story. Expert creators get technical details. Beginners get human explanation of what the score means.

---

### SCORING & OUTPUT

Read `${CLAUDE_SKILL_DIR}/references/validation-scoring.md` for:
- Hard veto rules (pre-scoring)
- Scoring formula: `OVERALL = (DNA×0.50) + (STRUCTURAL×0.30) + (INTEGRITY×0.20)`
- Verdict logic (READY / NEEDS WORK / NOT READY)
- Output format template
- Token budget report
- Guided iteration (draft fixes for failures)
- Auto-fix rules (--fix flag)
- Batch validation (--batch)
- Publish pre-flight
- Persona-aware rendering
- State update templates (.meta.yaml + STATE.yaml)

---

## Quality Gate

The Validator skill itself passes if:
- It correctly identifies product type from `.meta.yaml` or file structure
- It runs all checks appropriate for the requested MCS level
- Every failed check includes a specific, actionable fix instruction
- Score calculation matches formula: `passed / total × 100`
- `.meta.yaml` is updated after every validation run
- `--fix` never modifies content that the creator wrote

---

## Anti-Patterns

1. **Validating without reading product-dna** — Always load type-specific DNA before checking patterns
2. **Skipping blocking stages** — Stage 1-2 must pass before Stage 3+
3. **Generic fix instructions** — Every failure needs a specific, actionable fix
4. **Modifying creator content in --fix** — Only structural/formatting fixes
5. **Running Stage 8 for MCS-1** — Value intelligence adds noise at MCS-1, skip it

## Compact Instructions

When context is compressed, preserve:
- Product slug, type, and current MCS level being validated
- Stage progress (which stages passed/failed)
- Overall score and verdict (READY/NEEDS WORK/NOT READY)
- Top 3 failures with fix instructions
- Value intelligence score if Stage 8 ran
- Whether --fix or --batch mode is active
- **UX rule:** Celebrate work not person. Show score trajectory if 2+ data points. Use ux-vocabulary.md tiers (Verified/Premium/Elite not MCS-1/2/3) in user-facing output.
