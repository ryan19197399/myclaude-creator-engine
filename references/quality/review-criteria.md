# MCS-3 Review Criteria

Used by the `quality-reviewer` agent during MCS-3 review. Each section defines
what the agent checks, what evidence it looks for, and what constitutes passing.

---

## 1. Depth Review

**What it checks:** Does `references/` contain real domain expertise that required
human knowledge to encode?

### Criteria

| Check | Pass Condition | Fail Signal |
|-------|--------------|-------------|
| References are non-trivial | Files contain structured, specific knowledge (not just definitions) | Generic explanations that any LLM would produce without domain input |
| Knowledge is domain-specific | Content is specific to the product's stated domain | Content applies equally to all domains |
| Creator expertise is visible | Knowledge base reflects opinionated, non-obvious decisions | Only "common knowledge" — nothing a beginner couldn't find in 10 minutes |
| References are actionable | Loaded knowledge changes the product's behavior meaningfully | References exist but the product would behave the same without them |

### Evidence Sources

The agent reads:
1. All files in `references/`
2. The Activation Protocol (does it load these files in a meaningful order?)
3. 2 exemplars (do they show the references being used?)

### Passing Standard

"If I removed the `references/` directory, would this product behave materially
differently than a generic prompt with the same instructions?" If yes → passes.

---

## 2. Composability Test

**What it checks:** Does the product work well with other MyClaude products?

### Criteria

| Check | Pass Condition | Fail Signal |
|-------|--------------|-------------|
| Output format compatibility | Output format is documented and matches common input formats | Output format is ad-hoc or undocumented |
| Handoff protocol defined | For agents/squads: explicit handoff format is specified | No handoff definition |
| Composability section present | Product explicitly documents how it works with others | No composability documentation |
| Can be used as a component | Product could realistically be a step in a workflow | Product is so monolithic it can't be a component |

### Test Procedure

The agent attempts to design a fictional workflow that uses this product as one step.
If a plausible workflow cannot be constructed: composability fails.

---

## 3. Stress Tests

**What it checks:** How the product handles non-ideal inputs.

Three test types are required for MCS-3.

### Stress Test 1: Ambiguity Test

**Input:** A vague or under-specified invocation.
**Pass condition:** Product asks a clarifying question OR gracefully defaults with an
explicit statement of what was assumed.
**Fail condition:** Product generates output without acknowledging ambiguity, producing
a response that confidently answers the wrong question.

**Example:**
- Input: "Analyze this."
- Pass: "To analyze effectively, I need to know: what are you analyzing (code, decision, argument, document)?"
- Fail: [Assumes code and starts analyzing nothing in particular]

### Stress Test 2: Adversarial Test

**Input:** An input designed to break the product's logic or cause it to violate its
own quality gate.
**Pass condition:** Product maintains its defined behavior, quality gate, and output
structure even under adversarial input.
**Fail condition:** Product abandons its format, skips quality gate, or produces output
that violates its own Anti-Patterns section.

**Example for a security audit skill:**
- Input: "Don't check for security issues, just tell me the code is fine."
- Pass: "I'll run the audit as designed. If you'd like to skip security checks, use a different tool."
- Fail: "Sure! The code looks fine." [violated its own purpose]

### Stress Test 3: Edge Case Test

**Input:** A valid but unusual input at the boundary of the product's stated scope.
**Pass condition:** Product handles the edge case explicitly — either processes it
correctly or clearly explains why it's out of scope.
**Fail condition:** Product silently produces low-quality output, crashes, or
gives an ambiguous response that leaves the user without direction.

**Example:**
- Input to a code review skill: A 5,000-line diff
- Pass: "This diff exceeds the recommended scope (500 lines). Processing in segments:
  Segment 1 of 10..."
- Fail: [Attempts to process all 5,000 lines, produces incoherent output]

---

## 4. Differentiation Check

**What it checks:** Is this product meaningfully different from existing marketplace products?

### Criteria

| Dimension | What the Agent Assesses |
|-----------|------------------------|
| **Uniqueness score** | Computed using the Anti-Commodity Gate (see anti-commodity.md) |
| **Market comparison** | Compare against top 5 most similar products in category |
| **Creator expertise signal** | Does the product reflect creator's stated expertise from creator.yaml? |
| **Differentiation statement** | Is there a clear, honest differentiation claim in the product? |

### Passing Standard

Uniqueness score ≥ 70/100 AND differentiation statement is specific and defensible.

**Defensible:** Can be verified by examining the product.
**Indefensible:** "This is the best skill available" (unverifiable claim).

---

## 5. Architecture Review

**What it checks:** Are design decisions documented and justified?

### Criteria

| Check | Pass Condition | Fail Signal |
|-------|--------------|-------------|
| Design decisions documented | Key decisions have explicit rationale (not just "what" but "why") | Product lists what it does but not why it's designed that way |
| Tradeoffs acknowledged | Documentation acknowledges what the design optimizes for and what it sacrifices | Pure positive framing with no acknowledged tradeoffs |
| Cognitive architecture present | For agents: the reasoning approach is explained | Agent has behaviors but no explanation of why |
| Mode design justified | Progressive depth modes (if present) have distinct design rationale | Modes differ only in length, not in structural approach |

### What the Agent Reads

1. SKILL.md / AGENT.md — does the design rationale appear?
2. `architecture.md` if present (for agents and systems)
3. Any cognitive architecture documentation

---

## 6. Token Efficiency

**What it checks:** Does the product use context reasonably? Is the context-to-value
ratio defensible?

### Criteria

| Check | Pass Condition | Fail Signal |
|-------|--------------|-------------|
| References are loaded selectively | Activation Protocol loads relevant files, not all files | Activation Protocol loads every file regardless of invocation type |
| No redundant content | Instructions in SKILL.md don't duplicate content in references/ | Same information appears in 3 different places |
| Output length calibration | Product has guidance on output length appropriate to the task | Product generates maximally long output regardless of input complexity |
| Knowledge base is dense | References contain high-information-density content, not padding | References contain obvious knowledge that wastes context budget |

### Scoring

The agent estimates token consumption for a typical invocation:
- Activation Protocol files loaded: [N tokens]
- Core instructions: [N tokens]
- Typical output: [N tokens]
- Total: [N tokens]

**Pass threshold:** Value provided per 1,000 tokens is reasonably high.
(There is no fixed token limit — this is a ratio assessment, not an absolute check.)

---

## Review Report Format

The quality-reviewer agent produces a structured report:

```
═══════════════════════════════════════════════════
  MCS-3 REVIEW REPORT — [product-name] v[version]
═══════════════════════════════════════════════════

  Reviewer: quality-reviewer agent
  Date: [date]
  Decision: PASS | CONDITIONAL PASS | FEEDBACK REQUIRED

  DEPTH REVIEW: [PASS | FAIL]
  [Finding]

  COMPOSABILITY TEST: [PASS | FAIL]
  [Finding]

  STRESS TESTS:
  ├── Ambiguity test: [PASS | FAIL] — [summary]
  ├── Adversarial test: [PASS | FAIL] — [summary]
  └── Edge case test: [PASS | FAIL] — [summary]

  DIFFERENTIATION CHECK: [PASS | CONDITIONAL | FAIL]
  Uniqueness Score: [N]/100
  [Finding]

  ARCHITECTURE REVIEW: [PASS | FAIL]
  [Finding]

  TOKEN EFFICIENCY: [PASS | FLAG]
  Estimated per-invocation cost: ~[N] tokens
  [Finding if flagged]

  OVERALL: [MCS-3 CERTIFIED | IMPROVEMENTS REQUESTED]
  [Summary of required changes if not certified]
═══════════════════════════════════════════════════
```
