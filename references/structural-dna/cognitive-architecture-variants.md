# Cognitive Architecture Variants

> **Layer:** substrate declaration. Consumed by `product-dna/minds.yaml` mind_forge_schema.A4_cognitive_architecture_canonical.alternative_decompositions.documented_at, by the /validate warning that fires when a codex entry uses an alternative decomposition without a translation table, and by the SELF-CLONE forge protocol when it needs to name which decomposition it populates.
>
> **Binding disciplines inherited:** Clause I (Source Fidelity), Clause IV (Named Trade-Offs), Clause V (Rigor > Ergonomics), Principle P4 (Contract Before Narrative), Principle P8 (Invisibility of Mechanism). The marketplace taxonomy is unchanged — this document refines one operational detail of the mind codex, nothing else.

---

## §1 — What this document declares

The Engine adopts a canonical cognitive architecture with seven layers and seven DNA strands. A creator who prefers a different decomposition may use one of the three alternative decompositions declared below — each maps back to the canonical via an explicit translation table. A codex entry that uses an alternative must declare the mapping; `/validate` emits a warning (not a block) pointing at this file when a non-canonical decomposition is detected.

This document does not introduce a new architecture. It names the canonical, documents three alternatives already observable in the wider cognitive-architecture practice, and provides the translation tables so that no creator has to choose between structural fidelity and the freedom to think in the decomposition that fits their domain.

It also declares which alternative is the canonical target of the SELF-CLONE forge protocol — a single forward reference from this document to a protocol that is authored separately, preserving Clause II separation of authoring from application.

---

## §2 — The canonical: seven layers, seven DNA strands

The canonical decomposition lives in `product-dna/minds.yaml` under `cognitive_architecture.layers` and `cognitive_architecture.dna_strands`. This document summarizes it — the codex remains the source of truth.

### §2.1 — The seven layers

| Layer | Name | Primary responsibility |
|---|---|---|
| L1 | boot | Startup discipline, session initialization, activation protocol. The layer that fires before any substantive reasoning and establishes the operating state. |
| L2 | cognitive_core | Reasoning patterns, mental models, the architecture of thought itself. The layer where the mind does its work. |
| L3 | personality_engine | Voice, affect, calibration, the recognizable texture of the mind. What makes this mind sound like this mind rather than any other. |
| L4 | knowledge_domains | Domain-specific knowledge bases, subject matter the mind treats as load-bearing. What the mind knows, indexed by territory. |
| L5 | reasoning_engine | Inference strategies, decision-making protocols, the named procedures the mind runs when it reaches a fork. How the mind chooses. |
| L6 | metacognition | Self-awareness, confidence signaling, the internal monitor. The layer that notices when the mind is operating outside its reliable zone. |
| L7 | output_synthesis | Integration of the prior six layers into a single user-facing response. The layer where everything collapses into the message that ships. |

### §2.2 — The seven DNA strands

| Strand | Name | What it guards |
|---|---|---|
| C1 | intent_recognition | Reading what the user actually wants, not what the request literally says. |
| C2 | context_awareness | Tracking which state is live, which is stale, which belongs to a different conversation. |
| C3 | reasoning_chain | The audit trail from inputs to conclusion, readable after the fact. |
| C4 | uncertainty_quantification | Naming confidence explicitly rather than defaulting to assertive phrasing. |
| C5 | self_correction | Catching and revising mistakes without being asked. |
| C6 | meta_reflection | Observing the mind's own operation and flagging patterns worth changing. |
| C7 | output_calibration | Matching the register and shape of the output to the consumer of the output. |

### §2.3 — Why this is the canonical

Three reasons operational, not hierarchical.

**First — boot discipline as first-class.** L1 boot is the only layer among the four decompositions in this document that treats startup discipline as a named layer rather than an assumed precondition. A cognitive architecture that does not declare its startup routine tends to drift in session-persistent contexts. Making boot a layer forces the mind to declare what it reads and verifies before reasoning begins. This alone justifies seven layers over six.

**Second — reasoning engine as first-class.** L5 reasoning_engine is explicit about the procedures the mind runs at decision points. The three alternatives below fold reasoning into either "cognitive processing" (A2 variant) or "decision architecture" (A5 variant) or "cognitive layer" (A6 variant) — each of those collapses inference strategy into a broader container. The canonical keeps the container split so that the named procedures can be validated independently.

**Third — the strands are orthogonal to the layers.** A two-axis schema (seven layers × seven strands) produces a 49-cell matrix that can be validated cell by cell. The alternative decompositions collapse the strands into the layers, which is simpler to diagram but harder to audit. Engine discipline prefers auditability.

The seven layers are the target of every forged mind's cognitive architecture declaration; the seven strands are the invariants the /validate cognitive fidelity scoring rubric scores against. Both live unchanged in `product-dna/minds.yaml cognitive_architecture` — the codex is the source of truth and this document is a consumer of it.

---

## §3 — Alternative decomposition: content-oriented seven layers (variant A)

**Observed shape in the wider practice.** A single-mind extraction factory models cognitive architecture as seven layers organized by the kind of content each layer holds: Knowledge → Cognitive Processing → Execution → Personality → Context → Meta-Cognitive → KB Integration. This variant treats architecture as a content ontology — every layer is a different category of thing the mind carries.

### §3.1 — The seven content layers

| Variant layer | Content category |
|---|---|
| Knowledge | Subject-matter facts, procedural knowledge, domain vocabulary |
| Cognitive Processing | Reasoning patterns that operate on the knowledge |
| Execution | Action protocols, how the mind moves from decision to output |
| Personality | Voice, tone, affect, the recognizable surface texture |
| Context | Situational awareness, what the mind is tracking right now |
| Meta-Cognitive | Self-reflection, confidence monitoring, bias detection |
| KB Integration | How external knowledge bases plug into the mind |

### §3.2 — Translation table, variant A → canonical

| Variant A layer | Canonical target | Mapping note |
|---|---|---|
| Knowledge | L4 knowledge_domains | Direct mapping. |
| Cognitive Processing | L2 cognitive_core + L5 reasoning_engine | Splits into two canonical layers — the canonical separates the substrate of thought (L2) from the named procedures (L5) that operate on it. |
| Execution | L7 output_synthesis | Direct mapping with a wider scope — the canonical treats execution as the point where the prior layers collapse into a single response. |
| Personality | L3 personality_engine | Direct mapping. |
| Context | C2 context_awareness strand | The variant models context as a layer; the canonical models it as a strand that operates across layers. A creator using variant A must either promote context to a strand or declare that their mind has a dedicated context layer outside the canonical seven. |
| Meta-Cognitive | L6 metacognition + C6 meta_reflection strand | Splits into the layer (what the mind monitors) and the strand (how the monitor is audited). |
| KB Integration | L4 knowledge_domains (as an access pattern) | The variant treats KB integration as a distinct layer; the canonical treats it as an access modality of L4 that the codex describes via the knowledge_base field. |

### §3.3 — When variant A fits

Variant A fits when the creator's natural decomposition is content-centric: the creator first lists everything the mind needs to hold, and only then thinks about how the holdings interact. This is a reasonable starting point for a mind whose primary value is encyclopedic depth in a single domain. Creators from knowledge-engineering backgrounds often reach for this shape first.

### §3.4 — When variant A fails

Variant A fails when the creator needs to declare reasoning strategies independently of the knowledge they operate on. Because variant A folds reasoning into Cognitive Processing, the codex cannot point at a named inference procedure without also pointing at the knowledge the procedure consumes. This couples audits that should be independent.

---

## §4 — Alternative decomposition: extraction-depth eight layers (variant B)

**Observed shape in the wider practice.** A paired research plus crystallization pipeline models cognitive architecture as eight layers organized by extraction depth — from surface linguistic markers down to the deepest cognitive invariants. Layers: Linguistic Surface → Pattern Recognition → Master Mental Models → Decision Architecture → Values → Obsessions → Singularity → Productive Paradoxes. This variant treats architecture as a descent: each layer goes deeper into what the mind fundamentally is.

### §4.1 — The eight extraction-depth layers

| Variant layer | Depth territory |
|---|---|
| Linguistic Surface | Vocabulary, characteristic phrases, the audible signature of the mind |
| Pattern Recognition | Recurring metaphors, analogies, cross-domain mappings the mind reaches for |
| Master Mental Models | The 3-5 lenses through which the mind filters every substantive problem |
| Decision Architecture | The 5-10 recognizable patterns of choice under constraint |
| Values | The 5-7 commitments the mind would not compromise |
| Obsessions | The 3-5 questions the mind cannot stop thinking about |
| Singularity | The uncompressible core — what makes this mind not substitutable |
| Productive Paradoxes | The 3-5 tensions the mind holds together as generative force |

### §4.2 — Translation table, variant B → canonical

| Variant B layer | Canonical target | Mapping note |
|---|---|---|
| Linguistic Surface | L3 personality_engine (vocabulary + voice) | The variant names linguistic signature as a standalone layer; the canonical treats it as content inside L3. |
| Pattern Recognition | L2 cognitive_core (metaphors as reasoning primitives) | The variant promotes recurring metaphors to a layer; the canonical treats them as an operating mechanism of L2. |
| Master Mental Models | L2 cognitive_core + L5 reasoning_engine | Master models cross L2 (the models themselves) and L5 (how they are selected at decision time). |
| Decision Architecture | L5 reasoning_engine (named procedures) | Direct mapping. |
| Values | L3 personality_engine (inviolable preference set) + critical-layer floor in fidelity_declaration | Values are both a personality attribute and a critical fidelity dimension — the mapping spans the canonical layer and the separate fidelity formula. |
| Obsessions | L2 cognitive_core (persistent question set) | The variant treats obsessions as a structural layer; the canonical treats them as a persistent driver inside L2. |
| Singularity | L3 personality_engine (uncompressible core) + critical-layer floor | Same pattern as values — both a personality attribute and a fidelity invariant. |
| Productive Paradoxes | L2 cognitive_core (tension-held reasoning) + critical-layer floor | Paradoxes are a cognitive operating mode and a fidelity invariant simultaneously. |

### §4.3 — When variant B fits

Variant B fits when the creator is producing an artificial mind whose origin is a specific human or a specific body of work, and the extraction problem is the primary challenge. The eight layers are organized as a descent — the creator extracts from the outside in, starting with the audible vocabulary and ending with the inarticulable singularity. This shape matches the natural workflow of the extraction rather than the natural shape of the finished mind.

### §4.4 — When variant B fails

Variant B fails when applied to an origin other than artificial. A synthetic mind built from a declared purpose has no linguistic signature to extract at the surface layer, so the descent begins from nothing. A hybrid fusion mind composed from multiple artificial sources has multiple linguistic surfaces that must be blended rather than descended through. Variant B is a natural fit for exactly one origin and must be retranslated to the canonical for the other two.

### §4.5 — Variant B is the decomposition target of the SELF-CLONE forge

The SELF-CLONE forge protocol — a guided methodology that turns a creator's own reasoning into an installable cognitive clone whose origin is artificial with the creator as the sole human referent — populates the eight layers of variant B as its canonical target shape, then maps those eight layers back to the canonical seven via the translation table in §4.2 before writing the codex entry.

The reasoning is direct: the eight dimensional target counts declared in `product-dna/minds.yaml` mind_forge_schema.A6_artificial_mind_schema.dimensional_profile (distinctive_terms, recurring_metaphors, master_mental_models, inviolable_values, core_obsessions, productive_paradoxes, unique_sensors, decision_signatures) are nearly isomorphic to variant B's eight layers, with decision_signatures joining as the eighth extraction axis alongside paradoxes. A creator running SELF-CLONE against themselves fills the eight dimensional counts, which populate variant B, which translates back to the canonical seven layers. The canonical remains the sealed target; variant B is the operational path that walks there.

The canonical SELF-CLONE forge protocol is authored at `references/self-clone-forge.md`. That document declares the two operational modes (distillation-first and elicitation-first), the five honesty floor gates, the typology-at-end convention, the dimensional routing algorithm, and the fidelity contract. This section names the decomposition the protocol consumes; the protocol document names the elicitation procedure — neither crosses into the other's scope, honoring Clause II separation.

---

## §5 — Alternative decomposition: lifecycle eight layers (variant C)

**Observed shape in the wider practice.** A single-clone forge models cognitive architecture as eight layers organized by runtime lifecycle — the stages through which a mind passes during its operational existence rather than the static contents it holds. Layers: Identity → Context → Cognitive → Methodology → Metacognition → Persona → Communication → Evolution. This variant treats architecture as a process signature: what happens across the lifetime of an invocation.

### §5.1 — The eight lifecycle layers

| Variant layer | Lifecycle stage |
|---|---|
| Identity | Boot-time identity assertion — who the mind is, before any task runs |
| Context | Situation ingestion — what is in the environment right now |
| Cognitive | Active reasoning — the core processing while a task runs |
| Methodology | Named procedures invoked during the reasoning |
| Metacognition | Self-monitoring during and after reasoning |
| Persona | Voice rendering during output synthesis |
| Communication | Message shaping for the specific consumer |
| Evolution | Post-session learning that writes back to the mind's own definition |

### §5.2 — Translation table, variant C → canonical

| Variant C layer | Canonical target | Mapping note |
|---|---|---|
| Identity | L1 boot | Direct mapping with widened scope — the canonical boot layer also initializes identity. |
| Context | C2 context_awareness strand | The variant treats context as a layer; the canonical treats it as a strand operating across all layers. |
| Cognitive | L2 cognitive_core | Direct mapping. |
| Methodology | L5 reasoning_engine (named procedures) | Direct mapping. |
| Metacognition | L6 metacognition + C6 meta_reflection strand | Splits into the layer and the strand, mirroring variant A's treatment of the same territory. |
| Persona | L3 personality_engine | Direct mapping. |
| Communication | L7 output_synthesis | Direct mapping with widened scope — the canonical treats communication as the final collapse into user-facing form. |
| Evolution | C5 self_correction strand + delta log discipline | The variant promotes evolution to a layer; the canonical treats session-to-session learning as a strand plus an external discipline (the delta log written at session seal). |

### §5.3 — When variant C fits

Variant C fits when the creator is thinking operationally about what happens while the mind runs rather than structurally about what the mind holds. Creators with a strong runtime or execution background tend to reach for this shape — the lifecycle view matches how they debug and profile a system under load. It is the most process-native of the three variants.

### §5.4 — When variant C fails

Variant C fails when the creator needs to declare a static invariant that does not fit naturally into a lifecycle stage. Values are the clearest case: a value is not a runtime event, it is a structural commitment that binds every runtime event. Variant C has no clean home for values, so creators using it end up folding values into Identity or Persona — both of which dilute the runtime-centric framing the variant exists to provide.

---

## §6 — Migration rule

A codex entry that uses an alternative decomposition must declare the mapping to the canonical explicitly, in-line, using the translation table from the relevant variant section above. The declaration lives in the codex entry's `cognitive_architecture_declaration` field and names three things:

1. **Which variant is in use** — variant A, B, or C, by the letter and the name from this document.
2. **Which variant layers populate which canonical layers and strands** — copied from the translation table, with the creator's specific content substituted.
3. **Which variant layers have no clean canonical mapping** — explicitly declared as gaps the creator has resolved by a named choice, with the choice documented.

`/validate` at stage 4 (DNA tier 2) checks for the declaration and emits a warning when a non-canonical decomposition is detected without a translation. The warning is not a block — the canonical permits variants, it does not forbid them. The block fires only when the variant is used without any declaration, because that is the case where an auditor cannot recover the canonical mapping from the codex alone.

The migration rule is one-way: a codex entry may declare a variant and map to the canonical, but the canonical itself is not edited. The seven layers and seven strands are the sealed target; the variants are documented recognitions of other valid decompositions that creators bring to the Engine and want to keep thinking in.

---

## §7 — Why three variants and not four, five, or none

A catalog of one canonical plus three alternatives reflects three operational pressures held in balance.

**Why not zero alternatives.** A creator who naturally thinks in variant A, B, or C would be forced to translate their thinking into the canonical before they could begin encoding a mind. Translation under creation pressure is where fidelity gets lost. The alternatives exist so that a creator can start in their native decomposition and translate at the end, when the translation has time to be careful.

**Why not more alternatives.** Every additional variant adds a translation table, a mapping audit, and a documentation burden. The three variants above were chosen because each represents a distinct organizing principle — content (A), depth (B), lifecycle (C) — and together they span the observable range of how practitioners decompose cognitive architecture in the wider field. A fourth variant would need to introduce a new organizing principle, not just a new layer count.

**Why not a single universal format.** The canonical is not a universal format. It is the Engine's sealed target shape. A universal format would erase the distinction between the canonical and the variants, which would remove the load-bearing discipline that the canonical holds primacy while the variants are documented recognitions. The variants are not equals — they are alternative decompositions that map back to the canonical, and the canonical never maps to them.

---

## §8 — Open items and future extensions

Two items are declared open in this document and assigned to specific future work.

**First — the SELF-CLONE forge protocol is now authored.** §4.5 names variant B as the SELF-CLONE decomposition target. The canonical protocol is at `references/self-clone-forge.md` — the reciprocal back-reference in §4.5 is now live. The Clause II separation is honored: this document names the target shape, the protocol document names the procedure.

**Second — the possibility of a fourth variant.** If the wider practice surfaces a genuinely new organizing principle — not a new layer count within one of the three existing principles — this file may be extended with variant D. The discipline is binding: a new variant is added only when the organizing principle is demonstrably distinct from content, depth, and lifecycle, and when the addition is justified by observed creator pressure that the three existing variants cannot absorb through translation.

Neither open item blocks the migration rule, the translation tables, or the canonical declaration. Both are forward-only extensions.

---

## §9 — Cross-references

- `product-dna/minds.yaml` → `cognitive_architecture.layers` (the canonical L1-L7)
- `product-dna/minds.yaml` → `cognitive_architecture.dna_strands` (the canonical C1-C7)
- `product-dna/minds.yaml` → `mind_forge_schema.A4_cognitive_architecture_canonical.alternative_decompositions.documented_at` (the field that points at this document)
- `product-dna/minds.yaml` → `mind_forge_schema.A6_artificial_mind_schema.dimensional_profile` (the eight target counts that variant B populates)
- `references/engine-mind-forge-architecture.md` §5.4 — the L4 pattern card that declares the canonical and names the three alternative decompositions this document elaborates
- `references/engine-mind-forge-architecture.md` §4.1 (LAW-MF-1) — the dimensional genome template binding on artificial minds
- `references/self-clone-forge.md` — the canonical SELF-CLONE protocol that populates variant B (reciprocal back-reference from §4.5)

---

*Authored as the A4 consumer artifact. Canonical unchanged. Variants named. Translation tables explicit. One forward reference to the SELF-CLONE forge whose protocol is authored separately per Clause II.*
