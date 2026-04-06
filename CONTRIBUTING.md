# Contributing to MyClaude Studio Engine

Thanks for wanting to contribute. This project exists because people like you care about making Claude Code better for everyone — not just developers, but consultants, researchers, writers, and anyone with expertise worth sharing.

Every contribution makes the ecosystem stronger.

---

## Ways to Contribute

### Friction Reports (Most Valuable)

The single most valuable contribution is telling us where the engine feels wrong. Did a command confuse you? Did output feel unclear? Did you expect something that didn't happen?

Open an issue with the **friction** label and describe:
- What you were doing
- What you expected
- What actually happened
- How it made you feel (frustrated? confused? stuck?)

We track frictions as first-class data and turn them into systemic improvements. Your confusion is a design bug.

### New Product Types

Want to add a new product type? A product type needs four artifacts:

| Artifact | Location | Purpose |
|----------|----------|---------|
| DNA spec | `product-dna/{type}.yaml` | Which structural patterns apply |
| Template | `templates/{type}/` | Starter structure with guided annotations |
| Exemplar | `references/exemplars/` | A finished example showing what great looks like |
| Routing | `config.yaml` | How the engine discovers the new type |

Also update `structural-dna.md` applicability matrix so `/validate` knows which patterns to check.

### New Structural Patterns

The engine currently has 20 patterns across 3 tiers. To propose a new one:

1. Describe the pattern: what it checks, why it matters, how to fix violations
2. Define which product types it applies to
3. Propose the tier (Verified / Premium / Elite)
4. Show at least one real example of a product that would benefit from this check

### Documentation

Improvements, clarifications, translations — all welcome. The docs follow [Diataxis](https://diataxis.fr/):

| Doc type | Purpose | Example |
|----------|---------|---------|
| Tutorial | Learning by doing | `docs/getting-started.md` |
| How-to | Solving a specific task | `docs/guides/for-developers.md` |
| Reference | Looking up details | `docs/reference/commands.md` |
| Explanation | Understanding why | Architecture docs |

Please keep the same type within each doc — don't mix tutorial steps into a reference page.

### Bug Fixes and Quality

Found a bug? Fix it and submit a PR. Small fixes (typos, broken links, formatting) don't need an issue — just submit directly.

---

## Submitting a Pull Request

### Before You Start

1. Fork the repository
2. Create a branch from `main`: `git checkout -b your-feature`
3. Make your changes
4. Test your changes (run the relevant commands in Claude Code)
5. Submit a PR

### PR Title Format

Use conventional commits:

```
feat: add rust-analyzer product type
fix: /validate score calculation for bundles
docs: add Portuguese translation for FAQ
refactor: simplify /fill section walker
```

### PR Checklist

Before submitting, verify:

- [ ] No secrets or credentials committed
- [ ] No internal references (session logs, personal names, internal tool names)
- [ ] YAML files validate cleanly
- [ ] Changes tested in Claude Code
- [ ] Documentation updated if behavior changed
- [ ] Existing tests still pass (if applicable)

### What Makes a Good PR

- **Small and focused** — one concern per PR
- **Descriptive** — explain what changed and why
- **Tested** — show that it works, don't just claim it
- **Backwards-compatible** — don't break existing products or workflows

---

## Development Setup

```bash
git clone https://github.com/myclaude-sh/myclaude-creator-engine
cd myclaude-creator-engine
claude
```

The engine loads from `CLAUDE.md`. Run `/status` to see the current state. Run `/help` for all commands.

### Key Directories

```
.claude/skills/     — The 15 engine skills (this is where commands live)
product-dna/        — DNA specs per product type
templates/          — Starter templates per product type
references/         — Quality specs, exemplars, guides
docs/               — Public documentation
workspace/          — Active builds (gitignored)
```

---

## Code of Conduct

Be respectful. Be constructive. Focus on making the engine better for all creators.

We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). The short version: be kind, be inclusive, assume good intent.

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

## Questions?

Open an issue with the **question** label, or start a [Discussion](https://github.com/myclaude-sh/myclaude-creator-engine/discussions).

We are glad you are here.
