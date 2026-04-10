# Engine Mind-Forge Architecture

> **Layer:** canonical substrate authored in S126. Consumed by `product-dna/minds.yaml`, `product-dna/squad.yaml`, `quality-gates.yaml`, and the `/validate --level=3` discipline for the three mind-origin types. Extended by `references/composition-anatomy.md`, `references/intent-topology.md`, and the 140 CANON MCS arsenal.
>
> **Origin:** distilled by ALEMBIC (9 phases) across 6 source cognitive systems via 6 parallel Explore agents (A1-A6) during the S126 Mind Forge Campaign. Source dossiers at `docs/distillation/*-dossier.md`. Mission brief at `docs/distillation/_MISSION-BRIEF-S126.md`. Vault cross-reference at `docs/distillation/s126-vault-inventory.md`.
>
> **Binding disciplines inherited:** Clause I (Source Fidelity), Clause II (Separation of Production and Judgment), Clause IV (Named Trade-Offs), Clause V (Rigor > Ergonomics > Impact > Adaptability > Parsimony), Clause VIII (Every Token Earns Its Place). Principle P5 (Failure Mode Before Happy Path), P7 (Read Before Write ≥2:1), P8 (Invisibility of Mechanism), P9 (Recursive Integrity). The symmetric-drift discipline — optimistic drift and pessimistic drift are both violations of Clause I — binds every claim in this document. The marketplace taxonomy (mind, squad, skill, agent, system, workflow, hooks, claude-md, statusline, output-style, design-system, bundle, application) is **not renamed** — this document refines the content of the `mind` and `squad` codices, nothing else.

---

## §1 — What This Document Declares

This document declares the operational architecture by which the Engine forges three kinds of minds and composes them into teams at Anthropic-grade fidelity. It is the canonical answer to: *how does the Engine turn "I want a cognitive tool that thinks like X" into a resource whose thinking is mechanically defensible?*

It declares:

1. **Three mind origins** as operational categories (not marketing labels), with a codex-field test that a pipeline — not a human — can apply.
2. **Five fidelity mechanisms** bound to codex fields and validated at `/validate --level=3`.
3. **Six transferable patterns** promoted to LAW via the H3 Convergence Rule (3+ independent confirmations from the vault plus this campaign's dossiers).
4. **Four operational protocols** for hybrid fusion, multi-mind composition, graceful degradation, and recursive self-audit — each grounded in at least one dossier's pattern card.
5. **Six remaining structural gaps** named and assigned to follow-up sessions, including the cross-system meta-taxonomy that no single dossier could deliver and that the synthesis below provides a posteriori.
6. **A 4-session roadmap** for applying this document's refinement plans to the codices.

It does NOT declare:

- Implementation of the refinement plans against `product-dna/minds.yaml` or `product-dna/squad.yaml` — that is S127+ work, deliberately separated from the authoring session per Clause II.
- New marketplace taxonomy. The 13 types remain intocadas.
- Inheritance of target-system vocabulary. All operational language is in neutral cognitive-science / systems-design terms.

---

## §2 — Mind Origin Taxonomy: The Operational Rule (answers KIT-1, KIQ-1.1)

The founder's definitions inherited from S125 were the starting point. The six dossiers operationalized them into a pipeline-decidable rule.

### §2.1 — The three origins, operationally defined

| Origin | Operational definition | Pipeline test |
|---|---|---|
| **artificial** | A cognitive architecture whose design is causally grounded in documented artifacts produced by a real historical or living human. The architecture extracts the person's decision patterns, not their surface vocabulary. | `source_corpus.human_referents.length ≥ 1` AND `source_ingestion.mode == extraction_from_documents` |
| **synthetic** | A cognitive architecture designed from a declared purpose without any human referent. The starting point is a cognitive vacuum (a named problem, a missing mode of reasoning, a required failure-mode prevention) rather than a person. | `source_corpus.human_referents.length == 0` AND `design_starting_point ∈ {purpose, failure_mode_to_prevent, cognitive_vacuum}` |
| **hybrid_fusion** | A synthetic identity whose components are two or more artificial minds fused into one emergent voice. The identity is synthetic at the surface (a new name, a new voice); the genome is the compatibility-gated merger of multiple artificial cognitive profiles. | `source_minds.length ≥ 2` AND `source_minds[*].origin == artificial` AND `fusion_blueprint.compatibility_score ≥ threshold` |

### §2.2 — The naming-vs-function contradiction uncovered by A2

Agent A2's dossier on the Synthetic Intelligence Factory (SIF) delivered a critical finding: a system whose name declares *synthetic* may, by operational function, be an artificial-mind factory. SIF refuses to start extraction without ≥10 identified real humans; the Extractor phase blocks below that threshold. Pipeline test: `source_corpus.human_referents.length ≥ 10`. **The origin is artificial regardless of the label.**

This proves the operational rule: **labels are not origins.** The codex field `origin` is computed from the pipeline requirements, not declared in marketing copy. A mind declaring `origin: synthetic` whose `source_corpus.human_referents.length > 0` fails `/validate --level=3` with `origin_contradiction` error.

This closes **gap G1** (operational rule distinguishing artificial from synthetic at codex field level) — inverted: the rule fires at publish time, mechanically, by inspecting pipeline inputs, not by trusting self-declaration.

### §2.3 — Published Engine exemplars mapped to operational origins

| Exemplar | Declared category | Operational origin | Verification |
|---|---|---|---|
| An Engine global skill modeled on a Renaissance polymath | artificial | **artificial** | source corpus = primary codices + treatises attributed to the documented human; `human_referents: [one_historical_human]` |
| An Engine global skill designed as a pillar-based cognitive orchestrator | synthetic | **synthetic** | design starting point = declared orchestration purpose; `human_referents: []` |
| A published marketplace hybrid fusion product composed of three artificial minds | hybrid_fusion | **hybrid_fusion** | `source_minds: [three_named_artificial_minds]` — all three satisfy `origin == artificial` operationally |

All three pass the operational test. Codex wiring in S127+.

---

## §3 — Answers to the 13 Global KIQs

The mission brief §3 declared 13 global KIQs. Each is answered below with its primary source dossier(s) and the specific pattern card that operationalizes it. Declared gaps are marked explicitly.

| KIQ | Question | Answer (one sentence) | Source dossier(s) | Pattern card reference |
|---|---|---|---|---|
| 1.1 | What distinguishes artificial from synthetic at the forge level? | A codex-field test on `source_corpus.human_referents.length` applied at `/validate --level=3` — labels are not origins. | A2 (negative evidence), A5 (artificial only), A6 (artificial only) | §5 Pattern L1 |
| 1.2 | Minimum source corpus for a defensible artificial mind at each fidelity tier? | Per-layer asymmetric thresholds: Tier Excellence requires 8 cognitive layers all scored; Tier High ≥85% with critical layers ≥90%; Tier Functional 75-84% with thin-source protocol; Tier Insufficient <65% refuses to ship. Numeric targets per layer: ≥50 distinctive terms, ≥20 metaphors, 3-5 master models, 5-7 inviolable values, 3-5 obsessions, 3-5 paradoxes. | A5 (primary), A6 (confirms) | §5 Pattern L2, §5 Pattern L3 |
| 1.3 | How does a mature system refuse to forge when source material is insufficient? | Graceful degradation protocol: lower the fidelity tier by one step, tag every feature `confirmed / inferred / speculative`, require written justification in manifest, refuse the top tier below an asymmetric quantity floor (Sources < 20 forbids top tier regardless of subject APEX). | A5 (primary), A6 (confirms) | §5 Pattern L3 |
| 1.4 | What procedure turns reading the source into architecture that emulates? | Four-phase DEEP pipeline: Discover (1-5d reconnaissance, source inventory) → Extract (7-15d 8-layer decomposition with CLEARR per source, triangulation ≥3 independent sources) → Embody (3-7d architectural synthesis, system prompt authoring, KB compilation) → Perfect (5-11d 8-test validation, bounded refinement with ≤3 cycles or <5% marginal gain termination). | A5 (primary) | §5 Pattern L4, §5 Pattern L5 |
| 2.1 | When two artificial minds in the same team contradict each other, what protocol resolves without flattening? | Relation-typed classification: label every shared dimension as Complementary / Reinforcing / Productive Tension / Destructive Tension. Productive tensions are preserved as generative mechanisms. Destructive tensions halt synthesis on that dimension only, produce a structured 4-option decision packet for human resolution, and allow other dimensions to continue in parallel. | A3 (primary), A1 (squad-level analog) | §5 Pattern L6, §5 Pattern L7 |
| 2.2 | What hierarchy patterns are battle-tested in multi-mind systems? | Orchestrator-led with mandatory productive tension: one coordinator does no production (only routing and final validation); 3-5 producer minds, never ≤2 (no tension) and never >5 (cacophony); echo alert fires on total agreement; collective confidence capped at highest individual confidence. | A4 (primary), A2 (confirms), A1 (confirms) | §5 Pattern L8 |
| 2.3 | How does a team declare "we need another mind" vs "we need this mind deeper"? | Deeper when domain_depth is `deep` and the problem's failure mode maps to a single mind's genius zone. Another mind when the problem crosses ≥2 orthogonal cognitive axes and no existing mind spans both, enforced by a diversity gate on the 4-zone ontological taxonomy. | A4 (primary) | §5 Pattern L9 |
| 2.4 | What handoff contract prevents context loss between minds in one session? | Plural-field numeric admission payload (≥5 independent fields mixing counts, coverage, and structural flags) with producer self-convergence check, receiver input-veto, and loop-not-degrade fallback on admission failure. | A1 (primary) | §5 Pattern L10 |
| 3.1 | How are fidelity tiers operationalized in the forge (not marketing)? | Discrete tiers with strict feature-superset inheritance (higher tier ⊇ lower tier, no XOR features); each tier binds an authenticity target, an effort budget, and a mandatory feature set; weighted layer formula aggregates per-layer scores; critical layers (values, singularity, paradoxes) carry asymmetric floors. | A6 (primary), A5 (confirms) | §5 Pattern L2, §5 Pattern L3 |
| 3.2 | What mechanism catches optimistic drift at mind forge time? | Triangulation rule (every pattern ≥3 independent sources) + blind attribution test for hybrid fusion (<40% single-source attribution = pass) + specificity test (every value needs behavioral manifestation, every pattern needs observable signals, vague language blocks gate) + separation of producer from validator (Clause II). | A3 (primary), A2 (primary), A5 (confirms) | §5 Pattern L11 |
| 3.3 | What mechanism catches pessimistic drift? | Default-optimistic tier initialization (start at top tier; downgrade requires written justification + post-hoc review) + critical-layer asymmetric floors (a high score on surface layers cannot mask a low score on values). | A6 (primary), A5 (partial) | §5 Pattern L12 |
| 4.1 | Does the target system pass its own methodology when pointed at itself? | Yes, conditionally — evidence from A4 (pre/post session hooks + handoff discipline + CELF immutable layer + REFLECT constraint = recursive discipline operating) and from this document (§7 below applies its own patterns to itself). A6 explicitly fails this test; its empty `docs/nexus/` and zero self-audit is evidence that recursive integrity is a *habit*, not an architectural side-effect. | A4 (primary), A6 (negative evidence) | §5 Pattern L13, §7 recursive self-test |
| 4.2 | What does recursion-as-validation look like for a forge of minds? | Three concrete signals: (a) the forge's own state machine is a mind it can describe via its own template; (b) every forged mind's delta log contains at least one lesson the forge then incorporates into its own protocol; (c) session hooks wrap every substantive operation and the post-session hook writes a mandatory reflection into a governed register. | A4 (primary) | §5 Pattern L13 |

---

## §4 — H3 Convergence Rule — Law Promotions (this campaign)

The vault inventory §7 declared 5 H3 candidates awaiting third confirmation. **This campaign triggered all 5.** Per the H3 Convergence Rule (3+ independent confirmations promote an observation to LAW in the mind-forge architecture), the following are now LAW.

### §4.1 — LAW-MF-1: Artificial mind extraction uses a dimensional genome template with named target counts per dimension

**Prior confirmations:** MI-001 (Constelação Dimensional 68-dim), MI-016 (Layer 1 Extração de Genoma 68-dim), MI-013 (Linguistic Signature Framework 5 components).

**Third confirmation:** A5 Mental Clone Lab + Mind Research Architect. The target decomposes a source human into 8 cognitive strata with named numeric targets per stratum (≥50 distinctive terms, ≥20 metaphors, 3-5 master models, 5-7 inviolable values, 3-5 obsessions, 3-5 paradoxes). The 8-layer decomposition yields ~30-40 scored sub-dimensions — same order of magnitude as the 68-dim prior art, different top-level decomposition.

**Law statement:** Every artificial-mind forge MUST extract against a dimensional genome template with named numeric targets per dimension. The Engine canonical template uses 7 layers (inheriting from MCS-139 and the operational reading below in §6.3); target sibling variants (A2's 7-layer content template, A5's 8-layer, A6's 8-layer) are documented as alternate decompositions with migration notes, not competing truths. Dimension count per layer has a declared minimum that feeds the fidelity formula.

**Codex binding:** `product-dna/minds.yaml` §artificial_mind_schema.dimensional_profile[] — required field on every `origin: artificial` entry.

### §4.2 — LAW-MF-2: Synthetic minds require an internal coherence validation gate

**Prior confirmations:** MCS-001 (Falsification-First), MI-199 (Architectural Integrity & Coherence — 5 meta-principles).

**Third confirmation:** A2 SIF Validator agent. A 3-tier progressive validation where Tier 1 is a Consistency Checklist (no contradictions between layers; personality aligns with work style; decision speed aligns with context; communication style matches personality; values reflected in ethical limits) and Tier 2 Category 7 (meta-cognitive) plus Category 8 (ethics binary hard gate).

**Law statement:** Every synthetic-mind forge MUST carry an internal coherence validation gate as a separate producer-quarantined authority. The gate MUST be mechanical (a checklist, not prose), MUST be external to the producer agent (Clause II), and MUST include at least: (a) inter-layer non-contradiction, (b) personality-behavior alignment, (c) named ethical boundary as binary pass/fail.

**Codex binding:** `product-dna/minds.yaml` §synthetic_mind_schema.coherence_gate — required for every `origin: synthetic` entry.

### §4.3 — LAW-MF-3: Hybrid fusion uses dimensional compatibility analysis with weighted aggregate and numeric abort gate

**Prior confirmations:** MI-014 (Layer 2 Compatibility Analysis N×N matrix with S/N/A/D states and viability ≥0.6), MI-015 (Layer 3 Fusão Sinérgica — dimensional merging, synergy amplification, antagonism management).

**Third confirmation:** A3 CFL compatibility-matrix.md. Weighted aggregate compatibility score across four factors — Complementarity 0.25, Value Alignment 0.25, Cognitive Synergy 0.30 (highest weight), Worldview Coherence 0.20 — with a named penalty schedule (−30 for anti-value conflict, −20 for ontological conflict, −15 for >70% overlap) and a numeric abort gate at score <60.

**Law statement:** Every hybrid_fusion forge MUST carry a pre-synthesis numeric viability gate computed from decomposed per-source profiles across at least four named factors, with a declared abort threshold below which no synthesis is attempted. The factors MUST include cognitive synergy as highest weight. Below threshold, the fusion is rejected with a written reason — never silently downgraded.

**Codex binding:** `product-dna/minds.yaml` §hybrid_fusion_schema.pre_fusion_viability_gate — required for every `origin: hybrid_fusion` entry.

### §4.4 — LAW-MF-4: Multi-mind handoff requires a plural-field admission payload with loop-not-degrade fallback

**Prior confirmations:** SD-027 (Handoff Contracts — inter-wave context transfer), SD-016 (7-Component Agent Payload).

**Third confirmation:** A1 squad-creator-pro. A 9-field structured admission payload at the extraction→build specialist seam, with producer-side self-validation check, receiver-side input-veto enforcement, and an explicit loop-not-degrade fallback direction on admission failure. The payload shape IS the inter-agent contract; no side channels permitted.

**Law statement:** Every multi-mind team handoff MUST be guarded by a plural-field admission payload with ≥5 independent fields mixing numeric thresholds (counts, coverage percentages) and structural flags (marked/unmarked, typed/untyped, provenance-bearing). The producer MUST self-converge before handing off. The receiver MUST hold input-side veto and bounce incomplete payloads. The fallback direction MUST be loop (send back to producer) and MUST NOT be silent degradation (accept with warning).

**Codex binding:** `product-dna/squad.yaml` §handoff_contract_template — required for every squad with ≥2 producers. Fills GAP-COMPOSITION-1.

### §4.5 — LAW-MF-5: The forge MUST pass its own methodology when applied to itself

**Prior confirmations:** MCS-009 (Recursion as Self-Validation), MI-019 (Meta-Recursion and Self-Application Protocol).

**Third confirmation:** A4 Pantheon. Pre/post session hooks frame every session; dated handoff documents crystallize decisions paid in error; the constitutional layer is declared immutable-per-session; REFLECT is the only upward write; the dissolved "Convergence Engine" component became AP-09 Componente Fantasma — the deletion itself became an anti-pattern. The library passes its own discipline when pointed at itself.

**Negative evidence:** A6 mmos-standalone explicitly fails this test (empty `docs/nexus/`, no self-audit, no delta log). Negative evidence is data: it shows that recursive integrity is a **discipline that must be practiced**, not an emergent property.

**Law statement:** The Engine mind-forge MUST pass `/validate --level=3` when pointed at `references/engine-mind-forge-architecture.md` itself. Every substantive forge-related session MUST write one concrete improvement to a delta log. The forge MUST be describable as a mind via its own template (a reflexive self-description test).

**Codex binding:** `quality-gates.yaml` new gate `mind_forge_recursive_integrity` running at `/validate --level=3` against this document and against itself. Existing Engine discipline at P9 covers this; the mind-forge scope is the new subject of P9.

---

## §5 — Pattern Cards (Phase 6 FORMALIZE)

The 44 raw patterns extracted across 6 dossiers converge into 13 formal pattern cards below. Each card follows ALEMBIC §Phase 6 canonical form: Context, Problem, Forces, Resolution, Mechanism, Consequences, Known Instances (cross-dossier), Transfer Target, PRL, Generativity Test.

### §5.1 — Pattern L1: Operational Origin Test (codex-field, not marketing)

**Context.** A mind codex declares an origin field but self-declaration cannot be trusted (A2 naming inversion proves this).

**Problem.** Mind origin labels drift from operational reality; "synthetic" gets applied to artificial-extraction pipelines; "artificial" gets applied to personas with no extraction.

**Forces.** Marketing wants evocative labels. Integrity wants pipeline-decidable truth. Simplicity wants one field. Rigor wants verifiable provenance.

**Resolution.** Compute `origin` at `/validate` time from pipeline inputs: `human_referents.length ≥ 1 + extraction mode` → artificial; `human_referents.length == 0 + declared purpose` → synthetic; `source_minds.length ≥ 2 + all artificial` → hybrid_fusion. Self-declaration is a *claim* that the validator tests against reality.

**Mechanism (3 steps).** (1) Codex schema adds `source_corpus: {human_referents: [], source_artifacts: []}` and `design_starting_point: {purpose|failure_mode|cognitive_vacuum|null}` and `source_minds: []`; (2) `/validate --level=3` reads these fields and computes `origin_derived`; (3) if `origin_declared != origin_derived`, validation fails with `origin_contradiction` error.

**Consequences.** Mechanical honesty at publish time. Forces codex authors to populate pipeline-real fields. Kills the SIF-style naming inversion at the Engine level.

**Known instances.** A2 (negative — naming inversion discovered), A5 (artificial only, consistent), A6 (artificial only, consistent), A3 (hybrid_fusion consistent). 4 instances.

**Transfer target.** `product-dna/minds.yaml` §schema + `quality-gates.yaml` §origin_derivation_check.

**PRL: 8** — operationally ready, design is concrete, validator logic is a few lines.

**Generativity Test.** PASS. A creator who has never seen the six source systems, following the schema + validator, cannot ship a mind whose declared origin contradicts its pipeline inputs. The pattern is embedded in the mechanism.

### §5.2 — Pattern L2: Fidelity Tiers as Monotone Feature-Stacking Contract

**Context.** A forge outputs cognitive artifacts whose claimed emulation quality varies with source corpus depth, available time, and budget.

**Problem.** Continuous quality is hard to contract against; discrete tiers must be chosen; averaging across tiers produces silent quality loss.

**Forces.** Rigor (defend what we claim) vs ergonomics (serve constrained clients) vs parsimony (don't multiply tiers).

**Resolution.** Discrete tiers (recommended: 4 levels — Basic / Functional / High / Excellence) with strict feature-superset inheritance (higher tier ⊇ lower tier, no XOR features), each tier declaring authenticity target + effort budget + mandatory feature set.

**Mechanism (5 steps).** (1) Define canonical tier ladder with authenticity % per tier. (2) Every codex entry carries `fidelity_tier` field. (3) Feature flags are monotone: a feature listed at Functional is also required at High and Excellence. (4) Downgrade is explicit and requires justification written to metadata. (5) `/validate` refuses to ship a tier whose required features are missing.

**Consequences.** Defensible quality claims. No optimistic tier inflation. Mechanical refusal at the gate. Clients can choose their tier honestly.

**Known instances.** A5 (Excellence 90+ / High 85-89 / Functional 75-84 / Basic 65-74 / Insufficient <65), A6 (BASIC 75% / PREMIUM 85% / LEGEND 95% with monotone feature stacking), A2 (G1-G7 gates as horizontal threshold registry — sibling variant, not direct stack but monotone). 3 instances.

**Transfer target.** `product-dna/minds.yaml` §fidelity_tier + `quality-gates.yaml` §tier_feature_check.

**PRL: 7** — validated across 2 operational targets, adopt-ready.

**Generativity Test.** PASS. Creator with no prior exposure gets a tiered ladder + feature matrix and naturally produces a mind that declares its tier and ships its features.

### §5.3 — Pattern L3: Graceful Degradation via Confirmed/Inferred/Speculative Labels

**Context.** A source corpus for a target mind is thinner than the top fidelity tier requires.

**Problem.** Rigid halt produces false "cannot forge" verdicts; silent fabrication produces optimistic drift (a Clause I violation). The honest answer is between the two.

**Forces.** Rigor (don't claim what you cannot verify) vs utility (ship the best possible mind anyway) vs honesty (mark what was captured vs imagined).

**Resolution.** Three coordinated moves: (1) lower the fidelity tier by one step, (2) tag every extracted feature as one of `confirmed / inferred / speculative`, (3) require written justification in the manifest declaring why the downgrade was necessary.

**Mechanism (4 steps).** (1) Codex schema adds `source_adequacy_score` computed from corpus quantity × quality × diversity. (2) Below threshold, fidelity tier auto-downgrades with mandatory justification. (3) Every feature in the mind carries a provenance tag in three states. (4) The mind's system prompt renders `speculative` features with explicit uncertainty markers; the mind knows which of its traits are solid and which are guessed.

**Consequences.** Fills gap G3. Kills both optimistic drift (false claim of Excellence) and pessimistic drift (false rejection of forgeable subject). Creates audit trail of what was captured.

**Known instances.** A5 (upstream protocol for thin sources: floor drops 85→75, triple reading, three-state labels), A6 (dual-score gate with asymmetric quantity floor: Sources<20 auto-downgrades regardless of APEX), A1 (partial — provenance markers at extraction time as [SOURCE:] vs [INFERRED] dual-marker). 3 instances.

**Transfer target.** `product-dna/minds.yaml` §artificial_mind_schema.source_adequacy_gate + §fidelity_declaration.feature_provenance.

**PRL: 8** — two independent operational implementations + adjacent third confirmation; fills declared gap.

**Generativity Test.** PASS. The schema forces creators to carry provenance through the pipeline; a creator who never saw the sources cannot produce a mind that claims certainty about speculative traits.

### §5.4 — Pattern L4: Seven-Layer Cognitive Architecture (canonical, with sibling variants noted)

**Context.** A cognitive mind needs structured internal layers, not a flat persona.

**Problem.** Different dossiers present divergent layer counts: MCS-139 declares 7 (L1 Boot / L2 Cognitive Core / L3 Personality Engine / L4 Knowledge Domains / L5 Reasoning Engine + C1-C7 DNA strands); A2 declares 7 (Knowledge / Cognitive Processing / Execution / Personality / Context / Meta-Cognitive / KB Integration); A5 declares 8 (Linguistic Surface / Pattern Recognition / Master Models / Decision Architecture / Value Hierarchy / Core Obsessions / Singularity / Productive Paradoxes); A6 declares 8 (Identity / Context / Cognitive / Methodology / Metacognition / Persona / Communication / Evolution).

**Forces.** Canonical simplicity (one layer count) vs sibling prior-art respect (don't overwrite operational work) vs evolution (new decompositions may teach the canonical one).

**Resolution.** The Engine canonical is **MCS-139's 7 layers**, because: (a) it is the substrate already wired into the vault, (b) it includes a boot layer (startup discipline) that neither A2 nor A5 nor A6 carries, (c) it includes a reasoning engine as first-class which is critical for cognitive-depth minds. The three sibling variants (A2, A5, A6) are documented as **alternative content decompositions**, not competing architectures. A5's 8-layer brings asymmetric criticality (see §5.5 below) — a refinement the canonical should adopt as a *weighting overlay*, not a layer replacement. A6's 8-layer brings Theatre of Agents as internal multi-agent deliberation inside a single layer — a *pattern within L2 Cognitive Core*, not a competing layer count.

**Mechanism (3 steps).** (1) `product-dna/minds.yaml` declares the canonical 7 layers per MCS-139. (2) Alternative decompositions are documented in `references/structural-dna/cognitive-architecture-variants.md` as sibling prior art with migration notes. (3) Creator who supplies a 6-layer or 8-layer variant receives a `/validate` warning pointing at the canonical with translation table.

**Consequences.** Resolves the 7-vs-8 layer tension without forcing a winner. Preserves operational work from A2, A5, A6 as documented alternatives. Honors Clause I (no overwriting prior art as if novel).

**Known instances.** MCS-139 (vault canonical), A2 (7-layer sibling), A5 (8-layer sibling), A6 (8-layer sibling). 4 instances of the pattern "cognitive mind has ≥7 explicit layers with named responsibilities" — the pattern is robust even though the layer counts diverge.

**Transfer target.** `product-dna/minds.yaml` §cognitive_architecture_canonical + new `references/structural-dna/cognitive-architecture-variants.md`.

**PRL: 7** — vault prior art at PRL 7+, three independent sibling confirmations at PRL 6+ each.

**Generativity Test.** PASS. Creators following the canonical plus the variants document can produce any of the three layer counts and have the translation table.

### §5.5 — Pattern L5: Critical-Layer Asymmetric Floors with Weighted Fidelity Formula

**Context.** Per-layer validation of a forged mind where uniform thresholds let deep authenticity fail silently.

**Problem.** A mind with polished vocabulary and weak values passes a flat threshold. Surface layers (terms, metaphors) mask depth-layer failure (values, paradoxes, singularity).

**Forces.** Simplicity (uniform threshold) vs authenticity (weighted by criticality) vs mechanical-verifiability (must be computable).

**Resolution.** Some layers are **critical** (must exceed higher floor), others are **foundation** (adequate threshold OK). Aggregate fidelity is a weighted sum with declared per-layer weights; critical layers carry both higher floors and higher weights.

**Mechanism (4 steps).** (1) Declare `layer.is_critical: bool` per layer. Critical set (A5-derived): Values, Singularity, Paradoxes. (2) Declare `layer.weight: float` with non-uniform values (e.g., Values 0.20, Singularity 0.20, Models 0.15, Decisions 0.15, Obsessions 0.15, Paradoxes 0.15, Surface 0.10, Recognition 0.10 — weights sum to 1.25 intentionally to amplify criticals). (3) Fidelity formula `F = Σ(score_i × weight_i / weight_sum)`. (4) Critical layers below floor block publication regardless of aggregate.

**Consequences.** Prevents surface-polish masking depth failure. Makes "authenticity" a computable property. Honors the emula-vs-simula discipline at the math level.

**Known instances.** A5 (explicit weighted formula with asymmetric floors per 8 layers), A6 (monotone feature stacking carries implicit weight via feature count per tier), A3 (weighted compatibility score with 0.30 on Cognitive Synergy — highest — which is the closest to an asymmetric weight in that target). 3 instances.

**Transfer target.** `product-dna/minds.yaml` §fidelity_declaration.formula + §fidelity_declaration.critical_layers.

**PRL: 7** — operationally validated at A5, confirmed at A6, third confirmation at A3.

**Generativity Test.** PASS. The formula is mechanical; the critical-layer list is explicit.

### §5.6 — Pattern L6: Four-Valued Relation Taxonomy for Hybrid Fusion

**Context.** Preparing a dimensional synthesis plan when multiple source minds share a cognitive axis.

**Problem.** Ad-hoc synthesis produces inconsistent treatment — some dimensions averaged, some picked, some ignored — and contradictions leak into the final artifact.

**Forces.** Expressive freedom (let the synthesis breathe) vs mechanical reproducibility (audit every decision) vs honoring difference vs producing one voice.

**Resolution.** Every shared dimension is labeled exactly one of {Complementary, Reinforcing, Productive Tension, Destructive Tension}. Each label binds a specific synthesis template: Complementary → integrate-all; Reinforcing → amplify-common; Productive Tension → dialectic-generative (preserve both poles as live force); Destructive Tension → escalate to human (halt synthesis on that dimension).

**Mechanism (4 steps).** (1) Fusion blueprint carries a table: `[dimension, mind_a_value, mind_b_value, relation_type, synthesis_template]` per row. (2) Relation classifier tests orthogonality (different axes → Productive Tension) vs same-axis contradiction (→ Destructive Tension). (3) Template selection is mechanical from relation_type. (4) Destructive Tension triggers §5.7 escalation protocol.

**Consequences.** Kills chimera production. Every fusion decision is auditable. Contradictions are first-class citizens with typed treatment.

**Known instances.** A3 §fusion-protocols.md (4 full templates), A3 §compatibility-analyzer.md phase 1 step 3, A3 §fusion-engine.md synthesis methodology, A3 §fuse-consciousness.md cycle 1. 4 instances within A3. A1's "productive paradox navigation" checkpoint type is a single-mind sibling of this (1 additional external confirmation).

**Transfer target.** `product-dna/minds.yaml` §hybrid_fusion_schema.relation_taxonomy (new required field).

**PRL: 7** — operationally validated at A3 with 4 templates + 1 external sibling confirmation.

**Generativity Test.** PASS. The label set is small (4), the templates are explicit, the classifier is a simple test.

### §5.7 — Pattern L7: Destructive Tension Escalation Packet

**Context.** Fusion encounters a dimension where source minds hold same-axis incompatible positions.

**Problem.** Silent resolution produces chimeras; naive compromise ("somewhat real") loses both positions; halt of entire fusion wastes other dimensions' work.

**Forces.** Automation completeness vs human authority over worldview conflicts; coverage vs honesty about irreducible disagreement.

**Resolution.** Detect same-axis opposition (not orthogonal — that would be Productive Tension); halt synthesis on that dimension only; produce a structured 4-option decision packet (Explicit Preservation / Prioritize A / Prioritize B / Contextualize / Exclude Mind) with trade-offs for each option; parallel dimensions continue; human decides; decision documented in manifest.

**Mechanism (5 steps).** (1) Classifier labels dimension Destructive. (2) Parallel dimensions proceed. (3) Packet builder assembles the 4 options with concrete trade-off statements. (4) Human review gate. (5) Decision stored as `fusion_decision: {dimension, option_chosen, rationale, date}` in manifest.

**Consequences.** No silent compromise. Human retains authority over worldview-level conflicts. Other dimensions don't wait.

**Known instances.** A3 §fusion-engine.md synthesis methodology with full YAML template, A3 §fusion-protocols.md Template 4, A3 §compatibility-analyzer.md Destructive Tension classification, A3 §fusion-engine.md Worked Example. 4 instances within A3.

**Transfer target.** `references/engine-mind-forge-architecture.md` §fusion_conflict_protocol (this document) + reference from `product-dna/minds.yaml` §hybrid_fusion_schema.destructive_tension_protocol.

**PRL: 6** — validated at a single target but across 4 distinct files with consistent structure; transfer-ready with engineering caveat.

**Generativity Test.** PASS. Creator with no prior exposure, given the classifier + packet template, produces structurally identical escalations.

### §5.8 — Pattern L8: Orchestrator-Led Composition with Mandatory Productive Tension

**Context.** Multi-mind team on a single task.

**Problem.** Echo chamber (all minds agree, no new insight), cacophony (too many minds, no coherent output), or mono-voice flattening (one mind dominates).

**Forces.** Consensus efficiency vs insight from disagreement vs coordination overhead vs team size limit.

**Resolution.** Orchestrator-led hierarchy (one coordinator, no production — only routing and final validation); 3-5 producer minds (never ≤2, never >5); composer MUST guarantee ≥1 productive-tension edge between members; total agreement triggers ALERT (echo-chamber suspect); disagreements read FIRST during synthesis; collective confidence capped at highest individual confidence.

**Mechanism (5 gates).** (1) Size gate: 3 ≤ |team| ≤ 5. (2) Tension gate: registry stores `productive_tension:` edges per mind; composer verifies ≥1 edge exists across the selected team. (3) Echo alert: if all minds' outputs agree above a similarity threshold, halt and escalate. (4) Disagreement-first synthesis: the final output lists dissenting positions before consensus. (5) Confidence cap: team confidence ≤ max(individual confidences).

**Consequences.** Forces structured disagreement. Prevents echo-chamber consensus. Makes "multi-voice analysis" operationally meaningful.

**Known instances.** A4 Pantheon (explicit MP-10 principle + AP-01 anti-pattern + composer Phase 2 step 5 + composer Phase 4 step 2 + registry field per entry = 5 instances). A2 SIF (6-role disjoint factory, orchestrator-led, similar structure). A1 squad-creator-pro (tier-0 triage + tier-orchestrator coordination + 2 tier-1 specialists with strict role split + peer flat relationship = orchestrator-led with smaller team). 3 instances.

**Transfer target.** `product-dna/squad.yaml` §composition_gates + §orchestrator_led_team_template.

**PRL: 8** — three independent operational implementations.

**Generativity Test.** PASS. The 5 gates are mechanical; the team-size bounds are explicit; creators naturally produce compliant squads.

### §5.9 — Pattern L9: Origin-Enum Typed Library with Capability + Incapability Declaration

**Context.** A library holds multiple minds of varying origin, depth, and specialization.

**Problem.** Type collapse treats every entry as "just an agent". Duplicate near-archetypes multiply silently. Users cannot search ontologically.

**Forces.** Unified query surface vs origin-specific validation; search ergonomics vs cognitive-architecture introspection; library expansion vs coherence.

**Resolution.** (1) Every library entry declares `origin ∈ {artificial, synthetic, hybrid_fusion}` as schema-level enum. (2) Every entry declares `genius_zone[]` (capabilities) AND `kryptonite[]` (named incapabilities — required field). (3) Library carries two indexing axes: capability tags (for search) AND a 4-zone ontological taxonomy (Foundation / Processing / Expression / Context) cross-cut via template sections (for diversity and composition gates). (4) Slug is primary key; subset-rejection validator blocks duplicate near-archetypes without justification.

**Mechanism (4 fields + 1 validator).** `origin: enum`, `genius_zone: [string]`, `kryptonite: [string]`, `ontology_map: {zone, layers[]}`, `duplicate_archetype_policy` validator.

**Consequences.** Library is honest about what it holds. Capability + named-incapability enables matching and explicit scope declaration. Ontological taxonomy enables diversity gates in composition. Slug singleton prevents archetype chimera.

**Known instances.** A4 Pantheon (42-entry registry with all 4 fields + validator + 3 origin states coexisting in schema), A2 SIF (7-layer template with personality + context layers — sibling of the capability/incapability axis), A6 mmos-standalone (tier-gated mind with DNA Mental 8-layer — sibling with different decomposition). 3 instances.

**Transfer target.** `product-dna/minds.yaml` §schema (origin, genius_zone, kryptonite, ontology_map) + new `references/mind-library-indexing.md`. **Fills gap G4.**

**PRL: 7** — operationally validated at A4 at 42-entry scale with full 4-field schema.

**Generativity Test.** PASS. The schema forces declaration; creators cannot publish a mind without naming its incapability.

### §5.10 — Pattern L10: Plural-Field Admission Payload Handoff Contract

**Context.** Multi-specialist team where one producer's output is another producer's input and silent quality loss across the seam is unacceptable.

**Problem.** Generic "pass the baton" handoffs let the receiver inherit unmarked inferences, silently degraded fidelity, and missing provenance.

**Forces.** Throughput (ship, move on) vs fidelity (prove grounding or stall); producer wants closure vs receiver wants trusted raw material.

**Resolution.** Structured payload with ≥5 independent admission fields mixing numeric thresholds (counts, coverage) and structural flags (marked/unmarked, cited/inferred). Producer self-converges before handoff. Receiver holds input-side veto. Fallback direction on failure is loop (back to producer), never degrade. The payload shape IS the inter-agent contract.

**Mechanism (5 gates).** (1) Schema: `handoff_payload: {numeric_fields{}, structural_flags{}, provenance_tags{}}`. (2) Producer self-validation checklist before handoff. (3) Receiver input-veto: bounce if any field fails. (4) Loop-not-degrade rule: explicit fallback direction. (5) No side channels: everything inter-agent goes through the payload.

**Consequences.** No silent context loss. Clear responsibility allocation. Forced convergence before transfer. Detectable stall states. **Fills GAP-COMPOSITION-1.**

**Known instances.** A1 squad-creator-pro (9-field admission contract between extraction and build specialists + checklist gate + input-veto + loop-not-handoff rule = 4 instances). A2 SIF (handoff contract on every edge with trigger + package + verify + signal — structurally identical, plural-field). A3 CFL (layer-to-layer handoff with confidence ≥0.98 + Tier 1 100% + Tier 2 ≥60% + operationalization + structured handoff section = plural-field pattern at fusion pipeline level). 3 instances across 3 independent targets.

**Cross-reference.** **CONFIRMS SD-027 + SD-016 — THIRD INDEPENDENT CONFIRMATION — LAW-MF-4 promoted above.**

**Transfer target.** `product-dna/squad.yaml` §handoff_contract_template — required for every squad with ≥2 producers.

**PRL: 9** — three operationally validated implementations + two vault ancestors. CODIFY tier.

**Generativity Test.** PASS. The template forces field declaration; the loop-not-degrade rule is explicit.

### §5.11 — Pattern L11: Specificity Test + Behavioral Manifestation as Anti-Theater Ritual

**Context.** Any forge output about to ship with vague language ("think strategically", "value curiosity", "operate with rigor").

**Problem.** Descriptive prose passes superficial review but fails at the first edge case. The mind sounds deep but decides generically.

**Forces.** Readability (prose flows) vs operationality (prose must fire). Marketing vocabulary vs behavioral verification.

**Resolution.** Every pattern, heuristic, value, and trait in a mind codex MUST have: (a) observable signals, (b) step-by-step protocols OR behavioral manifestations, (c) at least one concrete example. Vague language blocks the validation gate.

**Mechanism (4 checks).** (1) Codex schema requires `behavioral_manifestations[]` field on every trait. (2) `/validate` runs a vague-language detector (regex for empty qualifiers: "strategically", "effectively", "with rigor", "thoughtfully" — unless paired with a concrete behavior). (3) Every value needs ≥1 "would do X, would not do Y" pair. (4) Every cognitive pattern needs ≥1 observable signal declared.

**Consequences.** Kills "Theater" anti-pattern at forge time. Forces creator to operationalize aspiration. Emula-vs-simula discipline becomes mechanical.

**Known instances.** A2 SIF (extractor Core Principle 4, validator Specificity Audit, quality-standards Specificity Test, assembler Common Error "super-abstraction" = 4 instances). A3 CFL (fusion-engine P5 behavioral operationalization, Cycle 3 "no abstractions" constraint, fusion-auditor Test 2 comparative baseline = 3 instances). A5 (upstream rule "every pattern needs observable signals" + downstream extract protocol). 3 targets.

**Cross-reference.** CONFIRMS MCS-121 (Bestiary Theater anti-pattern), CONFIRMS MCS-130 (Anti-Theater Detection), CONFIRMS MI-022 (Teste de Remoção). Multiple vault reinforcements.

**Transfer target.** `product-dna/minds.yaml` §behavioral_manifestation_requirement + `quality-gates.yaml` §stage_6_anti_commodity (vague-language detector extension).

**PRL: 8** — operationally validated across 3 targets + 3 vault ancestors.

**Generativity Test.** PASS. The vague-language detector is mechanical; the behavioral-manifestation schema is explicit.

### §5.12 — Pattern L12: Default-Optimistic Tier with Mandatory Downgrade Epistemics

**Context.** Forges where pessimistic drift (under-declaring authenticity to hedge against failure) is as dangerous as optimistic drift.

**Problem.** Teams silently downgrade to avoid blame, flattening quality to lowest common denominator. Pessimistic drift is symmetric to optimistic drift — both are violations of Clause I Source Fidelity.

**Forces.** Psychological safety (permission to claim less) vs quality floor (system demands the best feasible).

**Resolution.** (1) Initialize every new mind at the highest tier permitted by its viability gate. (2) Downgrade requires written justification in a standard template. (3) Justification is recorded in the mind's metadata. (4) Post-hoc review tracks whether downgrade was correct.

**Mechanism (4 steps).** (1) Codex schema initializes `fidelity_tier: max(viability_gate_output)`. (2) Downgrade writes `downgrade_rationale: {from, to, reason, date}`. (3) `/validate` refuses silent downgrades (downgrade without rationale = error). (4) Post-implementation review field tracks correctness.

**Consequences.** Forces conscious trade-off. Eliminates silent downgrade. The symmetric-drift discipline is operationalized at the forge level — a principle becomes a mechanical check at publish time.

**Known instances.** A6 mmos-standalone (explicit "Default LEGEND, justify downgrades" philosophy + Selection Template Step 4 downgrade-rationale field + Post-Implementation Review section tracks correctness = 3 instances). A1 squad-creator-pro (relative-to-dataset percentile grading is a sibling — it prevents both false reject and false pass). A5 (thin-source protocol is the opposite case — lower floor with explicit uncertainty; but the discipline of written justification is identical). 3 instances.

**Transfer target.** `product-dna/minds.yaml` §tier_declaration_protocol — converts the symmetric-drift principle into an operational mechanism at publish time.

**PRL: 7** — operational at A6 with post-hoc review evidence; sibling confirmations at A1, A5.

**Generativity Test.** PASS. The rationale-required field is mechanical.

### §5.13 — Pattern L13: Recursive Integrity via Hook-Framed Session + Immutable Constitutional Layer + Constrained Upward Writes

**Context.** Long-running cognitive system that must survive its own evolution without drifting from its own claims.

**Problem.** Drift between claim and code accumulates across sessions. Constitutional layer gets edited mid-session. Learning writes corrupt identity fields.

**Forces.** Development velocity vs constitutional integrity; learning autonomy vs identity protection.

**Resolution.** (1) Pre-session and post-session hooks frame every substantive session. (2) Constitutional layer (L0) is declared immutable-per-session; edits require a dedicated session. (3) REFLECT is the only upward-write protocol; it writes constrained fields only (observed_performance, compatibility_scores with confidence provenance); identity fields require human brownfield. (4) Dated handoff documents crystallize decisions paid in error. (5) Dissolved components become named anti-patterns (A4 AP-09 Componente Fantasma evidence).

**Mechanism (5 files/protocols).** (1) `hooks/pre-session-validate.sh` + `hooks/post-session-reflect.sh`. (2) CLAUDE.md immutability declaration. (3) REFLECT protocol with write-allowlist. (4) `handoffs/` directory with dated entries. (5) `references/anti-patterns.md` carries dissolved-component entries.

**Consequences.** The forge passes its own discipline. Delta logs become automatic. Lessons paid in error become structural — the deletion of a component becomes its anti-pattern entry, preventing re-invention.

**Known instances.** A4 Pantheon (all 5 mechanisms present). **Negative instance:** A6 mmos-standalone (empty docs/nexus/, no hooks, no self-audit, no delta log — explicit failure of recursive integrity). MCS-009 + MI-019 as vault ancestors. The Engine already has most of this (CLAUDE.md, handoffs/, session discipline). 2 positive operational instances + 1 negative + 2 vault ancestors = **third confirmation for H3 "Forge passes its own forge" → promoted to LAW-MF-5 above.**

**Transfer target.** Engine already has this discipline at session level; new application is to `references/engine-mind-forge-architecture.md` itself — `/validate --level=3` must pass when pointed at this document and at any mind forged via this document.

**PRL: 8** — operationally validated at A4 + Engine itself already operates the pattern.

**Generativity Test.** PASS. The hooks + handoffs + immutable layer + REFLECT discipline are all mechanical. Negative evidence from A6 confirms the pattern is disciplined, not emergent.

---

## §6 — PRL Assessment & Transfer Decisions (Phase 7 ASSESS)

Pattern Readiness Level per ALEMBIC §Phase 7 rubric. Transfer decision per PRL:

| Pattern | PRL | Transfer Decision | Engine Target |
|---|---|---|---|
| L1 Operational Origin Test | 8 | **CODIFY** | `product-dna/minds.yaml` §schema + `quality-gates.yaml` §origin_derivation_check |
| L2 Fidelity Tiers Monotone Stack | 7 | **ADOPT** | `product-dna/minds.yaml` §fidelity_tier |
| L3 Graceful Degradation + 3-State Labels | 8 | **CODIFY** (fills G3) | `product-dna/minds.yaml` §source_adequacy_gate + §feature_provenance |
| L4 7-Layer Canonical Architecture | 7 | **ADOPT** (reinforces MCS-139) | `product-dna/minds.yaml` §cognitive_architecture_canonical + `references/structural-dna/cognitive-architecture-variants.md` |
| L5 Critical-Layer Asymmetric Floors | 7 | **ADOPT** | `product-dna/minds.yaml` §fidelity_declaration.formula |
| L6 Four-Valued Relation Taxonomy | 7 | **ADOPT** | `product-dna/minds.yaml` §hybrid_fusion_schema.relation_taxonomy |
| L7 Destructive Tension Escalation | 6 | **ADOPT** | this document §fusion_conflict_protocol + `product-dna/minds.yaml` reference |
| L8 Orchestrator-Led Composition | 8 | **CODIFY** | `product-dna/squad.yaml` §composition_gates |
| L9 Origin-Enum Typed Library | 7 | **ADOPT** (fills G4) | `product-dna/minds.yaml` §schema + `references/mind-library-indexing.md` |
| L10 Plural-Field Admission Payload | 9 | **CODIFY** (fills GAP-COMPOSITION-1) | `product-dna/squad.yaml` §handoff_contract_template |
| L11 Specificity Test + Behavioral Manifestation | 8 | **CODIFY** | `product-dna/minds.yaml` §behavioral_manifestation_requirement + `quality-gates.yaml` §stage_6 |
| L12 Default-Optimistic Tier + Downgrade Epistemics | 7 | **ADOPT** | `product-dna/minds.yaml` §tier_declaration_protocol |
| L13 Recursive Integrity Hook Discipline | 8 | **CODIFY** (already operational at Engine level; extend to mind-forge scope) | `quality-gates.yaml` §mind_forge_recursive_integrity |

**Transfer summary:** 6 patterns CODIFY (PRL 8-9), 7 patterns ADOPT (PRL 6-7), 0 patterns EXPERIMENT or WATCH. Unusually high readiness — the mission brief was well-scoped and the six dossiers delivered high-grade convergent signal.

---

## §7 — Contradiction Matrix (Phase 5 ABSTRACT cross-dossier)

The 26 observed contradictions across 6 dossiers converge into 8 unique trade-offs at the mind-forge level. Duplicates (same contradiction in multiple targets = H3 convergence signal) are marked.

| ID | Improving | Worsens | Resolution | Source dossiers | Cross-dossier convergence |
|---|---|---|---|---|---|
| **CM-1** | Producer efficiency (close and move on) | Receiver trust in upstream grounding | Plural-field numeric admission payload + loop-not-degrade fallback | A1, A2, A3 | H3 (LAW-MF-4) |
| **CM-2** | Narrative richness of mind body | Decision-time activation of that content | Externalized matrix binding content to in-task checkpoints | A1 | Single target |
| **CM-3** | Depth per source dimension | Breadth across dimensions | Critical vs foundation layer asymmetric criticality | A5, A6 | Dual confirmation |
| **CM-4** | Fidelity floor for trust | Applicability to thin sources | Graceful degradation with 3-state labels | A5, A6 | Dual confirmation (G3 filled) |
| **CM-5** | Preserving source distinctiveness in fusion | Producing one coherent voice | Separate layers where distinctiveness lives (orthogonal dimensions via Productive Tension) from layer where unity is enforced (co-activation linguistic protocol at surface) | A3 | Single target but across 3 sub-protocols |
| **CM-6** | Mechanical automation of pipeline | Human authority over worldview conflicts | Escalate the irreducible, parallelize the resolvable (Destructive Tension packet) | A3 | Single target |
| **CM-7** | Producer creative freedom | Validation integrity | Worker-validator structural separation (not procedural) | A1, A2, A3, A4, A5 | **QUINTUPLE** — this is the most confirmed contradiction in the campaign; already Engine Clause II |
| **CM-8** | Library breadth | Per-entry depth | Fidelity maturity dial + composer reduced-fidelity warning + schema-enforced depth path only when complete | A4 | Single target |

**Synthesis.** CM-7 appearing in 5 of 6 dossiers is a strong signal that Clause II (Separation of Production and Judgment) is the most widely recognized discipline across the cognitive-systems field. CM-1 at triple confirmation is the handoff-contract LAW. CM-3 and CM-4 at dual confirmation anchor the fidelity and graceful-degradation patterns.

---

## §8 — Vault Cross-Reference Table

This section lists what the mind-forge architecture CONFIRMS, EXTENDS, and INTRODUCES against the 140 CANON MCS + 324 MI + 36 SD vault, honoring the prior-art discipline: before proposing a new pattern, the forge must declare what it confirms or extends from the vault.

### §8.1 — CONFIRMS (re-validates existing vault items as LAW)

| Vault item | Confirmation source |
|---|---|
| MCS-001 Falsification-First | L11 specificity test + A3 invisibility test |
| MCS-002 Uncertainty as Signal | L3 3-state provenance labels |
| MCS-003 Productive Tension / Named Trade-Offs | L6 four-valued relation taxonomy + CM-7 quintuple confirmation |
| MCS-005 Dual Mode / Discovery Before Structure | L1 origin test applied before forging begins |
| MCS-008 Source Fidelity / State-as-Truth | L3 graceful degradation + L11 specificity |
| MCS-009 Recursion as Self-Validation | **LAW-MF-5** third confirmation |
| MCS-058 Hub-and-Spoke Reference Pattern | A4 Pantheon 93% ambient-context reduction |
| MCS-072 Genius Layer Domain-Adaptive Kit | L9 origin-enum + genius_zone field |
| MCS-079 Reference Navigation Hygiene | A4 hub-and-spoke discipline |
| MCS-105..110 Calibration Tier Heuristics | L2 fidelity tiers + L5 critical-layer weights |
| MCS-111 Certainty Bands | L3 3-state provenance labels (reduced to binary admission gate) |
| MCS-121 Bestiary of 6 Anti-Patterns | L11 specificity test vs Theater; A4 10 anti-patterns as veto (extends 6 → 10) |
| MCS-130 Anti-Theater Detection | L11 specificity test |
| MCS-139 7-Layer Cognitive Architecture | L4 canonical retained with sibling variants |
| MI-008 Theatre of Agents | A6 5 internal sub-personas (Validator role confirms MI-008 quintet) |
| MI-014 N×N Compatibility Analysis | **LAW-MF-3** third confirmation |
| MI-015 Fusão Sinérgica | **LAW-MF-3** third confirmation (joint) |
| MI-018 Tolerance for Contradiction | L7 Destructive Tension distinguishes productive from destructive |
| MI-019 Meta-Recursion and Self-Application | **LAW-MF-5** joint confirmation |
| MI-022 Teste de Remoção | L11 specificity test |
| MI-129 Skill Composability L4+ contract | A4 6-contract interface formalism |
| SD-017 ORCHESTRATION.yaml 15-section | A4 6-contract formalism (sibling) |
| SD-023 QA Separation Principle | **CM-7 quintuple confirmation** (strongest contradiction convergence) |
| SD-016 7-Component Agent Payload | **LAW-MF-4** joint confirmation |
| SD-027 Handoff Contracts | **LAW-MF-4** joint confirmation |
| Symmetric-drift discipline (vault ancestor) | L12 default-optimistic initialization with mandatory downgrade epistemics operationalizes the principle at forge time |

### §8.2 — EXTENDS (adds operational detail to existing vault items)

| Vault item | Extension |
|---|---|
| MCS-072 Genius Layer | adds origin-enum orthogonal to genius/kryptonite axes |
| MCS-105..110 Calibration Tiers | adds critical-layer asymmetric floors + weighted formula |
| MCS-115 Cognitive Technique Matrix | adds A1 matrix-activation pattern (externalize latent content to decision checkpoints) |
| MCS-139 7-Layer Cognitive Architecture | adds sibling variants document + migration table |
| MI-014 N×N Compatibility | adds specific penalty schedule + abort threshold + 4 linguistic templates |
| MI-018 Tolerance for Contradiction | adds Destructive vs Productive distinction + escalation packet |
| MI-020 Completeness Checklist | adds dual-score gate with asymmetric floor |
| SD-002 Gate System G1-G4 | adds mechanical restart routing matrix (A2) + termination rule (A5) |

### §8.3 — NEW (introduces patterns not in vault)

- **L1 Operational Origin Test** — mechanical codex-field derivation of origin. No vault ancestor.
- **L6-L7 Four-Valued Relation Taxonomy + Destructive Tension Escalation** — linguistic-level fusion discipline. MI-013 covers per-mind voice extraction; this covers fusion-time anti-chimera. NEW.
- **L10 co-activation linguistic protocol (simultaneity markers mandatory, sequential markers banned, invisibility law)** — NEW. No vault item encodes fusion-time linguistic discipline at this granularity.
- **The SIF naming-vs-function inversion as negative evidence** — NEW operational insight. Future vault entry candidate.
- **Hot-load vs fresh-load discrimination at agent activation (A1 Step 1.5)** — NEW specialist activation branch. Future vault entry candidate.

---

## §9 — Four Structural Gaps — Declared and Assigned

The mission brief §8 declared 6 gaps. Five are filled. One remains open.

| Gap | Status | Filler or assignment |
|---|---|---|
| G1 artificial vs synthetic codex rule | **FILLED (inverted)** | L1 Operational Origin Test (derived at validate time, not declared in marketing) |
| G2 fusion failure modes as anti-patterns | **FILLED** | A3 5 named modes + remediation (dossier §5 pattern 8); transfer to `references/engine-mind-forge-architecture.md` §fusion_failure_modes (this section is a pointer) |
| G3 graceful degradation for thin sources | **FILLED** | L3 (A5 primary, A6 confirms) |
| G4 mind library indexing principle | **FILLED** | L9 (A4 primary) |
| G5 cross-system meta-taxonomy | **REMAINS OPEN** — synthesized a posteriori in §10 below | A6 explicitly rejects the role; main-thread synthesis required |
| G6 emula vs simula validation ritual | **FILLED** | A2 specificity test + behavioral manifestation (L11) |

Plus four new structural gaps surfaced during S125 (GRADUATION, SYMBIOSIS, HARVEST, COMPOSITION-2) are restated here for S127+ work:

- **GAP-COMPOSITION-1** (pre-existing, declared in `references/composition-anatomy.md`): now **FILLED** by L10 (plural-field admission payload, LAW-MF-4).
- **GAP-COMPOSITION-2:** when a hybrid fusion mind needs to collaborate with a team of artificial minds — is the fusion result a reusable primitive in a multi-mind team? A3 explicitly flags this as missing. **REMAINS OPEN — assigned to S128.**
- **GAP-GRADUATION:** when does a mind graduate from `pending` to `complete` status, and what is the promotion ritual? A4 has a 2-state dial; A5 has tier migration paths. Not yet canonical. **REMAINS OPEN — assigned to S129.**
- **GAP-SYMBIOSIS:** when two minds in a team influence each other's evolution over time. A4's REFLECT protocol partially covers this. **REMAINS OPEN — assigned to S129.**
- **GAP-HARVEST:** when insights from a forged mind's deployment flow back into the forge itself to improve the protocol. A2's meta-agent partially covers this. **REMAINS OPEN — assigned to S130.**

---

## §10 — Cross-System Meta-Taxonomy (synthesized a posteriori — closes G5)

The six source systems do not form a tidy hierarchy because they were built independently for different purposes. A6's honest hypothesis revision (the target is a sibling, not a meta-container) means no single system classifies the others. The meta-taxonomy below is therefore synthesized by the main thread across all 6 dossiers, observing their functional roles in the cognitive-systems ecosystem.

### §10.1 — Functional topology of the 6 source systems

| System | Primary function | Mind origins handled | Level of maturity |
|---|---|---|---|
| **A1 squad-creator-pro** | Team forge — produces coordinated specialist squads from extracted experts | artificial (via clones) | mature (v3.0) |
| **A2 SIF** | Single-mind factory for domain specialists | artificial (despite "synthetic" label) | mature (v1.2) |
| **A3 CFL** | Hybrid fusion lab — produces single-identity fused minds from ≥2 artificial minds | hybrid_fusion | mature (polish score 8.9/10) |
| **A4 Pantheon** | Mind library + composer — holds multi-origin minds and composes them into squads | all three | mature (v1.1, 42 entries) |
| **A5 MCL+MRA** | Paired research + crystallization pipeline for single artificial minds | artificial only | mature (v2.0 upstream) |
| **A6 mmos-standalone** | Single clone forge — siblings of A5 | artificial only | in development |

### §10.2 — Ecosystem role discrimination

Each system occupies a distinct functional cell:

| Cell | Role | Systems |
|---|---|---|
| **Forge (single mind)** | Extract or synthesize one cognitive architecture | A2, A5, A6 |
| **Forge (fusion)** | Compose two or more artificial minds into one hybrid | A3 |
| **Forge (team)** | Produce a multi-specialist team from extracted experts | A1 |
| **Library (holding)** | Index, store, invoke, and compose minds on demand | A4 |
| **Meta-container** | *None* — no source system fills this role; A6 hypothesis revised |

The Engine's role is the **Amplifier** — it is neither a specific forge nor a library nor a meta-container. It is the **standardized cognitive tooling substrate** that any creator can use to forge minds of any origin at Anthropic-grade fidelity using patterns distilled from all six sources.

### §10.3 — Why G5 has no native resolution

The six source systems were built by a single founder over years in response to specific problems. There is no meta-taxonomy because there is no meta-purpose — each system was scoped for a tactical need. The Engine is the first artifact that *could* be a meta-container, because its mission is precisely to standardize the forge patterns across origin types. The meta-taxonomy is therefore NOT an extract from any source — it is an **emergent property of the Engine itself when it operationalizes the LAWs in §4**.

**G5 is closed not by discovery but by construction:** the cross-system taxonomy IS the Engine's §4 five LAWs + §5 thirteen patterns applied to the three mind origins. The Engine's `product-dna/minds.yaml` after S127 refinement will *be* the meta-taxonomy, and its `product-dna/squad.yaml` after S127 refinement will *be* the composition meta-protocol.

---

## §11 — Four-Session Roadmap for Materialization

This document authors the architecture. Applying it to codices is separate work per Clause II.

| Session | Scope | Primary writes | Gates |
|---|---|---|---|
| **S127** | Apply refinement plans to `product-dna/minds.yaml` and `product-dna/squad.yaml` | Both codex files; new `references/structural-dna/cognitive-architecture-variants.md` | `/validate --level=3` PASS on both codices; drift-check PASS |
| **S128** | Apply quality-gate extensions for L1 (origin derivation), L3 (source adequacy), L10 (handoff contract), L11 (behavioral manifestation), L13 (mind-forge recursive integrity) | `quality-gates.yaml` new stages + 5 new check definitions | `/validate` self-test PASS on this document; arming tests for each new gate |
| **S129** | Close GAP-GRADUATION and GAP-SYMBIOSIS by extending `references/composition-anatomy.md` | composition-anatomy extension; migration tables for fidelity dials | GAP-COMPOSITION-2 partial fill if scope permits |
| **S130** | Close GAP-HARVEST; D40 remainder (agent.yaml, system.yaml, output-style.yaml, skill.yaml substrate voice drain) | 4 substrate-voice drains + delta log capture protocol | full substrate-voice perimeter at 13 files; D40 closure |

Session S127 is the earliest candidate to implement the refinement plans in `docs/sessions/S126/minds-codex-refinement-plan.md` and `docs/sessions/S126/squad-codex-refinement-plan.md` (authored alongside this document — see §12 cross-reference).

---

## §12 — Cross-References

### §12.1 — Authored in S126 (siblings of this document)

- `docs/distillation/squad-creator-pro-dossier.md` — A1 source dossier
- `docs/distillation/sif-dossier.md` — A2 source dossier
- `docs/distillation/cognitive-fusion-lab-dossier.md` — A3 source dossier
- `docs/distillation/pantheon-dossier.md` — A4 source dossier
- `docs/distillation/mental-clone-lab-dossier.md` — A5 source dossier
- `docs/distillation/mmos-standalone-dossier.md` — A6 source dossier
- `docs/sessions/S126/minds-codex-refinement-plan.md` — exact additions for `product-dna/minds.yaml` (S127 consumer)
- `docs/sessions/S126/squad-codex-refinement-plan.md` — exact additions for `product-dna/squad.yaml` (S127 consumer)
- `docs/handoffs/S126-mind-forge-architecture-handoff.md` — the session-seal document

### §12.2 — Inherited prior art (S126 consumed, not modified)

- `docs/frameworks/ALEMBIC.md` — the 9-phase distillation framework used
- `docs/frameworks/MICA-v2.md` — the consolidation discipline
- `docs/consolidated/INJECTION-MAP.md` — the Sprint 8 injection hotspots
- `docs/distillation/_MISSION-BRIEF-S126.md` — the scope contract
- `docs/distillation/s126-vault-inventory.md` — the ~240 vault items cross-reference
- All 8 `docs/consolidated/CANON-*.md` files — the 140 MCS arsenal
- All `docs/extracts/meta-intelligence*.md` files — the 324 MI items

### §12.3 — Engine substrate this document extends

- `product-dna/minds.yaml` — refinement plan authored, application in S127
- `product-dna/squad.yaml` — refinement plan authored, application in S127
- `references/composition-anatomy.md` — extension in S129
- `references/intent-topology.md` — unchanged in S126
- `references/capability-matrix.md` — unchanged in S126
- `quality-gates.yaml` — extension in S128

---

## §13 — P9 Recursive Self-Test

Per Clause VII Recursion as Validation: this document MUST pass its own methodology when applied to itself.

### §13.1 — Applying the 13 patterns to this document

- **L1 Operational Origin Test.** Does this document declare its origin operationally? YES — §1 declares it as an ALEMBIC-distilled synthesis from 6 source dossiers, not as a novel authorship.
- **L2 Fidelity Tiers.** Does this document declare its own fidelity tier? YES — the PRL assessments in §6 give explicit readiness levels per pattern, and §9 declares which gaps remain open.
- **L3 Graceful Degradation.** Does this document tag uncertain claims? YES — §10 explicitly declares G5 is closed "by construction not discovery"; §5.4 explicitly declares 3 sibling layer-count variants rather than collapsing them.
- **L4 7-Layer Architecture.** Does this document itself follow 7-layer architecture? PARTIAL — the document is structured but not layered per MCS-139; this is a pattern for mind codices, not for substrate documents, so the test does not apply directly.
- **L5 Critical-Layer Floors.** Does this document weight its claims? YES — LAW promotions in §4 are marked as LAW (critical); pattern cards in §5 are marked PRL (weighted); sibling variants in §10 are marked as "not hierarchy". 
- **L6-L7 Relation Taxonomy + Destructive Tension.** Does this document handle contradictions? YES — §7 Contradiction Matrix names 8 trade-offs with resolutions; the 7-vs-8 layer tension is treated as sibling prior art not destructive contradiction.
- **L8 Orchestrator-Led Composition.** Does this document show its orchestration? YES — the ALEMBIC 9 phases are the orchestration; Phases 2-4 were delegated to 6 agents; Phases 5-9 run in main thread.
- **L9 Origin-Enum Typed Library.** Does this document declare origin types? YES — §2 operationalizes all three.
- **L10 Plural-Field Admission Payload.** Does this document carry its own handoff admission? YES — this section §13 is the self-test; §11 is the handoff to S127; §12 is the cross-reference graph.
- **L11 Specificity Test.** Does this document pass the behavioral manifestation test? YES — every pattern card has a concrete Mechanism section with numbered steps; every LAW has a codex binding field.
- **L12 Default-Optimistic Downgrade Epistemics.** Does this document default to high claim + justified downgrades? YES — all 5 H3 candidates triggered at top tier with named evidence; G5 downgraded with written reason.
- **L13 Recursive Integrity.** This very section is the recursion. 

### §13.2 — Generativity Test applied to the document itself

"If a creator who has never seen the six source systems reads this document, can they naturally produce a mind codex that embodies these patterns?"

**Answer:** YES for the 6 CODIFY patterns (L1, L3, L8, L10, L11, L13), PARTIAL for the 7 ADOPT patterns (still require S127 codex wiring to be fully mechanical), and pending for the open gaps. The document is generative in §5 pattern cards and PRL assessments; it is *declarative but not yet mechanical* in the refinement plans (those are the S127 consumer's work).

### §13.3 — Delta log entry (one concrete improvement from this session)

The concrete improvement this session contributes to the Engine's operational discipline is recorded in the session handoff, where development-lineage observations belong. The substrate document records only the forge architecture itself — the history of how this architecture came to be lives in `docs/handoffs/S126-mind-forge-architecture-handoff.md` §4 meta-learnings. This separation is itself the discipline the architecture describes: substrate speaks in the present about the present; history lives in the handoff.

---

## §14 — Seal Statement

This document is sealed as the S126 canonical mind-forge architecture. It authors 13 formal pattern cards, 5 LAW promotions via H3 Convergence, answers all 13 global KIQs (with G5 closed by construction in §10), declares 5 additional structural gaps with session assignments, and provides a 4-session roadmap for materialization. It passes its own P9 recursive self-test per §13. The refinement plans at `docs/sessions/S126/minds-codex-refinement-plan.md` and `docs/sessions/S126/squad-codex-refinement-plan.md` are the S127 consumer artifacts; those files declare the EXACT section additions to be applied in a separate future session per Clause II Separation of Production and Judgment.

Authored: 2026-04-09 · Session: S126 · Framework: ALEMBIC v1.0 · Quality bar: Anthropic Grade

*"Six rivers enter. One confluence exits. The taxonomy stays. The intelligence deepens."*
