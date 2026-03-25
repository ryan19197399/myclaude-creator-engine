# Workflow Exemplar: Code Review Workflow

**MCS Level:** 3 (State-of-the-Art)
**Demonstrates:** 5 steps with explicit dependencies, error handling per step,
configurable variables, 2 execution examples (happy path + failure recovery),
composability documentation.

---

## File: `WORKFLOW.md`

```markdown
# Code Review Workflow

**Purpose:** Systematic review of a pull request or code change for quality, security,
and adherence to project conventions — producing an actionable review report.

**Trigger:** Manual — invoked by a developer before merging a PR
**Duration:** 10-30 minutes depending on diff size
**Tools Required:** Read, Bash (git diff), Grep, optional: Glob
**Version:** 1.4.0
**Author:** @devtools

---

## Trigger Conditions

**Run when:**
- A PR is ready for review (author has self-reviewed)
- A significant refactor is complete and needs validation
- A new feature implementation requires quality gate before merge

**Preconditions (must be true before starting):**
- [ ] Git repository is accessible
- [ ] The branch or PR diff can be read
- [ ] `CLAUDE.md` or project conventions are available

**Do NOT run when:**
- Draft PRs (not ready for review)
- Diff is over 2,000 lines — split into multiple focused reviews first
- No project conventions are defined (run `/create claude-md` first)

---

## Input Requirements

| Input | Required | Format | Description |
|-------|----------|--------|-------------|
| `diff` | Yes | git diff output or file path | The code changes to review |
| `project_conventions` | Yes | CLAUDE.md path or file | Standards to check against |
| `review_depth` | No | `quick` \| `standard` \| `thorough` | Default: `standard` |
| `focus_areas` | No | comma-separated list | E.g., "security,performance,tests" |
| `pr_description` | No | text | Context about what the change does |

**Input validation:** Before starting:
- Verify diff is non-empty
- Verify `project_conventions` file exists and is readable
- Warn (don't abort) if diff > 500 lines: "Large diff — review may take longer"

If validation fails: "Cannot start review: [specific missing input]. Provide [X] to continue."

---

## Step Sequence

| Step | Name | Depends On | Input | Output |
|------|------|-----------|-------|--------|
| 01 | Context Load | — | `project_conventions`, `pr_description` | loaded context |
| 02 | Diff Analysis | 01 | `diff`, loaded context | structured diff summary |
| 03 | Convention Check | 02 | diff summary, conventions | violations list |
| 04 | Security Scan | 02 | diff summary | security findings |
| 05 | Report Assembly | 03, 04 | all findings | final review report |

*Steps 03 and 04 can run in parallel — both depend on Step 02 only.*

### Step 01: Context Load

**What it does:** Loads project conventions and PR context before analyzing anything.
Running analysis without context produces generic feedback, not actionable review.

**Actions:**
1. Read `project_conventions` (CLAUDE.md or equivalent)
2. If `pr_description` provided, read it and extract: purpose, scope, what NOT to review
3. Identify key conventions that apply to this diff type (are there TypeScript rules?
   testing requirements? security mandates?)

**Success condition:** Conventions are loaded and relevant rules are identified.

**File:** `steps/01-context-load.md`

---

### Step 02: Diff Analysis

**What it does:** Parses the diff and creates a structured summary of what changed.
Does not make quality judgments — only describes what happened.

**Actions:**
1. Count: lines added, lines removed, files changed
2. Identify: new functions/methods, modified functions, deleted code
3. Identify: new dependencies, changed interfaces, modified tests
4. Flag: large functions (>50 lines added), missing tests for new code

**Success condition:** Structured summary of all changes, grouped by concern.

**File:** `steps/02-diff-analysis.md`

---

### Step 03: Convention Check

**What it does:** Checks the diff against loaded project conventions.
Reports violations with specific file:line references.

**Actions:**
1. Check naming conventions (file names, function names, variable names)
2. Check code structure rules (import order, function length, etc.)
3. Check documentation requirements (JSDoc/docstrings where required)
4. Check test coverage (does new code have corresponding tests?)

**Success condition:** All convention checks complete; violations list generated
(empty list is valid — no violations is a pass).

**File:** `steps/03-convention-check.md`

---

### Step 04: Security Scan

**What it does:** Checks the diff for common security patterns.
Runs in parallel with Step 03.

**Actions:**
1. Grep for: hardcoded secrets, API key patterns
2. Check: input validation on new API endpoints or functions accepting user input
3. Check: authentication/authorization on new routes
4. Check: SQL construction patterns (parameterized vs. string concatenation)
5. Check: dependency additions — are new packages known/trusted?

**Success condition:** Security scan complete; findings list generated
(empty list is valid — no findings is a pass).

**File:** `steps/04-security-scan.md`

---

### Step 05: Report Assembly

**What it does:** Combines findings from Steps 03 and 04 into the final review report.

**Actions:**
1. Combine convention violations + security findings
2. Prioritize: Critical (security) > High (broken functionality) > Medium (quality) > Low (style)
3. Write summary assessment
4. Add actionable next steps

**Success condition:** Structured report with all findings, severities, and clear next steps.

**File:** `steps/05-report-assembly.md`

---

## Output / Deliverables

| Artifact | Format | Location | Purpose |
|----------|--------|----------|---------|
| `review-report.md` | Markdown | `workspace/[branch-name]/` | Primary deliverable — post as PR comment |
| `violations.json` | JSON | `workspace/[branch-name]/` | Machine-readable for CI integration |

---

## Error Handling

### Step-Level Errors

| Step | Error Condition | Action |
|------|----------------|--------|
| 01 | `project_conventions` file not found | Abort with: "Cannot load project conventions from [path]. Verify CLAUDE.md exists or provide path." |
| 02 | Diff is empty | Abort with: "No changes found in diff. Verify the diff input is correct." |
| 02 | Diff exceeds 2000 lines | Warn user, continue but note in report: "Large diff — consider splitting review" |
| 03 | Convention file has syntax error | Skip convention check, continue with security scan, note in report |
| 04 | Grep fails (permissions) | Fall back to Read-based scan; note limitations in report |
| 05 | No findings (normal case) | Report: "No violations found. Code is ready to merge." |

### Abort Conditions

Stop and alert the user if:
- `diff` input is not readable — Error: "Cannot read diff. Check file path or provide diff directly."
- Both Step 03 and Step 04 fail — Error: "Review cannot complete. [specific errors]. Fix and restart."

### State on Abort

When aborting: Save progress to `workspace/[branch-name]/partial-review.md` with what was completed.
To resume: restart from the last completed step by providing its output directly.

---

## Completion Criteria

The workflow is complete when:

- [ ] All 5 steps have completed (or non-blocking steps have noted failures)
- [ ] `review-report.md` exists and contains the structured report
- [ ] Report includes a clear merge recommendation (merge / request changes / needs discussion)
- [ ] Every finding has: severity, location (file:line), description, and recommended action

**Final quality check:** Verify the merge recommendation is present and justified.

---

## Configuration

See `config/variables.yaml` for all configurable parameters.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_diff_lines` | 2000 | Warn above this threshold |
| `review_depth` | `standard` | `quick` (03 only) \| `standard` (03+04) \| `thorough` (03+04+architecture) |
| `security_patterns_file` | `references/security-patterns.md` | Patterns to grep for in security scan |
| `conventions_path` | `CLAUDE.md` | Default project conventions file |

---

## Execution Examples

### Example 1: Standard Review — Happy Path

**Input:**
```bash
# Diff: 87 lines across 3 files
# pr_description: "Add user authentication to the profile API endpoint"
# review_depth: standard
```

**Step 01 output:** Loaded CLAUDE.md conventions: TypeScript strict mode, no any,
auth required on all `/api/user/*` routes, tests required for new functions.

**Step 02 output:** 3 files changed. New function: `authenticateRequest()` (23 lines).
New route: `GET /api/user/profile`. No tests added for `authenticateRequest()`.

**Step 03 output:** 1 violation:
- Medium: `GET /api/user/profile` has no corresponding test in `__tests__/`

**Step 04 output:** 1 finding:
- Medium: `authenticateRequest()` uses `jwt.verify()` without specifying `algorithms`
  option (algorithm confusion vulnerability)

**Final report:**

```markdown
## Code Review: add-profile-auth
**Merge Recommendation:** ⚠️ Request Changes

**Findings (2):** 0 critical, 0 high, 2 medium, 0 low

### FINDING-001: Missing Test Coverage
**Severity:** Medium | **Type:** Convention Violation
**Location:** `src/auth/authenticateRequest.ts` (new function, no test)
**Description:** `authenticateRequest()` has no test coverage. Project conventions
require tests for all new functions.
**Action:** Add `__tests__/auth/authenticateRequest.test.ts`

### FINDING-002: JWT Algorithm Not Specified
**Severity:** Medium | **Type:** Security
**Location:** `src/auth/authenticateRequest.ts:12`
**Description:** `jwt.verify(token, secret)` without `{ algorithms: ['HS256'] }` allows
algorithm confusion attacks.
**Action:** Add `algorithms` option: `jwt.verify(token, secret, { algorithms: ['HS256'] })`

## Summary
Two medium-severity issues. Neither blocks functionality but both should be fixed before
merge per project standards. Estimated fix time: 20 minutes.
```

---

### Example 2: Failure Recovery

**Scenario:** Step 04 security scan fails (Bash unavailable), but Step 03 completes.

**Step 04 output (error):** Bash tool unavailable. Falling back to Read-based scan.

**Fallback action:** Agent uses Grep tool instead of Bash to scan for patterns.
Notes in report: "Security scan used Grep fallback — may miss patterns requiring
execution-time analysis."

**Workflow continues and completes** with note in report.

---

## Composability

- **Can be triggered by:** Pre-merge hooks, `/validate` command
- **Output feeds into:** PR merge gates, code quality metrics dashboards
- **Used as step in:** `release-preparation-workflow` (step 03 of 7)
- **Complements:** The Security Audit Agent can perform deeper analysis on specific files flagged by this workflow
```

---

## Quality Verification

This exemplar demonstrates:

- [x] 5 steps with explicit dependency table (Steps 03 and 04 parallel)
- [x] Input requirements with required/optional distinction
- [x] Per-step error handling: retry, fallback, skip, abort cases
- [x] Abort conditions with specific error messages
- [x] State preservation on abort
- [x] Completion criteria with checklist
- [x] `config/variables.yaml` documentation
- [x] 2 execution examples: happy path and failure recovery
- [x] Composability section
- [x] MCS-3 criteria met
