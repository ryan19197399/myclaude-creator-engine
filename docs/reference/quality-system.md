# Quality System

How the engine measures and ensures product quality.

---

## Score Formula

```
Overall = (DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)
```

- **DNA** — Compliance with structural patterns across 3 tiers
- **Structural** — File organization, references, activation protocol
- **Integrity** — Internal consistency, no dead references, no placeholders

## Quality Tiers

| Tier | Score | Name | What It Proves |
|:-----|:------|:-----|:--------------|
| Tier 1 | >= 75% | **Verified** | Functional, documented, core patterns present |
| Tier 2 | >= 85% | **Premium** | Professional craft, advanced patterns, anti-commodity signals |
| Tier 3 | >= 92% | **Elite** | State-of-the-art structural DNA, expert-level patterns |

## What Gets Checked — 20 Structural Patterns

### Tier 1 — Universal (7 patterns, required for Verified)

Every product must pass these. They are the foundation.

| Pattern | What It Checks | Fail Example |
|:--------|:---------------|:-------------|
| **Activation Protocol** | Product loads context before acting — reads files, assembles state | Jumps to output without reading any references |
| **Anti-Pattern Guard** | Documents what NOT to do — at least 5 anti-patterns | No guidance on misuse or common mistakes |
| **Progressive Disclosure** | Reveals complexity gradually, not all at once | Dumps 50 configuration options upfront |
| **Quality Gate** | Has verifiable success criteria, not aspirational goals | "Produce high-quality output" instead of measurable criteria |
| **Self-Documentation** | Explains itself during use — what it's doing and why | Silent execution with no transparency |
| **Graceful Degradation** | Handles missing inputs, partial data, unexpected state | Crashes or gives nonsense when a file is missing |
| **Attention-Aware Authoring** | Structured for how LLMs process text — important content first | Buries critical instructions at the end of a long file |

### Tier 2 — Advanced (8 patterns, required for Premium)

Products with nontrivial execution logic.

| Pattern | What It Checks |
|:--------|:---------------|
| **Question System** | Asks good questions before acting — clarifies ambiguity |
| **Confidence Signaling** | Communicates certainty levels — doesn't present guesses as facts |
| **Pre-Execution Gate** | Verifies conditions before executing — checks prerequisites |
| **State Persistence** | Maintains state across interactions — tracks progress |
| **Testability** | Can be tested in an isolated sandbox — reproducible behavior |
| **Composability** | Works with other products — clean interfaces, no conflicts |
| **Hook Integration** | Exposes lifecycle hooks — can be extended by other products |
| **Cache-Friendly Design** | Optimized for context window efficiency — no unnecessary token cost |

### Tier 3 — Expert (5 patterns, required for Elite)

Multi-agent and complex systems.

| Pattern | What It Checks |
|:--------|:---------------|
| **Orchestrate, Don't Execute** | Coordinates rather than does everything itself |
| **Handoff Specification** | Passes work cleanly to humans or other tools with explicit payloads |
| **Socratic Pressure** | Challenges assumptions rather than complying blindly |
| **Compound Memory** | Learns and improves across sessions |
| **Subagent Isolation** | Properly scopes delegated tasks — no context leaks between agents |

## Validation Stages

The `/validate` command checks your product through a multi-stage pipeline:

```
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │Structural│──→│Integrity │──→│  DNA     │──→│  CLI     │
  │ files?   │   │ refs ok? │   │ patterns │   │ preflight│
  │          │   │ no stubs?│   │ 20 checks│   │ ready?   │
  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
       │ BLOCK        │ BLOCK        │ BLOCK         │ BLOCK
       ▼              ▼              ▼               ▼
                                              ┌──────────┐   ┌──────────┐
                                              │  Anti-   │──→│  Value   │
                                              │Commodity │   │  Intel   │
                                              │ unique?  │   │ market?  │
                                              └────┬─────┘   └────┬─────┘
                                                   │ COACH        │ ADVISE
                                                   ▼              ▼
```

Stages in detail:

1. **Structural** (blocking) — Files exist, organization correct
2. **Integrity** (blocking) — No dead references, no placeholders
3. **DNA** (blocking for Tier 1) — Structural patterns present
4. **CLI Preflight** (blocking) — Ready for packaging
5. **Anti-Commodity** (coaching) — What makes this unique?
6. **Value Intelligence** (advisory) — Market position and portfolio role

Blocking stages must pass before packaging. Coaching and advisory stages provide guidance but don't prevent progress.

## Running Validation

```
/validate                   # Check active product
/validate --level=2         # Premium check
/validate --level=3         # Elite check (PRO edition)
/validate --fix             # Auto-fix what can be fixed
/validate --batch           # Validate all products
```

## Understanding Your Score

When you run `/validate`, the engine shows:

**Passing:**
```
READY — 92% (target: 85%)
18/20 structural patterns passing.

  ✦ Elite quality. Craft verified.
```

**Needs work:**
```
NEEDS WORK — 72% (target: 85%)
Top 3 fixes:
  1. Anti-patterns: 2 found, need 5 — add edge cases your product should refuse
  2. Quality gate: criteria not verifiable — use measurable criteria, not aspirational
  3. References: activation protocol must load at least one file

Fix these, then re-run /validate.
```

The engine always tells you **what** failed, **why** it matters, and **how** to fix it. No guessing required.

## Baseline Delta — Measuring Real Value

When you run `/scout` before building, the engine measures what Claude already knows about your domain. This creates a **baseline** — the percentage of domain coverage Claude handles well without your product.

After you build your product, the engine computes the **baseline delta**: how many percentage points of gap coverage your product adds.

```
Baseline: Claude covers 67% of kubernetes-security on its own.
Your product covers the remaining 33% — attack paths, CIS benchmarks,
hardening checklists that Claude can't do alone.

Baseline delta: +33 points vs Claude vanilla.
```

A delta of +33 means your product fills 33 percentage points of gaps. This is measurable, specific value — not "my product is good," but "my product adds exactly this much capability that didn't exist before."

The baseline delta appears in `/validate` output when a scout report exists. It is advisory — it does not affect your quality score, but it tells you exactly how much real value your product delivers.

---

## Score Trajectory

Across multiple products, the engine tracks your quality trajectory:

```
Score trajectory: 78% → 92% → 100% across 3 products
Your craft is visibly improving.
```

This is computed from data, not stored as a label. The engine observes your work and reports what it sees.

---

**Next:** [Commands Reference](commands.md) · [Product Types](product-types.md) · [Getting Started](../getting-started.md)
