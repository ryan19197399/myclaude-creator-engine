# MyClaude CLI — Command Reference

> Quick reference for all `myclaude` CLI commands used by Studio Engine v3.0.0.
> Package: `@myclaude-cli/cli` | Min version: `0.9.0` | Install: `npm i -g @myclaude-cli/cli`

---

## Authentication

### `myclaude login`

Authenticate with myclaude.sh. Interactive browser-based OAuth flow.

- **Used by:** /publish (required), /onboard (optional)
- **When needed:** Before any publish operation; during onboarding for marketplace features
- **Fallback:** Block publish; skip marketplace features in other skills
- **Output:** Interactive — opens browser

### `myclaude whoami`

Verify current authentication status and return username.

- **Used by:** /onboard (phase 6c), /publish (pre-flight)
- **Syntax:** `myclaude whoami 2>/dev/null`
- **Output:** Text — username if authenticated, error message if not
- **Fallback:** Prompt `myclaude login`

---

## Validation

### `myclaude validate --json`

Run marketplace validation against a `.publish/` directory. Checks vault.yaml, file structure, secrets, license, frontmatter, agent-skills-spec compliance.

- **Used by:** /validate (stage 6), /publish (step 5)
- **Syntax:** `cd workspace/{slug}/.publish && myclaude validate --json 2>/dev/null`
- **Output:** JSON `{ "valid": bool, "errors": [], "warnings": [] }`
- **Fallback:** Skip stage 6 with warning: "myclaude CLI not installed"
- **Severity:** Blocking during /publish, warning during /validate

### `myclaude doctor --json`

Health check for marketplace configuration and CLI setup.

- **Used by:** /validate (stage 6, post-validation)
- **Syntax:** `myclaude doctor --json 2>/dev/null`
- **Output:** JSON `{ "score": number }`
- **Fallback:** Skip silently
- **Note:** Score < 8.0 triggers warning with `myclaude doctor --fix` suggestion

---

## Publishing

### `myclaude publish`

Publish the staged `.publish/` directory to myclaude.sh. Requires prior authentication.

- **Used by:** /publish (step 6)
- **Syntax:** `cd workspace/{slug}/.publish && myclaude publish`
- **Output:** Interactive — confirmation prompt + result text
- **Fallback:** Block. Show manual upload alternative: `myclaude.sh/publish`
- **Severity:** Blocking
- **Prerequisites:** `myclaude login`, `myclaude validate --json` passes

---

## Marketplace Search

### `myclaude search`

Query the marketplace for products by keyword, category, or sort order.

- **Used by:** /explore, /create, /think, /onboard, /package, /publish
- **Variants:**
  ```bash
  myclaude search "{query}" --json 2>/dev/null
  myclaude search --category {type} --sort downloads --limit {n} --json 2>/dev/null
  myclaude search --category {type} --sort newest --limit 10 --json 2>/dev/null
  myclaude search --category {type} --sort price-desc --limit 5 --json 2>/dev/null
  ```
- **Output:** JSON array of product objects
- **Fallback:** Skip silently — no marketplace context shown
- **Sort options:** `downloads`, `newest`, `price-desc`
- **Categories:** `skills`, `squads`, `systems`, `agents`, `workflows`, `minds`, `bundles`

### `myclaude trending --json`

Fetch currently trending products on the marketplace.

- **Used by:** /explore, /think
- **Syntax:** `myclaude trending --json 2>/dev/null`
- **Output:** JSON array of trending products
- **Fallback:** Skip silently

### `myclaude workspace --recommend --json`

Get product recommendations based on current workspace context.

- **Used by:** /explore
- **Syntax:** `myclaude workspace --recommend --json 2>/dev/null`
- **Output:** JSON array of recommended products
- **Fallback:** Skip silently

---

## Analytics & Profile

### `myclaude stats`

Retrieve install counts and analytics for published products.

- **Used by:** /status
- **Variants:**
  ```bash
  myclaude stats --json 2>/dev/null              # aggregate
  myclaude stats {slug} --json 2>/dev/null       # per-product
  ```
- **Output:** JSON `{ "installs": number, "downloads": number, "rating": number }`
- **Fallback:** Show "—" for marketplace metrics

### `myclaude my-products --json`

List all products published by the authenticated user.

- **Used by:** /status
- **Syntax:** `myclaude my-products --json 2>/dev/null`
- **Output:** JSON array of owned products
- **Fallback:** Skip marketplace intelligence section

### `myclaude notifications --json`

Fetch activity feed (new installs, reviews, mentions).

- **Used by:** /status
- **Syntax:** `myclaude notifications --json 2>/dev/null`
- **Output:** JSON array of activity items
- **Fallback:** Skip notifications display

### `myclaude profile pull --json`

Pull creator profile including level and XP from marketplace.

- **Used by:** /status, /publish (post-publish reminder)
- **Syntax:** `myclaude profile pull --json 2>/dev/null`
- **Output:** JSON `{ "level": number, "xp": number, "username": string }`
- **Fallback:** Skip level display

### `myclaude profile sync`

Push local creator.yaml profile to the marketplace.

- **Used by:** /onboard (phase 6c)
- **Syntax:** `myclaude profile sync`
- **Output:** Text confirmation
- **Fallback:** Skip; creator can sync manually later

---

## Payments

### `myclaude stripe status`

Check if Stripe is connected for paid product distribution.

- **Used by:** /onboard (phase 6c), /package (paid products)
- **Syntax:** `myclaude stripe status 2>/dev/null`
- **Output:** Text — "connected" or "not connected"
- **Fallback:** Warn; block paid product packaging
- **Severity:** Blocking for paid products only

### `myclaude stripe connect`

Initiate Stripe Connect onboarding for payment processing.

- **Used by:** /onboard (guided), /package (guided)
- **Syntax:** `myclaude stripe connect`
- **Output:** Interactive — opens browser for Stripe onboarding
- **Fallback:** Direct to myclaude.sh Stripe setup page

---

## Product Management

### `myclaude install {slug}`

Install a product from the marketplace.

- **Used by:** /explore (install action), /create (README template)
- **Syntax:** `myclaude install {slug}`
- **Output:** Interactive — download + install confirmation
- **Fallback:** Manual install instructions

### `myclaude update --all`

Update all installed marketplace products to latest versions.

- **Used by:** Utility (user-initiated)
- **Syntax:** `myclaude update --all`
- **Output:** Text — update summary
- **Fallback:** Manual per-product reinstall

### `myclaude list`

List all installed marketplace products.

- **Used by:** Utility (user-initiated)
- **Syntax:** `myclaude list`
- **Output:** Text — table of installed products
- **Fallback:** Glob `.claude/skills/*/` for local inventory

### `myclaude info {slug}`

Show detailed information about a marketplace product.

- **Used by:** Utility (user-initiated)
- **Syntax:** `myclaude info {slug}`
- **Output:** Text — product details, version, author, description
- **Fallback:** Direct to `myclaude.sh/p/{slug}`

---

## Setup

### `myclaude setup-mcp`

Configure MCP server integration for Claude Code.

- **Used by:** /onboard (phase 6c)
- **Syntax:** `myclaude setup-mcp 2>/dev/null`
- **Output:** Text — setup confirmation
- **Fallback:** Skip with pro-tip: "Run `myclaude setup-mcp` to let Claude Code search and install products directly"

---

## Diagnostics

### `myclaude --version`

Check installed CLI version. Used for compatibility verification.

- **Used by:** /explore (activation protocol step 2)
- **Syntax:** `myclaude --version 2>/dev/null`
- **Output:** Text — version string (e.g., `0.9.0`)
- **Fallback:** Degrade to offline mode — show install instructions, offer non-marketplace alternatives
- **Severity:** Silent-skip — no user-visible warning on failure

---

## Common Patterns

### JSON output convention

All read-only marketplace queries use `--json 2>/dev/null`:
```bash
myclaude <command> --json 2>/dev/null
```

### Working directory for publish operations

```bash
cd workspace/{slug}/.publish && myclaude <validate|publish>
```

### CLI availability check

```bash
if command -v myclaude &>/dev/null; then
  # CLI available
else
  echo "Install: npm i -g @myclaude-cli/cli"
fi
```

### Skills that never invoke CLI

`/fill`, `/map`, /import`, `/help`, `/test` — these are content-only or internal-only skills with no marketplace interaction.
