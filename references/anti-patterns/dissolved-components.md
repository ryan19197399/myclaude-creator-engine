# Dissolved Components — Anti-Pattern Registry

> **Layer:** substrate declaration. Consumed by `product-dna/minds.yaml` mind_forge_schema.A11_recursive_integrity.dissolved_component_policy.storage — this file is the storage target that policy points at.
>
> **Binding disciplines inherited:** Clause I (Source Fidelity — a deletion is a fact the organism paid in error to discover, and the organism speaks about it in the present), Clause IV (Named Trade-Offs — every dissolution entry names what was lost and what was gained), Principle P9 (Recursive Integrity — the forge remembers the components it removed so a future creator does not re-invent them under pressure).

---

## §1 — What this document is

The Engine evolves. As the Engine evolves, components get removed. A removed component is information: it tells a future creator that the Engine tried something, paid attention to how it behaved, and decided the cost of keeping it exceeded the cost of losing it. Without a registry of dissolutions, that information vanishes and the same component tends to be re-invented the next time the Engine meets the problem that originally motivated it.

This file is the registry. Every component the Engine removes during evolution gets a named entry here, structured so a future creator can find the reason the removal happened, the replacement (or the declared gap), and the re-invention signature that would cause someone to propose the removed component again.

The file is empty of entries at the moment of its first authoring — no component has yet been formally dissolved under this policy. The schema declaration and the worked example below establish the shape that entries take when the first dissolution is processed. The policy begins to operate on removals that happen after this file exists; historical removals are not retroactively cataloged, because retroactive cataloging without the paired evolution notes produces narrative rather than record.

---

## §2 — The dissolved-component schema

Every entry in this file declares exactly five fields, in this order. The order matters — a reader looking up a dissolution in a hurry reads the name first, the function second, the reason third, and only goes deeper if they need to understand whether their current proposal is a re-invention.

### §2.1 — Field 1: `original_name`

The name the component had while it existed, verbatim. If the component had multiple names over its lifetime, all of them are listed with the canonical one marked. A reader searching for "that thing I remember we once had" needs to be able to find the entry by any name it was called.

### §2.2 — Field 2: `function`

One sentence describing what the component did while it existed, in the organism's own present-tense voice adapted to past. Not what it was supposed to do — what it actually did during the period it was in use. The distinction matters because a component often dissolves precisely because intended function and actual function drifted apart.

### §2.3 — Field 3: `reason_for_removal`

One paragraph naming why the component was removed. The paragraph must name:

- **The observed cost** the component imposed (token load, maintenance burden, coupling that prevented a desired change, a recurring mistake the component made).
- **The observed benefit** the component provided (the reader needs to know what was lost, not just what was gained by losing it).
- **The tipping-point observation** that changed the cost-benefit from "worth keeping" to "worth removing". A dissolution is an event, not a gradient; the entry names the event.

### §2.4 — Field 4: `replacement_or_declared_gap`

Exactly one of two forms:

- **`replacement`** — the name of the component that now covers the function the dissolved component used to cover, plus a one-sentence note on how the replacement handles the function differently. If the replacement handles only part of the function, the entry names the part it covers and treats the uncovered part as a declared gap.
- **`declared_gap`** — the name of the function that is no longer covered by any component in the Engine, plus a one-sentence note on why the gap is acceptable. A gap is acceptable only when the reason the function was needed has itself dissolved, or when the function is now delegated to a different layer of the stack (the creator, another tool, an external process).

Both forms are allowed but exactly one must be present. A dissolution without a declared replacement or gap is incomplete and blocks the /validate recursive integrity check.

### §2.5 — Field 5: `re_invention_signature`

The signal that a future creator is about to re-invent the dissolved component without realizing it. This is the most important field in the entry, because it is what the registry exists to prevent.

The signature is a short, concrete description of the pattern a creator would propose if they met the original problem without knowing the dissolution history. The signature lives in the registry so that a reviewer — or a future creator doing prior-art scan — can cross-reference a new proposal against the signature and notice the collision.

A good re-invention signature names the architectural move, not just the name. Naming the architectural move ensures that a creator proposing the same idea under a different name still triggers the match.

---

## §3 — Worked example: the Phantom Component pattern

No component has been dissolved under this policy yet. An entry shape is shown below as a template, using a documented case from the wider practice — a published cognitive library that dissolved a component it had originally proposed and recorded the dissolution as a named anti-pattern. The template is marked as illustrative so readers do not mistake it for a real Engine dissolution.

```yaml
# ILLUSTRATIVE TEMPLATE — not an actual Engine dissolution
# Shows the entry shape using a documented case from the wider practice
# This entry becomes real only when the first Engine component is formally dissolved

entry_id: TEMPLATE-01
original_name:
  canonical: "Convergence Engine"
  also_known_as: []
  status: illustrative_template

function: |
  The Convergence Engine was declared as a standalone component responsible for
  merging the outputs of multiple cognitive sub-agents into a single coherent
  response, treating the merge as a distinct layer of the architecture with its
  own state and its own validation rules.

reason_for_removal: |
  Observed cost: the component grew into a parallel reasoning engine that
  shadowed the work of the sub-agents it was supposed to merge, producing a
  second-order cognition layer whose outputs no downstream consumer trusted.
  Observed benefit: the explicit merge step was easier to audit than an
  implicit merge would have been — a reader could point at the component and
  see where the synthesis decision was made. Tipping-point observation:
  during a routine review, the component was found to be contradicting the
  sub-agents it was supposed to merge, producing a synthesis that no
  individual sub-agent had proposed and that no quality gate could verify
  against a source. The component was no longer a merger; it had become a
  competitor. It was removed the same session.

replacement_or_declared_gap:
  form: replacement
  replacement_name: "disagreement-first synthesis protocol built into the orchestrator body"
  note: |
    The orchestrator no longer has a dedicated merge component. It carries a
    synthesis protocol declaration in its own body: dissenting positions are
    listed first, convergent positions second, the final recommendation third,
    with named trade-offs attached. The protocol runs as part of the
    orchestrator's normal output synthesis layer rather than as a separate
    component, which eliminates the shadow-cognition failure mode while
    preserving the auditability benefit.

re_invention_signature: |
  A creator proposes a new standalone component responsible for "merging",
  "synthesizing", "converging", or "integrating" the outputs of multiple
  reasoning sub-agents, and treats the merge as a layer with its own state.
  The signature fires regardless of the proposed name — the architectural
  move is "promote the merge from a protocol to a component", and that move
  is the one this entry exists to flag. A reviewer encountering the
  proposal should open this file, read the template above, and ask the
  creator to justify why the proposal does not reproduce the failure mode
  the template describes.
```

---

## §4 — How entries are added

A component dissolution that qualifies for an entry in this file meets all three of the following conditions:

1. **The component existed in a sealed state of the Engine.** A proposal that was discussed and rejected before reaching a sealed state is not a dissolution — it is a discarded option, and it lives in the session record, not here. A dissolution concerns something that was real.

2. **The removal was deliberate.** A component that disappeared because a refactor accidentally orphaned it is a bug, not a dissolution. The entry criterion requires that the removing session named the removal as an intentional act and declared at least the `reason_for_removal` and `replacement_or_declared_gap` fields inline in that session's record.

3. **The re-invention risk is real.** Some components dissolve into the background of the Engine without leaving a pattern anyone would re-propose. A trivially specific helper that was deleted because its one call site moved does not need an entry. The re-invention signature field is the test: if the entry's re-invention signature reads as an obvious architectural move that any thoughtful creator might propose, the dissolution qualifies. If the signature requires a long explanation to describe a pattern no one would naturally re-propose, the dissolution does not qualify.

Entries are appended in chronological order by sealed dissolution. Each entry carries an `entry_id` of the form `DSN-NN` (Dissolution Number, zero-padded) assigned by the session that authors the entry. The ID is permanent — entries are never renumbered.

Entries are never deleted from this file. A dissolution that turns out to have been wrong — the dissolved component is reinstated in a later session — produces a new entry below the original, not a removal of the original. The original entry remains as the record of what was tried and why the trial ended, even if the trial was eventually reversed. A reinstatement entry carries a back-reference to the original and names the second tipping-point observation that motivated the reversal.

---

## §5 — What this file does not do

This file is a registry, not a governance document. It does not:

- **Decide which components should be dissolved.** That decision lives with the session that proposes the dissolution, defended against Clause IV (named trade-offs) and Clause V (rigor over ergonomics). This file records the decision; it does not make it.
- **Serve as a veto on new proposals.** A proposal that matches a dissolved component's re-invention signature is not automatically rejected — it is flagged for review. A second iteration of the same idea might be warranted if the surrounding architecture has changed enough that the original failure mode no longer applies. The signature triggers scrutiny, not refusal.
- **Replace the session handoff record.** A dissolution is discussed in full in the session that enacts it; the handoff for that session carries the complete reasoning. This file carries the structured registry entry that survives after the handoff has passed out of fresh context. Both records exist; neither is a substitute for the other.
- **Carry retroactive entries.** Components that were removed before this file existed are not cataloged retroactively. Retroactive cataloging without the paired session context produces narrative rather than record, and narrative is not what Clause I asks for from substrate. The policy operates forward from this file's creation.

---

## §6 — Cross-references

- `product-dna/minds.yaml` → `mind_forge_schema.A11_recursive_integrity.dissolved_component_policy.storage` — the field that points at this file
- `product-dna/minds.yaml` → `mind_forge_schema.A11_recursive_integrity.dissolved_component_policy.rationale` — the sentence that declares why deletions get stored as named anti-patterns
- `references/engine-mind-forge-architecture.md` §4.5 — LAW-MF-5 (the forge must pass its own methodology when applied to itself), which is the constitutional source of the dissolution policy
- `references/engine-mind-forge-architecture.md` §5.13 — the L13 pattern card for recursive integrity that names dissolved components as one of the five concrete mechanisms the discipline uses

---

*This file is the storage declared by A11 of the mind-forge schema. It begins empty of actual entries and holds the shape that entries take when the first dissolution is processed. The forge that forgets what it has removed will re-invent the removals under pressure; the forge that remembers has one less way to drift.*
