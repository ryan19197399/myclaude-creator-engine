# Use Cases

How different professionals use the Studio Engine to build tools that solve real problems in their domain.

```
THE ARC — every use case follows this shape:

  FRUSTRATION               EXPERTISE               PRODUCT
  ───────────               ─────────               ───────
  Claude gives you          You have 10+            Anyone installs
  generic advice.           years of knowing        your methodology
  Your methodology          exactly what to do.     with one command.
  sits in your head.        The engine captures     Claude becomes
  Nobody else can           it, section by          your specialist.
  access it.                section.

  ────── /scout ──→──── /create + /fill ──→──── /validate + /publish ──→
```

---

## For Lawyers and Legal Professionals

### Contract Review Advisor

A corporate lawyer builds an advisor that applies her 12 years of contract review methodology to any agreement Claude analyzes.

**The frustration without the engine:** She asks Claude to review a vendor agreement. Claude identifies the major clauses correctly — indemnification, liability cap, termination. But it misses that the "best efforts" language in Section 4.2 means something entirely different under Delaware law than New York law. It doesn't catch that the renewal clause auto-extends with a 90-day notice window that practically guarantees lock-in. It gives her what a second-year associate would give her. She has 12 years of pattern recognition that Claude cannot access — and no way to make it accessible.

**The problem:** Claude can identify standard contract clauses, but it misses jurisdiction-specific risks, doesn't know which "standard" terms actually favor the counterparty, and can't flag the subtle language patterns that experienced lawyers catch — the difference between "best efforts" and "commercially reasonable efforts" in Delaware vs. New York.

**What she builds:**

```
/scout contract-review
```
> Claude covers general clause identification well. Gaps: jurisdiction-specific risk scoring,
> party-favoring language detection, renewal/termination trap patterns, indemnity scope analysis.
> Recommendation: cognitive mind.

```
/create minds
```

During `/fill`, the engine asks:
- "Walk me through the first 5 things you check in any new contract."
- "What are the 3 most common traps you see in indemnification clauses?"
- "When you see a 'best efforts' clause, what determines whether it's actually risky?"
- "Describe a situation where a standard-looking clause cost a client real money."

**The result:** An installable advisor that any lawyer on her team — or any client — can use. Claude goes from generic contract analysis to applying her specific methodology: jurisdiction-aware risk scoring, party-favoring language detection, the patterns she has learned from reviewing thousands of agreements.

```
✦ Result
  ┌─────────────────────────────────────────────────────┐
  │  myclaude install contract-review-advisor            │
  │                                                     │
  │  Before: Claude gives second-year associate output  │
  │  After:  Claude applies 12 years of pattern         │
  │          recognition — jurisdiction-aware,           │
  │          party-favoring, trap-detecting              │
  └─────────────────────────────────────────────────────┘
```

---

### Compliance Checklist Workflow

A compliance officer at a fintech builds a workflow that standardizes how his team verifies regulatory compliance across new product launches.

**What he builds:** A `workflow` product with step-by-step verification: data privacy assessment → licensing requirements by state → consumer protection obligations → documentation checklist. Each step has explicit pass/fail criteria and escalation rules.

**Why it matters:** Every new analyst follows the same process. Nothing gets skipped. The checklist updates when regulations change — one update, every team member gets it.

---

## For Marketing Professionals

### Brand Positioning Advisor

A brand strategist with 10 years of experience packages her differentiation methodology as an installable advisor.

**The frustration without the engine:** She asks Claude to help position a B2B SaaS product. Claude responds with "identify your target audience and craft a unique value proposition." That is the equivalent of a doctor saying "try to be healthier." Her 10-year methodology has 4 diagnostic steps that distinguish messaging problems from identity problems from market problems — and Claude has no access to any of it. She has tried writing it into CLAUDE.md files. It works for one project. Then she starts a new project and the methodology is gone.

**The problem:** Claude gives generic positioning advice — "find your unique value proposition," "know your audience." Her methodology is specific: a 4-step diagnostic that identifies whether a brand has a messaging problem, an identity problem, or a market problem, with different solutions for each.

**What she builds:**

```
/scout brand-positioning
```
> Gaps: differentiation in crowded markets, emotional positioning for B2B,
> repositioning without losing existing customers.

During `/fill`, the engine asks:
- "How do you diagnose whether a brand has a messaging problem vs. an identity problem?"
- "What are your warning signs that positioning needs work?"
- "Walk me through a repositioning case where the obvious move was wrong."

**The result:** Anyone who installs her advisor gets her specific diagnostic framework. A startup founder describes their company, and Claude responds with her methodology — not generic advice, but the same structured analysis she would give in a consulting engagement.

```
✦ Result
  ┌─────────────────────────────────────────────────────┐
  │  myclaude install sofia-brand-positioning            │
  │                                                     │
  │  Before: "Find your unique value proposition"       │
  │  After:  4-step diagnostic that distinguishes       │
  │          messaging problems from identity problems   │
  │          from market problems — with different       │
  │          solutions for each                          │
  └─────────────────────────────────────────────────────┘
```

---

### Content Strategy System

A content director builds a `system` that combines three products:
- A `minds` advisor with her editorial strategy framework
- A `skill` that analyzes content gaps against competitor coverage
- A `workflow` for the monthly editorial planning process

**Why a system:** Each piece works alone, but together they create an editorial intelligence stack. The advisor informs strategy, the skill provides data, and the workflow ensures the team executes consistently.

---

## For Consultants and Coaches

### Business Model Advisor

A business coach who has guided 200+ startups through product-market fit builds a cognitive mind with his framework.

**The frustration without the engine:** A founder in his community asks Claude for help with product-market fit. Claude gives a textbook answer about customer interviews and MVP testing. It is correct and completely useless — because it doesn't know the 6 diagnostic questions he asks in every first session, or the pattern he has seen across 200+ startups where founders who describe their product before their customer always fail. His 15 years of coaching is sitting in his head while his community gets generic AI advice.

**The problem:** Claude can explain business model concepts, but it doesn't know his specific diagnostic sequence — the 6 questions he asks every founder in the first session, the pattern-matching from 200+ cases, the red flags that predict failure before the founder sees them.

**What he builds:**

During `/fill`, the engine asks:
- "What are the 6 questions you ask every founder in the first session?"
- "What patterns have you seen in businesses that fail to find product-market fit?"
- "When a founder says 'everyone is my customer,' what do you actually do next?"
- "Describe your framework for determining whether to pivot or persist."

**The result:** His community installs the advisor. A founder describes their business, and Claude walks them through his exact framework — the same sequence, the same probing questions, the same pattern recognition. Not generic startup advice. His methodology.

---

### Sales Methodology Workflow

A sales trainer builds a `workflow` that standardizes her team's discovery call process: qualification criteria → needs assessment → objection mapping → proposal framework. Each step has the questions to ask, the signals to listen for, and the decision criteria for moving forward or disqualifying.

---

## For One-Person Businesses

### The Solo Operator Stack

A solopreneur who runs a design agency loses 2 hours every week on the same operational tasks — client intake briefs that follow the same structure, brand audits that check the same criteria, proposals that use the same pricing psychology. He does these manually every time because he never found a way to encode them into his tools. The engine gives him that way.

He builds a bundle of 4 products that automate the parts of his business he does repeatedly:

| Product | Type | What It Does |
|:--------|:-----|:-------------|
| Client Intake | workflow | Standardized onboarding: brief → scope → timeline → contract checklist |
| Brand Audit | skill | Analyzes a client's existing brand assets against his evaluation rubric |
| Proposal Writer | minds | Applies his proposal methodology — scope framing, pricing psychology, deliverable structure |
| Project Review | squad | 3-agent team: design critic + copy reviewer + accessibility checker |

**How he builds it:**

```
/scout design-agency-operations
/create workflow    → client-intake
/create skill       → brand-audit
/create minds       → proposal-writer
/create squad       → project-review
/create bundle      → design-agency-stack
```

Each product takes 15–30 minutes. The bundle packages them together. His future self — or anyone running a similar agency — installs everything with one command.

```
✦ Result
  ┌─────────────────────────────────────────────────────┐
  │  myclaude install design-agency-stack                │
  │                                                     │
  │  Before: 2 hours/week on repetitive operations      │
  │  After:  4 products handle intake, audits,          │
  │          proposals, and reviews automatically        │
  │                                                     │
  │  One afternoon to build. Hours saved every week.    │
  └─────────────────────────────────────────────────────┘
```

**Why this works:** He is not selling software. He is packaging the operational intelligence he has built over years of running his business. The engine handles structure and quality. He provides the expertise.

---

### Freelancer Efficiency Kit

A freelance developer builds three tools that save her hours every week:
- A `hooks` product that runs her pre-commit checklist automatically on every file write
- A `skill` that generates client-facing changelogs from git history in her specific format
- A `claude-md` that enforces her coding standards across all client projects

Total build time: one afternoon. Time saved: hours per week, compounding.

---

## For Researchers and Academics

### Literature Review Advisor

A PhD researcher builds an advisor that applies her systematic review methodology — the specific inclusion/exclusion criteria framework, the quality assessment rubric, the synthesis approach she has refined across 15 publications.

**During `/fill`:**
- "What are your inclusion criteria categories? Walk me through each one."
- "How do you assess methodological quality? What's your rubric?"
- "When two studies contradict each other, what's your resolution framework?"

**The result:** Her graduate students install the advisor. They get her methodology applied to their literature reviews — consistent quality, her framework, without scheduling time with her.

---

### Data Analysis Workflow

A data scientist builds a `workflow` that standardizes his team's analysis process: data profiling → outlier detection → feature selection → model evaluation → report generation. Each step has explicit quality gates — the analysis doesn't proceed until data quality passes threshold.

---

## The Pattern

Every use case follows the same arc:

1. **You feel the friction** — you explain the same thing repeatedly, Claude gives generic advice where you have specific methodology, your team operates inconsistently, or you spend hours on repetitive operational tasks
2. **You have expertise** that Claude doesn't have natively — your methodology, your frameworks, your pattern recognition from years of practice
3. **`/scout` measures the gap** — what Claude already covers vs. where your knowledge adds real value. The baseline delta tells you exactly how many points of capability your product would add
4. **`/fill` captures your thinking** — the engine asks domain questions, you answer in plain language, it writes the structure
5. **`/validate` verifies quality** — 20 structural patterns ensure your product is robust, not just functional
6. **`/publish` distributes it** — anyone installs with one command. Your expertise becomes infrastructure

The engine doesn't create the expertise. You have that already. The engine turns it from something locked in your head into something installable, validated, and shareable — permanently.

---

**Next:** [Getting Started](getting-started.md) · [For Domain Experts](guides/for-domain-experts.md) · [Product Types](reference/product-types.md)
