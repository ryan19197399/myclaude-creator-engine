# Skill vs Agent — The Four Discriminators

Most creators choosing between a skill and an agent are choosing between two shapes that look alike on the surface but behave very differently in practice. This document exists to make that choice fast and correct. It is the discriminator layer of discovery-mode `/create` — the same four tests the 12-step algorithm applies internally (Steps 2-5 in `references/capability-matrix.md`), written here as plain questions a creator can answer without knowing the algorithm exists.

**Layer:** Canonical substrate. Consumed by `.claude/skills/create/` during Guided mode discovery and surfaced in the creator-facing explanation when the algorithm proposes a form. Also read by `/think` when the creator invokes the `skill-or-agent` subcommand to reason about a choice without forging.

**Reading order:** §1 why this split matters → §2 the four questions → §3 worked examples → §4 edge cases → §5 when neither fits.

---

## §1 — Why the Split Matters

The distinction between skill and agent is not a matter of preference or aesthetics. It is a distinction between two fundamentally different runtime shapes, and getting it wrong produces products that look right on disk but behave wrong in practice.

A **skill** runs inside the creator's current session. It inherits the parent context — the conversation so far, the files currently open, the reasoning the creator has been building up. When a skill activates, it does not start from zero; it starts from everything the creator has been thinking. A skill is an amplifier of the creator's current working memory.

An **agent** runs in an isolated fork. It does not see the parent's conversation, it does not inherit the creator's in-progress reasoning, it starts with a clean context window and its own system prompt and its own tool pool. When an agent is spawned, it does not think with the creator — it thinks for the creator, in parallel, and returns a structured report at the end. An agent is a delegate, not an extension.

This is not a size difference — a skill can be larger than an agent and vice versa. It is not a complexity difference — a skill can be more complex than an agent and vice versa. It is a **runtime shape** difference: who shares working memory with whom. Products that get this wrong waste tokens, produce misaligned output, or contaminate the creator's reasoning with the output of a process that should have been isolated.

The four discriminators below test runtime shape. Each is a yes/no question; the combined answers map to a small set of canonical shapes; the shape maps to a form. Run the four questions in order. Do not skip.

---

## §2 — The Four Discriminators

### Q1 — Continuity: Does this capability need the creator's current working context to function?

Ask yourself: *"If I spawned this capability fresh, with no memory of what I was just doing, would it still be useful — or would it need me to re-explain everything?"*

| Answer | Meaning | Runtime shape bias |
|---|---|---|
| **YES — it needs my current context** | The capability is an extension of the creator's own thinking. Its value depends on inheriting what the creator has been building up. | **Skill** (parent context preserved) |
| **NO — it works from cold start** | The capability can operate from first principles, given a well-defined input. It does not depend on the creator's in-progress reasoning. | **Agent** (isolated context, task-spawned) |

**The test in one sentence:** a cognitive audit companion that watches the creator's current decision stream needs continuity. A security audit that reviews a specific file does not.

**Why this is the first question.** Continuity is the strongest signal in the matrix. When the answer is clearly YES or clearly NO, the other three questions usually confirm rather than override. When the answer is UNCLEAR, the next three questions do the real work — and continuity is resolved by whichever way they lean.

### Q2 — Invocation: Will the creator remember to invoke this capability at the right moment?

Ask yourself: *"If this capability exists but the creator forgets it exists, does its value die?"*

| Frequency | Answer | Runtime shape bias |
|---|---|---|
| **Daily** | YES — daily use keeps recall fresh. Any invocation mechanism works. | Any — let other discriminators decide |
| **Weekly** | YES — weekly is neutral; memory holds. | Any — let other discriminators decide |
| **Monthly or rarer** | NO — the creator will forget. The capability dies on the shelf. | **Ambient skill** — the capability must wake itself when the relevant moment arrives |

**The mechanism that solves rare-use invocation.** A skill with a `paths:` frontmatter glob is dormant until a file matching the glob is touched. The creator does not invoke it; the environment invokes it. This is the only native way in the platform to build a capability that appears on demand without requiring memory. If the capability would be used rarely and must still exist, force this shape.

**The counter-case.** An agent invoked automatically is not a thing in the platform — agents are spawned explicitly via the Task tool, not triggered by file patterns. If the creator cannot be relied on to remember a rare-use agent, the agent is the wrong shape. Change it to a path-scoped skill.

### Q3 — Pollution: Would this capability's reasoning pollute the creator's current thinking if mixed with it?

Ask yourself: *"Would running this capability inside the creator's working memory contaminate the work the creator is doing?"*

| Case | Pollution risk | Runtime shape bias |
|---|---|---|
| **Code review of the creator's in-progress code** | HIGH — the reviewer inherits the creator's justifications for the code and rubber-stamps its own author | **Agent** — isolation protects the review from the very reasoning it is reviewing |
| **Second opinion on an architectural decision the creator just made** | HIGH — the second opinion reads the decision and tends to agree, losing its independence | **Agent** |
| **Generic code transformation the creator asked for** | LOW — the transformation executes, does not opine | **Skill** or agent, other discriminators decide |
| **Research or synthesis that augments the creator's current thinking** | LOW — amplification is the goal, not contamination | **Skill** |

**The canonical pollution case.** An advisor reviewing the same code it is helping to write is structurally compromised. Both the reviewer and the author share one working memory; the reviewer reads the creator's reasoning for why the code is right, and its output inherits that reasoning. The fix is isolation — a task-spawned agent with read-only tool pool starts from the code as it exists on disk, not from the creator's justifications. This is why `code_reviewer_agent` is a cell in the topology, distinct from `reasoning_skill_cognitive` even though both are advisors: the pollution test separates them.

**The inverse case.** A Renaissance-perspective skill applied to a design decision **should** see the creator's current reasoning — that is where blind spots live. Mixing perspective and reasoning is the goal, not the problem. Pollution is a threat only when the capability's output is supposed to be independent of the reasoning it is reading. When the capability is supposed to amplify that reasoning, pollution is the feature.

### Q4 — Output Shape: What does the creator receive at the end — amplified reasoning inside their current thinking, or a structured report they read after?

Ask yourself: *"When this capability finishes running, what does the creator hold in their hands?"*

| Answer | Output shape | Runtime shape bias |
|---|---|---|
| **Amplified reasoning inside the current conversation** — the creator's own thinking became sharper because the capability ran | The capability is an amplifier | **Skill** (output merges into parent conversation) |
| **A structured report the creator reads after** — a document, a list, a scorecard, a named deliverable | The capability is a delegate | **Agent** (output is returned as a task result) |

**Why this is separate from continuity.** A capability can need continuity (Q1=YES) but still produce a structured report (Q4=report). That combination is rare but valid — it describes a skill that reads parent context deeply but delivers its conclusion as a named section rather than as inline amplification. In that case, the skill wins: continuity is the stronger signal.

A capability can lack continuity (Q1=NO) but produce amplified reasoning for the creator to read after (Q4=amplification). This combination usually collapses to "the creator wanted a second perspective on something specific" — and the right shape is an agent that returns a structured report framed as amplification. The output *reads* like amplification, but the runtime shape is agent.

**The decision rule when Q1 and Q4 disagree:** continuity wins. Shared working memory is a stronger signal than output framing. If the capability needs the parent context, it is a skill regardless of how its output looks.

---

## §3 — Worked Examples

Each example runs through the four questions. The result maps to a canonical cell from `references/intent-topology.md` §4.

### Example A — *"I want a cognitive audit companion that thinks alongside me during decisions."*

| Question | Answer | Signal |
|---|---|---|
| Q1 Continuity | **YES** — "alongside me" is the signature of shared working memory | Skill |
| Q2 Invocation | Daily (the creator explicitly said "during decisions" — high frequency) | Neutral |
| Q3 Pollution | LOW — the goal is amplification, not independent review | Skill |
| Q4 Output shape | Amplified reasoning | Skill |

**Four skill signals, zero agent signals. Routes to `reasoning_skill_cognitive` (cognitive skill, invoked via slash command or ambient path-scoped).**

### Example B — *"I want a security audit specialist that reviews my code for vulnerabilities."*

| Question | Answer | Signal |
|---|---|---|
| Q1 Continuity | NO — the audit works from the code as it exists on disk, not from in-progress reasoning | Agent |
| Q2 Invocation | Weekly-to-monthly (reviews run per-feature, not continuously) | Neutral |
| Q3 Pollution | **HIGH** — reviewing the creator's in-progress code while the creator is justifying it | Agent |
| Q4 Output shape | Structured report (vulnerability list with severities) | Agent |

**Four agent signals, zero skill signals. Routes to `code_reviewer_agent` (agent adviser, read-only, task-spawned).**

### Example C — *"I want a Renaissance-perspective tool that appears when I'm designing to provoke cross-domain thinking."*

| Question | Answer | Signal |
|---|---|---|
| Q1 Continuity | **YES** — "when I'm designing" means the perspective needs to see the design in progress | Skill |
| Q2 Invocation | Monthly or rarer (the creator does not design every day) | **Ambient skill — the perspective must wake itself** |
| Q3 Pollution | LOW — cross-domain provocation is amplification, not independent review | Skill |
| Q4 Output shape | Amplified reasoning (cross-domain analogies injected into current thinking) | Skill |

**Four skill signals, with one forcing `ambient_path_scoped` delivery because of Q2. Routes to `perspective_skill_cognitive` (cognitive skill, ambient-preferred via `paths:` frontmatter matching design-file globs).**

### Example D — *"I want a TypeScript refactoring specialist that hardens types across my codebase."*

| Question | Answer | Signal |
|---|---|---|
| Q1 Continuity | NO — the refactor operates on files, not on the creator's current reasoning | Agent |
| Q2 Invocation | Occasional (major refactor events, not continuous) | Neutral |
| Q3 Pollution | LOW — execution, not opinion | Skill or agent |
| Q4 Output shape | Structured report (files modified, type errors resolved) | Agent |

**Three agent signals, one neutral. Routes to `domain_specialist_executor` (agent specialist, write-capable, task-spawned).** Note: the Q3 answer is LOW pollution, but Q1 and Q4 dominate — execution from cold start with a structured completion report is the agent signature.

### Example E — *"I want a scout that researches a domain before I build products in it."*

| Question | Answer | Signal |
|---|---|---|
| Q1 Continuity | Partial — the scout needs to know *which* domain, but not the creator's in-progress reasoning about it | Either |
| Q2 Invocation | Explicit — the creator types `/scout` intentionally | Invoked |
| Q3 Pollution | LOW — research is independent by nature | Either |
| Q4 Output shape | Structured report (the scout report markdown) | Agent-leaning |

**Ambiguous on Q1, but the scout is already a skill in the Engine — which is correct because the continuity it needs is minimal (just the domain name) and the research work it does benefits from having access to the creator's profile for tailoring.** Routes to `procedural_skill` (skill procedural with WebSearch + WebFetch, invoked via `/scout` command).

**Why this example matters.** It shows the algorithm handling a partial-continuity case: the capability needs *some* parent context (to read `creator.yaml` for domain tailoring) but not the creator's in-progress reasoning. Partial continuity routes to skill when the parent context it needs is substrate (profile, configuration) rather than working memory. This is a genuinely fine-grained distinction and is one of the cases where real creator feedback is most useful for refining the heuristic.

---

## §4 — Edge Cases

The four discriminators resolve most cases cleanly. A small number of cases resist clean resolution; each is named here with the Engine's default handling.

### Edge 1 — The capability needs continuity for input and isolation for output

A creator asks: *"I want something that reads my current design decision and produces a brutal critique I can read after."* Q1 says continuity (the critique needs to see the design). Q4 says structured report (the critique is a named deliverable). Q3 says pollution (the critique is a review of the creator's reasoning, not an amplification of it).

**Engine default:** pollution wins. The capability is built as an agent that receives the design decision as input at spawn time (the creator copies it into the task prompt), not as a skill that reads the design from the parent's working memory. The structural integrity of the critique matters more than the ergonomic convenience of automatic input. The creator trades one extra copy-paste for independent judgment.

### Edge 2 — The capability needs isolation but produces amplified reasoning

A creator asks: *"I want a fusion mind that brings three strategic frames together for a high-stakes decision."* Q1 is YES in spirit (the mind thinks about the creator's decision) but NO in runtime (the mind has its own cognitive architecture that should not mix with the creator's reasoning). Q4 is "amplified reasoning" in feeling but "structured report" in mechanism.

**Engine default:** the mind wins. Apex embodied cognition delivered in isolation is a distinct cell (`apex_cognitive_mind`). The 5-layer architecture and 7 DNA strands require runtime isolation — mixing them into the parent would both dilute the cognition and pollute the creator. The mind receives the decision as input at spawn time, runs its full cognitive flow in isolation, and returns a structured report that reads like amplification. This is the reason minds exist as a distinct form — they are cognitions strong enough to need their own runtime.

### Edge 3 — The capability could be either and the creator has no preference

A creator asks: *"I want something that helps me review pull requests. I don't care how it's shaped."*

**Engine default:** read `creator.intent_profile.working_rhythm`. If `iterative_with_feedback`, bias skill (the review happens alongside the creator's PR work). If `sprint_delegated`, bias agent (the review is a delegated task the creator returns to). If `hybrid`, read `usage_frequency_expectation`: daily → skill, weekly or rarer → agent. The tiebreaker chain is deterministic, so two sessions with the same answers produce the same result.

### Edge 4 — The capability wants to be ambient-but-invoked

A creator asks: *"I want a skill that is always there but only speaks when I explicitly ask it something."* This sounds like a contradiction but describes a real pattern: a skill the creator wants available via slash command and ambient path-scoped at the same time, depending on context.

**Engine default:** both delivery mechanisms are allowed on one skill. The frontmatter declares `paths:` for ambient activation and a slash command name for explicit invocation. The two mechanisms coexist — ambient activation fires on file match, explicit invocation fires on command. This is a native capability of the skill primitive and is enumerated in `references/intent-topology.md` cells 2 and 6.

### Edge 5 — None of the discriminators fire strongly

A creator asks: *"I want a tool that makes my work better."* All four discriminators return UNCLEAR. The algorithm has no signal.

**Engine default:** the algorithm does not propose a form. Instead, it routes to `/scout` with a suggestion: *"I don't have enough signal from your intent to propose a form. Want me to research your domain first? `/scout {inferred_domain}` will show what Claude already knows and where the gaps are, and then we can decide together."* Discovery mode is not a forcing function — when the signal is absent, the answer is to gather signal, not to guess.

---

## §5 — When Neither Skill Nor Agent Fits

The four discriminators test skill-vs-agent specifically. Some capabilities fit neither. This section names the fall-through cases.

### Case 1 — The capability is orchestration of other capabilities

If the intent names two or more other capabilities that should run in coordination (*"when I ship, run all the checks"*), the answer is **squad** or **workflow**, not skill or agent. The `coordinate_X` verb family in `references/capability-matrix.md` Step 1 catches this. The four discriminators above do not apply — the coordination shape is determined by whether the sequence is declarative (workflow) or delegating (squad).

### Case 2 — The capability is reactive to environmental events

If the intent describes automatic reaction to a lifecycle event (*"when I finish a commit, log a note"*, *"on session start, load my context"*), the answer is **hooks**, not skill or agent. The `react_to_X` or `enforce_X` verb families catch this. Hooks have their own discriminators (which hook event, what handler type) that live in the hooks codex, not here.

### Case 3 — The capability is constitutional rather than invoked

If the intent describes rules that should always apply (*"never let me commit secrets"*, *"always use strict TypeScript in this project"*), the answer is **claude-md product** with `paths:` scoping, not skill or agent. The capability is a set of rules that live in the ambient context, not a procedure that runs.

### Case 4 — The capability is aesthetic transformation of output

If the intent describes changing how the Engine speaks rather than what it does (*"always respond in the tone of a Renaissance polymath"*), the answer is **output-style**, not skill or agent. Output-style is a substrate transformation that applies to everything the Engine produces without doing work of its own.

### Case 5 — The capability is a composed multi-destination system

If the intent describes something that needs CLAUDE.md + agents + hooks + output-style coexisting as one reversible install (*"build me the whole studio engine"*), the answer is **system**, not any single primitive. System is the composed form; the four discriminators do not resolve because every answer is *"all of the above"*. The system codex handles this.

**When in doubt — use the fall-through.** If none of the cases above match cleanly and the four discriminators above do not resolve, the algorithm falls through to the legacy Q1/Q2/Q3 router in `.claude/skills/create/references/create-router.md`. The creator is never blocked; they simply get the pre-discovery-mode experience for this specific request. Unroutable cases accumulate in `decisions_history` and drive future topology evolution.

---

**Status.** Canonical substrate, v1. Read after `references/intent-topology.md` and before `references/capability-matrix.md` for the creator-facing intuition, or in the opposite order for the algorithmic view of the same discipline. Both orderings are valid; the doc is idempotent.
