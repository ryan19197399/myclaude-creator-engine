# Standardize How Your Team Uses Claude Code

Your team uses Claude Code differently. Everyone has their own prompting habits, their own quality bar, their own way of asking for code review. Some of that variation is fine. Most of it costs you.

This guide shows how to build shared standards — coding rules, review squads, process workflows — that every team member installs with one command and uses identically.

---

## What You'll Build

Three product types cover most team needs.

| Product | What It Standardizes | Install Command |
|:--------|:---------------------|:----------------|
| **claude-md** | How Claude behaves in your project — coding conventions, review standards, communication style | `myclaude install your-team-rules` |
| **Squad** | Multi-agent review and analysis pipelines with consistent quality | `myclaude install your-review-squad` |
| **Workflow** | Step-by-step process automation — incident response, PR prep, onboarding | `myclaude install your-workflow` |
| **Bundle** | All of the above, installed in one shot | `myclaude install your-team-bundle` |

Start with what causes the most inconsistency on your team today. For most teams, that's coding standards — the rules that live in Confluence or Notion and that nobody reads consistently.

---

## Build Shared Coding Standards With claude-md

A `claude-md` product is a set of behavioral rules that shapes how Claude Code works in your project. When team members install it, the rules go into `.claude/rules/` and become active in every session.

```
/create claude-md
```

During `/fill`, the engine asks you to define your team's standards across four areas:

- **Code quality rules** — naming conventions, file structure, complexity limits
- **Review criteria** — what a passing PR looks like, what triggers a mandatory human review
- **Communication style** — how Claude should explain its reasoning to your team
- **Forbidden patterns** — antipatterns, deprecated APIs, or approaches your team has explicitly ruled out

A completed coding standards section looks like this:

```markdown
## Code Quality Standards

Function length: 40 lines maximum. If longer, decompose.
Naming: descriptive over clever. `getUserById` not `getUser`.
Tests: every public function has a test. Untested code is not mergeable.
Async: always handle errors in async functions. Silent failures are
       not acceptable.

## Forbidden Patterns
- `eval()` — no exceptions
- Direct DOM manipulation outside designated component files
- `console.log` in committed code
- Magic numbers without a named constant
```

Once published and installed, Claude Code enforces these rules in every session — without the team needing to remember them or reference a separate document.

**Expected result after install:**

```
myclaude install acme-coding-standards

Installing: acme-coding-standards
  ✓ Rules loaded: coding-standards.md → .claude/rules/
  ✓ 4 quality gates active
  ✓ 8 forbidden patterns registered
  Active in this project. Claude will follow these standards automatically.
```

---

## Build a Review Squad — Consistent Multi-Agent Analysis

A squad is a team of specialized agents that coordinate on a shared task. For code review, each agent owns a specific lens — security, logic, style — and a router synthesizes their findings into a single coherent report.

```
/create squad
```

A well-structured PR review squad looks like this:

```
PR Review Squad
├── security-agent    → injection vectors, auth gaps, dependency risk, secrets
├── logic-agent       → unreachable branches, off-by-ones, resource leaks, async pitfalls
├── style-agent       → convention enforcement against team coding-standards.md
└── router            → receives PR diff, dispatches to all three, synthesizes priority-ordered report
```

During `/fill`, you define each agent's responsibilities explicitly. The engine enforces that routing is unambiguous — no agent receives work outside its defined scope.

Sample output when the squad runs a PR review:

```
PR Review: feature/user-auth-refactor

SECURITY (security-agent)
  HIGH   JWT secret pulled from process.env without validation — line 47
  MEDIUM Refresh token not invalidated on logout — line 203

LOGIC (logic-agent)
  HIGH   Race condition in concurrent login attempts — line 89-94
  LOW    Unreachable error branch in token parser — line 156

STYLE (style-agent)
  INFO   3 functions exceed 40-line limit (team standard)
  INFO   2 magic numbers without named constants

Summary: 2 HIGH blockers must be resolved before merge.
```

Every team member running this squad gets the same analysis, at the same quality bar, every time.

---

## Build a Team Workflow — Standardize Your Processes

Workflows turn your team's manual processes into guided, step-by-step automation. The same checklist. The same sequence. The same outputs.

```
/create workflow
```

Good candidates for team workflows:

- **Incident response** — triage steps, escalation criteria, post-mortem format
- **PR preparation** — self-review checklist before requesting review
- **Sprint planning** — ticket refinement criteria, estimation guidelines
- **New engineer onboarding** — day-one setup, first-week tasks, resources

During `/fill`, you define each step in the process: what Claude does, what inputs it needs, what outputs it produces, and what the success condition is. The engine structures this as a runnable guide — not documentation, but active process support.

An incident response workflow step looks like this:

```markdown
## Step 2: Classify the Incident

Ask the engineer to provide:
- Affected systems (list)
- User impact scope (none / limited / widespread)
- Time of first alert

Classify as:
- P1 (SEV-1): widespread user impact, requires immediate escalation
- P2 (SEV-2): limited user impact, can be handled by on-call
- P3 (SEV-3): no user impact, schedule for next business day

Output: incident classification + recommended responder
```

---

## Validate Before Distributing — Quality Across the Team

Shipping a broken standard to your whole team creates more inconsistency than no standard at all. Validate everything before distributing.

```
/validate --level=2
```

Premium (85%+) is the right bar for team tools. It ensures the product is complete enough that team members who weren't involved in building it can use it without confusion.

Validation output for a squad:

```
Validation: pr-review-squad
Score: 91% — nearing Elite

PASSED (18/20)
  ✓ All agents have explicit scope definitions
  ✓ Routing logic is unambiguous
  ✓ Output format is consistent across agents
  ✓ Error handling defined for tool failures
  ...

NEEDS WORK (2/20)
  ✗ No fallback behavior when security-agent finds zero issues
  ✗ Missing guidance for partial PR reviews (single-file diffs)

Fix these before distributing. Run /validate after fixing.
```

Require Premium (85%) as your team's minimum bar for any shared product. Set Elite (92%) as the standard for anything that runs automatically without human review.

---

## Distribute to Your Team — One Command Per Member

Once a product is published, every team member installs it identically.

```
myclaude install pr-review-squad
myclaude install acme-coding-standards
myclaude install incident-response-workflow
```

Or bundle everything into a single install:

```
/create bundle
```

A bundle groups multiple products under one install command. Your team setup goes from a multi-step process to:

```
myclaude install acme-team-bundle

Installing: acme-team-bundle
  ✓ acme-coding-standards (rules)
  ✓ pr-review-squad (agents)
  ✓ incident-response-workflow (workflow)
  3 products installed. Your Claude Code environment matches team standards.
```

Every team member gets the same agents, the same rules, the same workflows. No manual setup. No drift between environments.

---

## Maintain Standards Over Time

Team tools need maintenance as your standards evolve. The Engine handles this through versioning.

When you update a published product, the state machine tracks it as a new version. Team members who already have it installed see an update prompt. You don't break existing setups — you improve them.

To update a live product:

1. Edit the product files in `workspace/your-product/`
2. The state machine automatically marks it as needing re-validation
3. Run `/validate`, then `/package`, then `/publish`
4. Team members run `myclaude update your-product` to pull the latest

Keep a changelog section in your product. Teams that know what changed adopt updates faster.

> ✦ One product, one install command, every team member on the same page. That's what shared standards look like.

---

**Next:** [All Commands](../reference/commands.md) · [Product Types](../reference/product-types.md) · [Quality System](../reference/quality-system.md)
