# Structural DNA — Tier 2 (Advanced)

> Loaded on-demand by `/validate` (level ≥ 2) and `/create` when scaffolding products
> with nontrivial execution logic. Not loaded at boot. See `structural-dna.md` for
> the boot-resident layer (9 architectural principles + Tier 1 universal patterns).

8 patterns. Required for MCS-2. Products with nontrivial execution logic.

---

### D5: Question System

**Tier:** 2 — Advanced

**Problem it solves:**
A product that assumes input produces misaligned output. When input is ambiguous,
guessing is worse than asking — it produces confident wrong output that takes longer
to correct than if the product had simply asked.

**Rule:**
Every product with variable input must define a question system: what to ask, when to
ask it, and what to do with the answer. Questions must be minimal (one at a time),
specific (not "tell me more"), and actionable (the answer must change behavior).

**Validation check:**
```
grep -i "question\|if missing.*ask\|ask.*if\|clarif\|\$ARGUMENTS\|\$0" {PRIMARY_FILE}
AND presence of argument handling table or "if not provided" pattern
```
PASS if question/argument handling found. PARTIAL if $ARGUMENTS used but no handling logic.

---

### D6: Confidence Signaling

**Tier:** 2 — Advanced

**Problem it solves:**
Claims stated without certainty markers are indistinguishable from facts. A product
that says "This code has a race condition" with the same confidence as "I'm 40% sure
this code has a race condition" misleads users and erodes trust when it's wrong.

**Rule:**
Every product that makes claims or recommendations must use graduated confidence signals.
Use explicit markers: (high confidence), (moderate confidence), (low confidence),
or quantitative ranges. Never present uncertain output as certain.

**Validation check:**
```
grep -i "confidence\|high confidence\|moderate confidence\|low confidence\|certainty\|likely\|may be\|possible" {PRIMARY_FILE}
```
PASS if confidence signaling pattern found with at least 2 levels. PARTIAL if only one level.

---

### D7: Pre-Execution Gate

**Tier:** 2 — Advanced

**Problem it solves:**
Acting without precondition checks causes silent failures deep in execution.
A product that starts work before verifying that required files exist, auth is valid,
or dependencies are present will fail in unpredictable ways that are hard to debug.

**Rule:**
Every product with external dependencies or required context must define and run
pre-execution checks BEFORE starting work. Checks must be explicit (not assumed),
automated where possible, and must produce clear failure messages with remediation steps.

**Validation check:**
```
grep -i "precondition\|pre-execution\|before executing\|verify.*before\|check.*exists\|requires.*present" {PRIMARY_FILE}
```
PASS if pre-execution check pattern found. PARTIAL if checks described but not gated.

---

### D8: State Persistence

**Tier:** 2 — Advanced

**Problem it solves:**
Without state, every session starts from zero. Patterns discovered, decisions made,
and preferences learned disappear when the session closes. State persistence is what
distinguishes a product from a one-shot prompt.

**Rule:**
Any product that learns, tracks, or builds across sessions must define a state file
(YAML or JSON) with explicit schema. State must be append-safe (reading never breaks
if state is partial) and the schema must be documented in the product.

**Validation check:**
```
glob: *.yaml OR *.json in product directory (excluding vault.yaml, plugin.json)
AND grep "state\|session\|persist\|memory\|track" in that file or PRIMARY file
```
PASS if state file exists with documented schema. PARTIAL if state section documented but no file.

---

### D15: Testability

**Tier:** 2 — Advanced

**Problem it solves:**
A product that can't be tested can't be improved. Without test scenarios, creators
ship products they can't verify and buyers can't trust. Testability is not optional
for products that execute nontrivial logic.

**Rule:**
Every product with execution logic must include test scenarios with expected outputs.
Minimum 3 scenarios: happy path, edge case, adversarial input. Expected output must
be specific enough to verify (not "output should be good").

**Validation check:**
```
grep -i "## test\|## example\|## scenario\|expected output\|sample input\|test case" {PRIMARY_FILE_OR_README}
AND count examples → must be ≥3
```
PASS if 3+ scenarios with expected outputs. PARTIAL if examples exist but <3 or without expected output.

---

### D16: Composability

**Tier:** 2 — Advanced

**Problem it solves:**
A product that conflicts with other products gets uninstalled. Hardcoded absolute paths,
common command names that clash, and global state mutations make products incompatible
with real-world Claude Code environments where many products coexist.

**Rule:**
All file references must be relative. Command names must be specific to the product
domain (not /help, /status, /run, /start, /stop). No modifications to global config
or shared state. Product must be installable alongside any other MyClaude product.

**Validation check:**
```
grep -n "absolute path\|^/[a-z]" {ALL_FILES} → must be 0 matches
AND grep -n "^command: /help\|^command: /status\|^command: /run\b" SKILL.md → must be 0
AND grep -n "globalconfig\|global state\|~/" {ALL_FILES} → must be 0 matches
```
PASS if zero violations. PARTIAL if references are relative but command name conflicts.

---

### D17: Hook Integration

**Tier:** 2 — Advanced

**Problem it solves:**
Manual steps that could be automated become bottlenecks and are frequently skipped.
Hooks (PostToolUse, FileChanged, SessionStart, Stop) allow products to automate
workflow integration without requiring the user to remember to trigger them.

**Rule:**
Any product that benefits from lifecycle automation must document which Claude Code hooks
it uses (or could use), what they trigger, and how to configure them. Hook documentation
belongs in README or a dedicated hooks section in the primary file.

**Validation check:**
```
grep -i "hook\|sessionstart\|posttooluse\|filechanged\|stop\|automation" {PRIMARY_FILE_OR_README}
```
PASS if hooks section documented with at least 1 hook. PARTIAL if hooks mentioned but not documented.

---

### D20: Cache-Friendly Design

**Tier:** 2 — Advanced

**Problem it solves:**
claude-md products are loaded every turn as part of the prompt's dynamic zone. Unoptimized
claude-md products waste tokens on every turn, increase ambient cost, and can fragment the
prompt cache. Products without scope limitation load even when irrelevant.

**Rule:**
Products of type claude-md must be optimized for ambient cost:
1. Use `paths:` frontmatter to scope activation to relevant file types
2. Keep primary file under 2K chars (stricter than general 4K — always in context)
3. Use @include for modular composition when content exceeds 2K
4. Never include dynamic content (dates, counters) that would bust the prompt cache

**Evidence:**
[SOURCE: prompts.ts:106-115] — Static/Dynamic boundary in system prompt
[SOURCE: claudemd.ts:254-279] — Path-scoped conditional rules
[SOURCE: systemPromptSections.ts:32-38] — DANGEROUS_uncached requires reason

**Validation check:**
```
For claude-md products:
1. Check paths: frontmatter exists → PASS if specific globs, COACHING if absent
2. Check primary file char count → PASS if <2K, WARNING if 2K-4K, BLOCKING if >4K
3. Check for dynamic content patterns (date, time, counter) → WARNING if found
```
PASS if all 3 checks pass. PARTIAL if paths missing but size OK. FAIL if >4K chars.
