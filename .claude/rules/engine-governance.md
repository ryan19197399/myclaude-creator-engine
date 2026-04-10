# Engine Governance Rules

These rules are enforced by Claude Code's rules system for the MyClaude Studio Engine.

## Workspace Boundary
- All product files MUST be created within `workspace/` directory
- Path traversal patterns (`../`, `..\\`) in slugs are forbidden
- Slug format: `^[a-z0-9][a-z0-9-]{2,39}$`

## State Machine Integrity
- Product state transitions follow quality-gates.yaml strictly
- File edits to validated/packaged products trigger regression to "content" state
- Published products remain published — new edits are tracked as next version

## Creator Profile
- Skills that depend on creator.yaml MUST check for its existence before proceeding
- Missing creator.yaml → suggest /onboard, do not proceed with assumptions

## Creator Language
- All Engine output (messages, questions, confirmations, errors, celebrations) MUST be in `creator.yaml → creator.language`
- This governs Engine-to-creator communication, NOT product content (product locale is handled by the locale-adaptive clause in forged files)
- If `creator.language` is absent, default to `en`

## Quality Gates
- /validate MUST run before /package
- /package MUST run before /publish
- /publish MUST require explicit creator confirmation
- WHY comments MUST be fully stripped in .publish/ — verify with grep
