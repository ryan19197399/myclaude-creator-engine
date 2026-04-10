# Composition Anatomy — How the Three Axes Compose and Where They Don't

This document explains how `delivery_mechanism × operational_nature × cognitive_depth` compose into habitable cells, why some cells are orphan (no forge path exists), and what structural composition looks like when it does exist. It is the substrate behind the 7 v1 habitable cells and 12 v2 deferred cells in `references/intent-topology.md` §4-§5.

**Layer:** Canonical substrate. Consumed by `.claude/skills/create/` during Step 9 (LOOKUP_CANONICAL_CELL) when a match candidate lives in the grey zone between single-type cells and multi-type compositions. Also read by `.claude/skills/validate/` Stage 0 Intent Coherence when a product's `intent_declaration` declares a composition and the validator needs to know whether the composition is forgeable.

**Reading order:** §1 the three axes recap → §2 why composition is the hard problem → §3 the composition taxonomy → §4 habitable compositions in v1 → §5 orphan cells and GAP-COMPOSITION-1 → §6 what v2 unlocks.

---

## §1 — The Three Axes Recap

From `references/intent-topology.md` §2, the three transversal axes are:

- **Delivery mechanism** (6 values): `ambient_constitutional`, `ambient_path_scoped`, `invoked_slash_command`, `invoked_task_spawn`, `reflex_hook_binding`, `composed_system`.
- **Operational nature** (4 primitives): `executor`, `advisor`, `orchestrator`, `observer`.
- **Cognitive depth** (3 values): `procedural`, `advisory`, `cognitive`.

The cartesian product is 6 × 4 × 3 = 72 theoretical combinations. The topology declares 7 habitable v1 cells and 12 deferred v2 cells — 19 cells total out of 72 theoretical positions. The remaining 53 positions are either physically impossible (the platform does not allow them) or structurally meaningless (the combination has no coherent use case). This document explains which is which and names the cases where composition across types would unlock new cells but no forge path exists yet.

**The three axes are transversal**, meaning an artifact can live on any combination of values without its type predetermining the values. A skill can be procedural, advisory, or cognitive. An advisor can live inside a skill, an agent, a mind, or a hook. A cognitive architecture can be delivered ambient or spawned. This transversal structure is exactly what the flat 13-type menu hid — and exactly what the discovery-mode rewrite exposes.

**What the axes do not cover.** Two more properties matter for forge decisions and are intentionally not axes: (a) composition arity (single-type vs multi-type), and (b) install destination (local vs marketplace). These are not axes because they do not determine the runtime shape of a single artifact; they determine how multiple artifacts are bundled and distributed. Both are handled at the `composed_system` delivery value and at the `/package` stage, not at the cell lookup stage.

---

## §2 — Why Composition Is the Hard Problem

Single-type cells are tractable. The algorithm picks a type (skill, agent, minds, hooks, claude-md, statusline, output-style, design-system, workflow, squad, system, bundle, application), applies the three axes, and gets a canonical form. The forge path is well-trodden — `/create {type}` with the appropriate sub-type argument scaffolds the product, `/fill` walks the sections, `/validate` runs the gates, `/package` prepares distribution, `/publish` ships.

Composition is where the algorithm meets the edge of what the current forge can build. A capability expressed in creator intent may naturally require two or more types working together — a hook that spawns a mind, a skill that triggers an agent, a claude-md fragment that declares a constitutional contract for a skill bundle. These compositions are structurally sound (the Claude Code platform allows them; the 6 certified codices can describe them) but the Engine's `/create` skill has no single path that forges a multi-type product in one motion.

This gap is named explicitly as **GAP-COMPOSITION-1** in §5 below. Naming it matters because silent gaps drive creators into the exact trap the discovery-mode rewrite exists to eliminate: choosing the wrong single type because the right multi-type composition is not available. A creator who wants "a hook that observes and a mind that reflects" will, today, be forced to build either (a) a hook alone and feel the output is shallow, or (b) a mind alone and feel it lacks reactivity. Both feel wrong because neither is right. The right answer is composition, and composition is not yet forgeable in one motion.

The topology handles this by routing would-be multi-type cells to the v2 deferred set with an explicit `blocked_by: GAP-COMPOSITION-1` marker. The `/create` regression suite does not test against them — they are documented, not denied. When the multi-type forge path is unlocked, those cells are promoted from v2 to v1 via an additive wave, not a rewrite.

---

## §3 — The Composition Taxonomy

Not all compositions are equal. This section distinguishes three classes, each with a different structural shape and a different relationship to the current forge.

### §3.1 — Class A: Intra-Type Composition (forgeable in v1)

Two or more instances of the same type composed inside one product. The canonical example is a **squad**: multiple agents coordinated by a squad orchestrator, all delivered as one installable bundle. Another is a **bundle**: multiple published products of mixed types composed into one install but with no runtime coordination between them.

**Shape:** one codex covers the composition (`squad.yaml` for squads, `bundle` handling in the package pipeline for bundles). One forge path exists (`/create squad`, `/package` with bundle flag).

**Why this is tractable.** The composition is a first-class concept in the codex that governs it. Squads know about multi-agent orchestration because the squad codex declares the patterns; bundles know about multi-product packaging because the package pipeline was built for it. Intra-type composition does not cross codex boundaries — which is what makes it forgeable in v1.

### §3.2 — Class B: Bundled Multi-Type Composition (forgeable in v1 via system)

A capability that requires multiple different types coexisting as one reversible install — CLAUDE.md fragment + agents + squads + hooks + output-style, all dispatched to their respective destinations when the creator runs `myclaude install {slug}`. This is exactly what the **system** primitive handles.

**Shape:** the system codex (`product-dna/system.yaml`, certified S118c) declares the `install_manifest` structure that routes each sub-part to its correct destination. The creator forges the system as one product; the installer splits it at install time. The runtime composition happens at the moment of install, not at forge time.

**Why this is tractable.** System is the composed primitive — its entire purpose is to coordinate multi-destination install. The apex system archetype (`cognitive_organism`) explicitly allows cognitive minds inside the composition, which means a system can include a mind, a hook, a skill, and a claude-md fragment in one install. The constraint is that the composition is declared as a **system**, not as any of the individual sub-types — which means creators who want the composed shape must choose the system form, not the mind form or the hook form.

**What this does not handle.** A creator who wants a hook and a mind *without* wanting to think about it as a system. From the creator's perspective, they want two tools that work together, and being forced to wrap the composition in a system feels heavy. System exists for cases where the composition is explicit and named; it is less good for cases where the composition is implicit and emergent. That distinction is what Class C covers.

### §3.3 — Class C: Implicit Multi-Type Composition (orphan in v1 — GAP-COMPOSITION-1)

A capability expressed in intent that naturally spans two types, where the creator is not thinking about a system but about "two things that work together". The canonical example from `references/intent-topology.md` §5 is `longitudinal_observer`: a hook that observes commits and a mind that reflects on the accumulated observations. The creator's intent is *"watch for patterns across sessions"*. The natural shape is hook + mind, with the hook feeding observations into memory and the mind reading memory on invocation.

**Shape:** no single codex covers this. The hooks codex knows about hook handlers but not about cognitive minds. The minds codex knows about 5-layer architecture but not about hook-triggered observation. Neither codex declares the interop contract between hook and mind — and `/create` has no sub-command that scaffolds both at once.

**Why this is orphan.** A composition whose natural shape crosses codex boundaries has no forge path unless one codex learns about the other, or a new meta-codex is introduced that specifically handles the interop. Both options are codex-scale work (a new codex means a new certification; teaching one codex about another means changing two certified artifacts simultaneously). Neither is in v1 scope.

**How the Engine handles it in v1.** The topology declares `longitudinal_observer` as a `hypothesized_cells_v2` entry with `blocked_by: GAP-COMPOSITION-1` and `type: hooks + minds (composition)`. When a creator's intent routes to this cell, Step 9 of the algorithm falls through to the legacy Q1/Q2/Q3 router and the creator is offered two separate forge paths (build the hook first, build the mind second) with an explicit note: *"This capability naturally wants to be a hook and a mind working together, but the Engine cannot yet forge multi-type compositions in one motion. You can build both pieces separately now, or wait for a future wave that unlocks one-motion composition."*

The creator is never blocked. They are informed, given a partial path forward, and the unroutable marker accumulates in `decisions_history` for future promotion.

---

## §4 — Habitable Compositions in v1

The 7 v1 cells in `references/intent-topology.md` §4 include no Class C compositions. They include exactly one Class A composition surface — the `project_constitution` cell is a claude-md product that composes with other products via `paths:` scoping at the install layer, not at the forge layer. The other 6 v1 cells are single-type.

The Class B composition (system) is not enumerated in the 7 v1 cells even though it is forgeable, because the system cell (`cognitive_organism_full_stack` in the v2 set) has no independent v1 exemplar that a creator would forge from scratch — the Engine itself is the only live example, and the Engine was built via direct system forge, not via discovery-mode routing. Deferring the system cell to v2 is honest about that fact.

**The v1 composition surface is small by design.** The discovery-mode rewrite is a routing improvement, not a composition primitive expansion. Compositions are handled by the existing codices (squad for multi-agent, bundle for multi-product install, system for multi-destination install) and do not require discovery-mode routing in v1. A creator who wants a squad runs `/create squad` directly; a creator who wants a system runs `/create system` directly. Discovery mode's job is to catch the creators who do not know they want a squad or a system — and for those cases, the v1 surface correctly routes to single-type forms and leaves the composition primitives for creators who already know the term.

---

## §5 — Orphan Cells and GAP-COMPOSITION-1

### §5.1 — GAP-COMPOSITION-1 Declaration

**Gap:** the Engine's `/create` skill has no single forge path that scaffolds a product composing two or more types that do not share a codex. The `composed_system` delivery mechanism handles the installation side of composition (via system's `install_manifest`) but does not handle the **forge** side — there is no `/create {typeA}+{typeB}` command, and the individual type codices (hooks, minds, skill, agent) do not declare interop contracts with each other.

**Affected v2 cells (from `references/intent-topology.md` §5):**

- `longitudinal_observer` — hook + minds composition. A PostToolUse AgentHook that spawns a research-partner mind on commit events. The intent is *"watch for patterns across sessions and reflect on them"*. No forge path exists.

**Why this gap is honest rather than fixable in v1.** Three reasons.

1. **Certification integrity.** The 6 certified codices (output-style, skill, agent, squad, system, minds) are closed. Adding interop contracts between two of them (e.g., hooks learning about minds) would require re-certifying both. Re-certification is a codex-level wave of its own, never a drive-by edit.

2. **Composition semantics are not yet named.** What does *"a hook that spawns a mind"* mean structurally? Does the mind inherit the hook's trigger context? Does the hook wait for the mind's output? Does the mind write to the same memory scope the hook reads? These are semantic choices that need to be declared before a forge path can be built. No wave in the current plan declares them.

3. **The creator is not blocked.** The legacy Q1/Q2/Q3 fall-through produces partial forward motion: the creator builds the hook, builds the mind, connects them manually. The result is less elegant than a one-motion composition but is functionally complete. The gap is a UX gap, not a capability gap.

### §5.2 — Promotion Path for GAP-COMPOSITION-1

The gap is closed when three conditions hold:

1. A new substrate document (`references/composition-contracts.md` or similar) declares the semantic contract between hook and minds (and any other interop pair that proves needed from `decisions_history` evidence).
2. One codex (likely minds, since it is the apex of the family-skill lineage) is extended with a section that declares how it composes with hook-scope and claude-md-scope.
3. `.claude/skills/create/` learns a new sub-command that reads the composition contract and scaffolds both types in one motion, with the composition manifest declared in the product's `.meta.yaml`.

Until all three hold, GAP-COMPOSITION-1 stays open and the affected v2 cells remain deferred. The gap is not forgotten; it is named, tracked, and fed by longitudinal evidence for when the promotion becomes worth the re-certification cost.

### §5.3 — Other Potential Orphan Cells (not yet named)

GAP-COMPOSITION-1 is the only composition gap currently named with an affected v2 cell. Two additional composition surfaces are structurally possible and may surface in future iterations:

- **Skill composition** — a skill that delegates to another skill without spawning an agent (both run in the parent context). This is partially handled today via the `skills:` frontmatter heredity on agents, but no analogous mechanism exists for skill-to-skill delegation. No v2 cell currently declares this, so no gap is declared.
- **Output-style composition** — multiple output-styles applied in layered order (signature + voice + formatting). The current output-style codex handles single-style application; layered application would require a composition contract. No v2 cell declares this.

These surfaces are listed here for completeness, not because they block anything. If evidence from `decisions_history` shows creators hitting them, they become candidate gaps in a future wave.

---

## §6 — What v2 Unlocks

When the v2 wave runs (some time after v1 stabilizes and `decisions_history` accumulates evidence), the promotion candidates from `hypothesized_cells_v2` are the queue of work. The 12 deferred cells split into three groups by what they need to become habitable:

### Group 1 — Cells waiting for exemplars only (8 cells)

These cells are structurally tractable today; they are deferred only because no v1 canonical example exists in `references/exemplars/` or creator workspace to anchor regression testing. Promotion is additive: write the exemplar, add the cell to v1, add a regression test.

- `general_purpose_agent` — blocked by "general-purpose is a native built-in, not a forged product"; promotion requires clarifying when the Engine forges a wrapper vs recommends the built-in.
- `squad_coordinator` — blocked by "squad forge has a mature direct path"; promotion is mostly about deciding whether discovery mode should route to squad or let creators choose it explicitly.
- `event_reflex` — same pattern; hooks forge has a mature direct path.
- `procedural_workflow` — same pattern; workflow forge has a mature direct path.
- `voice_fragment` — same pattern; output-style forge has a mature direct path.
- `visual_design_language` — same pattern; design-system is its own vertical.
- `ambient_status_display` — same pattern; statusline forge has a mature direct path.
- `marketplace_composition` — same pattern; bundle forge has a mature direct path.

### Group 2 — Cells waiting for disambiguation (2 cells)

These cells have structural overlap with v1 cells and promotion requires naming the disambiguator.

- `domain_advisor_agent` — overlaps structurally with `code_reviewer_agent`. Promotion requires disambiguating *"advisor at advisory depth"* from *"advisor at procedural depth"* when both live in an agent. The minds codex has already done this work for minds; the agent codex may need a similar extension.
- `cognitive_organism_full_stack` — overlaps with the system codex's apex archetype. Promotion requires deciding whether discovery mode routes to system or lets creators choose the form explicitly.

### Group 3 — Cells waiting for GAP-COMPOSITION-1 (1 cell)

- `longitudinal_observer` — the only cell blocked on GAP-COMPOSITION-1. Promotion requires the full three-condition sequence declared in §5.2.

### Group 4 — Cells that may never promote (1 cell)

One cell is a non-Claude-Code-primitive product and will likely never enter discovery-mode routing:

- `deployable_application` — real software handled by a separate forge path; discovery-mode routing is orthogonal to application forge.

This cell stays in v2 as documentation, not as a promotion queue. The topology includes it because honesty about the full combinatorial surface is cheaper than silence — a creator who asks *"can I forge an application this way?"* deserves an answer, not a shrug.

---

## §7 — What This Document Does Not Cover

Three topics are structurally related to composition but live elsewhere:

1. **The runtime host derivation** when a composition spans multiple hosts — handled by `references/runtime-host-dag.md`, which computes host sets per `(delivery, nature)` pair and returns a merged set for composed products.
2. **The package-time split** when a composition must dispatch to multiple install destinations — handled by `product-dna/system.yaml install_manifest` and by the `/package` skill's bundle handling. Composition at forge time is this document; composition at install time is not.
3. **The sub-agent handoff spec** when a squad coordinates multiple agents — handled by DNA pattern D10 in `structural-dna.md` and by `product-dna/squad.yaml`. Inter-agent handoff is a squad concern, not a general composition concern.

---

**Status.** Canonical substrate, v1. Declares GAP-COMPOSITION-1 and the three composition classes (intra-type, bundled multi-type, implicit multi-type). Read alongside `references/intent-topology.md` §5 (the v2 cell list) and `references/capability-matrix.md` §7 (unroutable fall-through contract).
