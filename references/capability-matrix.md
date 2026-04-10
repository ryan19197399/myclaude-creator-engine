# Capability Matrix — The Decision Algorithm for `/create` Discovery Mode

This document defines how the Engine reasons from a creator's intent to a product form proposal. It is the operational core of `/create` in discovery mode — the 12-step decision algorithm, the wiring between `creator.intent_profile` fields and decision steps, the Express↔Guided dual mode with mid-session transition protocol, and the longitudinal feedback loop that lets the Engine calibrate its own confidence over time.

**Layer:** Canonical substrate. Consumed by `.claude/skills/create/` as the primary routing logic. Read after `references/intent-topology.md` — this document assumes the three axes, host derivation, and habitable cells are already understood. Extended by `references/skill-vs-agent-discriminators.md` (how steps 2, 3, 4, 5 actually discriminate in practice) and `references/composition-anatomy.md` (when the algorithm falls through to "don't know yet").

**Reading order:** §1 intent_profile fields → §2 wiring table → §3 12-step algorithm → §4 Express vs Guided → §5 transition protocol → §6 longitudinal feedback loop → §7 implementation contracts.

---

## §1 — The 7 `intent_profile` Fields

The decision algorithm reads seven causal fields from `creator.intent_profile` (schema v3 of `creator.yaml`, delivered in the onboard-bridge wave). Each field has a specific downstream consumer in the algorithm — no decorative fields, no fields without a declared purpose.

| Field | Values | Captured by | Consumed by steps |
|---|---|---|---|
| `domain_depth` | `deep` \| `working` \| `foundational` | onboard Phase 2 inference + Phase 3 confirmation | 2 (continuity context weight), 6 (depth justification) |
| `working_rhythm` | `iterative_with_feedback` \| `sprint_delegated` \| `hybrid` | onboard Phase 2 scan (session length patterns) + Phase 3 confirmation | 2 (continuity tiebreaker) |
| `usage_frequency_expectation` | `daily_multiple` \| `daily_single` \| `weekly` \| `monthly` \| `occasional` | onboard Phase 3 question | 3 (invocation mode), 9 (cell ranking) |
| `maintenance_appetite` | `deep_and_slow` \| `balanced` \| `fast_and_simple` | onboard Phase 3 question | 6 (depth cap) |
| `target_audience` | `personal_only` \| `team_only` \| `marketplace_public` \| `hybrid` | onboard Phase 3 question | 9 (cell ranking), 10 (naming and invisibility strictness) |
| `licensing_tolerance` | `conservative_own_only` \| `moderate_public_domain` \| `permissive_all` | onboard Phase 3 conditional (only if genius sub-type candidate) | 10 (genius-library filter) |
| `external_dependency_tolerance` | `isolated_no_deps` \| `trusted_deps_only` \| `permissive_all` | onboard Phase 2 scan (existing MCP usage) + Phase 3 confirmation | 10 (tool pool defaults) |

**Field absence is a first-class case.** Any of the seven fields may be absent when `/create` runs (the creator onboarded before schema v3, or skipped an optional question, or the inference engine returned low confidence). The algorithm never fails on absence — it applies the declared default and records `default_applied: {field}` in the `intent_declaration` output. Post-hoc auditing reads those markers to detect patterns in missing-field fallbacks and drive schema evolution.

**Causal discipline.** Every field in the table above has at least one consumer step. A field without a consumer is decorative and must be removed. This rule is enforced at codex validation time — adding a field to `creator.yaml` schema without adding a consumer here is blocked.

---

## §2 — Wiring Table: Step ↔ Field Afferent Map

The wiring table closes the afferent-efferent loop between §1 and §3. Each step declares which `intent_profile` fields it reads, what default it applies if a field is absent, and what decision it outputs. Implementation in `.claude/skills/create/` reads this table as the contract — no step reads a field not declared here, and no step writes a decision not declared here.

| Step | Reads fields | Default if absent | Decision output |
|---|---|---|---|
| **1 PARSE_INTENT** | *(reads creator's natural-language input, not intent_profile)* | Ask single clarifying question | `verb_family ∈ {do, advise, coordinate, observe, enforce, react}` |
| **2 APPLY_CONTINUITY_TEST** | `working_rhythm`, `domain_depth` | `working_rhythm: hybrid` | `continuity_bias ∈ {parent, isolated, unclear}` |
| **3 APPLY_INVOCATION_TEST** | `usage_frequency_expectation` | `weekly` (neutral) | `invocation_mode ∈ {remembered, needs_auto}` |
| **4 APPLY_POLLUTION_TEST** | *(derived from verb_family + continuity_bias)* | — | `pollution_risk ∈ {pollutes, safe}` |
| **5 APPLY_OUTPUT_TEST** | *(derived from verb_family)* | — | `output_shape ∈ {amplified_reasoning, structured_report}` |
| **6 RESOLVE_DEPTH** | `maintenance_appetite`, `domain_depth` | `balanced` | `depth ∈ {procedural, advisory, cognitive}` |
| **7 RESOLVE_NATURE** | *(derived from verb_family)* | — | `nature ∈ {executor, advisor, orchestrator, observer}` |
| **8 DERIVE_HOST** | *(computed from delivery × nature per topology §3)* | — | `host set` |
| **9 LOOKUP_CANONICAL_CELL** | `target_audience`, `usage_frequency_expectation` *(ranking only)* | Rank by depth ascending | Matched cell from `habitable_cells_v1` or `unroutable` |
| **10 PROPOSE_FORM** | `target_audience`, `licensing_tolerance`, `external_dependency_tolerance` | Skip filter | `proposed_form + 2 alternatives + rationale` |
| **11 RECORD_DECISION** | *(reads all prior step outputs)* | — | `intent_declaration` written to `.meta.yaml` |
| **12 APPEND_TO_HISTORY** | *(appends to decisions_history)* | — | Append-only log entry in `STATE.yaml` |

**Two implementation invariants.**

1. **Every field read via explicit path.** A step that reads `working_rhythm` reads it via `creator.intent_profile.working_rhythm`, not via inference, not via ambient context. If the field is absent at that path, the step applies the table's default and records the fallback. This makes missing-field behavior auditable.

2. **Every step that derives from prior outputs declares the derivation.** Steps 4, 5, 7, 8 do not read `intent_profile` — they derive from earlier step outputs. Their "reads" column is marked *derived* explicitly so that the afferent wiring cannot be misread as "no inputs".

**One exogenous input not in the wiring table.** A scout report (`workspace/scout-{slug}.md`), if present for the intent's domain, is not read by any single step — it is read once at the start of the algorithm and its findings are injected into Step 1 PARSE_INTENT as additional context for verb-family classification and into Step 9 LOOKUP_CANONICAL_CELL as a ranking boost (products grounded in scout research rank higher when multiple cells match). The scout source path is recorded in `scout_source` on the `intent_declaration` output. Scout is the Engine's way of saying: *"I did my homework before proposing — this proposal is grounded, not guessed."* A creator who ran `/scout` before `/create` gets proposals that read the domain; a creator who skipped scout gets proposals that read only their intent. Both paths are valid; the record distinguishes them.

**Afferent-efferent symmetry.** §1 declares what each field feeds; this table declares what each step reads. Without both sides, the implementation would have to guess which field belongs to which step — and guessing is the exact failure mode discovery mode exists to eliminate. The two tables together close the loop: every field has a declared consumer, every step has a declared set of inputs, and the wiring is auditable without reading a single line of implementation code.

---

## §3 — The 12-Step Decision Algorithm

Each step is written as a contract: what it reads, what it decides, what it passes forward. Steps execute in order; no step may be skipped in Guided mode (Express mode skips all steps — see §4). The algorithm is embedded as subsection logic inside `.claude/skills/create/references/create-router.md`; this document is its source of truth.

### Step 1 — PARSE_INTENT

**Reads:** the creator's natural-language expression of what they want to build. In Guided mode this is the first prompt text after `/create` (no sub-type argument); in Express mode this step is skipped entirely.

**Classifies:** the verb family at the root of the creator's intent. Six families, covering the full semantic surface of what a Claude Code product can do.

| Verb family | Example phrasings | Maps to nature (preview) |
|---|---|---|
| `do_X` | *"refactor all my TypeScript files to strict mode"*, *"scaffold a new landing page"* | executor |
| `advise_on_X` | *"help me think about tradeoffs in this design"*, *"review this for security issues"* | advisor |
| `coordinate_X` | *"when I'm shipping, run all the checks in order"*, *"review squad for pull requests"* | orchestrator |
| `observe_X` | *"notice when I'm making the same mistake twice"*, *"watch for patterns across sessions"* | observer |
| `enforce_X` | *"make sure I never commit secrets"*, *"block any PR that breaks the rules"* | executor (hook-bound) |
| `react_to_X` | *"when I finish a commit, do Y"*, *"on session start, load Z"* | executor or observer (hook-bound) |

**Outputs:** `verb_family` + the raw intent text preserved verbatim for inclusion in `intent_declaration`.

**Ambiguity handling.** If the intent expresses two verb families in one sentence (*"review my code and fix the security issues"* = advise + do), the algorithm splits: the creator is offered a choice between two routes or a composed system. This is the primary surface where the algorithm asks a clarifying question in Guided mode — every other ambiguity is resolved via default.

**LLM-dependent.** This step cannot be deterministic — natural-language verb classification requires LLM judgment. The §7 canonical examples in `references/intent-topology.md` serve as regression test anchors: each example's intent text must produce its canonical verb family in dry-run testing. Missing a single anchor breaks the gate.

### Step 2 — APPLY_CONTINUITY_TEST

**Reads:** `verb_family` (from step 1) + `creator.intent_profile.working_rhythm` + `creator.intent_profile.domain_depth`.

**Decides:** does this capability need the creator's current working context to function?

| Answer | Continuity bias | Delivery axis bias |
|---|---|---|
| YES — needs parent context | `parent` | `ambient_constitutional`, `ambient_path_scoped`, `invoked_slash_command` |
| NO — works from cold start | `isolated` | `invoked_task_spawn`, `composed_system` |
| UNCLEAR | `unclear` → tiebreaker below | — |

**Tiebreaker:** if the verb family alone does not resolve, read `working_rhythm`. `iterative_with_feedback` → bias `parent`. `sprint_delegated` → bias `isolated`. `hybrid` → remain `unclear` and escalate to Step 9 ranking logic (ambiguity is valid here; it carries forward and is resolved by the canonical cell lookup).

**`domain_depth` weight.** When domain_depth is `deep`, the continuity bias strengthens toward `parent` — deep-domain creators benefit more from ambient perspective that appears beside their existing expertise. When `foundational`, the bias strengthens toward `isolated` — foundational-depth creators benefit more from a separate mind that teaches, not a perspective that augments.

**Outputs:** `continuity_bias` passed to Step 4.

### Step 3 — APPLY_INVOCATION_TEST

**Reads:** `verb_family` + `creator.intent_profile.usage_frequency_expectation`.

**Decides:** will the creator remember to invoke this capability at the right moment, or does it need to appear automatically when the moment arrives?

| `usage_frequency_expectation` | Invocation mode | Delivery axis bias |
|---|---|---|
| `daily_multiple` or `daily_single` | `remembered` (any mechanism works; frequent recall stays fresh) | any |
| `weekly` | `remembered` (neutral; frequency supports recall) | any |
| `monthly` or `occasional` | `needs_auto` (infrequent recall forgets) | force `ambient_path_scoped` — the only native ambient that is not always-loaded |

**Why this matters.** A cognitive audit skill the creator invokes twice a month will be forgotten by week three — they won't remember it exists, and the capability dies on the shelf. Forcing `ambient_path_scoped` means the skill wakes itself when the relevant file is touched. A daily-use skill has the opposite problem — always-on ambient delivery wastes tokens on a capability the creator can trigger themselves. Frequency determines the correct ambient surface.

**Outputs:** `invocation_mode` passed to Step 9 ranking.

### Step 4 — APPLY_POLLUTION_TEST

**Reads:** `verb_family` + `continuity_bias` (from step 2). Does not read `intent_profile` directly.

**Decides:** would this capability's reasoning pollute the parent context if mixed with it?

| Verb family | Pollution risk | Required host axis |
|---|---|---|
| `advise_on_X` where the target IS the parent's current code | `pollutes` | Force `agent_spawn` host — isolation protects review integrity |
| `advise_on_X` where the target is external or orthogonal | `safe` | `session_root` allowed |
| `do_X` where the mutation is on shared state | `safe` (execution does not pollute) | `session_root` allowed |
| `coordinate_X` | `safe` (routing does not pollute) | `session_root` allowed |
| `observe_X` | `safe` (write-to-memory only) | — |
| `enforce_X` / `react_to_X` | depends on handler nature — defer to step 7 | — |

**The canonical pollution case.** An advisor reviewing the same code it is helping to write inherits the same justifications it produced. This is structural contamination, not a bug — it happens because both the reviewer and the author share one working memory. The fix is isolation: a code-review advisor is delivered via `invoked_task_spawn` so that its reasoning starts from the code as it exists on disk, not from the creator's in-progress rationale. Cell 4 `code_reviewer_agent` in the topology encodes exactly this.

**Outputs:** `pollution_risk` + host-axis override (when `pollutes`) passed to Step 8.

### Step 5 — APPLY_OUTPUT_TEST

**Reads:** `verb_family`. Does not read `intent_profile`.

**Decides:** what does the creator receive at the end — amplified reasoning inside their current thinking, or a structured report they read after?

| Verb family + context | Output shape | Vector bias |
|---|---|---|
| `advise_on_X` with continuity_bias=parent | `amplified_reasoning` | skill vector (cognitive or advisory) |
| `advise_on_X` with continuity_bias=isolated | `structured_report` | agent vector (adviser) |
| `do_X` | `structured_report` (completion summary) | agent vector (specialist) or skill (procedural) |
| `coordinate_X` | `structured_report` with handoff trail | squad vector |
| `observe_X` | `structured_report` to memory, no user output | hooks + observer nature |

**Why this is a distinct step from nature.** The output shape is downstream of verb but upstream of nature in a specific case: an advisor can deliver either amplified reasoning (skill) or a structured report (agent), and the difference is determined by continuity, not by the advisor-vs-executor split. Separating output shape from nature preserves the option.

**Outputs:** `output_shape` passed to Step 7 and Step 10.

### Step 6 — RESOLVE_DEPTH

**Reads:** `creator.intent_profile.maintenance_appetite` + `creator.intent_profile.domain_depth` + the current `verb_family`.

**Decides:** what cognitive depth does this capability warrant — procedural, advisory, or cognitive?

**Cap based on `maintenance_appetite`:**
- `fast_and_simple` → cap at `procedural` or `advisory`. Cognitive is denied; creator's maintenance band cannot sustain a 5-layer architecture.
- `balanced` → prefer `advisory`, allow `cognitive` if the next gate (justification) passes.
- `deep_and_slow` → allow `cognitive` if the domain warrants.

**Cognitive justification gate.** If the proposed depth is `cognitive`, the step requires three conditions before proceeding:

1. **Singularity markers** — at least 3 concrete markers specific to this cognition that distinguish it from a generic reasoning layer (named patterns of thought, declared failure modes, specific domain anchors).
2. **Named cognitive flow** — a 3-to-6 step cognitive sequence the mind actually runs when activated (not a vague "it thinks about X").
3. **Concrete reasoning patterns** — at least 3 patterns with specific triggers that fire inside the cognitive flow.

If any condition is missing, the step downgrades to `advisory` and records the downgrade with the missing condition named. The creator can override the downgrade by providing the missing material — the Engine's default is to refuse cognitive depth without justification, not to grant it and hope.

**`domain_depth` amplification.** When `domain_depth: deep`, the justification gate is slightly relaxed — deep-domain creators have the material to justify cognitive depth natively. When `foundational`, the gate is strictly enforced — foundational-depth creators are more likely to propose cognitive depth they cannot sustain.

**Outputs:** `depth` passed to Step 9.

### Step 7 — RESOLVE_NATURE

**Reads:** `verb_family` from Step 1. Does not read `intent_profile`.

**Decides:** the operational nature primitive from §2.2 of `references/intent-topology.md`.

| Verb family | Nature |
|---|---|
| `do_X` | `executor` |
| `advise_on_X` | `advisor` |
| `coordinate_X` | `orchestrator` |
| `observe_X` | `observer` |
| `enforce_X` | `executor` (hook-bound — host axis will be set by Step 8) |
| `react_to_X` | `executor` if the handler mutates, `observer` if write-to-memory only |

**Outputs:** `nature` passed to Step 8 and Step 9.

### Step 8 — DERIVE_HOST

**Reads:** `nature` (from Step 7), the delivery axis biases accumulated in Steps 2-4, and the host override from Step 4 if `pollution_risk == pollutes`.

**Decides:** the runtime host set, computed from the `(delivery, nature)` derivation table in `references/runtime-host-dag.md`. The host is never declared on the artifact — it is always derived here at decision time.

**Tie-breaking across multiple delivery candidates.** If Steps 2-4 left more than one valid delivery candidate (e.g., skill could be `ambient_path_scoped` or `invoked_slash_command`), Step 8 picks the primary based on the pollution test and invocation mode:
- If `pollution_risk == pollutes` → force `invoked_task_spawn` regardless of earlier biases.
- If `invocation_mode == needs_auto` → force `ambient_path_scoped`.
- Otherwise → pick `invoked_slash_command` as the primary with `ambient_path_scoped` as a secondary (the algorithm proposes both when appropriate, letting the creator choose).

**Outputs:** `host_set` and primary `delivery_mechanism` passed to Step 9.

### Step 9 — LOOKUP_CANONICAL_CELL

**Reads:** `delivery_mechanism`, `nature`, `depth`, plus `creator.intent_profile.target_audience` and `creator.intent_profile.usage_frequency_expectation` for ranking when multiple cells match.

**Decides:** which cell from `habitable_cells_v1` in `references/intent-topology.md` §4 matches the triple `(delivery, nature, depth)`.

**Match cases:**

| Match count | Action |
|---|---|
| 1 match | Use it. Proceed to Step 10. |
| 2+ matches | Rank by the two ranking fields. `marketplace_public` + `daily_multiple` ranks public-facing cells higher (`reasoning_skill_cognitive` over `procedural_skill` if both match). `personal_only` + `occasional` ranks personal cells higher. Proceed to Step 10 with the top-ranked cell + alternatives preserved for Step 10 proposal. |
| 0 matches | Fall through to the "don't know yet" branch: the legacy Q1/Q2/Q3 router in `.claude/skills/create/references/create-router.md` handles the request. Record `unroutable: true` + `unroutable_reason` in `intent_declaration` for post-hoc analysis. The creator is never blocked. |

**`unroutable_reason` is a closed enum with five values**, each pointing to a different remediation path:

| Value | Meaning | Signal for |
|---|---|---|
| `no_habitable_cell` | No v1 cell matches the `(delivery, nature, depth)` triple and no v2 cell either. Genuinely novel intent. | v2 candidate discovery |
| `v2_cell_deferred` | A v2 `hypothesized_cells_v2` entry matches the triple, but the cell is not in v1 scope yet. The creator is told which v2 cell matched and why it is deferred. | v2 → v1 promotion queue |
| `blocked_by_composition_gap` | The intent matches a v2 cell whose `blocked_by` field names an open composition gap (e.g., `GAP-COMPOSITION-1`). Remediation requires gap closure, not exemplar accumulation. | Gap closure prioritization |
| `ambiguous_between_cells` | 2+ cells match and the ranking fields did not break the tie (both cells return identical ranking scores). The algorithm offers the top 2 as alternatives in Step 10 and asks the creator to pick. | Ranking rule refinement |
| `explicit_legacy_router` | The creator voluntarily bypassed the 12-step walk by invoking `--legacy-router` OR by answering "I don't know yet" at Step 1. The forge is marked unroutable to preserve the bypass signal, but the reason is volitional, not a walk failure. These forges contribute to the legacy-usage frequency signal — high rates here indicate creators trust the legacy tree over discovery mode, which is a UX signal distinct from topology gaps. | Discovery mode UX calibration |

**Why fall-through, not failure.** Discovery mode is not a gate — it is an amplifier. When the algorithm cannot route cleanly, the creator still gets a product, via the existing router. Over time, the `unroutable` markers accumulate in `decisions_history` with their specific `unroutable_reason`, and the distribution drives different improvement paths: high `no_habitable_cell` rates signal new cell candidates; high `v2_cell_deferred` rates signal promotion priority; high `blocked_by_composition_gap` rates signal which gaps to fix first; high `ambiguous_between_cells` rates signal ranking rule refinement. The fall-through is not just a safety valve — it is the longitudinal learning signal.

**Outputs:** `matched_cell` + `ranked_alternatives` (up to 2) passed to Step 10.

### Step 10 — PROPOSE_FORM

**Reads:** `matched_cell`, `ranked_alternatives`, plus `creator.intent_profile.target_audience`, `creator.intent_profile.licensing_tolerance` (only if the matched cell is `apex_cognitive_mind` and the creator has expressed interest in the genius sub-type), `creator.intent_profile.external_dependency_tolerance` (for tool pool defaults).

**Decides:** the final form proposal shown to the creator. Format is fixed:

```
Proposed form: <canonical_form from matched_cell>
Rationale: <one sentence naming the discriminators that produced the match>
Alternatives: <up to 2 alternatives, each with one-line reason to prefer it>
Override: <one line reminding the creator they can pick a different form if they disagree>
```

**Invisibility audit.** If `target_audience` is `marketplace_public` or `hybrid`, the proposed form passes through the invisibility check (substrate vocabulary, author names, internal acronyms must not leak into the creator-facing description). This is the same discipline enforced by `scripts/codex-drift-check.py INVISIBILITY_PATTERN`, applied at proposal time to catch violations before the creator sees them.

**Genius-library filter.** If the matched cell is `apex_cognitive_mind` and the creator's intent mentions a genius sub-type candidate (by descriptor, never by name), `licensing_tolerance` filters the proposal: `conservative_own_only` → only the creator's own profiles. `moderate_public_domain` → public-domain profiles only. `permissive_all` → full library available.

**Tool pool defaults.** `external_dependency_tolerance` sets the default tool pool for the forged product: `isolated_no_deps` → no MCP references, no external API calls in scaffolding. `trusted_deps_only` → allow known-stable MCPs. `permissive_all` → full defaults. The creator can override at `/fill` time.

**Outputs:** `proposal` block (form + rationale + alternatives + override affordance) shown to the creator.

### Step 11 — RECORD_DECISION

**Reads:** all prior step outputs.

**Writes:** a single `intent_declaration` block to the product's `.meta.yaml`.

```yaml
intent_declaration:
  captured_at: <ISO>
  creator_said: <verbatim intent text, or "(express mode)">
  mode: express | guided | legacy_fallback  # legacy_fallback covers forges routed via the Section 1 legacy router
  mode_switches: []  # appended via §5 transition protocol (never populated in legacy_fallback mode)
  language: <detected language code, e.g., en, pt-BR — used for announcements>
  scout_source: null | <relative path to workspace/scout-{slug}.md if a scout report informed this decision>
  engine_parsed:
    verb_family: <from step 1>
    continuity_bias: <from step 2>
    invocation_mode: <from step 3>
    pollution_risk: <from step 4>
    output_shape: <from step 5>
    depth: <from step 6>
    nature: <from step 7>
    delivery_mechanism: <from step 8 primary>
    host_set: <from step 8>
  matched_cell: <cell_id from step 9, or null if unroutable>
  ranked_alternatives: [<cell_id>, <cell_id>]
  proposed_form: <canonical_form from step 10, or null if unroutable>
  unroutable: false | true
  unroutable_reason: null | no_habitable_cell | v2_cell_deferred | blocked_by_composition_gap | ambiguous_between_cells | explicit_legacy_router
  unroutable_gap_id: null | <gap id string when unroutable_reason == blocked_by_composition_gap>
  creator_choice: accepted | overridden
  override_to: null | <creator's chosen form>
  override_reason: null | <creator's explanation>
  discriminators_applied: [continuity, invocation, pollution, output, depth]
  defaults_applied: [<field_name>, ...]  # any intent_profile field that fell back to default
```

**Schema compatibility with `engine-proactive.md` §15.** The `scout_source` field is the contract point between this schema and the Engine's proactive intelligence layer. `engine-proactive.md` §15 (fill-without-scout gap warning) reads `.meta.yaml` and checks for `scout_source` to decide whether to surface the intelligence-gap warning. By declaring the field explicitly here, discovery-mode `/create` stays compatible with the existing proactive contract without silent drift. When `scout_source` is null, the proactive layer fires its SOFT or DIRECT framing depending on creator experience; when present, the warning is suppressed because research already happened.

**Why this record exists.** Three consumers read it downstream: (a) `/validate` Stage 0 Intent Coherence reads `matched_cell` and verifies the forged product still adheres to the declared cell; (b) `decisions_history` in `STATE.yaml` appends a reference to this block for longitudinal calibration; (c) post-hoc auditing reads `defaults_applied` to detect patterns in missing-field fallbacks. Without this record, the Engine's reasoning evaporates after forge and cannot be audited.

### Step 12 — APPEND_TO_HISTORY

**Reads:** the `intent_declaration` from Step 11.

**Writes:** a new entry to `STATE.yaml decisions_history`, the longitudinal record defined in §6 below.

**Execution guarantee.** Steps 11 and 12 are the last two steps of the algorithm for one reason: source fidelity. If either write fails, the entire algorithm's output is lost. They run in order, not in parallel, and the algorithm does not report "forge ready" until both writes succeed. This encodes Clause I (Source Fidelity) at the implementation layer.

---

## §4 — Express vs Guided: The Dual Mode

The 12-step algorithm is Guided mode. Express mode bypasses it. Both modes produce the same `intent_declaration` schema — the difference is where the Engine's intelligence operates: at the front (Guided) or at the back (Express).

### §4.1 — Express Mode

**Trigger:** `creator.profile.technical_level ∈ {advanced, expert}` AND `creator.preferences.workflow_style == autonomous`. Both conditions must hold. If only one holds, Guided mode runs.

**Flow:**

```
/create <type> <slug> [--<sub_type>]
```

The creator names the form directly via sub-command. The Engine does not walk the 12 steps. Intent parsing is replaced by defaults: `verb_family` is inferred from the type, `continuity_bias` comes from the type's default delivery, `depth` comes from the `--<sub_type>` flag if present, and so on. The `intent_declaration` written at Step 11 records `creator_said: "(express mode)"` and `mode: express`.

**Back-of-flow intelligence.** Express mode does not skip intelligence — it relocates it. The `/validate` pipeline includes Stage 0 Intent Coherence which reads the Express `intent_declaration` and verifies that the forged product still adheres to the type + sub-type the creator declared. If the scaffolded files drift from the declaration (e.g., a `--procedural` skill gains cognitive-depth markers during `/fill`), Stage 0 surfaces the drift as a coherence warning. Stage 0 is advisory, not blocking — Express creators are trusted to know what they are doing, but the Engine still checks.

**Why Express exists.** Advanced creators resent being asked questions they already know the answer to. Forcing them through 12 steps every time degrades ergonomics and the tool loses their trust. Express respects their autonomy; the back-stage coherence check preserves quality.

### §4.2 — Guided Mode

**Trigger:** `creator.profile.technical_level ∈ {beginner, intermediate}` OR `creator.preferences.workflow_style == guided`. Either condition suffices.

**Flow:** full 12-step algorithm as declared in §3. Discovery questions ask the creator to clarify ambiguity at natural gates (Step 1 on ambiguous verb, Step 6 on cognitive justification). The Engine never asks more than one question per gate — a second question in the same gate is a protocol violation and indicates the gate needs redesign, not more interrogation.

**Front-of-flow intelligence.** Guided mode runs the full algorithm before scaffolding. By the time the creator confirms the proposal at Step 10, every decision has been made and recorded. `/fill` inherits a fully-reasoned `intent_declaration` and has nothing to second-guess.

### §4.3 — Both Modes Share One Data Contract

The same `intent_declaration` schema is written by both modes. The same `decisions_history` append happens. The same Stage 0 validation runs. The dual mode is not two systems — it is one system with two entry points that converge on a single data contract. This is the non-negotiable structural discipline: if the two modes diverged in their output, the Engine would have two populations of products with incompatible metadata, and longitudinal calibration would degrade asymmetrically.

---

## §5 — Transition Protocol: Mid-Session Mode Switching

The dual mode trigger in §4 fires once, at the start of `/create`. In real use, 30-40% of sessions are mixed: a creator starts in Express and hesitates, or starts in Guided and accelerates. Without a declared transition protocol, the implementation would invent behavior ad-hoc — which is the exact failure mode discovery mode exists to eliminate. This section declares the protocol.

### §5.1 — Rule 1: Express → Guided Escalation

**Triggers (any one suffices). Triggers are language-aware: the Engine matches the creator's expressive register in both English and Portuguese (and mirrors any additional language the creator uses via `creator.yaml language:`).**

- **(a) WH-question during Express flow** — the creator types a clarifying question instead of confirming.
  - English: *"what does cognitive mean?"*, *"which one is the discovery mode?"*, *"wait — what's the difference?"*
  - Portuguese: *"o que significa cognitivo?"*, *"qual é a diferença?"*, *"espera — o que isso quer dizer?"*, *"como assim?"*
- **(b) Explicit hesitation markers** — the creator emits a recognized hesitation phrase.
  - English: *"I'm not sure"*, *"let me think"*, *"hmm"*, *"actually..."*, *"maybe not"*
  - Portuguese: *"não tenho certeza"*, *"deixa eu pensar"*, *"hmm"*, *"na verdade..."*, *"pera"*, *"espera aí"*, *"acho que não"*, *"não sei não"*
- **(c) Double rejection** — the creator rejects the Express default proposal twice in a row.
  - English: two sequential `no`, `not that one`, `wrong`, `that's not it`
  - Portuguese: two sequential `não`, `esse não`, `errado`, `não é isso`, `nem é esse`

**Language detection source.** The Engine reads `creator.yaml language:` if present; otherwise it mirrors the language of the last 3 creator messages. Both trigger sets are active simultaneously — the creator may code-switch mid-session without losing transition coverage.

**Action:** drop from Express to Guided mode starting at the current decision gate. Do not re-run discovery from Step 1 — preserve what the creator already confirmed. Re-run from the failed gate forward. The transition is announced in one line, in the creator's language:
- English: *"Switching to guided discovery — I'll walk through the remaining decisions with you."*
- Portuguese: *"Mudando para modo guiado — vou passar pelas decisões restantes com você."*

**Recording:** a `mode_switch` entry is appended to the `intent_declaration`:

```yaml
mode_switch:
  from: express
  to: guided
  trigger: wh_question | hesitation_marker | double_rejection
  at_step: <1-12>
  at_time: <ISO>
```

### §5.2 — Rule 2: Guided → Express Shortcut

**Triggers (any one suffices).**

- **(a) Explicit override** — the creator types a command-style escape.
  - Command flags: `--express`, `--autonomous` (language-agnostic)
  - English: *"just pick"*, *"skip the questions"*, *"stop asking"*, *"you choose"*, *"whatever you think"*
  - Portuguese: *"pode escolher"*, *"pula as perguntas"*, *"para de perguntar"*, *"você decide"*, *"tanto faz"*, *"o que você achar"*
- **(b) Fluency detection** — the creator completes 2 consecutive Guided gates without any hesitation signal AND has `creator.profile.technical_level ∈ {advanced, expert}`. The Engine infers the creator is ready to accelerate.

**Action:** skip remaining Guided gates for the current product. Apply Express defaults for every remaining step. Announce the transition in one line, in the creator's language:
- English: *"Got it — I'll move faster from here. Finalizing your proposal now."*
- Portuguese: *"Entendi — vou acelerar daqui. Finalizando sua proposta agora."*

**Recording:** a `mode_switch` entry with `from: guided, to: express, trigger: explicit_override | fluency_detected`.

### §5.3 — Protocol Invariants

Three invariants prevent the transition protocol from degrading into chaos.

1. **At most 2 mode switches per product.** A single `/create` run can have at most two switches (A→B→A). More than 2 switches indicates confusion the protocol cannot resolve — the Engine escalates to a direct question: *"Would you like to start over, or continue with your current choices?"* The creator's answer is final.

2. **Transitions are never silent.** Every switch is announced in exactly one line before continuing, in the creator's own language (detected from `creator.yaml language:` or from recent conversation). The creator always knows what the Engine is doing, in words they would use themselves. Silent mode switching is a trust violation and is explicitly forbidden.

3. **The schema is the same across modes.** A product created in Guided mode, switched to Express at Step 8, then switched back to Guided at Step 10, writes one `intent_declaration` with a `mode_switch` array of 2 entries. The field structure is identical — the array is the only place that grows.

### §5.4 — Trigger Calibration

The exact trigger phrasings in §5.1 and §5.2 are initial calibration, not final. The protocol runs against real creator sessions and iterates the trigger list — specifically, the "fluency detection" heuristic in Rule 2b (two consecutive gates without hesitation) may prove too aggressive or too conservative in practice. The **presence** of the protocol is non-negotiable; the **exact triggers** are refined against observed sessions and fed back into this document via explicit edit, never silent drift.

---

## §6 — Longitudinal Feedback Loop

The feedback loop is how the Engine calibrates its own confidence over time. Every `/create` decision is recorded; every forge outcome is captured; every retrospective verdict accumulates evidence about whether the Engine's proposals match creator intent in practice. Without this loop, the Engine ships the same proposal quality forever. With it, the Engine improves asymmetrically — it gets better at the cells it sees often and remains humble about the cells it sees rarely.

### §6.1 — `decisions_history` Schema (extension to `STATE.yaml`)

```yaml
decisions_history:
  - date: <ISO>
    slug: <product_slug>
    creator_intent: <verbatim intent text, or "(express mode)", or "(legacy router menu)">
    mode: express | guided | legacy_fallback
    mode_switches: [<mode_switch entries from §5>]
    scout_source: null | <path to workspace/scout-*.md if a scout report grounded this decision>
    engine_proposal:
      cell_id: <matched cell from topology §4, or null if unroutable>
      form: <canonical_form, or null if unroutable>
      rationale: <one sentence>
      alternatives: [<cell_id>, <cell_id>]
    unroutable: false | true
    unroutable_reason: null | no_habitable_cell | v2_cell_deferred | blocked_by_composition_gap | ambiguous_between_cells | explicit_legacy_router
    unroutable_gap_id: null | <gap id string when unroutable_reason == blocked_by_composition_gap, e.g., GAP-COMPOSITION-1>
    creator_choice: accepted | overridden
    override_to: null | <creator's chosen form>
    override_reason: null | <creator's explanation>
    forge_completed: true | false
    published: true | false
    outcome_30d:
      install_count: null | integer
      user_rating: null | float
      creator_self_uses: null | boolean
      reported_issues: []
    retrospective_verdict: null | correct | wrong_form | wrong_depth | wrong_cell
    retrospective_captured_at: null | <ISO>
```

### §6.2 — Loop Closure Points

The loop has five closure points — moments where the Engine reads or writes a `decisions_history` entry during the normal pipeline.

1. **`/create` completion** — initial entry written (Step 12 of the algorithm).
2. **`/validate` completion** — `forge_completed` field updated.
3. **`/publish` completion** — `published` field updated. For unpublished products, the entry remains but `outcome_30d` stays null.
4. **30 days post-publish** — the `/status` dashboard detects an entry with `published: true` and `published_at >= 30_days_ago` and no `retrospective_verdict`, and prompts the creator: *"You published `{slug}` 30 days ago. Looking back — did the form match what you actually needed? (correct / wrong_form / wrong_depth / wrong_cell)"*. The creator's answer fills `retrospective_verdict`.
5. **Next `/create` invocation** — `decisions_history` is read as prior for proposal ranking (Step 9 uses it to weight cells that have accumulated `correct` verdicts higher).

### §6.3 — Engine Confidence Calibration

The Engine reads its own `decisions_history` and sets the tone and offering shape of future proposals based on accumulated evidence.

| Accumulated state | Engine confidence | Tone + offer shape |
|---|---|---|
| ≥5 entries with `retrospective_verdict: correct` | HIGH | Assertive: *"Based on your pattern, this is a skill."* + 1 alternative |
| ≥3 entries with any `wrong_*` verdict | MODERATE | Humble: *"I've proposed wrong forms for you a few times — let me show you alternatives."* + 3 alternatives + explicit prompt: *"Can you tell me what made the previous proposals wrong? I'll use that to calibrate."* |
| <3 entries with any retrospective verdict captured | LOW | Learning: *"I'm still learning your patterns."* + 2-3 alternatives equally weighted + no assertive framing |

**Per-creator, not per-Engine.** The calibration is read per-creator from their own `decisions_history`. Two creators on the same version of the Engine get different tones based on their own forge histories. This is how the Engine adapts to individual creators without requiring individual configuration.

**Calibration caps.** HIGH confidence never eliminates the "override" affordance in Step 10 — the creator always retains the ability to reject the proposal. Even at HIGH confidence, the proposal is a suggestion, not a command. This is the non-negotiable application of Engine Clause II (Separation of Production and Judgment): the `/create` skill proposes; the creator decides; the two authorities never collapse into one.

### §6.4 — Promotion Signal for v2 → v1 Cell Promotion

The `decisions_history` also feeds the promotion path for `hypothesized_cells_v2` → `habitable_cells_v1`. A v2 cell is a candidate for promotion when at least three entries exist where the creator's intent would have routed to that v2 cell cleanly, the creator accepted the legacy-router fallback, and the forged product was published with a `correct` retrospective verdict. Three such entries constitute empirical grounding — the cell moves from hypothesis to habitable, is added to `references/intent-topology.md` §4 via explicit wave (not silent edit), and becomes part of the regression test surface. Promotion is additive and safe.

---

## §7 — Implementation Contracts

This section declares the non-negotiable contracts the `.claude/skills/create/` implementation honors when executing this algorithm. Each contract is the invariant a downstream consumer relies on; violating one regresses the algorithm and every consumer that reads its output.

### Contract C1 — Afferent reads via explicit path

Every step that reads an `intent_profile` field reads it via the explicit path `creator.intent_profile.{field}`. Inference is forbidden — either the field is present, or the declared default applies. Post-hoc auditing depends on the `defaults_applied` marker in `intent_declaration`; that marker is reliable only if reads are explicit.

### Contract C2 — Derivation steps declared as derived

Steps 4, 5, 7, 8 do not read `intent_profile`. Their wiring in §2 is marked *derived*, and implementation must preserve that marker. A derivation step that silently starts reading an `intent_profile` field drifts the afferent wiring and breaks the auditability the table guarantees.

### Contract C3 — Host never declared

Step 8 computes the host from the derivation table in `references/runtime-host-dag.md`. The result is not written to the artifact. No forged product declares a `host` field. This is the operational form of the vestigial-organ elimination from the topology.

### Contract C4 — Unroutable fall-through is a feature

Step 9 returning zero matches is not a failure. The algorithm falls through to the legacy Q1/Q2/Q3 router and records `unroutable: true` in the `intent_declaration`. The implementation never blocks the creator on zero matches — it always produces a path forward, even if that path is the legacy router.

### Contract C5 — Stage 11 and Stage 12 are atomic

The two write steps at the end of the algorithm are atomic in the sense that the algorithm does not report `forge_ready` until both writes succeed. If either fails, the algorithm rolls back to the proposal state and reports the failure with remediation. Source fidelity depends on this — a forge that proceeds without the `intent_declaration` written is a forge without memory.

### Contract C6 — Dual-mode data contract identical

Express and Guided modes write the same `intent_declaration` fields. The only mode-specific field is `mode` itself and the optional `mode_switch` array. Every other field is populated in both modes — in Express, populated from defaults; in Guided, populated from the algorithm. A product whose `intent_declaration` is missing fields because it was created in Express is a contract violation and is caught by the regression suite.

### Contract C7 — Transition protocol announces every switch

Every `mode_switch` entry in `intent_declaration.mode_switches` corresponds to exactly one visible announcement in the session output. Silent switches are forbidden. The regression suite verifies the invariant: for every `mode_switch` entry, the session transcript contains the corresponding announcement line.

### Contract C8 — Confidence calibration reads only the creator's own history

`decisions_history` is per-`STATE.yaml`, which is per-workspace (for the Engine, that means per-creator). Cross-creator calibration is forbidden — the Engine does not aggregate history across creators to influence a specific creator's proposals. This is both a privacy discipline and a correctness discipline: what works for one creator's domain may be wrong for another's.

### Contract C9 — Null-safe schema population across modes

Every field in the `intent_declaration` schema is populated on every forge, regardless of mode. Fields that are not applicable in the current mode are populated with `null` (for single-value fields) or `[]` (for list-valued fields) — never omitted. Specifically: `mode_switches` is `[]` in Express mode unless a transition fired; `unroutable` is `false` in the happy path; `unroutable_reason` and `unroutable_gap_id` are `null` unless `unroutable == true`; `scout_source` is `null` when no scout report was read. This null-safe discipline protects downstream consumers — `/validate` Stage 0, `/status` dashboard, `decisions_history` calibration — from having to distinguish "field absent" from "field null". The schema is always structurally complete.

### Contract C10 — Language mirrors creator throughout the protocol

The `language` field recorded at Step 11 is used by every announcement in the transition protocol (§5), by the proposal phrasing in Step 10, and by the cognitive-justification downgrade explanation in Step 6. The creator never sees English text when they are interacting in Portuguese, and never sees Portuguese text when they are interacting in English. If the creator code-switches mid-session, the Engine mirrors the last 3 messages' dominant language. Language is a first-class axis of voice, not a translation layer after the fact — phrases are composed in the target language, not translated from English.

---

**Status.** Canonical substrate, v1. Read in conjunction with `references/intent-topology.md` (axes, host derivation, cells) and `references/skill-vs-agent-discriminators.md` (discriminator details). Changes to this document regress the algorithm and every downstream consumer — edits require an explicit decision, not a drive-by cleanup.
