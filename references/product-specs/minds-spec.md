# Product Spec: Minds

## Definition

Minds are advisory agents — they think, advise, and challenge, but never modify files
or run commands. They encode domain expertise, mental models, thinking processes, and
communication style. Minds are the NON-DEV gateway type — written by and for strategists,
researchers, consultants, and domain experts with zero coding knowledge required.

Technically, a mind is a native Claude Code agent (`AGENT.md` with YAML frontmatter)
with `denied-tools` restricting all file-writing and execution tools. This makes the
mind advisory-only: it can reason, analyze, and advise, but cannot change your codebase.

A mind is NOT:
- A skill with execution logic
- A prompt template
- A chatbot personality or persona
- A knowledge base dump

A mind IS:
- Domain expertise encoded as behavior
- A thinking process, not just knowledge
- Accessible to non-developers
- Self-aware of its boundaries
- An advisor that thinks alongside you, never acts on your behalf

---

## Install Path

Minds install as a single flat file:

```
.claude/agents/{slug}.md
```

This is Claude Code's native `.claude/agents/` directory — auto-discovered by Claude Code
without any configuration. The file IS the mind. No subdirectory needed.

---

## YAML Frontmatter (Required)

Every mind's `AGENT.md` must begin with this frontmatter:

```yaml
---
name: {slug}
description: "One-line description of what this mind advises on"
model: claude-sonnet-4-6
denied-tools: [Write, Edit, Bash, NotebookEdit]
auto-memory: true
---
```

**`denied-tools` explanation:** By blocking `Write`, `Edit`, `Bash`, and `NotebookEdit`,
the mind can only think and respond — it cannot create files, modify code, or run commands.
This is what makes it an advisor rather than an executor. The restriction is intentional
and communicates trust to buyers: this mind will never touch your files.

---

## Canonical File Structure

```
workspace/{slug}/
├── AGENT.md              # Mind definition: frontmatter + identity + thinking (REQUIRED)
├── README.md             # Marketplace documentation (REQUIRED)
├── references/
│   ├── domain-knowledge.md   # Deep domain expertise
│   └── exemplars.md          # Example conversations
├── examples/
│   └── examples.md       # Buyer-facing conversation examples
└── .meta.yaml            # Engine state (auto-generated)
```

The `AGENT.md` file is what gets installed. During `/package`, it is renamed to
`{slug}.md` to match the flat-file convention at `.claude/agents/{slug}.md`.
Everything else stays in the workspace as the source of truth for the creator.

**Rename rule:** `workspace/{slug}/AGENT.md` → packaged as `{slug}.md` → installed
to `.claude/agents/{slug}.md`. This matches the proven pattern where existing Claude
Code agents use flat `{name}.md` files (e.g., `architect.md`, `researcher.md`).

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `AGENT.md` | Frontmatter + identity, thinking process, questions, boundaries | MCS-1 |
| `README.md` | What the mind does, example conversation, install | MCS-1 |
| `references/` (1+ file) | Domain knowledge loaded at activation | MCS-1 |

---

## Required Sections in AGENT.md

1. **YAML frontmatter** with `denied-tools: [Write, Edit, Bash, NotebookEdit]`
   **Security note:** `denied-tools` does not block the Agent tool. Minds can theoretically spawn sub-agents with unrestricted access. Mitigate by adding an explicit instruction in the boundaries section: "Does NOT spawn sub-agents with Write, Edit, or Bash access." This is a Claude Code platform limitation (G016).
2. **Identity:** Who this mind is, expertise areas, perspective
3. **How This Mind Thinks:** Mental models and thinking process
4. **Questions This Mind Always Asks:** Input triage in plain language
5. **How This Mind Communicates:** Tone, style, uncertainty behavior
6. **What This Mind Refuses To Do:** Explicit boundaries
7. **When Not To Use:** Anti-use cases
8. **What This Mind Loads:** Context loading sequence (replaces "Activation Protocol")
9. **Checklist:** Output verification checklist (replaces "Quality Gate")
10. **Common Mistakes:** Builder guidance (replaces "Anti-Patterns")

---

## Voice Requirements

- WHY comments use plain language, not DNA pattern jargon
- Discovery questions use business language
- Template assumes zero coding knowledge
- Examples show conversations, not code

**NOT:** `<!-- WHY: D5 (Question System) — Implements structured input triage -->`
**YES:** `<!-- WHY: Great minds ask before they answer. Define the questions yours always asks. -->`

---

## MCS Requirements

### MCS-1: Publishable
- [ ] `AGENT.md` with valid YAML frontmatter including `denied-tools`
- [ ] All required sections present
- [ ] `README.md` with example conversation
- [ ] At least 1 file in `references/`
- [ ] Plain language throughout (no technical jargon)
- [ ] Boundaries clearly defined

### MCS-2: Quality
- [ ] 3+ mental models documented
- [ ] Question system with specific questions per context
- [ ] Confidence signaling — mind declares uncertainty
- [ ] 5+ common mistakes documented
- [ ] 3+ conversation examples in different domains

---

## DNA Requirements

See `product-dna/minds.yaml`.
