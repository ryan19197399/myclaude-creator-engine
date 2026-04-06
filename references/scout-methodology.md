# Scout Methodology — Baseline Testing & Gap Analysis

## Why Baseline Testing Matters

Every Claude Code product competes with one free alternative: **Claude itself**.

If a product doesn't demonstrably improve on what Claude vanilla provides, it has zero value.
The baseline test makes this competition explicit and measurable.

## The Baseline Test Protocol

### What to test
Ask Claude vanilla to be an expert in the target domain. The prompt must be:
- **Broad enough** to surface Claude's full knowledge (not a single narrow question)
- **Structured enough** to produce comparable outputs (key concepts, approaches, pitfalls)
- **Honest** — don't sandbag the baseline to make gaps look bigger

### Epistemic limitation
The baseline is a **simulation**, not an observation. Claude generates it with the Engine's
CLAUDE.md in context, which may inflate quality (the Engine context primes better reasoning).
A true vanilla baseline would require a clean session without Engine instructions. Treat the
baseline as "upper bound of Claude vanilla" and note this in the Confidence section of every
scout report. Gaps found against an inflated baseline are STILL real — they're just conservative.

### Standard baseline prompt
```
You are an expert in {domain}. Explain:
1. The key concepts a practitioner must understand
2. Common approaches and when to use each
3. Best practices that distinguish experts from beginners
4. Common pitfalls and how to avoid them
5. How a professional would approach a new project in this domain
```

### Evaluating the baseline
| Rating | Meaning | Product implication |
|--------|---------|-------------------|
| **Strong** | Covers 80%+ accurately | Product must go DEEP — surface-level won't add value |
| **Moderate** | Covers 50-80%, some gaps | Product fills specific gaps — targeted value |
| **Weak** | Covers <50% or has errors | Product has high potential — significant value add |

## The 4-Lens Gap Analysis

### Lens 1: Missing
What topics weren't mentioned at all? These are blind spots — Claude doesn't know it doesn't know.

**How to find:** Compare baseline against a domain expert's mental model. What would an expert
notice is absent? Check: advanced techniques, edge cases, recent developments, cross-domain
connections, tooling, real-world constraints.

### Lens 2: Shallow
What was mentioned but lacks the depth a practitioner needs?

**How to find:** For each topic in the baseline, ask: "Could someone ACT on this advice?"
If the answer is "they'd need to Google more first," it's shallow.

### Lens 3: Wrong
What common misconceptions or outdated information appears?

**How to find:** Look for: deprecated practices presented as current, oversimplifications that
lead to wrong decisions, missing caveats on recommendations, version-specific advice without
version context.

### Lens 4: Generic
What lacks the specificity of real-world experience?

**How to find:** Look for: textbook advice without production context, "best practices" without
tradeoff discussion, recommendations without "it depends" qualifiers, absence of war stories
or failure modes.

## Severity Rating

| Severity | Definition | Action |
|----------|-----------|--------|
| **Critical** | Gap could cause harm, significant waste, or fundamentally wrong decisions | MUST be addressed by a product |
| **Significant** | Expert would immediately notice; noticeably better with product | SHOULD be addressed |
| **Minor** | Improves experience but baseline is functional | NICE to address if natural |

## From Gaps to Products

The gap-to-product mapping follows the Engine's taxonomy:

- **Knowledge gaps** (missing/shallow expertise) → **minds** (advisory intelligence)
- **Process gaps** (missing workflows/procedures) → **skill** or **workflow**
- **Judgment gaps** (needs context-dependent decisions) → **agent**
- **Multi-perspective gaps** (needs specialized collaboration) → **squad**
- **Systemic gaps** (entire domain needs infrastructure) → **system**
- **Consistency gaps** (output quality varies) → **claude-md** or **output-style**

## Research Integration

External research transforms gap analysis from "Claude talking about itself" into
"evidence-based intelligence." Priority research targets:

1. **Critical gaps** — 2-3 searches each, fetch best results
2. **Significant gaps** — 1-2 searches each
3. **Trends** — what's changing in the domain RIGHT NOW
4. **Failures** — case studies of what goes wrong (highest learning density)

Research quality > research quantity. 5 well-synthesized sources beat 20 shallow summaries.
