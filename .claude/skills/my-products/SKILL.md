---
name: my-products
description: >-
  Show your published and installed myClaude products with marketplace status.
  Lists workspace drafts, published products, and install counts via the myClaude CLI.
  Use when the creator asks "what have I published", "my products", "show my stuff",
  "how are my products doing", or "marketplace status".
---

# My Products

Show a unified view of the creator's product portfolio across workspace and marketplace.

## What to Show

### 1. Workspace Products (local)
!`ls workspace/*/.engine-meta.yaml 2>/dev/null || echo "No products in workspace/"`

### 2. Published Products (marketplace)

Check if the myClaude CLI is available and authenticated:
```bash
myclaude whoami 2>/dev/null
```

If authenticated, show published products:
```bash
myclaude list 2>/dev/null
```

### 3. Product Details

For each published product the creator asks about:
```bash
myclaude info {slug}
```

## Output Format

```
MY PRODUCTS

Local (workspace/):
  {slug}: {category} — {status} (last validated: {date})
  ...

Published (myclaude.sh):
  {slug}: {category} — v{version} — {downloads} downloads
  View: https://myclaude.sh/p/{slug}
  ...

Not yet published:
  {slug}: validated, ready for /publish
  ...
```

If CLI is not installed or not authenticated:
```
Published products: install myClaude CLI to check
  npm i -g @myclaude/cli && myclaude login
```
