---
document: structural-dna
product: MyClaude Studio Engine
version: 3.0.0
status: CANONICAL
date: 2026-04-08
---

# Structural DNA — Architectural Principles and 20 Patterns

> Every DNA pattern is a lesson extracted from production systems. Each one represents
> a failure mode that has caused real products to underperform or be abandoned.
> Apply them and your products inherit structure that took years to discover.
>
> The 20 DNA patterns are the **operational** layer. They exist because 9 deeper
> **architectural** principles demand them. The principles are the why; the patterns
> are the how. If the patterns conflict with the principles, the principles win.

---

## Architectural Principles — The 9 Upstream Laws

These nine principles govern every resource the Engine forges. They are upstream of the
20 DNA patterns: when a forge decision is ambiguous, trace back to the principles. The
patterns implement the principles; the principles are not negotiable.

### P1 — Purpose Before Shape

The resource's reason to exist is declared before its structure. "What capability does
this amplify, for whom, measured how?" is answered before "skill or agent or workflow?"
A resource scaffolded from a template without a declared purpose inherits the template's
purpose by default — which is almost never the creator's real intent.

**Implication:** `/scout` and `/create` both begin with purpose elicitation. A scaffold
built without an answer to "what changes when someone uses this?" is a shell, not a product.

### P2 — Constraint Before Feature

What the resource refuses to do is specified before what it does. "This tool does NOT X"
is written first; "this tool does Y" is written second. Boundaries prevent scope creep,
reduce false expectations, and make the resource composable with others.

**Implication:** Every forged resource has a "When Not To Use" section (DNA pattern D14
is the operational form). Missing this section blocks validation.

### P3 — Composition Over Monolith

Small resources that compose beat large resources that try to do everything. A 2000-line
resource is suspect until proven irreducible. Composition is the path to scale, reuse,
and maintainability in a marketplace of thousands of resources built by thousands of creators.

**Implication:** `/create` coaches toward the smallest viable surface. Bundle and system
types exist explicitly to compose smaller resources, not to justify monoliths.

### P4 — Contract Before Narrative

The public interface — inputs, outputs, side effects, preconditions — is specified
formally. Prose that describes "how the resource thinks" is secondary to the contract
that describes "what the resource promises and requires." A contract can be tested;
narrative cannot.

**Implication:** `context_contract` in `config.yaml → routing.{type}` is load-bearing.
Every type declares `needs_in_window`, `provides_to_window`, `strips_from_window`.
Forged resources inherit and specialize these.

### P5 — Failure Mode Before Happy Path

Every resource declares how it degrades before how it succeeds. What happens when input
is ambiguous? When a dependency is missing? When the resource is uncertain? These
answers are first-class artifacts, not footnotes. A resource that can only succeed on
perfect input is brittle by design.

**Implication:** DNA pattern D14 (Graceful Degradation) is universal — required for
every type at every tier. `/validate` blocks resources without an explicit degradation section.

### P6 — State at the Edge

State lives in files at the boundary of the resource — `STATE.yaml`, `.meta.yaml`,
`creator.yaml` — never in implicit conversation memory. A resource that depends on
conversation history to function fails when context compresses, when sessions restart,
or when another resource shares the window. Files are durable; memory is not.

**Implication:** DNA pattern D8 (State Persistence) operationalizes this. The Engine's
own `/compact` instructions in `CLAUDE.md` encode the same law for the Engine itself.

### P7 — Read Before Write

Every operation reads real state before writing new state. The ratio is ≥2:1 — for every
Write tool call, at least two Read tool calls precede it. Abstract reasoning without
grounding in real state produces confident wrong answers. Reading is cheap; rewriting
over wrong assumptions is expensive.

**Implication:** Every skill's activation protocol reads product state, creator profile,
and workspace before any Write tool call. `/validate` audits this ratio per skill and
flags skills whose ratio falls below 2:1.

### P8 — Invisibility of Mechanism

Users experience capability, not machinery. Internal vocabulary — framework names, model
names, academic references, author names, methodology acronyms — stays internal. User-facing
strings speak the user's language. A resource that requires the user to learn vocabulary
before extracting value is a tax, not an amplifier.

**Implication:** `/validate` runs a user-facing grep that blocks any resource whose README,
SKILL.md user-facing sections, or UX strings contain internal vocabulary the creator did
not define as user-facing. The coaching layer translates mechanism to user terms.

### P9 — Recursive Integrity

The resource passes its own validator. A linting skill that fails its own lints is not
trustworthy. A framework generator whose framework fails its own generator is not
trustworthy. A Studio Engine that fails its own `/validate --level=3` is not trustworthy
to produce state-of-the-art resources for anyone else.

**Implication:** The Engine dogfoods itself. `/validate --target=engine` runs the full
pipeline against the Engine's own files. Every release must pass before ship. This is
how the Engine earns the right to validate others.

### P10 — Touch Integrity

Every user touchpoint is the product, not a mechanism of it. The voice, the visual rhythm,
the emotional register, and the sense of continuity must be identical across every skill,
every error path, every idle moment, every return session. A single inconsistent touch
degrades the whole — the Creator does not distinguish between `/status` and `/package`
and `/validate` and an error message; they experience **one thing** called myClaude, and
any seam shows.

This is the principle P1-P9 converge toward. Purpose, constraint, composition, contract,
failure mode, state at the edge, read-before-write, invisibility of mechanism, and
recursive integrity each produce technical rigor inside the forge. P10 is what the Creator
**feels** when that rigor meets them. A technically perfect Engine with five inconsistent
voices degrades to a tool; a technically perfect Engine with one unified voice becomes an
environment the Creator cannot bear to leave.

**Implication.** Every Engine skill that produces Creator-facing output loads
`references/quality/engine-voice-core.md` at activation — the micro voice contract is
the floor, not a peak-moment option. The full `references/quality/engine-voice.md`
loads only at specific peak moments inside a skill (publish celebration, first-impression
onboard closing, validate verdict, WOW frames) where the extended substrate earns its
cost. Concurrent-skill ambient load is bounded by Clause VIII; voice-core's fixed size
keeps the bound reachable.

The `✦` symbol, the Master Craftsperson archetype, the three tones (conducting /
celebrating / confronting), the six anti-patterns, and the error-as-intimacy distinction
are inherited by every touchpoint automatically — not re-invented per skill. `/validate`
Stage 9 Voice Coherence audits the enforcement as advisory.

**Implication for error paths:** an error is not a degraded output — it is a first-class
touchpoint and carries the same voice discipline. Engine-fault errors (internal bug, drift,
unexpected state) adopt a slightly self-critical collaborative tone; environment-fault
errors (YAML parse, CLI timeout, missing file) stay diagnostic-and-safe. Conflating the
two is a P10 violation because it tells the Creator that the Engine does not distinguish
between "I erred" and "something outside erred" — and that distinction is where trust
compounds.

The nine earlier principles produce a system that is structurally correct. P10 is what
makes a system of rigorous principles feel like one thing — the texture the Creator
touches instead of the architecture the Creator would otherwise see.

### How the 10 Principles Map to the 20 Patterns

| Principle | Primary DNA patterns |
|---|---|
| P1 Purpose Before Shape | D1 (Activation Protocol) — defines purpose at boot |
| P2 Constraint Before Feature | D2 (Anti-Pattern Guard), D14 (Graceful Degradation) |
| P3 Composition Over Monolith | D3 (Progressive Disclosure), D16 (Composability), D20 (Cache-Friendly) |
| P4 Contract Before Narrative | D5 (Question System), D10 (Handoff Specification) |
| P5 Failure Mode Before Happy Path | D6 (Confidence Signaling), D14 (Graceful Degradation), D7 (Pre-Execution Gate) |
| P6 State at the Edge | D8 (State Persistence), D12 (Compound Memory) |
| P7 Read Before Write | D1 (Activation Protocol), D7 (Pre-Execution Gate) |
| P8 Invisibility of Mechanism | D13 (Self-Documentation), D19 (Attention-Aware Authoring) |
| P9 Recursive Integrity | D4 (Quality Gate), D11 (Socratic Pressure), D15 (Testability) |
| P10 Touch Integrity | D13 (Self-Documentation), D14 (Graceful Degradation), D19 (Attention-Aware Authoring) |

When a DNA pattern fails validation, the coaching message names the principle it violates
— not the abstract pattern number. Creators learn the why through the patterns, and the
patterns earn their weight through the principles.

---

## Meta-Architecture

### The Fractal Principle

These 20 patterns follow a self-similar structure at every scale:
- **Macro** (system level): the product as a whole has Goal → Input → Processing → Output → Validation
- **Meso** (module level): each component within the product repeats the same structure
- **Micro** (node level): each individual instruction follows the same contract

This isn't aesthetic — it's functional. When the same grammar repeats at all scales, the product is easier to understand, debug, extend, and teach. A skill's Activation Protocol (D1) works the same way whether it's a standalone skill or a component inside a system.

### Six-Layer Processing Flow

Every state-of-the-art Claude Code product follows a six-layer processing flow.
The 20 DNA patterns distribute across these layers:

```
BOOT LAYER
  Load context, routing rules, core config
  DNA: D1 (Activation Protocol), D3 (Progressive Disclosure)
    |
INPUT TRIAGE
  Classify request, identify specialists, check preconditions
  DNA: D5 (Question System), D7 (Pre-Execution Gate)
    |
EXECUTION
  Route to specialist, apply pressure, execute with disclosure
  DNA: D9 (Orchestrate Don't Execute), D10 (Handoff Spec),
       D11 (Socratic Pressure), D18 (Subagent Isolation)
    |
STATE CAPTURE
  Log decisions, update state, check quality signals
  DNA: D8 (State Persistence), D12 (Compound Memory)
    |
SYNTHESIS
  Integrate outputs, surface tensions, apply final validation
  DNA: D4 (Quality Gate), D6 (Confidence Signaling)
    |
OUTPUT
  Graduate confidence, show reasoning, declare uncertainty
  DNA: D13 (Self-Documentation), D14 (Graceful Degradation)
```

### How Tiers Compose

Tiers are cumulative. Tier 2 requires Tier 1 as foundation. Tier 3 requires Tier 2.
A product at MCS-2 must pass all Tier 1 AND Tier 2 checks. A product at MCS-3 must
pass all 18. The tiers reflect structural complexity:

- **Tier 1** patterns apply to everything. A single-file prompt needs D1, D4, D13.
- **Tier 2** patterns require that the product has nontrivial execution logic.
  A prompt with no branching doesn't need D8 (state) — it's not applicable.
- **Tier 3** patterns apply to multi-agent systems. A solo skill has no agents to
  orchestrate, no handoffs to specify, no subagents to isolate.

The DNA Applicability Matrix in the PRD defines R (required) / o (optional) / — (not applicable)
per product type. The /validate skill reads this matrix to determine which patterns to check.

---

## TIER 1 — UNIVERSAL
*7 patterns. Required for every product at every MCS level.*

---

### D1: Activation Protocol

**Tier:** 1 — Universal

**Problem it solves:**
A product that responds without loading context produces generic output. Without an explicit
activation sequence, Claude uses whatever is ambient in the session — which may be wrong,
incomplete, or from a different project entirely.

**Rule:**
Every product must define an explicit activation sequence that loads domain knowledge,
anti-patterns, and user intent BEFORE taking action. The sequence must be ordered:
knowledge first, constraints second, intent third.

**Example structure:**
```markdown
## Activation Protocol

Before responding to any invocation:
1. Read `references/domain-knowledge.md`
2. Read `references/anti-patterns.md`
3. Parse input for specific request type
4. Apply domain context to interpretation
```

**Validation check:**
```
grep -i "activation protocol\|## activation\|before responding\|load.*context\|context.*load" {PRIMARY_FILE}
AND
grep -c "references/" {PRIMARY_FILE} → must be ≥1
```
PASS if both match. PARTIAL if activation section found but no references/ link.

---

### D2: Anti-Pattern Guard

**Tier:** 1 — Universal

**Problem it solves:**
Without documenting what NOT to do, users and the product itself repeat known errors.
Anti-patterns are accumulated failure knowledge — without them, every session risks the
same mistakes that were already discovered and solved.

**Rule:**
Every product must contain a section listing at least 5 anti-patterns with description
and prevention. Anti-patterns are failure modes specific to this product's domain —
not generic "don't break things" advice.

**Example structure:**
```markdown
## Anti-Patterns

| Pattern | Why It Fails | Prevention |
|---------|-------------|------------|
| Reviewing code without reading tests | Misses intended behavior | Always read tests/ before reviewing src/ |
```

**Validation check:**
```
grep -i "anti-pattern\|## anti-pattern\|## what not\|## never\|## avoid" {PRIMARY_FILE}
AND count items in section → must be ≥5
```
PASS if section found with ≥5 items. PARTIAL if section found but <5 items.

---

### D3: Progressive Disclosure

**Tier:** 1 — Universal

**Problem it solves:**
Loading all knowledge into the primary file wastes context window on every invocation.
A product whose SKILL.md is 2000 lines burns context before the creator even types a request.

**Rule:**
Primary file must be under 500 lines. Deep knowledge lives in references/. Primary file
contains structure and protocols; references/ contains domain content loaded on-demand.
Product type determines required depth: skills can be tighter, systems need more.

**Validation check:**
```
wc -l {PRIMARY_FILE} → must be <500
AND
glob: references/ → must exist with ≥1 file
AND
grep "inline knowledge dump\|CONTEXT:\|BACKGROUND:" {PRIMARY_FILE} → must be 0 matches
```
PASS if primary file <500 lines and references/ exists. PARTIAL if references/ exists but
primary file >500 lines.

---

### D4: Quality Gate

**Tier:** 1 — Universal

**Problem it solves:**
Without explicit checkpoints, output quality varies based on ambient session state.
Quality gates force verification before delivery — they make implicit standards explicit.

**Rule:**
Every product must define at least 3 verifiable quality criteria that can be checked
before output is delivered. Criteria must be checkable, not aspirational.
"Output must be clear" is aspirational. "Output contains exactly 3 sections" is checkable.

**Example structure:**
```markdown
## Quality Gate

Before delivering output, verify:
- [ ] All referenced files exist
- [ ] No placeholder content (TODO, lorem ipsum)
- [ ] Output matches requested format
- [ ] If skill: activation protocol was followed
```

**Validation check:**
```
grep -i "quality gate\|## quality\|before deliver\|before output\|output criteria\|acceptance" {PRIMARY_FILE}
AND count verifiable items (grep "- \[" or "1\. " in quality section) → must be ≥3
```
PASS if section with ≥3 checkable items. PARTIAL if section found but <3 items.

---

### D13: Self-Documentation

**Tier:** 1 — Universal
*(ID gap is intentional — D13 belongs in Tier 1 per the PRD applicability matrix.)*

**Problem it solves:**
A product without a README isn't installed. Buyers need install instructions, usage
examples, and requirements. A product that assumes context will underperform for
every new user.

**Rule:**
Every product must have README.md following `templates/readme/README.md.template`.
The README is a product showcase — it sells first, documents second.

**Required sections (MCS-1 minimum — 6 sections):**
1. Hero — product name + problem hook (what it solves)
2. Install — must include `myclaude install {slug}`
3. Quick Start — at least one usage example
4. Features — at least 3 features with substantive description
5. Requirements — Claude Code version + any dependencies
6. License

**Recommended sections (MCS-2 — full showcase):**
7. "Is this for me?" — qualifier (yes if / not for you if)
8. Use Cases — scenario table with real workflows
9. How It Works — method explanation (earns trust)
10. Type-specific section (Usage/Architecture/Events/etc.)
11. Compatibility — platform list
12. Language — locale-adaptive statement

**Trilingual (MCS-2+ recommended):**
EN, PT-BR, ES language blocks with anchor navigation.
Each language has FULL content — not just translated headers.

**Validation check:**
```
glob: README.md → must exist
AND grep -i "## install" README.md → must match
AND grep "myclaude install" README.md → must match
AND grep -i "## quick.start\|## usage\|## how to use\|## commands\|## inicio" README.md → must match
AND grep -i "## features\|## funcionalidades\|## caracteristicas\|## what it does" README.md → must match
AND grep -i "## requirements\|## requisitos\|## prerequisites" README.md → must match
```
PASS if all required sections found and non-empty. PARTIAL if README exists but missing sections.

---

### D14: Graceful Degradation

**Tier:** 1 — Universal

**Problem it solves:**
A product that fails silently or crashes on missing context destroys creator trust.
Buyers don't know what went wrong; they just see a non-working product and uninstall it.

**Rule:**
Every product must document how it behaves when context is incomplete, input is
ambiguous, or dependencies are unavailable. The product must degrade gracefully:
produce partial output with explanation, or ask for clarification — never fail silently.

**Example structure:**
```markdown
## When Not To Use

- If {required_context} is unavailable: explain what's needed, suggest alternatives
- If input is ambiguous: ask one clarifying question, not five
- If dependencies not installed: report exactly what's missing and how to install
```

**Validation check:**
```
grep -i "when not to use\|degradation\|## limitations\|## error handling\|## if.*missing\|## fallback" {PRIMARY_FILE}
```
PASS if section found with at least 2 handled cases. PARTIAL if section found but only 1 case.

---

### D19: Attention-Aware Authoring

**Tier:** 1 — Universal

**Problem it solves:**
Products that place critical constraints at the top and boilerplate at the bottom get worse
model compliance. The transformer architecture pays more attention to content at the END of
the context window (recency bias). Products structured backwards waste the highest-attention
position on generic context.

**Rule:**
Every product must structure content from generic to specific, with critical constraints
and rules positioned in the LAST 30% of the primary file (before Compact Instructions).
Structure: Context/Background → Knowledge/References → Execution Logic → Critical Rules/Constraints.

**Evidence:**
[SOURCE: claudemd.ts:9-10] — "Files are loaded in reverse order of priority"
[REF: Liu et al. (2023) "Lost in the Middle" — U-shaped attention curve in long contexts]

**Example structure:**
```markdown
## When to Use / Identity           ← generic (low attention position)
## Activation Protocol              ← procedural
## Core Instructions                ← domain logic
## Output Format                    ← structural
## Quality Gate                     ← verification
## Anti-Patterns                    ← constraints (HIGH attention position)
## Compact Instructions             ← technical (always last)
```

**Validation check:**
```
For primary file:
Identify sections with keywords: critical, rules, always, never, must, constraints
Check if these sections are in the LAST 30% of the file (by line count)
```
PASS if critical sections in last 30%. PARTIAL if mixed. COACHING if critical sections in first 50%.

---

## TIER 2 & TIER 3 — load-on-demand

Tier 2 (8 patterns) and Tier 3 (5 patterns) are NOT loaded at boot. They live in
`references/structural-dna/` and are read on-demand by `/validate` (level ≥ 2 or 3)
and `/create` when scaffolding products that cross MCS-1. This honors Constitutional
Clause VIII (Every Token Earns Its Place) and DNA D3 (Progressive Disclosure) — the
patterns earn their cost only when a forge actually needs them.

### TIER 2 — ADVANCED (8 patterns, MCS-2)

Required for any product with nontrivial execution logic. Full bodies (problem,
rule, example, validation check) in `references/structural-dna/tier2.md`.

- **D5 Question System** — ambiguous input → one clarifying question, never five.
- **D6 Confidence Signaling** — graduated certainty markers; never bare claims.
- **D7 Pre-Execution Gate** — verify preconditions before work, not after failure.
- **D8 State Persistence** — cross-session learning lives in files, not memory.
- **D15 Testability** — ≥3 scenarios with verifiable expected outputs.
- **D16 Composability** — relative paths, domain-specific commands, zero global mutations.
- **D17 Hook Integration** — document lifecycle automation surface explicitly.
- **D20 Cache-Friendly Design** — claude-md products under 2K chars, no dynamic content.

### TIER 3 — EXPERT (5 patterns, MCS-3)

Required only for multi-agent products (squad, system). Full bodies in
`references/structural-dna/tier3.md`.

- **D9 Orchestrate, Don't Execute** — orchestrators route; specialists do the work.
- **D10 Handoff Specification** — every agent-to-agent transfer is contractual.
- **D11 Socratic Pressure** — agents self-challenge before delivering output.
- **D12 Compound Memory** — cross-session memory configured via native scopes.
- **D18 Subagent Isolation** — `context: fork`; semantic boundaries reinforce it.

### Reference files (load-on-demand only)

- `references/structural-dna/tier2.md` — full Tier 2 definitions
- `references/structural-dna/tier3.md` — full Tier 3 definitions
- `references/structural-dna/dependency-graph.md` — Requires/Enables/Therefore table
- `references/structural-dna/applicability-matrix.md` — R/o/— per type × pattern

`/validate` reads these per the level requested. `/create` reads tier2/tier3 only
when the type's applicability matrix marks ≥1 pattern as Required at that tier.
The Engine is recursively coherent: P3 (Composition Over Monolith) and D3
(Progressive Disclosure) demand exactly this split.

---

*structural-dna.md — MyClaude Studio Engine*
*Boot-resident: 10 architectural principles + Tier 1 universal patterns + Tier 2/3 pointers.*
*Full Tier 2 / Tier 3 / dependency graph / applicability matrix in `references/structural-dna/`.*
