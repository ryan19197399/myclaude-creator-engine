# Brand Voice Studio — Non-Code Exemplar

**Product Type:** system
**MCS Level:** 2 (Professional)
**Target Persona:** Marketer / Agency / Brand Manager (zero coding knowledge)
**Composition:** 1 skill (voice extractor) + 1 mind (brand voice clone) + 1 claude-md (tone rules) + hooks (brand guard)
**Purpose:** Proves the MyClaude Engine creates world-class products for NON-developers.

---

## Why This Exemplar Exists

Every other Engine exemplar demonstrates code-centric products. This exemplar proves the Engine's 13 product types serve ANY domain by showing a complete marketing system where:

- The **skill** extracts brand voice from writing samples (no code involved)
- The **mind** embodies the brand's voice for content generation
- The **claude-md** enforces tone rules as always-on guardrails
- The **hooks** prevent off-brand content from being published

**Key CC platform features demonstrated:**
- `## Compact Instructions` — preserves brand context during long content sessions
- Path-scoped rules — tone rules only activate for content files
- `@include` directive — modular brand knowledge base
- Token economics — claude-md rules optimized for minimal ambient cost

---

## File Structure

```
brand-voice-studio/
├── CLAUDE.md                    # System boot + routing (<4K chars recommended)
├── STATE.yaml                   # Brand state (active voice, content queue)
├── README.md                    # This file
├── skills/
│   └── voice-extractor/
│       ├── SKILL.md             # Voice DNA extraction skill
│       └── references/
│           └── extraction-framework.md
├── agents/
│   └── brand-voice.md           # Mind that writes in brand voice
├── rules/
│   └── tone-guard.md            # Path-scoped tone enforcement
├── hooks/
│   └── brand-guard.json         # PreToolUse hook for content validation
└── references/
    ├── brand-kit.md             # Brand values, personality, vocabulary
    └── anti-voice.md            # What the brand NEVER sounds like
```

---

## File: `CLAUDE.md`

```markdown
# Brand Voice Studio

> Your brand's voice, systematized. Extract it, clone it, guard it.

**Version:** 1.0.0
**Components:** 4 — voice extractor (skill), brand voice (mind), tone guard (rules), brand guard (hooks)
**Entry Point:** Describe what you need: "extract voice from samples", "write in brand voice", or "review content for tone"

---

## Boot Sequence

1. Read `references/brand-kit.md` → brand values, personality, vocabulary
2. Read `STATE.yaml` → active voice profile, content queue
3. Detect intent → route to component

## Routing

| User Says | Route To | Why |
|-----------|----------|-----|
| "extract voice", "analyze samples", "voice DNA" | `/voice-extractor` | Extraction skill |
| "write as brand", "create content", "draft" | `@brand-voice` | Mind-based generation |
| "review tone", "check brand alignment" | Manual review against `rules/tone-guard.md` | Rules reference |

## Components

| Component | Type | Purpose |
|-----------|------|---------|
| voice-extractor | skill | Extracts Voice DNA from writing samples |
| brand-voice | mind | Writes content in the brand's authentic voice |
| tone-guard | claude-md | Always-on tone enforcement rules |
| brand-guard | hooks | Blocks off-brand content before publishing |

## Rules

- NEVER generate content without loading brand-kit.md first
- NEVER approve content that violates anti-voice.md patterns
- Ask for writing samples before extracting voice (minimum 3 samples)
- Always signal confidence: "High brand alignment" / "Review recommended"

## Compact Instructions

When summarizing this conversation, always preserve:
- The active brand voice profile and its signature phrases
- Brand values and personality traits from brand-kit.md
- Any content in progress and its current tone alignment score
- The anti-voice patterns that must be avoided
- Which component is actively engaged and its state
```

---

## File: `skills/voice-extractor/SKILL.md`

```markdown
---
name: voice-extractor
description: >-
  Extract brand voice DNA from writing samples. Identifies signature phrases,
  tone patterns, vocabulary preferences, and communication style.
  Use when: brand needs voice documentation or clone setup.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
argument-hint: "[samples-path] [--depth surface|deep]"
---

# Voice Extractor

> Turn writing samples into documented Voice DNA.

## When to Use

- When onboarding a new brand and need to capture their voice
- When creating a brand-voice mind and need extraction inputs
- When auditing existing content for voice consistency

## When NOT to Use

- For generating content (use @brand-voice mind instead)
- For real-time tone checking (use tone-guard rules instead)

## Activation Protocol

1. Read `references/extraction-framework.md` — extraction methodology
2. Ask for writing samples (minimum 3, ideally 5-10)
3. Classify sample quality (authentic voice vs. generic/scripted)
4. Extract Voice DNA dimensions

## Question System

| Input | Required | If Missing |
|-------|----------|-----------|
| Writing samples | Yes | "Share 3-5 writing samples that best represent the brand voice." |
| Brand context | No | Assume from samples. Ask: "Any brand values I should know?" |
| Depth mode | No | Default: deep |

## Core Instructions

### Extraction Dimensions

For each sample, extract:

1. **Vocabulary fingerprint** — signature words, forbidden words, jargon level
2. **Sentence architecture** — length, complexity, active vs. passive
3. **Tone markers** — warmth (1-10), formality (1-10), confidence (1-10)
4. **Rhetorical patterns** — questions, imperatives, stories, data
5. **Anti-patterns** — what this voice NEVER does

### Output Structure

```
## Voice DNA: {Brand Name}

### Signature Phrases
- "{phrase_1}" — used in {N} samples
- "{phrase_2}" — used in {N} samples

### Tone Profile
- Warmth: {N}/10
- Formality: {N}/10
- Confidence: {N}/10

### Vocabulary Rules
- ALWAYS use: {word_list}
- NEVER use: {anti_word_list}

### Anti-Voice (What This Brand NEVER Sounds Like)
- {anti_pattern_1}
- {anti_pattern_2}
```

## Quality Gate

- [ ] Minimum 3 samples analyzed
- [ ] All 5 extraction dimensions covered
- [ ] At least 3 signature phrases identified with source attribution
- [ ] Anti-voice section has 3+ concrete patterns
- [ ] Tone profile numbers backed by evidence from samples

## Anti-Patterns

- **Generic voice**: Extracting "professional and friendly" — every brand is that. Find the SPECIFIC.
- **Inventing voice**: Adding characteristics not evidenced in samples.
- **Ignoring anti-patterns**: The "never" list is as important as the "always" list.
- **Single-sample extraction**: One sample is an anecdote. Three samples reveal patterns.
- **Jargon assumption**: Don't assume the brand wants technical language unless samples prove it.

## Compact Instructions

When summarizing this conversation, always preserve:
- Which writing samples were analyzed and their quality classification
- Extracted Voice DNA dimensions (all 5) with evidence
- Signature phrases with source attribution
- Anti-voice patterns identified
- Current extraction progress (which samples done, which pending)
```

---

## File: `rules/tone-guard.md`

```markdown
---
paths:
  - content/**
  - drafts/**
  - copy/**
---

# Tone Guard — Brand Voice Enforcement

These rules activate ONLY when working on content files (content/, drafts/, copy/).

## Voice Requirements

All content in these directories MUST align with the brand voice profile.

### Always
- Use signature phrases from Voice DNA when natural
- Match the tone profile: warmth {N}/10, formality {N}/10, confidence {N}/10
- Write in active voice unless the brand specifically uses passive

### Never
- Use words from the anti-vocabulary list
- Sound like: {anti_voice_patterns}
- Use generic marketing clichés ("leverage", "synergize", "at the end of the day")
- Claim expertise the brand hasn't demonstrated

## Compact Instructions

When summarizing, always preserve:
- All voice rules (they are this product's core value)
- The path-scoped activation conditions (content/**, drafts/**, copy/**)
- Anti-vocabulary list and anti-voice patterns
```

---

## What This Exemplar Demonstrates

| Engine Feature | How It's Used | Non-Dev Benefit |
|---------------|---------------|-----------------|
| **system** type | Orchestrates 4 components | One install = complete brand toolkit |
| **Compact Instructions** | In every component | Long content sessions preserve brand context |
| **Path-scoped rules** | `paths: [content/**, drafts/**]` | Rules only fire for content files |
| **Token economics** | claude-md rules kept minimal | Low ambient cost for always-on tone guard |
| **Progressive disclosure** | Voice extraction: surface → deep modes | Non-devs start simple |
| **Question system** | "Share 3-5 samples" before extraction | Guided experience, no blank page |
| **Anti-pattern guard** | Voice extraction anti-patterns | Prevents generic/hallucinated voice |
| **Quality gate** | Minimum 3 samples, 5 dimensions | Quality without technical jargon |

---

*This exemplar proves: the MyClaude Engine is not just for developers.*
*A marketer with zero coding knowledge can install this system and have*
*their brand voice extracted, cloned, and guarded — entirely within Claude Code.*
