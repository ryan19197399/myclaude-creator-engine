---
name: quick-publish
description: >-
  Publish pipeline shortcut for an existing product: validate, package, and publish in
  sequence. Use when a product already exists in workspace/ and the creator wants to ship
  it quickly, or says "quick publish", "ship this", or "validate and publish".
argument-hint: "[product-path]"
disable-model-invocation: true
---

# Quick Publish — Validate and Ship

Pipeline: `/validate` -> `/package` -> `/publish` for an existing product.

## Flow

### Step 1 — Validate
Execute the `/validate` flow on the target product:
- Auto-detect product type from .engine-meta.yaml
- Run MCS checks at the creator's quality target
- Report score

Only proceed when validation passes.

### Step 2 — Package
Execute the `/package` flow:
- Strip guidance comments
- Generate vault.yaml
- Stage .publish/

### Step 3 — Publish
Execute the `/publish` flow:
- Show summary, require explicit confirmation
- Invoke `myclaude publish`

## Behavior

- If no product path is provided, check workspace/ for products and ask which one
- If multiple products exist, list them and ask
- Never proceed past a failed step
