# Application Exemplar: CLI Utility — Markdown Linter

**MCS Level:** 2 (Quality)
**Demonstrates:** README that earns 30-second install decision, working source structure,
CLAUDE.md config, architecture documentation, error handling, real usage examples.

---

## File: `README.md`

```markdown
# md-lint

Lints Markdown files for broken links, missing alt text, inconsistent heading hierarchy,
and custom rule violations. Designed for documentation repositories and content pipelines.

Zero configuration for sensible defaults. Fully configurable for strict environments.

## Quick Start

```bash
npm install -g @toolcraft/md-lint
md-lint docs/             # Lint all .md files in docs/ directory
```

---

## Installation

**Requirements:**
- Node.js 20+ (tested on 20.11.0 and 22.x)
- npm 10+ or pnpm 9+

**Install globally:**
```bash
npm install -g @toolcraft/md-lint
```

**Install as dev dependency (for CI):**
```bash
npm install --save-dev @toolcraft/md-lint
```

**Verify installation:**
```bash
md-lint --version
# Expected: md-lint 1.3.0
```

---

## Usage

### Basic

```bash
# Lint a single file
md-lint README.md

# Lint a directory (recursive)
md-lint docs/

# Lint with specific rules
md-lint docs/ --rules broken-links,alt-text,heading-hierarchy
```

### Output Formats

```bash
# Default: human-readable (color output, grouped by file)
md-lint docs/

# For CI: compact output (one issue per line)
md-lint docs/ --format compact

# For tooling: JSON output
md-lint docs/ --format json > lint-results.json

# GitHub Annotations format (for GitHub Actions)
md-lint docs/ --format github
```

### Example Output (Default)

```
✖ 3 errors, 2 warnings found

docs/api-reference.md
  Line 45  error    Broken link: ./nonexistent.md  broken-links
  Line 92  warning  Image missing alt text          alt-text

docs/guide.md
  Line 12  error    H3 follows H1 (skip level)     heading-hierarchy
  Line 34  error    Broken external link: https://old.example.com/removed
  Line 67  warning  Image missing alt text          alt-text
```

### All Options

```
md-lint [paths...] [options]

Arguments:
  paths                Files or directories to lint (default: current directory)

Options:
  --rules <list>       Comma-separated rules to run (default: all)
  --ignore <list>      Comma-separated patterns to ignore (e.g., "node_modules,dist")
  --format <format>    Output format: text | compact | json | github (default: text)
  --config <path>      Config file path (default: .md-lint.yaml if exists)
  --fix                Auto-fix issues that can be fixed automatically
  --max-warnings <n>   Fail if warnings exceed this count (default: none)
  --timeout <ms>       Network timeout for link checking (default: 5000)
  --help, -h           Show this help message
  --version, -v        Show version
```

---

## Configuration

### Config File (`.md-lint.yaml`)

```yaml
# .md-lint.yaml — Optional configuration file
rules:
  broken-links:
    enabled: true
    check-external: true      # Set false to skip external HTTP checks
    timeout: 8000             # Override per-rule timeout
  alt-text:
    enabled: true
  heading-hierarchy:
    enabled: true
    allow-h1-multiple: false  # Fail if multiple H1 headings exist
  custom-vocabulary:
    enabled: false
    words: []                  # Custom required/forbidden words

ignore:
  - "CHANGELOG.md"
  - "vendor/**"
  - "**/_drafts/**"

output:
  format: text
  max-warnings: 10
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MD_LINT_TIMEOUT` | `5000` | Default network timeout (ms) |
| `MD_LINT_NO_COLOR` | `false` | Disable color output (`true` to disable) |

---

## Available Rules

| Rule | Auto-fix | Description |
|------|---------|-------------|
| `broken-links` | No | Checks internal file references and external URLs |
| `alt-text` | No | Flags images without `alt` attributes |
| `heading-hierarchy` | Yes | Ensures heading levels don't skip (H1 → H3 without H2) |
| `trailing-whitespace` | Yes | Removes trailing whitespace |
| `consistent-list-style` | Yes | Enforces consistent list markers within a list |

---

## Architecture

```
src/
├── cli/
│   ├── index.ts         # CLI entry point and argument parsing
│   └── formatter.ts     # Output formatters (text, compact, json, github)
├── linter/
│   ├── engine.ts        # Core linting orchestration
│   ├── rules/           # Individual rule implementations
│   │   ├── broken-links.ts
│   │   ├── alt-text.ts
│   │   └── heading-hierarchy.ts
│   └── reporter.ts      # Result aggregation and exit code
├── parser/
│   └── markdown.ts      # Markdown AST parser (wraps unified/remark)
└── config/
    └── loader.ts        # Config file discovery and merging
```

**Key dependencies:**
- `unified` + `remark` — Markdown parsing to AST
- `commander` — CLI argument parsing
- `got` — HTTP client for external link checking (with retry and timeout)
- `chalk` — Terminal color output

**Design decisions:**
- Rule implementations receive the AST, not raw text — this prevents false positives from
  regex-based parsing and enables precise line-number reporting
- External link checking is async and batched — 10 concurrent requests by default,
  configurable via `--timeout`

See `docs/architecture.md` for full design decisions.

---

## Development

```bash
# Clone and install
git clone https://github.com/toolcraft/md-lint
cd md-lint
pnpm install

# Run in watch mode
pnpm dev

# Run tests
pnpm test

# Build for production
pnpm build

# Lint this project's own docs
pnpm lint:docs
```

---

## Known Limitations

- External link checking makes real HTTP requests — use `--rules broken-links` with
  `check-external: false` in CI for speed
- Very large files (>50,000 lines) may be slow on first parse — subsequent runs use caching
- Does not validate Markdown inside fenced code blocks

---

## License

MIT — see `LICENSE`

---

**Version:** 1.3.0 | **Author:** @toolcraft | **Changelog:** CHANGELOG.md
```

---

## File: `CLAUDE.md` (project CLAUDE.md for development on this app)

```markdown
# md-lint — Development CLAUDE.md

**Stack:** TypeScript 5 + Node.js 20 + unified ecosystem
**Purpose:** Claude Code development config for md-lint project itself

## First Action

1. Read `docs/architecture.md` — understand rule engine design and AST approach
2. Check `src/linter/rules/` — see existing rules for implementation patterns before creating new ones
3. Run `git status` before any file modification

## Rule Implementation Pattern

Every rule in `src/linter/rules/` follows this interface:

```typescript
import type { VFile } from 'vfile';
import type { LintResult, Rule } from '../types';

export const myRule: Rule = {
  name: 'my-rule',
  description: 'One sentence description',
  fixable: false, // true if --fix can auto-correct

  check(tree: Root, file: VFile): LintResult[] {
    const results: LintResult[] = [];
    // Visit AST nodes, push to results for each finding
    return results;
  },

  fix?(tree: Root): Root {
    // Mutate and return the AST (only if fixable: true)
    return tree;
  }
};
```

Never implement rules using regex on the raw file content — always use the AST.

## Testing

Tests live alongside source: `src/linter/rules/broken-links.test.ts`
Test fixtures live in `test/fixtures/` — never use real URLs in tests, use mock fixtures.

Run: `pnpm test` — all tests must pass before commit.

## Security

Never make network calls except in the `broken-links` rule using the `got` client.
No `eval()`, no dynamic imports outside of the plugin loader.
```

---

## Quality Verification

This exemplar demonstrates:

- [x] First paragraph earns the 30-second install decision
- [x] Quick Start: 2 commands from zero to working
- [x] Requirements with specific versions (not "Node.js")
- [x] `--verify` command to confirm installation
- [x] 3+ usage examples with real commands and real output
- [x] All CLI options documented
- [x] Config file with real YAML example
- [x] Architecture section with decisions (not just file tree)
- [x] Known limitations section
- [x] CLAUDE.md for future development
- [x] MCS-2 criteria met
