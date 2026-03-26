---
name: quick-skill
description: >-
  Full pipeline shortcut: create a skill, validate it, package it, and publish it in one
  guided session. Walks the creator through each step, verifying success before proceeding
  to the next. Use when the creator wants the fastest path from idea to marketplace,
  or says "quick skill", "fast track", or "idea to publish".
argument-hint: "[skill-name]"
disable-model-invocation: true
---

# Quick Skill — Idea to Marketplace

Full pipeline: `/create skill` -> `/validate` -> `/package` -> `/publish` in one guided session.

## Flow

### Step 1 — Create
Execute the `/create skill` flow:
- Ask discovery questions
- Generate scaffold in workspace/
- Verify MCS-1 structural compliance

Pause and let the creator fill in content. When they signal readiness ("done", "ready", "validate"), proceed.

### Step 2 — Validate
Execute the `/validate` flow:
- Run MCS checks at the creator's quality target (from creator.yaml)
- Report score and any issues
- If issues exist, help fix them before proceeding

Only proceed when validation passes.

### Step 3 — Package
Execute the `/package` flow:
- Strip guidance comments
- Generate vault.yaml
- Stage .publish/ directory

### Step 4 — Publish
Execute the `/publish` flow:
- Show summary and ask for confirmation
- Invoke `myclaude publish` from .publish/

## Behavior

- Never skip steps
- Verify each step succeeded before proceeding
- If a step fails, help the creator resolve it
- The creator can exit at any step — progress is saved in workspace/
