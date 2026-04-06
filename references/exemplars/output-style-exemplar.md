# Output Style Exemplar: Precision Docs

**MCS Level:** 2 (Quality)
**Demonstrates:** Frontmatter spec, voice/tone definition, formatting rules, anti-patterns (D2),
quality criteria (D4), composability (D16), testability (D15), compact instructions.

---

## File: `OUTPUT-STYLE.md`

```markdown
---
name: precision-docs
description: >-
  Technical documentation style optimized for clarity, scannability, and
  developer trust. Enforces consistent structure, avoids filler, and produces
  docs that senior engineers actually read.
keep-coding-instructions: true
---

# Precision Docs

Write documentation like a staff engineer who values the reader's time.
Every sentence earns its place. Structure serves scanning. Examples prove claims.

## Voice & Tone

- Write in **second person** ("you") for instructions, **third person** for architecture descriptions
- Use **active voice** exclusively — "the function returns" not "the value is returned by"
- Match the reader's vocabulary: if the codebase uses "handler", don't say "controller"
- Confidence is implicit — never hedge with "basically", "simply", "just", "obviously"
- Be direct: "This function parses JSON" not "This function is responsible for parsing JSON"

## Formatting Rules

- **Headers:** H2 for major sections, H3 for subsections. Never skip levels (no H2 → H4)
- **Code blocks:** Always include language identifier. Inline code for identifiers (`functionName`), blocks for examples (≥2 lines)
- **Lists:** Bullet for unordered collections, numbered for sequential steps. Max 7 items per list before grouping
- **Tables:** Use for comparisons (≥3 items × ≥2 attributes). Never for single-column data
- **Line length:** Wrap prose at ~80 chars in source. No single-sentence paragraphs unless transitional
- **Sections:** Every H2 section starts with 1-2 sentence summary before details
- **Links:** Reference format `[display text](path)` — never bare URLs in prose

## Anti-Patterns

- Never start sentences with "It should be noted that" or "It is important to"
- Never use passive voice when the agent is known ("was called" → "the scheduler called")
- Never write walls of text without structure — max 4 sentences before a heading, list, or code block
- Never explain what code does line-by-line when the code is self-documenting
- Never use "etc." — enumerate or use "and related X" with a specific noun

## Quality Criteria

- [ ] Every code example compiles/runs (no pseudocode without labeling it as such)
- [ ] No section exceeds 300 words without a code block, table, or diagram reference
- [ ] Every H2 section has a 1-2 sentence lead that works as a standalone summary
- [ ] Zero instances of hedging words: "basically", "simply", "just", "obviously", "actually"
- [ ] All technical terms consistent with codebase naming (verified against source)

## Examples

### Before (fails quality criteria)

```
It should be noted that the authentication middleware is basically responsible
for checking if the user is authenticated. It simply looks at the JWT token
and validates it. If the token is valid, it just passes the request through.
```

### After (passes quality criteria)

```
The auth middleware validates the JWT token on every request.

- **Valid token:** attaches `req.user` and calls `next()`
- **Expired token:** returns `401` with `{ error: "token_expired" }`
- **Missing token:** returns `401` with `{ error: "token_required" }`
```

---

## Compact Instructions

When summarizing, always preserve:
- The style name (precision-docs) and all voice rules (active voice, second person, no hedging)
- Formatting rules (header hierarchy, code block language identifiers, list limits)
- Anti-patterns (no passive voice, no wall of text, no "etc.")
- The `keep-coding-instructions: true` setting
```

---

## File: `README.md`

```markdown
# Precision Docs

Technical documentation output style that enforces clarity, scannability, and developer trust.

## What It Does

Transforms Claude's documentation output into staff-engineer-grade technical writing:
- Active voice, second person, zero filler words
- Enforced structure (headers, code blocks, lists with limits)
- Quality criteria that catch common documentation anti-patterns

## Install

```bash
myclaude install precision-docs
```

Or manually copy `precision-docs.md` to `.claude/output-styles/`.

## Usage

Select in Claude Code settings or activate per-session:

```
/output-style precision-docs
```

Works with any codebase. Pairs well with documentation skills and code-review agents.

## Requirements

- Claude Code >= 1.0.0
- No additional dependencies
```

---

## DNA Compliance

| Pattern | Status | Evidence |
|---------|--------|---------|
| D2: Anti-Pattern Guard | ✅ PASS | 5 anti-patterns with specific, testable rules |
| D4: Quality Gate | ✅ PASS | 5 checkable criteria with [ ] format |
| D13: Self-Documentation | ✅ PASS | README with what/install/usage/requirements |
| D15: Testability | ✅ PASS | Before/after examples with clear quality delta |
| D16: Composability | ✅ PASS | No hardcoded paths, works across codebases |

**MCS Score Estimate:** ~88% (MCS-2 Quality)

---

## Why This Exemplar Works

1. **Voice section is actionable, not aspirational.** "Active voice exclusively" beats "be professional."
2. **Anti-patterns name specific patterns.** "Never start with 'It should be noted'" vs generic "avoid filler."
3. **Quality criteria are machine-checkable.** Word count limits, hedging word grep, code block presence.
4. **Before/after examples prove the difference.** Not just rules — demonstrated impact.
5. **Compact Instructions preserve the minimum viable style.** If context truncates, the style survives.
6. **Frontmatter uses `keep-coding-instructions: true`.** Style augments; doesn't replace coding ability.
