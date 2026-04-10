# Self-Clone Forge Protocol

> **Layer:** canonical substrate. Consumed by `product-dna/minds.yaml` mind_forge_schema.A12_self_clone_elicitation_protocol, by `/fill` via the content pack at `references/fill-content-packs/self-clone.md`, and by `/validate` stage 7b cognitive fidelity scoring when evaluating a cognitive mind whose origin is artificial with `source_corpus.human_referents = [creator_self]`.
>
> **Binding disciplines inherited:** Clause I (Source Fidelity), Clause II (Separation of Production and Judgment), Clause IV (Named Trade-Offs), Clause V (Rigor > Ergonomics), Clause VIII (Every Token Earns Its Place). Principle P7 (Read Before Write ≥2:1), P8 (Invisibility of Mechanism), P9 (Recursive Integrity). The marketplace taxonomy is unchanged — this document refines one operational protocol of the mind codex, nothing else.

---

## §1 — What SELF-CLONE Is

SELF-CLONE is a guided protocol a creator runs against themselves, via the `/fill` skill walker when `sub_type=self`, to produce an installable cognitive mind whose `origin` is derived mechanically as `artificial` with `source_corpus.human_referents = [creator_self]`.

The protocol exists to fill an operational gap: `product-dna/minds.yaml` at `cognitive_sub_types.self` declares that cognitive minds of the SELF sub-type require elicitation with the creator as the primary source, but no operator existed to perform the elicitation. SELF-CLONE is that operator.

### §1.1 — Two modes

The protocol operates in two modes, selected mechanically by corpus density at the start of the walker:

**Distillation mode** triggers when the creator has ≥ three published or sealed Engine artifacts (skills, handoffs, substrate documents, or equivalent) totaling ≥ 20,000 tokens of documented work. The walker first reads the available artifacts and extracts first-draft proposals for the eight dimensional targets mechanically. Elicitation runs only on dimensions where distillation confidence falls below 0.7 (mapping to the `inferred` provenance tag). Typical gap-question count: 15 to 25.

**Elicitation mode** triggers when the distillation threshold is not met. The walker runs the full structured elicitation protocol across all eight dimensions. Typical question count: 10 to 15 at Tier Functional, 50 to 75 at Tier High, 100+ at Tier Excellence.

### §1.2 — Mode-selection rule

The mode is determined by a mechanical check at walker startup:

```
if creator_corpus_tokens >= 20_000 and creator_artifact_count >= 3:
    mode = distillation
else:
    mode = elicitation
```

The mode is recorded in the product's `.meta.yaml` under `self_clone_mode: distillation | elicitation` for auditing and for the adversarial reader gate at seal time.

### §1.3 — Reconciliation with declared elicitation range

`cognitive_sub_types.self.elicitation_questions_range: "10-15"` in the codex is the cold-creator Tier Functional case. The full protocol's 100+ questions is the cold-creator Tier Excellence case. The distillation mode's 15-25 gap questions is the high-corpus-creator case across any tier. The three cases coexist; the mode-selection rule decides which fires. A reader of both the codex field and this protocol sees the rule that reconciles the numbers, not a contradiction.

### §1.4 — What SELF-CLONE is not

SELF-CLONE is not a personality test. It does not diagnose the creator against a taxonomy. Typology probes run only at the end as retrospective mirrors the creator can recognize or refuse — never as canonical input.

SELF-CLONE is not a replacement for `/map`, `/create`, or `/fill`. It composes with each: `/create` routes the creator into the self sub-type and scaffolds; `/fill` loads the content pack when `sub_type=self` is detected; `/map` continues to extract domain knowledge on a separate axis.

SELF-CLONE is not a guarantee of fidelity. The clone is a high-fidelity approximation captured through eight dimensional axes. It explicitly does not capture: bodily intuition, unarticulated pattern recognition, cross-context judgment that depends on lived experience the creator cannot render in writing. The honesty floor gates make this non-capture mechanical, not rhetorical.

---

## §2 — Origin Contract

SELF-CLONE produces an artificial-origin mind. The origin derivation fires mechanically at `/validate --level=3`:

- `source_corpus.human_referents = [creator_self]` — length ≥ 1
- `source_ingestion.mode = extraction_from_documents` (distillation mode) or `extraction_from_elicitation` (elicitation mode)
- `design_starting_point = null` — the starting point is not a declared purpose; it is a documented human

The origin is `artificial` by derivation rule. A SELF-CLONE product that declares `origin: synthetic` fails validation with `origin_contradiction` error.

The creator's licensing position is clean: `licensing: "Creator owns the persona — no third-party attribution issues."` This is inherited directly from the `cognitive_sub_types.self` declaration.

---

## §3 — Seven-Layer Target

SELF-CLONE populates the eight dimensional target counts declared in `product-dna/minds.yaml` mind_forge_schema.A6_artificial_mind_schema.dimensional_profile:

| # | Dimensional target | Minimum | Ideal | Criticality |
|---|---|---|---|---|
| 1 | distinctive_terms | ≥ 50 | 100 | foundation |
| 2 | recurring_metaphors | ≥ 20 | 40 | foundation |
| 3 | master_mental_models | 3 | 5 | critical |
| 4 | inviolable_values | 5 | 7 | critical (floor 0.90) |
| 5 | core_obsessions | 3 | 5 | critical |
| 6 | productive_paradoxes | 3 | 5 | critical (floor 0.80) |
| 7 | unique_sensors | ≥ 10 | 20 | foundation |
| 8 | decision_signatures | ≥ 5 | 10 | critical |

The eight targets map to the extraction-depth eight-layer alternative decomposition (variant B) documented in `references/structural-dna/cognitive-architecture-variants.md` §4. Variant B is the operational path; the canonical seven-layer architecture is the sealed target. The translation table in §4.2 of the variants document maps every variant B layer back to the canonical layers and strands.

SELF-CLONE does not redefine the eight dimensions or the target counts. It populates them. The eight counts are the contract.

---

## §4 — Ordered Elicitation

### §4.1 — Ordering principle

Every dimensional target follows a three-phase ordering within its elicitation block:

1. **Phase I — Instances**: concrete, specific, anchored to real situations with timestamps where possible. The first thing the creator sees is a request for direct observable content, not a request for a pattern.
2. **Phase II — Pattern**: the invariant across the instances. The creator abstracts from their own data, not from a prompt.
3. **Phase III — Counter-proof**: the removal test inverted. The creator names a concrete situation where the pattern would fail to predict their behavior. This is honesty floor gate 1 integrated into the question flow.

Questions at each phase expand per tier. Tier Functional: one question per phase (3 per dimension). Tier High: two to three per phase (6-9 per dimension). Tier Excellence: four to five per phase (12-15 per dimension) plus the three-day delay reconciliation.

### §4.2 — Mode tagging

Every question in the content pack carries a mode tag:

- **DIST** — distillation reading (the walker reads creator artifacts and answers mechanically)
- **ELIC** — creator elicitation (the walker asks the creator directly)
- **BOTH** — distillation first, then elicitation for confirmation or gap-filling

In distillation mode, DIST questions fire first. ELIC questions fire only on dimensions where distillation confidence < 0.7. BOTH questions fire distillation first; if distillation confidence ≥ 0.7, the creator confirms or refines the draft without answering the full elicitation question.

### §4.3 — Behavioral manifestation binding

Every question targeting a critical-layer dimension (master mental models, inviolable values, core obsessions, productive paradoxes, decision signatures) carries the behavioral manifestation requirement inherited from `mind_forge_schema.A5_behavioral_manifestation_requirement`:

- Observable signal declared
- "Would do X, would not do Y" pair present
- At least one concrete example anchored to a verifiable situation

Vague language ("strategically", "effectively", "with rigor", "thoughtfully") without a paired concrete behavior blocks the validation gate. The walker enforces this at question time by requiring concrete instances before accepting an answer.

### §4.4 — Stopping rules per dimension

**Foundation-tier dimensions** (distinctive_terms, recurring_metaphors, unique_sensors): stop at the minimum count with at least 60% at confidence ≥ 0.7, or at the ideal count with at least 40% at confidence ≥ 0.8, whichever comes first.

**Critical-tier dimensions with 0.80 floor** (productive_paradoxes): stop only when the minimum count is met AND every entry passes the behavioral manifestation requirement AND every entry has a named counter-proof.

**Critical-tier dimensions with 0.90 floor** (inviolable_values): same as 0.80 floor but additionally requires at least one entry to pass the three-day delay rule with discrepancy < 30%. If the three-day delay cannot run in the session window, the dimension is tagged `pending_delay_verification` and the clone ships at Tier High instead of Tier Excellence.

The walker computes the count and the confidence distribution after each answer and reports to the creator: "dimension X is at Y% of target, next question addresses Z."

---

## §5 — Typology Probe

Typology probes (DISC, Enneagram, MBTI, or other frameworks the creator may know) run exclusively at the end of the elicitation, after all eight dimensions are populated. They are retrospective mirrors, not diagnostic instruments.

### §5.1 — Three-step mirror protocol

**Step 1 — Surface the clustered pattern in the creator's own words.** The walker synthesizes a short paragraph summarizing the populated dimensions: the decision signature cluster, the value emphasis, the recurring metaphor source domains, the core obsessions, the productive paradox pattern. The summary uses the creator's own vocabulary extracted during elicitation — no typology language yet.

**Step 2 — Offer the typology vocabulary as optional language.** The walker presents: "Some creators recognize a pattern like this in the language of one or more personality typologies. Would you like to see the closest match in any of these vocabularies? Your answer becomes part of your cognitive profile; it is not a diagnosis of you."

Three options:
- **Yes, show me** — walker presents the closest match using its own pattern recognition. No scoring algorithm is imported.
- **No, skip** — walker records `typology_preference: refused` and proceeds to close.
- **Unfamiliar** — walker records `typology_preference: unfamiliar` and proceeds.

**Step 3 — Record the response as a signal.** Whatever the creator chose becomes a dimension in the final cognitive profile: `typology_recognition: {typology, label, reaction}`. Recognition says "the creator narrates themselves in this language" — which is itself a cognitive signature. Refusal says the opposite. Both are data.

### §5.2 — Why this ordering

Typology at the start of the protocol is anchoring bias. "I am INTJ, therefore strategic" produces inflated responses downstream. The creator narrates in typology language, and the walker captures typology-filtered self-report rather than underlying cognition.

Typology at the end is a falsification instrument. The dimensions are already populated from direct observation (artifacts + elicitation + counter-proofs). The typology probe then asks whether the creator recognizes themselves in an external vocabulary — and whichever way they answer becomes data about their relationship to the vocabulary, not about the vocabulary being ground truth.

---

## §6 — Reverse Engineering (Distillation Mode)

### §6.1 — The principle

Distillation mode reads the creator's existing corpus and extracts first-draft populated dimensions mechanically before any elicitation runs. The creator's documented work is the riverbed; their current self-report is the water. The riverbed remembers what the water forgets.

### §6.2 — Distillation procedure per dimension

For each of the eight dimensional targets, distillation executes a specific mechanical procedure. The procedures read the creator's corpus and produce a first-draft populated dimension with a confidence score.

**distinctive_terms**: Tokenize the corpus, compute frequency distribution against baseline English, extract words and phrases with frequency ≥ 5× baseline. Tag domain-specific terms separately. Present the top 50-100 for creator confirmation. Confidence ≥ 0.8 when ≥ 50 high-frequency terms extracted.

**recurring_metaphors**: Scan for cross-domain analogy patterns, group by source domain, retain source domains appearing in ≥ 2 independent documents. Confidence ≥ 0.8 when ≥ 20 distinct analogies in ≥ 4 source domains across ≥ 3 documents.

**master_mental_models**: Scan for reasoning chains from problem to conclusion, abstract to structural frame, cluster by similarity, retain clusters with ≥ 3 independent instances across ≥ 2 domains. Confidence ≥ 0.7 when 3-5 frames extracted with clear cross-domain presence.

**inviolable_values**: Scan for decisions where the creator paid a visible cost rather than taking a shortcut. Cluster principles across decisions. Retain clusters with ≥ 3 costly decisions across independent contexts. Confidence ≥ 0.7 when ≥ 5 principles extracted with cost-paid evidence.

**core_obsessions**: Scan for question-shaped constructions, cluster by topic and shape, retain clusters with ≥ 3 independent instances across at least a six-month span. Confidence ≥ 0.7 when 3-5 questions extracted with sustained presence.

**productive_paradoxes**: Scan for passages where two claims are held in tension without resolution. Retain tensions appearing in ≥ 3 passages. Confidence ≥ 0.7 when ≥ 3 tensions extracted with clear non-resolution structure.

**unique_sensors**: Scan for observations the creator flagged as important. Cross-reference with what practitioners in the same context typically flag. Retain creator-specific observations. Confidence ≥ 0.7 when ≥ 10 creator-specific observations extracted.

**decision_signatures**: Scan for decision points where a named alternative was visible. Identify the chosen path, the alternative, and the trade-off. Cluster by characteristic pattern. Confidence ≥ 0.7 when ≥ 5 patterns extracted with clear trade-off reconstruction.

### §6.3 — Creator's three options on each distilled draft

After distillation produces a first-draft populated dimension, the creator sees the draft and chooses one of three responses per entry:

1. **Confirm** — the distillation is accurate. Entry marked `confirmed`.
2. **Refine** — close but needs edit. Creator overwrites with their version. Entry marked `confirmed`.
3. **Reject** — wrong or does not capture the creator. Entry removed. Elicitation question fires to fill the gap.

The distillation does not force acceptance. The creator always has final say. The value of distillation is that most entries are confirmed or refined in seconds, leaving elicitation budget for the dimensions distillation could not reach.

---

## §7 — Dimensional Routing

### §7.1 — The routing problem

Many elicited features belong to multiple dimensions. A decision pattern that reveals a value, applies a mental model, and fires a sensor is not uniquely assignable to one target count. Naive single-tag routing causes double-counting or underreporting.

### §7.2 — Primary-plus-secondary tagging

Every elicited feature carries one primary dimensional tag (the dimension where the feature's behavioral manifestation is most strongly observable) and up to two secondary dimensional tags.

**Weight distribution:**
- Primary tag: 1.0 contribution to the primary dimension's target count
- Each secondary tag: 0.5 contribution to the secondary dimension's target count
- Maximum total contribution per feature: 1.0 + 2 × 0.5 = 2.0, allocated across up to three dimensions

### §7.3 — Determining the primary tag

The primary tag is determined by answering: "in which dimension is the feature's behavioral manifestation most directly observable?"

- Rule for choosing under specified conditions → `decision_signatures`
- Lens applied to filter a problem → `master_mental_models`
- Commitment defended under cost → `inviolable_values`
- Recurring question the creator cannot stop asking → `core_obsessions`
- Tension held without resolution → `productive_paradoxes`
- Observation the creator reads from specific cues → `unique_sensors`
- Characteristic word or phrase → `distinctive_terms`
- Cross-domain analogy → `recurring_metaphors`

A feature that could be primary in three or more dimensions is probably a composite — split it into separate features, one per dimension.

### §7.4 — Critical-layer counting rule

Critical-layer dimensions (values, paradoxes, singularity equivalents) apply the stopping rule only to primary tags. Secondary contributions do not count toward the critical-layer floor. The critical-layer floor is about the strength of direct behavioral manifestation, and secondary tags are by definition not the strongest manifestation.

---

## §8 — Integration with Primitives

SELF-CLONE composes with seven Engine primitives without modifying any:

### §8.1 — `cognitive_sub_types.self`

SELF-CLONE is the operator that fills the `requires_elicitation: true` declaration. The 10-15 question range is reconciled with the full protocol via the mode-selection rule in §1.2. No modification to the sub-type declaration.

### §8.2 — `lifecycle.map.type_specific.minds_specific_prompts`

The five creator-facing prompts run before SELF-CLONE if the creator chose to run `/map`. SELF-CLONE's deeper elicitation extends them without re-asking. If the creator skipped `/map`, SELF-CLONE proceeds from cold. No modification to `/map` or the prompts.

### §8.3 — `discovery_questions.ordered_questions`

The ten ordered discovery questions run inside `/create`. By the time SELF-CLONE triggers (inside `/fill`), the ten questions are already answered. SELF-CLONE does not re-ask any. No modification to the ordered questions.

### §8.4 — `/fill` walker

`/fill` gains one branch: when `.meta.yaml.type == "minds" AND .meta.yaml.minds_sub_type == "self"`, the branch loads `references/fill-content-packs/self-clone.md` and routes the walker through the protocol. All other `/fill` behavior is unchanged. The branch is additive.

### §8.5 — `mind_forge_schema.A3` (graceful degradation)

Every SELF-CLONE entry carries one of the three provenance tags: `confirmed` (direct evidence from artifact or anchored example), `inferred` (cross-referenced across sources without direct evidence), `speculative` (creator could not produce an anchor, or the pattern did not survive the counter-proof gate). No modification to A3.

### §8.6 — `mind_forge_schema.A5` (behavioral manifestation requirement)

Every SELF-CLONE elicitation question is structured to produce output that honors A5: observable signal, would-do/would-not-do pair, concrete example. No modification to A5.

### §8.7 — `mind_forge_schema.A6` (dimensional profile)

SELF-CLONE populates the eight target counts declared in A6. It does not redefine the eight dimensions or the counts. No modification to A6.

---

## §9 — Non-Contradiction Declaration

SELF-CLONE explicitly declares non-contradiction against every element of the sealed architecture at `references/engine-mind-forge-architecture.md`.

### §9.1 — Against the five laws

| Law | Status | Rationale |
|---|---|---|
| LAW-1 (dimensional genome template) | HONORED | Populates the eight target counts from A6 directly |
| LAW-2 (synthetic coherence gate) | NOT APPLICABLE | SELF-CLONE produces artificial-origin minds, not synthetic |
| LAW-3 (hybrid fusion viability) | NOT APPLICABLE | SELF-CLONE produces single-source minds, not fusions |
| LAW-4 (handoff admission payload) | HONORED BY SHAPE | Internal distillation-to-elicitation handoff follows plural-field admission |
| LAW-5 (forge passes its own methodology) | HONORED AS APEX | SELF-CLONE IS the physical embodiment — the Engine turning its own methodology on the creator who built it. The external adversarial reader gate is the honest admission that the forge cannot apply itself to itself without another observer |

### §9.2 — Against the thirteen pattern cards

| Pattern | Status | Note |
|---|---|---|
| L1 Operational Origin Test | HONORED | `origin: artificial` derived from pipeline inputs |
| L2 Fidelity Tiers Monotone Stack | HONORED | Tier ladder maps onto two modes and per-dimension stopping rules |
| L3 Graceful Degradation | HONORED | Every entry carries three-state provenance tag |
| L4 Seven-Layer Architecture | HONORED | Populates variant B, maps back to canonical via translation table |
| L5 Critical-Layer Asymmetric Floors | HONORED | Values 0.90, paradoxes 0.80, singularity 0.85 |
| L6 Four-Valued Relation | NOT APPLICABLE | Single-mind, not fusion |
| L7 Destructive Tension | NOT APPLICABLE | Same |
| L8 Orchestrator-Led Composition | NOT APPLICABLE | Single-mind, not multi-mind squad |
| L9 Origin-Enum Library | HONORED | Ships with `kryptonite[]` from honesty floor manifest |
| L10 Plural-Field Handoff | HONORED BY SHAPE | Internal handoff follows plural-field pattern |
| L11 Specificity + Behavioral Manifestation | HONORED | Every critical-layer question requires concrete signal |
| L12 Default-Optimistic Tier | HONORED | Initializes at highest tier, downgrades require rationale |
| L13 Recursive Integrity | HONORED | Protocol is describable as a mind via its own template |

**Summary: 9 HONORED, 4 NOT APPLICABLE (L6, L7, L8 — single-mind scope; LAW-2 — artificial origin). 0 CONTRADICTED.**

---

## §10 — Fidelity Contract

### §10.1 — Three artifacts

Each successful SELF-CLONE run produces three artifacts in `workspace/{slug}/`:

1. **The cognitive mind files** — the `AGENT.md`, `cognitive-core.md`, `personality.md`, `knowledge-base.md`, `reasoning-engine.md`, and `examples/examples.md` populated with the creator's extracted dimensions via the standard `/fill` write discipline.

2. **The coherence diff** — `self-clone-diff.md` — lists dimensions where the creator's self-report and their artifact-derived distillation disagreed, with each disagreement tagged and the creator's reconciliation choice recorded. This diff is often more valuable than the clone itself as operational self-knowledge.

3. **The honesty floor manifest** — `self-clone-manifest.md` — contains the five gates' output: counter-proofs per dimension, three-day delay reconciliations, adversarial reader predictions with outcomes, signed incaptable list, and the three "Il invisibile invisibile" decisions.

### §10.2 — Publish hygiene

The coherence diff and the honesty floor manifest are by default stripped from the `.publish/` bundle during `/package`. The creator may explicitly opt in to publish them. The manifest carries personal cognitive data the creator may not want public.

### §10.3 — Fidelity measurement

The aggregate fidelity score is computed from the weighted formula declared in `mind_forge_schema.A2_fidelity_declaration`:

```
F = Σ(score_i × weight_i) / Σ(weight_i)
```

Critical layers (values at weight 0.20, singularity at 0.20, paradoxes at 0.15) carry both higher floors and higher weights. Foundation layers carry lower weights. The formula is the same used for any artificial mind — SELF-CLONE does not introduce a special scoring rule.

The fidelity verdict thresholds for the apex test:
- ≥ 0.85 — VALIDATED: the architectural decision is empirically confirmed
- 0.70 to 0.84 — CONDITIONALLY VALIDATED: the protocol works but specific dimensions need refinement
- < 0.70 — FALSIFIED: the protocol requires significant rework before it can be trusted

---

## §11 — Honesty Floor

The honesty floor consists of five mechanical gates that run during or after the elicitation. No gate is skippable. The gates exist because the subject of SELF-CLONE is the creator themselves, and self-perception carries structural bias that only mechanical gates can catch.

### §11.1 — Gate 1: Removal test inverted per dimension

Every critical-layer entry must come paired with a counter-proof — a concrete situation where the clone would fail to reproduce the creator. The counter-proof is the removal test: "if this dimension were absent, what specific reproducible cognitive move would the clone fail on?"

A dimension without a counter-proof is tagged `speculative` regardless of how confidently it was declared. Post-hoc rationalizations typically fail this gate because rationalized beliefs are not anchored to specific costly refusals.

### §11.2 — Gate 2: Three-day delay rule

For the three most critical entries across the whole clone, the walker re-asks the same question with different framing after a three-day delay. Creators who are rationalizing in the moment tend to produce significantly different answers when the rationalization has decayed.

Discrepancy > 30% between the two framings tags the entry as `unstable` and drops it below the critical-layer floor.

**Operational integration:** If the delay cannot run in the session window (single-session SELF-CLONE), the walker re-frames the same question with deliberate distance within the same session. This simulated delay is tagged `same_session_reframe` in the manifest. Tier Excellence requires the full three-day interval; Tier High accepts same-session reframing.

### §11.3 — Gate 3: Adversarial reader gate

Before the clone reaches `validated` state, a second Claude (not the collector) reads the produced clone and predicts three hypothetical decisions the creator would make. The predictions are cross-checked against what the creator would actually do (verifiable from documented decisions or direct confirmation).

If predictions contradict the creator's verified choices, the clone fails the gate. The gate ensures that production and judgment are separated when the subject is the creator themselves — the collector cannot be the validator.

This gate is non-skippable. The clone never reaches `validated` state without a second Claude running the prediction test.

### §11.4 — Gate 4: Signed incaptable list

The manifest refuses to seal until the creator writes in first person: "this clone does not capture: X, Y, Z." This is a signed creator declaration, not an Engine statement.

The creator names what the clone misses. The declaration is a first-class output, not a disclaimer. It populates the `kryptonite[]` field of the forged mind's library entry, making the incapability declaration visible to anyone who installs the mind.

### §11.5 — Gate 5: "Il invisibile invisibile"

A mandatory section where the creator names three recent decisions they took and cannot justify in writing. These three entries are stored as `uncapturable: true` anti-content in the manifest.

This is not what the clone is — it is what the clone explicitly cannot be. Three levels of observability:

1. **The visible** — creator artifacts, registered decisions, the documented record. SELF-CLONE captures this.
2. **The invisible within the visible** — choices the creator did not take that were available, paths not followed, declarations made with force that betray a contrary temptation. SELF-CLONE can partially capture this with adversarial technique.
3. **The invisible invisible** — bodily intuition, pattern recognition that does not pass through language, judgment taken in three seconds without knowing why. SELF-CLONE cannot capture this. The fifth gate names it honestly.

---

## §12 — Cross-Reference Table

| This document section | Consumed by | Relationship |
|---|---|---|
| §1 Two modes + mode-selection | `mind_forge_schema.A12` | A12 declares modes, this document defines them |
| §3 Eight dimensional targets | `mind_forge_schema.A6` | A6 declares targets, this document populates them |
| §4 Ordered elicitation | `references/fill-content-packs/self-clone.md` | Content pack carries the full question sequences |
| §5 Typology probe | Content pack §typology section | Three-step mirror protocol |
| §6 Distillation procedures | Content pack §distillation section | Per-dimension extraction procedures |
| §7 Dimensional routing | Content pack §routing section | Primary-plus-secondary tagging algorithm |
| §8 Primitive integration | `/fill` skill body | Single branch loading the content pack |
| §9 Non-contradiction | `references/engine-mind-forge-architecture.md` | READ-ONLY — this document honors, never modifies |
| §10 Three artifacts | `/validate` stage 7b + 7c | Validator checks presence of three artifacts |
| §11 Five honesty gates | `/validate` stage 7c | Validator checks manifest completeness |
| Variant B target | `references/structural-dna/cognitive-architecture-variants.md` §4.5 | Reciprocal reference — variants names the target, this document names the protocol |

---

## §13 — Forward Roadmap

### §13.1 — Immediate (completed in this session)

- A12 schema extension applied to `product-dna/minds.yaml`
- Content pack authored at `references/fill-content-packs/self-clone.md`
- `/fill` skill body extended with single branch
- Reciprocal back-reference added to `cognitive-architecture-variants.md` §4.5

### §13.2 — Apex test (this session if creator available)

- Run SELF-CLONE against the Engine author's own corpus in distillation mode
- Measure fidelity against the ≥ 0.85 threshold
- Seal verdict honestly per Clause IV

### §13.3 — Future sessions

- **Three-day delay empirical validation** — run the delay rule across a real three-day interval and compare with same-session reframing results to calibrate the discrepancy threshold
- **External validator protocol refinement** — specify the exact prompt the second Claude receives when running the adversarial reader gate
- **Content pack tier extensions** — author the Tier Excellence question expansions for each dimension
- **Graduation protocol** — define the promotion ritual from `pending` to `complete` status for SELF-CLONE products

---

*Canonical substrate sealed. The protocol fills the gap the codex opened. Two modes. Eight dimensions. Five honesty gates. One adversarial reader. The riverbed speaks before the water is asked.*
