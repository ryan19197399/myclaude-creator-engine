# Structural DNA — Tier 3 (Expert)

> Loaded on-demand by `/validate` (level 3) and `/create` when scaffolding multi-agent
> products (squad, system). Not loaded at boot. See `structural-dna.md` for the
> boot-resident layer (9 architectural principles + Tier 1 universal patterns).

5 patterns. Required for MCS-3. Multi-agent systems only.

---

### D9: Orchestrate, Don't Execute

**Tier:** 3 — Expert

**Problem it solves:**
An orchestrator that does specialist work produces mediocre output across all domains.
When the squad leader also does the code review AND the security audit AND the
documentation check, none of them get specialist-quality attention.

**Rule:**
Orchestrators route and coordinate. They do NOT contain domain instructions. A squad
orchestrator's SQUAD.md must contain a routing table with specialist assignments —
not the actual logic for how to do any of the specialties. Domain expertise lives
in the specialist agents.

**Validation check:**
```
For squad/system types:
grep "routing table\|route to\|delegate to\|assign to\|orchestrat" SQUAD.md OR SYSTEM.md → must match
AND grep -i "domain instruction\|specifically.*you should check\|step.*by.*step.*how to" SQUAD.md → must be 0
```
PASS if routing table found and no domain instructions in orchestrator. PARTIAL if orchestrator has both
routing AND some domain instructions.

---

### D10: Handoff Specification

**Tier:** 3 — Expert

**Problem it solves:**
Vague context at agent handoffs causes cascade degradation — each agent compounds the
ambiguity of the previous one, producing output that drifts progressively further from
the original intent.

**Rule:**
Every agent-to-agent handoff must specify exactly: what was done, what was decided
(including rejected alternatives), and what the next agent specifically needs.
The handoff template must be embedded in the product and used consistently.

**Example:**
```
HANDOFF: {source} → {target}
WHAT_DONE: {completed work summary}
WHAT_DECIDED: {decisions made + alternatives rejected}
WHAT_NEXT_NEEDS: {specific context for target}
FILES_MODIFIED: {list}
```

**Validation check:**
```
grep -i "handoff\|what_done\|what_decided\|what_next\|files_modified" {AGENT_FILES}
AND all agent files have handoff section
```
PASS if handoff template found in all agent files. PARTIAL if found in some but not all.

---

### D11: Socratic Pressure

**Tier:** 3 — Expert

**Problem it solves:**
Agents that accept their first output produce consistent but not improving quality.
Socratic pressure — challenging the output before delivering it — catches errors,
weak reasoning, and incomplete analysis that would otherwise reach the user.

**Rule:**
Agents that produce analysis or recommendations must include a self-challenge step:
"What is wrong with this output?" or "What would a critic say?" before finalizing.
The challenge must be genuine (not rhetorical) — it must be capable of changing the output.

**Validation check:**
```
grep -i "socratic\|challenge.*output\|what.*wrong\|critic\|falsif\|counter.*argument\|self.*challenge" {AGENT_FILES}
```
PASS if self-challenge pattern in ≥1 agent. PARTIAL if language suggests challenge but not structured.

---

### D12: Compound Memory

**Tier:** 3 — Expert

**Problem it solves:**
Without cross-session memory, agents start fresh every session. Patterns discovered,
anti-patterns encountered, and architectural decisions made disappear. Compound memory
is what allows a system to improve over time rather than plateau.

**Rule:**
Multi-agent systems must define memory configuration using Claude's native memory scopes
(user, project, local). Project memory persists patterns per-project. User memory
persists creator preferences across projects. At least one memory scope must be
configured in agent frontmatter.

**Validation check:**
```
grep -i "memory:\|user memory\|project memory\|local memory" {AGENT_FRONTMATTER}
AND at least one agent has memory: project or memory: user
```
PASS if ≥1 agent has memory configuration. PARTIAL if memory section present but scope unspecified.

---

### D18: Subagent Isolation

**Tier:** 3 — Expert

**Problem it solves:**
Agents without context isolation bleed session state into each other. When one agent's
conversation history is visible to another, it introduces bias, context pollution,
and makes the second agent's output dependent on the first's phrasing choices rather
than the actual task.

**Rule:**
Every subagent in a squad or system must run in isolated context (context: fork in
skill frontmatter OR defined as a separate subagent with own context window). Agents
must communicate through explicit handoffs, not shared session state.

**Semantic boundaries** reinforce isolation beyond `context:fork`:
- Use explicit scope instructions: "Within this agent, your function is X and ONLY X"
- Use XML-style delimiters (`<agent role="analyst">...</agent>`) in handoff payloads
- Never let one agent's domain knowledge leak into another — each loads its own references/
- The handoff spec (D10) IS the boundary contract between agents

**Validation check:**
```
grep "context: fork\|context:fork" {AGENT_SKILL_FILES} → must match ≥1
AND each agent is defined as separate subagent (own SKILL.md or AGENT.md)
```
PASS if context:fork present in all multi-agent definitions. PARTIAL if present in some agents but not all.
