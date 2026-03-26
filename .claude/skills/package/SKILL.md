---
name: package
description: >-
  Package a product for distribution without publishing. Strips guidance comments,
  generates vault.yaml manifest, and stages the .publish/ directory. Use when preparing
  a product for review before publishing, or when the creator says "package",
  "prepare for publish", or "stage it".
disable-model-invocation: true
argument-hint: "[product-path]"
---

# Package

Stage a product for distribution without invoking the myClaude CLI.

This is the first half of the `/publish` flow — it prepares everything but stops before uploading.

## Flow

1. **Verify validation** — Check `.engine-meta.yaml` for passing MCS-1 result. If not validated, prompt to run `/validate` first.

2. **Strip guidance comments** (CE-D12) — Remove all `<!-- GUIDANCE: ... -->` and `# GUIDANCE: ...` lines from a copy of the product files. Never modify originals.

3. **Generate vault.yaml** — Create the manifest following the CONDUIT v2 schema. Load `creator.yaml` for author metadata. All required fields: name, version, type, description, entry, license.

4. **Stage .publish/** — Create `workspace/{product-slug}/.publish/` with:
   - Cleaned product files (guidance stripped)
   - vault.yaml
   - CHANGELOG.md (generate if missing)
   - LICENSE (copy or generate from license field)

5. **Re-validate** — Run MCS-1 structural checks on `.publish/` contents to catch stripping errors.

6. **Report** — Show: file count, total size, license, MCS level, guidance comments stripped.

## vault.yaml Schema

Read the full schema from the `/publish` skill — this skill uses the same vault.yaml v2 format defined there.

## Output

```
Package ready: workspace/{slug}/.publish/
  Files: {N} | Size: {size} | License: {license} | MCS: {level}
  Guidance stripped: {N} occurrences

Next: /publish to ship to myclaude.sh
```
