# meta/ — Engine Evolution System

> Observational layer for continuous improvement of the MyClaude Studio Engine.
> Every friction found during real usage is captured, categorized, and resolved surgically.

## Purpose

This directory exists because the Engine's founder is also its heaviest user.
Frictions discovered during real product creation are more valuable than hypothetical requirements.
This system turns usage sessions into evolution fuel.

## Structure

```
meta/
├── README.md                ← You are here
├── frictions/               ← UX/DX friction points found during real usage
│   └── F-{NNN}-{slug}.md   ← One file per friction, structured format
├── roadmap/
│   └── backlog.yaml         ← Two-track backlog: Local + Ecosystem
├── sessions/
│   └── {date}-{slug}.md     ← Session logs: what was done, what was found
├── vision/
│   └── {slug}.md            ← Strategic architecture visions (not frictions)
├── principles/
│   └── evolution.md         ← Meta-principles governing Engine evolution itself
└── patterns/
    └── {slug}.md            ← Reusable patterns extracted from solved frictions
```

## Friction Lifecycle

```
DISCOVERED → DOCUMENTED → PRIORITIZED → DESIGNED → IMPLEMENTED → VALIDATED
   (session)    (F-NNN)     (backlog)     (pattern)    (code)       (re-test)
```

## Conventions

- Friction IDs: `F-001`, `F-002`, ... (never reused, even if deleted)
- Severity: `critical` | `high` | `medium` | `low`
- Effort: `XS` (<1h) | `S` (1-4h) | `M` (4-8h) | `L` (1-3d) | `XL` (3d+)
- Status: `open` | `designing` | `implementing` | `resolved` | `wont-fix`
- Sessions reference frictions they discover: `Discovered: F-001, F-002`
- Frictions reference sessions where they were found: `Source: session/2026-03-29-...`

## Rules

- Every friction MUST come from real usage, not speculation
- Every friction MUST have a concrete "user was trying to do X" story
- Solutions go in patterns/ BEFORE going into code
- Never resolve a friction without re-testing the original scenario
