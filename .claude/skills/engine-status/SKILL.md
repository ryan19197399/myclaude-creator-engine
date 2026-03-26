---
name: engine-status
description: >-
  Show myClaude Creator Engine status: loaded profile, workspace products, stale builds,
  and engine version. Use when the creator asks "what's the status", "show dashboard",
  "engine status", or at the start of a session to orient.
---

# Engine Status

Display a concise dashboard of the current Engine state.

## What to Show

### 1. Creator Profile
!`cat creator.yaml 2>/dev/null | head -20 || echo "No creator profile found. Run /onboard to get started."`

### 2. Workspace Products
!`ls workspace/*/.engine-meta.yaml 2>/dev/null || echo "No products in workspace/"`

### 3. Engine Version
!`head -3 CLAUDE.md 2>/dev/null | grep -i version || echo "v1.0.0"`

## Format

Present the information as a clean dashboard:

```
myClaude Creator Engine v1.0.0
Profile: {creator name} ({type}) | Quality target: {MCS level}
Products in workspace: {N}
  - {slug}: {status} (last validated: {date})
  - ...
```

If any product has not been validated in 30+ days, flag it:
```
  Warning: {slug} not validated in {N} days
```

If creator.yaml is missing, show only the onboarding prompt.
