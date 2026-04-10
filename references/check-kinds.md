# Check Kinds — Deterministic Validator Specification

> **Scope:** Canonical catalog of all deterministic check kinds the MyClaude
> Studio Engine can execute WITHOUT LLM involvement. Each kind has a
> well-defined handler that the `myclaude` CLI (or any compatible runner)
> dispatches by name.
>
> **Why this exists:** Clause VIII (Every Token Earns Its Place). Checks
> that can run as Node/Bash/regex in milliseconds should not burn LLM
> context. Deterministic checks run in the CLI; LLM is reserved for
> subjective judgment (substance scoring, anti-commodity, value intelligence).
>
> **Contract:** product-dna/*.yaml codices declare checks via
> `{ kind: <name>, ...args }`. The CLI reads the codex, dispatches each
> check to its handler, returns a JSON result. The LLM consumer of
> `/validate` parses the JSON and only applies coaching to failures —
> it never re-runs deterministic checks.

---

## Schema of a check declaration

Every structured check inside a product-dna codex follows this shape:

```yaml
check:
  kind: <enum from this catalog>      # required
  severity: blocking | warning | info # required
  stage: 1-8                          # required — which validation stage owns it
  fallback_to_llm: bool               # required — if CLI cannot run this check, fall back to LLM interpretation
  # kind-specific arguments follow:
  ...
```

Every check declaration MUST resolve to one of the canonical kinds below.
Unknown kinds cause `codex-drift-check.py` to fail validation.

---

## Canonical check kinds

### 1. `file_exists`

Check that a file exists at a given path relative to the product root.

**Args:**
- `path` (string, required) — relative path from product root
- `required_for_mcs` (list of ints, optional) — e.g., `[1, 2, 3]` means required at all MCS levels

**Example:**
```yaml
check:
  kind: file_exists
  path: "README.md"
  severity: blocking
  stage: 1
  fallback_to_llm: false
  required_for_mcs: [1, 2, 3]
```

**CLI handler:** `fs.existsSync(path.join(productRoot, args.path))`

---

### 2. `glob_pattern`

Check that at least N files match a glob pattern relative to the product root.

**Args:**
- `pattern` (string, required) — glob like `"references/**/*.md"`
- `minimum` (int, required) — minimum match count
- `maximum` (int, optional) — maximum match count (exceeds = warning or error)

**Example:**
```yaml
check:
  kind: glob_pattern
  pattern: "references/*.md"
  minimum: 1
  severity: blocking
  stage: 1
  fallback_to_llm: false
```

**CLI handler:** `glob.sync(args.pattern, { cwd: productRoot }).length >= args.minimum`

---

### 3. `line_count_ceiling`

Check that a file does not exceed a line count ceiling.

**Args:**
- `path` (string, required)
- `ceiling` (int, required) — hard maximum
- `warn_at` (int, optional) — soft warning threshold

**Example:**
```yaml
check:
  kind: line_count_ceiling
  path: "SKILL.md"
  ceiling: 500
  warn_at: 350
  severity: blocking
  stage: 3
  fallback_to_llm: false
```

**CLI handler:** `fs.readFileSync(path).toString().split('\n').length`

---

### 4. `char_count_ceiling`

Same as line_count_ceiling but for character count. Used for output styles
and claude-md products where per-character cost matters.

**Args:**
- `path` (string, required)
- `ceiling` (int, required)
- `warn_at` (int, optional)

---

### 5. `yaml_parse_valid`

Check that a YAML/JSON file parses without errors AND optionally that
specific fields exist.

**Args:**
- `path` (string, required)
- `required_fields` (list of strings, optional) — dotted paths like `"frontmatter.name"`

**Example:**
```yaml
check:
  kind: yaml_parse_valid
  path: "SKILL.md"
  required_fields: ["name", "description"]
  severity: blocking
  stage: 2
  fallback_to_llm: false
```

**CLI handler:** parse YAML frontmatter (for `.md` files) or whole file
(for `.yaml`), validate required dotted paths.

---

### 6. `frontmatter_field`

Check a specific frontmatter field against constraints (exists, type,
length, regex).

**Args:**
- `path` (string, required)
- `field` (string, required) — e.g., `"description"`
- `exists` (bool, optional)
- `type` (enum: string|number|boolean|array, optional)
- `min_length` (int, optional) — for strings, word count
- `max_length` (int, optional)
- `regex` (string, optional) — must match

**Example:**
```yaml
check:
  kind: frontmatter_field
  path: "SKILL.md"
  field: "description"
  exists: true
  min_length: 50
  max_length: 200
  severity: blocking
  stage: 2
  fallback_to_llm: false
```

---

### 7. `grep_section_exists`

Check that a markdown section header exists in a file.

**Args:**
- `path` (string, required)
- `section_pattern` (string, required) — regex matching header, e.g., `"^## Anti-Patterns"`
- `case_sensitive` (bool, optional, default false)

**Example:**
```yaml
check:
  kind: grep_section_exists
  path: "SKILL.md"
  section_pattern: "^## (Activation Protocol|Boot Sequence)"
  severity: blocking
  stage: 3
  fallback_to_llm: false
```

---

### 8. `grep_section_minimum_items`

Check that a section contains at least N list items.

**Args:**
- `path` (string, required)
- `section_pattern` (string, required) — regex matching the section header
- `minimum` (int, required) — minimum items
- `item_pattern` (string, optional, default `"^[-*] "`) — regex for list items

**Example:**
```yaml
check:
  kind: grep_section_minimum_items
  path: "SKILL.md"
  section_pattern: "^## Anti-Patterns"
  minimum: 5
  item_pattern: "^[-*] "
  severity: blocking
  stage: 3
  fallback_to_llm: false
```

**CLI handler:** scan file for section header, count subsequent list items
until next header of equal or higher level.

---

### 9. `regex_forbidden`

Check that a regex pattern does NOT appear in one or more files.

**Args:**
- `paths` (list of strings, required) — files to scan; supports globs
- `pattern` (string, required) — regex
- `exception_paths` (list of strings, optional) — files to skip

**Example:**
```yaml
check:
  kind: regex_forbidden
  paths: ["**/*.md", "**/*.yaml"]
  pattern: "ATHENA|Leonardo|MCS-\\d{3,}"
  severity: blocking
  stage: 7
  fallback_to_llm: false
```

**Used for:** invisibility grep, secret scan (extended patterns), no-hardcoded-paths.

---

### 10. `regex_required`

Inverse of `regex_forbidden` — a pattern MUST appear at least once.

**Args:**
- `path` (string, required)
- `pattern` (string, required)
- `minimum_occurrences` (int, optional, default 1)

**Example:**
```yaml
check:
  kind: regex_required
  path: "SKILL.md"
  pattern: "references/[a-z-]+\\.md"
  minimum_occurrences: 2
  severity: warning
  stage: 3
  fallback_to_llm: false
```

**Used for:** D3 Progressive Disclosure (body must reference references/ at least N times), pointer presence checks.

---

### 11. `secret_scan`

Run the CLI's native secret scanner against the product. Already implemented
in `myclaude validate` today — this check kind just declares which files to
include in the scan.

**Args:**
- `paths` (list of strings, required) — default `["**/*"]`
- `patterns_reference` (string, optional) — path to custom pattern file; defaults to CLI builtin

**Example:**
```yaml
check:
  kind: secret_scan
  paths: ["**/*"]
  severity: blocking
  stage: 2
  fallback_to_llm: false
```

---

### 12. `placeholder_scan`

Check that no files contain placeholder patterns from `config.yaml → placeholder_patterns`.

**Args:**
- `paths` (list of strings, required)
- `patterns_reference` (string, optional) — defaults to `config.yaml → placeholder_patterns`

**Example:**
```yaml
check:
  kind: placeholder_scan
  paths: ["**/*.md"]
  severity: blocking
  stage: 2
  fallback_to_llm: false
```

---

### 13. `reference_resolves`

Check that inline references to other files in the product resolve
(the target file exists).

**Args:**
- `path` (string, required) — file to scan for references
- `reference_pattern` (string, required) — regex that captures the reference target in group 1
- `target_relative_to` (string, optional) — root for resolution, defaults to product root

**Example:**
```yaml
check:
  kind: reference_resolves
  path: "SKILL.md"
  reference_pattern: "references/([a-z0-9/_-]+\\.md)"
  target_relative_to: "{product_root}"
  severity: warning
  stage: 3
  fallback_to_llm: false
```

**Used for:** orphan reference detection, broken @-imports.

---

### 14. `frontmatter_description_rubric`

**Hybrid check** — runs the structured description rubric from
`product-dna/skill.yaml → description_engineering.rubric` against the
skill's description field. Returns a 0-10 score per criterion.

**Args:**
- `path` (string, required)
- `rubric_reference` (string, required) — dotted path to the rubric declaration

**Example:**
```yaml
check:
  kind: frontmatter_description_rubric
  path: "SKILL.md"
  rubric_reference: "description_engineering.rubric"
  severity: warning
  stage: 3
  fallback_to_llm: true
  fallback_reason: "Semantic criteria (verb specificity, trigger quality) can be CLI-approximated but benefit from LLM coaching on failures."
```

**CLI handler:** runs the 5 dimensions (verb, domain, triggers, keywords, size) with regex+heuristic approximations. Items that fail get passed to LLM for coaching.

---

### 15. `composite_and`, `composite_or`, `composite_not`

Compose multiple checks with boolean logic.

**Args:**
- `children` (list of check declarations) — nested checks

**Example:**
```yaml
check:
  kind: composite_and
  severity: blocking
  stage: 3
  fallback_to_llm: false
  children:
    - kind: grep_section_exists
      path: "SKILL.md"
      section_pattern: "^## When NOT to Use"
    - kind: grep_section_minimum_items
      path: "SKILL.md"
      section_pattern: "^## When NOT to Use"
      minimum: 2
```

---

## Severity semantics

| Severity | Effect on validation verdict | CLI exit behavior |
|---|---|---|
| `blocking` | Failure blocks MCS level. `valid: false` in JSON output. | exit code non-zero |
| `warning` | Failure reduces score but does not block. `warnings[]` in JSON. | exit code 0 |
| `info` | Observational only. `info[]` in JSON. | exit code 0 |

---

## Stage ownership

Each check declares which validation stage owns it (1-8). The CLI can run
checks stage-by-stage, stopping at first blocking failure in blocking stages.

| Stage | Owner | Blocking |
|---|---|---|
| 1 | structural (file existence) | yes |
| 2 | integrity (parse + secrets + placeholders) | yes |
| 3 | DNA Tier 1 (universal patterns) | yes for MCS-1 |
| 4 | DNA Tier 2 (advanced patterns) | no |
| 5 | DNA Tier 3 (expert patterns) | no |
| 6 | CLI preflight (native `myclaude validate`) | yes |
| 7 | anti-commodity coaching | no |
| 8 | value intelligence | no |

---

## fallback_to_llm semantics

When `fallback_to_llm: false`, the CLI runs the check autonomously and
returns a deterministic pass/fail. The LLM never sees the check execution.

When `fallback_to_llm: true`, the CLI attempts the check but passes
ambiguous cases to the LLM for interpretation. Used for:
- Semantic quality judgments (is this description "vague"?)
- Substance scoring (anti-commodity)
- Context-dependent severity (is this hardcoded path acceptable?)

A check with `fallback_to_llm: true` MUST also declare `fallback_reason`.

---

## JSON output schema (CLI → LLM contract)

When the CLI runs deterministic checks against a product, it emits JSON
in this shape:

```json
{
  "product_slug": "my-skill",
  "type": "skill",
  "level": 2,
  "checks": [
    {
      "id": "stage-3.D2",
      "stage": 3,
      "kind": "grep_section_minimum_items",
      "pass": true,
      "message": "Anti-Patterns section found with 7 items (minimum 5)",
      "evidence": { "file": "SKILL.md", "line": 45, "items_counted": 7 }
    },
    {
      "id": "stage-3.D1",
      "stage": 3,
      "kind": "grep_section_exists",
      "pass": false,
      "severity": "blocking",
      "message": "Activation Protocol section not found in SKILL.md",
      "evidence": { "file": "SKILL.md", "searched_pattern": "^## (Activation Protocol|Boot Sequence)" },
      "fix_hint": "Add a section '## Activation Protocol' to SKILL.md after the title"
    }
  ],
  "scores": {
    "dna_tier1": 83.3,
    "dna_tier2": null,
    "structural": 100.0,
    "integrity": 100.0,
    "overall": 80.0
  },
  "verdict": "NEEDS_WORK",
  "mcs_level_achieved": 1,
  "llm_followups": [
    {
      "id": "stage-7.anti_commodity",
      "reason": "Substance scoring requires semantic interpretation beyond regex.",
      "context_for_llm": {
        "description": "the full description string",
        "body_excerpt": "first 500 chars of body",
        "anti_patterns_found": ["...", "..."]
      }
    }
  ],
  "token_savings_estimate": {
    "deterministic_checks_run": 24,
    "llm_checks_required": 2,
    "tokens_saved_estimate": 12000
  }
}
```

**The `llm_followups` array** is the explicit contract between CLI and
LLM: the CLI declares what it cannot decide, and for each item provides
the minimum context the LLM needs. The LLM consumer (`/validate` skill)
reads this array and invokes its own reasoning only for those items.

---

## Migration from legacy prose checks

Existing product-dna files use prose checks like `check: "grep anti-pattern section with >=5 items"`. These are **legacy** and supported as fallback:

- If `check` is a string, the CLI attempts a heuristic parse and falls back to `fallback_to_llm: true` if ambiguous.
- New codices MUST use structured `check: { kind: ... }`; prose checks are legacy-only.

When migrating a legacy check, the mapping is usually direct:
- `"grep X section with >=N items"` → `grep_section_minimum_items`
- `"file exists"` → `file_exists`
- `"primary file <500 lines"` → `line_count_ceiling`
- `"no hardcoded paths"` → `regex_forbidden`
- `"README with what/install/usage/requirements"` → composite of 4 `grep_section_exists`

---

## Implementation guidance for the CLI team

This file is the contract. When `myclaude validate` learns to consume
product-dna codices, the handler dispatch table should map kind names to
TypeScript functions. Skeleton:

```typescript
// packages/cli/src/validators/check-kinds.ts
type CheckKind =
  | "file_exists" | "glob_pattern" | "line_count_ceiling" | "char_count_ceiling"
  | "yaml_parse_valid" | "frontmatter_field" | "grep_section_exists"
  | "grep_section_minimum_items" | "regex_forbidden" | "regex_required"
  | "secret_scan" | "placeholder_scan" | "reference_resolves"
  | "frontmatter_description_rubric"
  | "composite_and" | "composite_or" | "composite_not";

interface CheckDeclaration {
  kind: CheckKind;
  severity: "blocking" | "warning" | "info";
  stage: number;
  fallback_to_llm: boolean;
  fallback_reason?: string;
  [k: string]: any;  // kind-specific args
}

interface CheckResult {
  id: string;
  stage: number;
  kind: CheckKind;
  pass: boolean;
  severity: "blocking" | "warning" | "info";
  message: string;
  evidence?: Record<string, any>;
  fix_hint?: string;
}

const handlers: Record<CheckKind, (c: CheckDeclaration, productRoot: string) => CheckResult> = {
  file_exists: (c, root) => { /* fs.existsSync */ },
  glob_pattern: (c, root) => { /* glob.sync */ },
  // ... etc
};

export function runCheck(decl: CheckDeclaration, productRoot: string, id: string): CheckResult {
  const handler = handlers[decl.kind];
  if (!handler) throw new Error(`Unknown check kind: ${decl.kind}`);
  return { ...handler(decl, productRoot), id };
}
```

The CLI's existing `myclaude validate` command continues to work as-is.
A new flag is added:

```
myclaude validate --codex product-dna/skill.yaml --json
```

When `--codex` is present, the CLI loads the codex, extracts all
structured checks (traversing `lifecycle.validate.per_stage_hooks` and
`dna_patterns.tier*.D*.check`), dispatches them to handlers, and returns
the canonical JSON output schema above.

---

## Token economics

Every deterministic check the CLI runs saves ~100-500 tokens of LLM
context that would otherwise be spent on:

1. Loading stage detail files into context
2. Reading the product file into context for grep
3. LLM interpretation of "what does this check mean?"
4. LLM production of the pass/fail verdict

**Conservative estimate per /validate invocation:**
- 24 deterministic checks × 250 tokens/check saved = 6,000 tokens
- 2 LLM follow-ups × 2,000 tokens = 4,000 tokens spent
- Net savings: ~60-70% vs. current pure-LLM execution

At marketplace scale (millions of validations/month), this is the
difference between marketplace economic viability and not.

---

*check-kinds.md v1.0 — MyClaude Studio Engine*
*Contract between product-dna codices and the myclaude CLI deterministic runner.*
