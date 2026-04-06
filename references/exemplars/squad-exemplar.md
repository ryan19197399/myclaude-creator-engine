# Squad Exemplar: Content Production Squad

**MCS Level:** 3 (State-of-the-Art)
**Composition:** 3 agents — Strategist, Writer, Editor
**Demonstrates:** Non-overlapping roles, explicit routing table, handoff protocol
with format spec, 2 complete workflow examples, capability index, escalation rules.

---

## File: `SQUAD.md`

```markdown
# Content Production Squad

**Purpose:** Transforms content briefs into publication-ready articles, posts, and
documentation with consistent strategy, clear writing, and editorial quality.

**Composition:** 3 agents
- `content-strategist` — Research, positioning, and structure planning
- `content-writer` — Draft creation with voice and audience calibration
- `content-editor` — Quality review, fact-checking, and final polish

**Entry Point:** Provide a content brief or topic. The squad routes automatically.
**Version:** 2.0.0
**Author:** @contentcraft

---

## Agent Roster

| Agent | File | Role | Handles |
|-------|------|------|---------|
| Content Strategist | `agents/content-strategist.md` | Research, angle, structure | Brief analysis, outline creation, audience positioning |
| Content Writer | `agents/content-writer.md` | First draft creation | Writing from brief or outline, voice application |
| Content Editor | `agents/content-editor.md` | Quality, accuracy, polish | Review, fact-check, readability improvement |

**Role boundaries:**
- Strategist does NOT write prose — only outlines and briefs
- Writer does NOT fact-check — assumes strategist input is accurate
- Editor does NOT rewrite from scratch — returns to writer if draft needs structural work

---

## Routing Logic

### Intent Detection

| Input Pattern | Detected Intent | Routes To |
|---------------|----------------|----------|
| "Write an article/post/doc about..." | `full-production` | Full workflow: Strategist → Writer → Editor |
| "I have an outline, write from it" | `write-from-outline` | Writer (skip Strategist) |
| "Review this draft" | `edit-only` | Editor directly |
| "Research and plan [topic]" | `strategy-only` | Strategist only |
| "Improve this article" | `edit-only` | Editor directly |

### Routing Decision Tree

```
IF input contains draft or existing content → Editor
IF input is brief/topic WITH "just write" or "quick draft" → Writer directly
IF input is brief/topic (standard) → Strategist → Writer → Editor
IF input is outline → Writer → Editor
IF intent is ambiguous → Ask: "Do you have a draft, an outline, or just a topic?"
```

---

## Handoff Protocols

### Standard Handoff Format

```markdown
## Handoff: [Source] → [Target]
**Task:** [What the target agent does next]
**Work Completed:** [What source agent produced]
**Current File:** [Location of output]
**Context:** [Audience, tone, constraints, word count target]
**Priority:** [High | Medium | Low]
**Deadline pressure:** [Yes — urgency | No — quality-first]
```

### Strategist → Writer Handoff

**Triggers when:** Content outline is complete and approved (or auto-proceeds in automatic mode)

**Required context package:**
```markdown
## Handoff: Content Strategist → Content Writer
**Task:** Write first draft from the attached outline
**Work Completed:** Content strategy + detailed outline
**Current File:** [workspace/[slug]/outline.md]
**Context:**
  - Audience: [defined audience profile]
  - Tone: [professional | conversational | technical | etc.]
  - Target word count: [N words]
  - Key message: [the single most important thing reader takes away]
  - SEO target (if applicable): [primary keyword]
  - Must include: [mandatory elements: CTA, statistics, examples, etc.]
**Priority:** [level]
```

**Writer cannot proceed without:** audience, tone, target word count, key message.

### Writer → Editor Handoff

**Triggers when:** First draft is complete.

```markdown
## Handoff: Content Writer → Content Editor
**Task:** Review and polish the attached first draft
**Work Completed:** First draft
**Current File:** [workspace/[slug]/draft-v1.md]
**Context:**
  - Strategy brief: [workspace/[slug]/outline.md]
  - Known weaknesses:** [sections writer flagged as needing attention]
  - Fact-check priority:** [sections making specific claims that need verification]
  - Word count:** [current] / [target]
**Priority:** [level]
```

---

## Workflows

### Workflow 1: Full Production (Topic → Publication-Ready)

**Trigger:** User provides a content brief or topic
**Duration:** ~45-90 minutes (depending on depth)

```
STAGE 1: Strategy (Content Strategist)
  Input: Content brief or topic
  Actions:
    1. Research audience pain points and existing content landscape
    2. Define unique angle: what does this say that others don't?
    3. Create structured outline with H2s, H3s, and key points per section
    4. Define key message, CTA, and SEO keywords (if applicable)
  Output: outline.md + strategy-brief.md
  Gate: User confirms OR auto-proceeds if audience/angle are clear
         ↓ (if approved)

STAGE 2: Writing (Content Writer)
  Input: outline.md + strategy-brief.md
  Actions:
    1. Load voice and style from references/voice-guide.md
    2. Write first draft section by section
    3. Apply audience calibration
    4. Flag any sections needing fact-checking
  Output: draft-v1.md
         ↓

STAGE 3: Editing (Content Editor)
  Input: draft-v1.md + outline.md
  Actions:
    1. Structural review: does the draft follow the outline's logic?
    2. Clarity review: is every sentence earning its place?
    3. Fact-check flagged claims
    4. Final polish: grammar, consistency, formatting
  Output: draft-final.md + edit-notes.md
         ↓

DELIVERY: draft-final.md + quality report
```

**Quality gate:**
- [ ] Word count within 10% of target
- [ ] Key message appears in intro and conclusion
- [ ] All flagged facts verified or clearly marked as unverified
- [ ] No placeholder content (no [INSERT STAT HERE])

---

### Workflow 2: Review and Improve (Draft → Polished)

**Trigger:** User provides an existing draft for improvement

```
STAGE 1: Edit (Content Editor)
  Input: Existing draft
  Actions:
    1. Assess structural integrity (does it have a clear argument?)
    2. If structure is broken → flag for Writer revision (see Escalation)
    3. If structure is sound → proceed with clarity + polish
  Output: draft-improved.md + edit-notes.md

IF structural issues found → Writer
  Input: draft-v1.md + editor notes
  Actions: Restructure based on editor feedback
  Output: draft-v2.md → back to Editor
```

**Quality gate:**
- [ ] Reading level appropriate for target audience (Flesch score: ≥60 for general, ≥40 for technical)
- [ ] No sentences over 35 words without a specific reason
- [ ] Opening paragraph answers: what is this, who is it for, why should I read it

---

## Quality Gates

| Workflow | Gate | Check | Pass Condition |
|----------|------|-------|---------------|
| Full Production | G1 (post-strategy) | Outline reviewed | User confirms OR auto-proceed rule met |
| Full Production | G2 (post-writing) | Draft quality | Word count ±10%, key message present |
| Full Production | G3 (post-edit) | Publication ready | No placeholder, all facts verified/flagged |
| Review & Improve | G1 (post-edit) | Structure sound? | If not → route to Writer for revision |

---

## Escalation Rules

The squad escalates to a human when:

1. **Brief is insufficiently defined** — no clear audience, no clear purpose. Ask: "Who reads this, and what should they do after reading it?"
2. **Factual claims cannot be verified** — Editor cannot verify a statistic and it's core to the argument. Flag explicitly rather than guess.
3. **Content requires legal/compliance review** — medical, legal, financial claims about a specific product. Flag and stop.
4. **Structural revision > 50% of draft** — If Editor's feedback requires rewriting more than half the article, escalate to user for decision rather than auto-revising.

When escalating: preserve all work-in-progress in `workspace/[slug]/`.
Include escalation summary: what was done, what the issue is, what decision is needed.

---

## Capability Index

See `config/capability-index.yaml` for machine-readable capability map.

**Quick reference:**

| Capability | Owner | Notes |
|-----------|-------|-------|
| Audience research and positioning | Content Strategist | THINKER mode — analysis, not writing |
| Content outline creation | Content Strategist | Returns structured outline, not prose |
| Blog post writing | Content Writer | Any topic with an outline |
| Technical documentation | Content Writer | Requires technical reviewer if domain-specific |
| Fact-checking | Content Editor | Web search enabled |
| Readability optimization | Content Editor | Flesch-Kincaid scoring |
| SEO on-page optimization | Content Strategist + Editor | Strategy sets keywords; editor confirms placement |
```

---

## File: `config/capability-index.yaml`

```yaml
# Content Production Squad — Capability Index v2.0.0
squad: content-production

capabilities:
  research_and_strategy:
    owner: content-strategist
    triggers: ["research", "strategy", "outline", "angle", "positioning"]
    produces: ["outline.md", "strategy-brief.md"]

  draft_creation:
    owner: content-writer
    triggers: ["write", "draft", "create content"]
    requires: ["outline.md OR direct brief"]
    produces: ["draft-v1.md"]

  editing_and_polish:
    owner: content-editor
    triggers: ["edit", "review", "improve", "polish", "proofread"]
    produces: ["draft-final.md", "edit-notes.md"]

  full_production:
    orchestrated_by: routing-table
    path: [content-strategist, content-writer, content-editor]
    triggers: ["write an article", "create content about", "blog post on"]
```

---

## Quality Verification

This exemplar demonstrates:

- [x] 3 agents with non-overlapping, explicitly bounded roles
- [x] Role boundaries documented (what each agent DOES NOT do)
- [x] Intent detection routing table
- [x] Handoff protocol with required context specification (not optional)
- [x] 2 complete workflow examples with stage-by-stage breakdown
- [x] Quality gates per workflow
- [x] Escalation rules with specific conditions
- [x] Capability index in YAML
- [x] MCS-3 criteria met
