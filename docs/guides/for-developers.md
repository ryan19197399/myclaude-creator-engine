# Build Developer Tools With the Studio Engine

You write code. This guide shows how to turn your development patterns — the ones you repeat on every project, the ones you teach to junior devs, the ones that live in your head — into installable tools that anyone can run with one command.

---

## Understand What You Can Ship

The Engine gives developers six product types worth knowing well.

| Type | What It Does | When to Use It |
|:-----|:-------------|:---------------|
| **Skill** | Single-purpose Claude tool with clear input/output | Code review, test generation, doc writing |
| **Agent** | Autonomous multi-step task runner with goal logic | Refactoring, dependency audits, release prep |
| **Hooks** | Lifecycle automation on Claude Code events | Pre-commit validation, session initialization |
| **Squad** | Multiple coordinated agents toward one goal | Full PR review pipeline, security audit teams |
| **Workflow** | Orchestrated step-by-step process | Incident response, deployment checklist |
| **System** | Combined skills + agents + configuration | Complete dev environment standards |

When in doubt, start with a Skill. It's the fastest path from idea to published tool.

---

## Build a Skill — Step by Step

The example below builds a code-review skill. Follow the same steps for any skill you have in mind.

### Step 1: Research the domain first

```
/scout code-review
```

The scout tests what Claude already knows about code review, maps the gaps, and checks the marketplace for similar tools. You'll see output like this:

```
Scout Report: code-review
Baseline: Claude handles style feedback well. Weak on security patterns,
          performance antipatterns in async contexts, and team-specific
          conventions.
Gap Score: 34% — strong build opportunity.
Recommendation: skill (focused) or agent (if multi-pass review needed).
Marketplace: 2 similar tools. Neither covers Rust or security-first review.
```

That gap score tells you exactly where your expertise adds value.

### Step 2: Scaffold the skill

```
/create skill
```

The engine asks what kind of skill you're building and generates a complete scaffold. You'll see the file appear at `workspace/code-review/SKILL.md` with sections waiting for your input.

### Step 3: Fill with your patterns

```
/fill
```

The engine walks through each section with targeted questions. For a code-review skill, it might ask:

- "What languages does this skill target?"
- "What categories of issues should it catch? (Style / Security / Performance / Logic)"
- "What output format does the reviewer expect? (Inline comments / Summary report / Priority list)"
- "Describe your most common anti-pattern — the thing juniors always miss."

You answer in plain text. The engine writes the structured content. A filled section looks like this:

```markdown
## Core Behavior

When invoked, perform a three-pass review:
1. **Security pass** — check for injection vectors, unsafe deserialization,
   hardcoded credentials, and missing input validation
2. **Logic pass** — flag unreachable branches, off-by-one risks, and
   resource leaks in async contexts
3. **Style pass** — enforce team conventions from .claude/rules/
```

### Step 4: Validate against the 20 patterns

```
/validate
```

The engine scores your skill against all 20 structural DNA patterns. You'll see a breakdown:

```
Validation: code-review
Score: 88% — Premium

PASSED (16/20)
  ✓ Clear purpose statement
  ✓ Explicit output format
  ✓ Anti-patterns section
  ✓ Examples with expected output
  ...

NEEDS WORK (4/20)
  ✗ No error handling guidance — add a "When This Fails" section
  ✗ Missing version constraint — what Claude version is this tested on?
  ...

To reach Elite (92%): fix these 4 patterns, then re-run /validate.
```

Fix the flagged patterns, re-run, hit Elite.

### Step 5: Test behavior before shipping

```
/test
```

The engine runs your skill against 5-8 behavioral scenarios — real inputs, checking that outputs match your intent. You'll see each scenario pass or fail with a diagnosis if something breaks.

### Step 6: Package and publish

```
/package
/publish
```

Once published, anyone on your team (or the marketplace) installs it with:

```
myclaude install code-review
```

---

## Build an Agent — When Skills Aren't Enough

A skill answers a question. An agent completes a task.

Use an agent when the work requires multiple steps, decision points, or tool calls that depend on each other. A dependency audit that reads `package.json`, queries the CVE database, cross-references your internal approved-versions list, and produces a remediation report — that's an agent.

```
/create agent
```

The engine asks for the agent's goal, the tools it needs access to, and the decision logic for edge cases. Key difference from a skill: you'll define **stop conditions** — when does the agent consider the task done?

A well-scoped agent definition looks like this:

```markdown
## Goal
Audit all third-party dependencies for known CVEs and version drift.

## Tools Required
- Read (package.json, lockfiles)
- WebSearch (CVE lookups)
- Write (audit-report.md)

## Stop Conditions
- All dependencies assessed
- Report written to audit-report.md
- Blockers (CRITICAL severity) surfaced to the user
```

---

## Build Hooks — Automate Your Development Lifecycle

Hooks attach to Claude Code events: session start, tool calls, permission prompts, and more. A hooks product is a set of automation rules that runs silently in the background.

```
/create hooks
```

A pre-commit validation hook, for example, fires before any file write and checks that the change doesn't violate your team's structural rules. During `/fill`, you'll define:

- **Which event triggers the hook** (PreToolUse / PostToolUse / Notification / Stop)
- **What the hook checks or does**
- **What happens on failure** (block / warn / log)

Expected output after publishing a hooks product:

```
myclaude install pre-commit-validator

Installing: pre-commit-validator
  ✓ Hooks registered: PreToolUse (Write), PreToolUse (Edit)
  ✓ Rules loaded from .claude/rules/pre-commit.yaml
  Active. Violations will block file writes with explanation.
```

---

## Build a Squad — Coordinate Multiple Agents

A squad is a team of agents with routing logic. Each agent owns a lane; the squad routes work to the right agent based on context.

```
/create squad
```

A PR review squad might look like this:

```
PR Review Squad
├── security-agent     → flags injection, auth issues, dependency risk
├── logic-agent        → catches unreachable code, off-by-ones, race conditions
├── style-agent        → enforces team conventions
└── router             → receives PR diff, routes to all three, synthesizes report
```

During `/fill`, you define each agent's role, the routing conditions, and how the squad synthesizes output from multiple agents into a single coherent response. The engine enforces that routing logic is explicit — no ambiguous handoffs.

---

## Hit Elite Quality — What the 20 Patterns Check

The Engine validates every product against 20 structural DNA patterns organized into three tiers.

| Tier | Patterns | What They Enforce |
|:-----|:---------|:------------------|
| **Tier 1 (Blocking)** | 7 patterns | Purpose, scope, output format, examples, anti-patterns |
| **Tier 2 (Standard)** | 8 patterns | Error handling, versioning, dependencies, edge cases |
| **Tier 3 (Elite, PRO)** | 5 patterns | Cognitive fidelity, baseline delta, value intelligence |

The fastest path to Elite:

1. Run `/validate --fix` — auto-fixes structural gaps where possible
2. Add a "When This Fails" section for every tool call that could error
3. Include at least three worked examples with expected output
4. Define explicit version constraints

Score formula: `(DNA patterns × 0.50) + (Structural × 0.30) + (Integrity × 0.20)`

---

## Import Existing Skills — Bring In What You've Already Built

If you have skills already living in `.claude/skills/`, don't rebuild them. Import them.

```
/import --scan
```

The engine scans your skills directory and shows what it found:

```
Found 4 existing skills:
  code-review     — importable (complete structure detected)
  test-generator  — importable (minor gaps, auto-fixable)
  db-optimizer    — needs work (missing output format, anti-patterns)
  api-docs        — importable

Run /import code-review to bring it into the pipeline.
```

Then:

```
/import code-review
/validate
/package && /publish
```

Each imported skill is scored. What passes ships. What doesn't gets a repair list.

> ✦ The tools you build for yourself today become the tools someone else installs tomorrow.

---

**Next:** [All Commands](../reference/commands.md) · [Quality System](../reference/quality-system.md) · [Product Types](../reference/product-types.md)
