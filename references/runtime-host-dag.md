# Runtime Host Derivation — The Computed Lookup Table

This document declares the derivation table that computes an artifact's runtime host set from the pair `(delivery_mechanism, operational_nature)`. Host is never declared on an artifact; it is always computed from the pair at validate time. This is the operational form of the vestigial-organ elimination from `references/intent-topology.md` §3 — the `host_compatibility` field was removed from codex declarations because its information is fully redundant with the pair that produces it.

**Layer:** Canonical substrate. Consumed by `.claude/skills/create/` Step 8 (DERIVE_HOST) in the 12-step algorithm defined in `references/capability-matrix.md`. Also consumed by `.claude/skills/validate/` Stage 0 Intent Coherence when checking that a forged product's declared delivery and nature produce a host set compatible with its type.

**Reading order:** §1 the three host labels → §2 the derivation table → §3 why host is derived, not declared.

---

## §1 — The Three Runtime Host Labels

At runtime, a Claude Code artifact executes in exactly one of three locations. These labels describe *where the execution actually happens* at the moment of invocation, not where the artifact's files live on disk.

| Label | Meaning |
|---|---|
| `session_root` | Execution happens in the creator's primary session. The parent context is shared. Tools available are the session's tool pool. Output flows into the parent conversation. |
| `agent_spawn` | Execution happens in a forked context spawned by the Task tool. The parent context is not shared. Own tool pool, own system prompt, own memory scope. Output returns as a task result. |
| `hook_handler → agent_spawn` | Execution begins as a hook handler (fired automatically on a canonical hook event) and, when the handler type is `AgentHook`, chains into a task-spawned execution. Two-stage runtime: trigger stage + work stage. |

A fourth label, `preloaded_in_agent`, is a specialization of `session_root` reachable only when an agent is spawned via `invoked_task_spawn` with an `ambient_path_scoped` skill in its `skills:` frontmatter. The skill preloads into the agent's fork context as an `isMeta` user message at spawn time. It is not an independent host — it is `session_root` inside a fork.

---

## §2 — The Derivation Table

Given a `(delivery_mechanism, operational_nature)` pair, read the row that matches both values. The output is the host set that applies to every artifact with that pair.

| Delivery | Nature | Host set | Example cell |
|---|---|---|---|
| `ambient_constitutional` | any | `[session_root]` | Cell 7 `project_constitution` (claude-md, procedural) |
| `ambient_path_scoped` | `executor` or `advisor` | `[session_root, preloaded_in_agent*]` | Cell 2 `perspective_skill_cognitive` (cognitive skill ambient-preferred) |
| `invoked_slash_command` | `executor` or `advisor` | `[session_root]` | Cell 1 `reasoning_skill_cognitive` (cognitive skill); Cell 6 `procedural_skill` |
| `invoked_task_spawn` | `executor` | `[agent_spawn]` | Cell 5 `domain_specialist_executor` (agent specialist) |
| `invoked_task_spawn` | `advisor` | `[agent_spawn]` | Cell 4 `code_reviewer_agent` (agent adviser); Cell 3 `apex_cognitive_mind` (cognitive minds) |
| `invoked_task_spawn` | `orchestrator` | `[agent_spawn]` | `squad_coordinator` (v2 — squad) |
| `invoked_task_spawn` | `observer` | `[agent_spawn]` | *(no habitable cell — observers are typically hook-bound, not task-spawned)* |
| `reflex_hook_binding` | `executor` | `[session_root, agent_spawn]` | `event_reflex` (v2 — hooks, BashCommandHook or HttpHook) |
| `reflex_hook_binding` | `observer` | `[hook_handler → agent_spawn]` | `longitudinal_observer` (v2 — hooks + minds, orphan, GAP-COMPOSITION-1) |
| `composed_system` | any | `[multi — inherited from composed sub-parts]` | `cognitive_organism_full_stack` (v2 — system) |

**\*** `preloaded_in_agent` appears only when an agent is spawned with the ambient-path-scoped skill in its `skills:` heredity frontmatter. For standalone ambient skills (the common case), the host set reduces to `[session_root]`.

**Reading the composed_system row.** A system product's host set is the union of the host sets of its composed sub-parts. A system containing one CLAUDE.md fragment + two agents + one hook produces `[session_root, agent_spawn, hook_handler → agent_spawn]` at install time. The system itself has no runtime host of its own — it is a composition primitive, not a runtime shape.

**Reading the two unreachable combinations.** The table explicitly marks `invoked_task_spawn × observer` as having no habitable cell. Structurally, an observer nature writes to memory scope without responding; task-spawn inherently expects a return value to the caller. A task-spawned observer would return nothing useful and would waste a fork context. Observers that run automatically belong in hooks; observers that run on demand in the session fold into the normal skill or agent patterns. The cell is empty by physics, not by oversight.

---

## §3 — Why Host Is Derived, Not Declared

Three structural reasons make host a derived property rather than a declared field on artifacts.

**Reason 1 — Zero information gain.** Enumerating the `(delivery, nature)` pairs in §2 produces a deterministic host set for every habitable combination. A `host:` field declared on an artifact duplicates this information exactly — it cannot say anything the pair does not already say. A field that duplicates its inputs is vestigial; it can only drift, never add signal.

**Reason 2 — No consumer in the existing substrate.** Neither `config.yaml` nor any of the 6 certified codices (output-style, skill, agent, squad, system, minds) reads a `host_compatibility` field. The field had no afferent nerve — nothing downstream consulted it. Adding a field without a consumer is architectural decoration, not architectural substance.

**Reason 3 — Drift-free by construction.** A declared field can drift from the values it duplicates: an artifact might declare `delivery: ambient_path_scoped` and `host: agent_spawn` and the inconsistency would silently propagate. A computed derivation cannot drift — it is the pair that produces the host, so the pair and the host are always in lockstep. Drift prevention is structural, not procedural.

**What this means for codex extensions.** When the 6 certified codices are extended with new fields in the codex-extension wave (delivery_mechanism and operational_nature added as declared attributes), they do **not** receive a `host` field. Any future substrate that needs the host computes it from the pair at read time via the table in §2. The table is the single source of truth; no artifact and no codex owns a redundant copy of it.

---

**Status.** Canonical substrate, v1. Pure derivation table, not a declared taxonomy. Read after `references/intent-topology.md` (which introduces the axes) and in conjunction with `references/capability-matrix.md` §3 Step 8 (which invokes this table during the decision algorithm).
