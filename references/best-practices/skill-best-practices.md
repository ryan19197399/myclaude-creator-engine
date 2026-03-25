# Skill Best Practices

Patterns from high-scoring MCS-3 skills. Each pattern is named, explained, and
accompanied by a contrast (good vs. weak implementation).

---

## Pattern 1: Activation Protocol Design (CE-D34)

**What it is:** An explicit ordered sequence of context-loading steps that run BEFORE
any response is generated.

**Why it matters:** Skills that don't load their reference files are just prompts with
extra files. The Activation Protocol is what transforms `references/` from a file
directory into an active knowledge base.

**Good implementation:**
```markdown
## Activation Protocol

Before responding to any invocation:
1. **Load domain expertise:** Read `references/domain-knowledge.md`
   — Contains: the 6-step analysis framework and confidence tier definitions
2. **Load anti-patterns:** Read `references/anti-patterns.md`
   — Contains: 12 common failures with detection patterns
3. **Load exemplars:** Read `references/exemplars.md`
   — Contains: 5 complete examples across different domains
4. **Identify invocation type:** Parse input to determine mode (surface/dive/radical)
5. **Run question system:** Check for required inputs before proceeding
```

**Weak implementation:**
```markdown
## Context
Read the files in references/ before responding.
```

**What makes the good version work:**
- Each file is named with its exact contents described
- Order is specified (broad → specific)
- Steps include an action after loading (what to do WITH the loaded context)

---

## Pattern 2: Question System Design (CE-D36 / H11)

**What it is:** A structured intake that clarifies ambiguous inputs BEFORE generating
output. "Best products are question systems, not answer systems."

**Why it matters:** Products that immediately generate output from ambiguous input
produce generic output. Products that ask one targeted question first produce specific,
useful output.

**Design principles:**
1. Never ask more than 3 questions at once
2. Required inputs trigger questions; optional inputs have defaults
3. Questions are targetted — not "tell me more" but "what specific X?"
4. State the assumption when defaulting on optional inputs

**Good implementation:**
```markdown
## Question System

Check for these inputs before generating:

| Input | Required | If Missing |
|-------|----------|-----------|
| Subject to analyze | Yes | Ask: "What are you analyzing? Provide the decision, system, or argument." |
| Analysis goal | No | Assume: "Identify weaknesses and improve quality" |
| Depth mode | No | Default: `dive` (state this assumption explicitly) |

When subject is ambiguous, ask ONE clarifying question.
When multiple inputs are missing, ask for ALL required ones in a single message.
Never ask for optional inputs unless user signals they want customization.
```

**Weak implementation:**
```markdown
If you need more information, ask the user.
```

---

## Pattern 3: Triage and Routing Pattern

**What it is:** A decision tree that routes different input types to different processing
paths within the skill.

**Why it matters:** A single skill often needs to handle multiple input types (a code
review skill might receive a file, a diff, or a description). Routing makes the skill
handle each type optimally instead of treating all inputs the same way.

**Good implementation:**
```markdown
## Input Routing

After loading context, identify input type:

| If input is... | Then... |
|---------------|---------|
| Code file path (exists) | Read the file, then analyze |
| Code snippet (inline) | Analyze inline content directly |
| Description of code | Ask for the actual code: "For accurate analysis, share the code." |
| Multiple items | Process each separately, summarize at end |
```

---

## Pattern 4: Progressive Depth Modes (CE-D36)

**What it is:** Three tiers of analysis depth — surface, dive, radical — with
meaningfully different behavior at each tier.

**Why it matters:** Different invocations need different depth. A quick sanity check
needs `surface`. A comprehensive analysis needs `radical`. Providing one mode for all
use cases either under-serves thorough users or overloads quick users.

**Good mode design — modes differ structurally, not just in length:**

| Mode | Structural difference | When to use |
|------|----------------------|-------------|
| `surface` | Steps 1-3 of 6-step framework, brief synthesis | Quick scan, time-constrained |
| `dive` | All 6 steps, standard output | Standard analysis (default) |
| `radical` | All 6 steps + devil's advocate section + second-order effects + alternative framings | Deep expertise, no time constraint |

**Weak mode design — modes differ only in length:**

| Mode | Difference |
|------|-----------|
| `quick` | Short output |
| `detailed` | Long output |

The weakness: `quick` and `detailed` produce the same type of analysis, just more or
less of it. Real depth modes produce different TYPES of analysis.

---

## Pattern 5: Semantic Emphasis for LLM Cognition

**What it is:** Using formatting (bold, code blocks, structure) to direct LLM attention
to the most important constraints.

**Why it matters:** LLMs are sensitive to formatting. Well-formatted instructions
produce more consistent behavior than prose instructions of identical content.

**Good use of semantic emphasis:**
```markdown
Before delivering output:
- **ALWAYS** cite the source for every claim
- **NEVER** include claims with T4 or T5 evidence without flagging them
- `surface` mode skips the pressure test
```

**Guidelines:**
- Use `**ALWAYS**` and `**NEVER**` for non-negotiable rules
- Use code formatting for mode names, parameter names, file paths
- Use tables for multi-row decision logic
- Use headers to create cognitive structure, not just visual separation

---

## Pattern 6: Reference Knowledge Base Structure

**What it is:** A structured `references/` directory where each file serves a distinct,
named purpose that the Activation Protocol explicitly loads.

**Good references/ structure:**
```
references/
├── domain-knowledge.md    # The methodology/framework (loaded 1st)
├── exemplars.md           # Complete examples showing the skill in action (loaded 2nd)
├── anti-patterns.md       # What to avoid with detection rules (loaded 3rd)
└── terminology.md         # Domain-specific vocabulary (loaded when needed)
```

**What makes it work:**
- Each file has ONE purpose (not a "misc" dump file)
- Activation Protocol specifies which file to load first and why
- Files are dense with information, not padding
- Exemplars file is distinct from domain knowledge

---

## Pattern 7: Quality Gate Pattern

**What it is:** A self-check the skill runs AFTER generating output, BEFORE delivering it.

**Good quality gate:**
```markdown
## Quality Gate

Before delivering output:
- [ ] Every claim has a confidence tier declared (T1-T4)
- [ ] Output includes both key findings AND a synthesis
- [ ] Mode was acknowledged explicitly in the output header
- [ ] At least one counterargument was considered (dive and radical modes)

If any check fails: revise the relevant section before delivering.
```

**Design rules:**
1. Each check must be specific enough to actually fail
2. The "if any check fails" action must be specific
3. Gate covers the most important outputs, not everything (4-5 items max)
4. Gate is checked at output time, not at design time

---

## Heuristics Summary

These 12 heuristics from the framework apply directly to skill design:

| H# | Heuristic | Applies To |
|----|-----------|-----------|
| H1 | AI-generatable content is not differentiation | References/ content |
| H2 | Start with the use case, not the technology | Trigger conditions |
| H3 | Three good exemplars teach more than ten pages of docs | Exemplars count |
| H6 | Every anti-pattern documented saves ten support questions | Anti-patterns section |
| H9 | Narrow and brilliant beats broad and mediocre | Scope of skill |
| H10 | Test with least obvious use case first | Stress testing |
| H11 | Question systems > answer systems | Question system design |
| H12 | Every product needs an Activation Protocol | Activation Protocol |
