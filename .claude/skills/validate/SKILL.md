---
name: validate
description: >-
  Run MCS quality validation on products in workspace/. Three-tier system: MCS-1
  structure, MCS-2 quality + anti-commodity, MCS-3 deep review. Returns scored reports
  with fix instructions. Use when: 'validate', 'check quality', or before publishing.
argument-hint: "[--level=1|2|3] [--fix] [--batch] [--express]"
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
1b. **Mode selection (Express vs Guided).** Read `creator.yaml → preferences.workflow_style`. Resolve the flow mode:
    - `--express` flag OR `workflow_style == "autonomous"` → **Express mode**. Skip the coaching explanations after each stage, suppress the remediation menu, and deliver a single verdict block at the end (pass/warn/fail + fix instructions in a compact list). Persona tone still holds; only the conversational scaffolding is trimmed.
    - `workflow_style == "guided"` or missing → **Guided mode** (default). Walk each stage with the full coaching voice and propose remediation interactively after failing stages.
2. **Maintain creator persona**: Read `creator.yaml` → adapt to `profile.type` and `technical_level`
3. **Load voice identity**: Load `references/quality/engine-voice-core.md`. Load the full `references/quality/engine-voice.md` only for peak moments (first-pass milestone celebration, confronting failure verdict) — see UX Stack below.
4. Load DNA requirements: `product-dna/{type}.yaml`
4b. **Load architectural DNA:** Read `structural-dna.md`. The 10 architectural principles and the Tier 1 DNA patterns (D1-D4, D13, D14) are the canonical audit baseline — Stages 3 and 5 grep the product against them, and any violation surfaces as coaching.
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

**Load detailed stage protocols from references/ on demand. Each stage is a separate file — load only the stage(s) you need for the current `--level`.**

| Stage | Name | Blocking | Reference |
|-------|------|----------|-----------|
| **0** | **Intent Coherence** (W3.7) | **advisory** | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-0-intent-coherence.md` |
| 1 | Structural | YES | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-1-structural.md` |
| 2 | Integrity | YES | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-2-integrity.md` |
| 3 | DNA Tier 1 | YES (MCS-1) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-3-dna-tier1.md` |
| 4 | DNA Tier 2 | no (MCS-2) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-4-dna-tier2.md` |
| 5 | DNA Tier 3 | no (MCS-3, PRO) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-5-dna-tier3.md` |
| 6 | CLI Preflight + 6b Health | YES (6) / advisory (6b) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-6-cli-preflight.md` |
| 7 | Anti-Commodity (+ 7b/7c/7d) | no (MCS-2+) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-7-anti-commodity.md` |
| 8 | Value Intelligence | no (MCS-2+) | Read `${CLAUDE_SKILL_DIR}/references/value-intelligence.md` (legacy) OR `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-8-value-intelligence.md` (new) |
| **9** | **Voice Coherence** | **advisory** | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-9-voice-coherence.md` |

**Stage 0 runs first** when `.meta.yaml` contains an `intent_declaration` block. It is advisory — surfaces coherence drift as coaching, never blocks. Skips silently for legacy products that lack the declaration, with a one-line advisory note.

**Stage 7 sub-stages (7b cognitive fidelity, 7c baseline delta, 7d composition check) are inside the stage 7 file — they only fire under their prerequisites and never need a separate load.**

**Index:** `${CLAUDE_SKILL_DIR}/references/validation-stages/_index.md` lists all stages with file paths and routing rules.

**Stage routing by level:**
- `--level=1` (MCS-1): Stages **0**, 1, 2, 3, 6, **9**
- `--level=2` (MCS-2): Stages **0**, 1, 2, 3, 4, 6, 7, 7b-7d, 8, **9**
- `--level=3` (MCS-3): Stages **0**, 1, 2, 3, 4, 5, 6, 7, 7b-7d, 8, **9**

Stage 9 (Voice Coherence) is the last stage at every level. Advisory — never blocks publish. Stage 9 audits the product against the myClaude voice contract (P10 Touch Integrity anchor).

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
6. **Blocking cascade hiding downstream issues** — When Stage 1-2 fails, downstream stages don't run. But the creator loses visibility into DNA/content issues that exist independently. After blocking failure, emit an advisory note: "Structural issues block full validation. After fixing these, re-run to see content-level results." Never silently hide what wasn't checked.

## Compact Instructions

When context is compressed, preserve:
- Product slug, type, and current MCS level being validated
- Stage progress (which stages passed/failed)
- Overall score and verdict (READY/NEEDS WORK/NOT READY)
- Top 3 failures with fix instructions
- Value intelligence score if Stage 8 ran
- Whether --fix or --batch mode is active
- **UX rule:** Celebrate work not person. Show score trajectory if 2+ data points. Use ux-vocabulary.md tiers (Verified/Premium/Elite not MCS-1/2/3) in user-facing output.
