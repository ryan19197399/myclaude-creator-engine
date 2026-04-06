# Onboard Protocol — Detail Reference

Full protocol for `/onboard`. Load this file when executing any onboarding phase.

---

## System Resilience (Scale Architecture)

This skill runs on millions of machines. Every scan can fail. Design for the worst case.

### Platform Detection (Phase 0 — runs BEFORE Phase 1)

```bash
uname -s 2>/dev/null || echo "WINDOWS"
echo $SHELL 2>/dev/null || echo $0 2>/dev/null || echo "unknown"
```

| Platform | Home Dir | Shell | Locale Command | Git Available |
|----------|----------|-------|----------------|---------------|
| macOS | `$HOME` or `~` | bash/zsh | `echo $LANG` | Usually yes (Xcode CLT) |
| Linux | `$HOME` or `~` | bash/zsh/fish | `echo $LANG` or `locale` | Package manager dependent |
| Windows (Git Bash) | `$USERPROFILE` or `$HOME` | bash | `powershell -c "..."` | Yes (bundled) |
| Windows (PowerShell) | `$env:USERPROFILE` | pwsh | `[CultureInfo]::CurrentCulture.Name` | Separate install |
| WSL | `$HOME` (Linux) | bash/zsh | `echo $LANG` | Yes |
| Docker/CI | `$HOME` or `/root` | sh/bash | May not exist | Varies |
| Codespaces/Gitpod | `$HOME` | bash | `echo $LANG` | Yes |

**Resolution order for `{home}`:**
1. `$HOME` (works on all Unix + Git Bash on Windows)
2. `$USERPROFILE` (Windows native)
3. `C:\Users\$USERNAME` (Windows fallback)
4. `/root` (Docker/CI fallback)

**RULE:** Never hardcode paths. Always resolve dynamically. Test with `test -d "{resolved_path}/.claude"` before scanning.

### Scan Failure Protocol

Every Phase 1 scan MUST be wrapped in error handling. A failing scan MUST NOT block the onboarding flow.

| Scan | Failure Mode | Impact | Fallback |
|------|-------------|--------|----------|
| Git Identity | git not installed, no global config | No name/email | `name_type = unknown`, ask in Phase 3 |
| Skills Glob | .claude/ doesn't exist | No skill count | `detected_skills_count = 0`, classify as beginner baseline |
| Rules Glob | No rules dir | No rules count | `detected_rules_count = 0`, does not affect level much (weight 1x) |
| CLAUDE.md Read | File doesn't exist | No style inference | `claude_md_type = none`, skip style analysis |
| settings.json Read | File doesn't exist or malformed JSON | No MCP count | `mcp_servers_count = 0`, does not affect level much (weight 1x) |
| Project Breadth | No projects dir | No project count | `active_projects_count = 0` |
| Workspace Scan | No workspace/ | No products | `unpublished_drafts = 0` |
| Locale | Command not found | No language | Fallback to `"en"`, infer from CLAUDE.md if available |

**Degradation rules:**
- 0 scans succeed → Full Path (ask everything). Show: "Could not detect your environment. Let me ask a few questions."
- 1-2 scans succeed → Standard Path with available data
- 3+ scans succeed → normal routing (Express/Standard/Full based on richness)
- **NEVER crash. NEVER show raw error messages.** If a scan throws, catch silently and set its output to the fallback value.

### Schema Versioning

`creator.yaml` includes a `schema_version` field. Current schema: **2**.

**Migration rules:**
- `/onboard update` or `/onboard` with existing `creator.yaml` → check `schema_version`
- If missing or < current → run silent migration:
  - Add new required fields with safe defaults
  - Never delete user data
  - Add `migrated_at` and `migrated_from` fields
  - Re-run Phase 1 scan to refresh `environment` section
- If current → proceed normally
- After migration, confirm: "Your profile was updated to schema v{N}. Anything to adjust?"

### Edge Case Matrix

| Scenario | What Happens | Expected Behavior |
|----------|-------------|-------------------|
| **Fresh install** | 0 skills, 0 projects, no CLAUDE.md, no git | Full Path. All defaults. Beginner. |
| **Corporate lockdown** | Git configured but no internet, restricted filesystem | Scan what's accessible, skip failures silently |
| **Multiple git identities** | Work email vs personal | Use global config. Don't ask about work/personal distinction |
| **Non-Latin names** | git name in CJK, Arabic, Cyrillic, etc. | Accept as-is. Name Intelligence only checks for handle patterns, not character sets |
| **Git name = email** | Some configs have email as name | Classify as `handle` (no spaces, has @ symbol) |
| **Empty git name** | `user.name` configured but empty string | Same as "no name found" |
| **Hundreds of skills** | 200+ skills installed | Scan still works (Glob returns all). Count correctly. Cap expertise inference at top 5 themes |
| **Corrupted settings.json** | Malformed JSON | Catch parse error, set `mcp_servers_count = 0` |
| **Disk permissions** | Can't read .claude/ dir | Catch permission error, treat as "no .claude/" |
| **Re-onboarding** | Running /onboard when creator.yaml already exists | Activation Protocol handles this → UPDATE MODE |
| **Concurrent sessions** | Two Claude sessions running /onboard | Write is atomic (single file). Last write wins. No locking needed |
| **Locale gibberish** | Locale returns invalid/empty string | Fallback to `"en"` |
| **WSL accessing Windows .claude/** | Paths cross filesystem boundaries | Resolve `{home}` within the native filesystem only. Don't cross WSL/Windows boundary |

### i18n Strategy

Question language detection priority:
1. Explicit language from CLAUDE.md content analysis (if clearly written in a specific language)
2. System locale
3. Fallback: English

**Supported question languages:**
- `en` — English (default)
- `pt-BR` — Portugues brasileiro
- `es` — Espanol
- `fr` — Francais
- `de` — Deutsch
- `ja` — Japanese
- `zh` — Chinese (Simplified)
- `ko` — Korean

For unsupported locales, use English. NEVER mix languages within a single AskUserQuestion call. All AskUserQuestion text MUST be in the detected language.

---

## Phase 1 — Silent Deep Scan (NO user interaction)

Run ALL scans in parallel:

**Scan 1: Git Identity + Name Intelligence**
```bash
git config --global user.name
git config --global user.email
```

**Name Classification Logic (mandatory — apply before Phase 2):**
1. If `user.email` matches `{N}+{handle}@users.noreply.github.com` → `github_handle = {handle}`, `email_type = noreply`
2. If `user.name` contains a space → `name_type = real_name` (e.g., "Jane Smith")
3. If `user.name` is single-word, lowercase, alphanumeric/hyphens only → `name_type = handle`
4. If standard email (not noreply), parse local part: `jane.smith@` → candidate "Jane Smith"

**Outputs:**
- `git_name`: raw value from `git config user.name`
- `git_handle`: extracted GitHub handle (from noreply email or handle-like name)
- `name_type`: `real_name` | `handle` | `ambiguous`
- `name_confidence`: `high` (real name with spaces) | `medium` (email-derived) | `low` (handle only)

**RULE:** When `name_type = handle`, Phase 3 MUST offer an explicit option to enter a display name. Do NOT silently use a handle as `creator.name`.

**Scan 2: User's .claude/ Root Directory**

Resolve the home directory cross-platform:
- Unix/macOS: `~/.claude/`
- Windows: `$USERPROFILE/.claude/` or `C:\Users\{user}\.claude\`

```
Glob: {home}/.claude/skills/**/*.md
Glob: {home}/.claude/rules/*.md
Read: {home}/.claude/CLAUDE.md (if exists — FIRST 80 LINES ONLY to detect language/style)
Read: {home}/.claude/settings.json (if exists — parse MCP server count from mcpServers keys)
Read: {home}/.claude/settings.local.json (if exists — may contain additional mcpServers)
Glob: {home}/.claude/projects/*/settings.json → scan each for mcpServers keys
Grep: "mcp__" in permissions.allow arrays → secondary MCP signal
```

Analysis:
- **Skills count + names** → infers technical_level and expertise topics
- **Rules files count** → infers governance sophistication
- **CLAUDE.md first 80 lines** → infers language, cognitive style
- **MCP servers (aggregated)** → Count unique server names across global settings, local settings, and all project settings. Add servers found via `mcp__*` permission patterns. Deduplicate by name. This is the `mcp_servers_count`.

**Scan 3: Project Breadth**
```
Glob: {home}/.claude/projects/*/memory/MEMORY.md
```
→ Number of active projects

**Scan 4: Engine Workspace**
```
Glob: workspace/*/.meta.yaml
```
→ Existing products, types and statuses

**Scan 5: Language Detection**
```bash
# Cross-platform locale detection
# Unix: echo $LANG
# Windows: powershell -c "[System.Globalization.CultureInfo]::CurrentCulture.Name"
```
→ Combined with CLAUDE.md language patterns for best guess

---

## Phase 2 — Inference Engine

Build a **draft profile** with confidence levels:

| Field | Inference Rule | Fallback if empty |
|-------|---------------|-------------------|
| `name` | git config user.name IF `name_type = real_name`. If `name_type = handle` → use handle as `git_handle` but leave `name` blank → must ask for display name | Leave blank → must ask |
| `language` | Locale + CLAUDE.md content language | `"en"` |
| `technical_level` | See matrix below | `"intermediate"` (safe middle) |
| `profile.type` | See classification rules below | `"hybrid"` |
| `expertise` | Skill names + topics from CLAUDE.md | Leave empty → must ask |
| `goals` | Cannot infer reliably | Must ask |

**Technical Level — Weighted Signal Scoring:**

| Signal | Weight | Scoring |
|--------|--------|---------|
| Skills count | **3x** | 0 skills: 0pt, 1-5: 3pt, 6-15: 6pt, 15+: 9pt |
| CLAUDE.md sophistication | **3x** | none: 0pt, basic: 3pt, custom: 6pt, cognitive framework: 9pt |
| Active projects | **2x** | 0-1: 0pt, 2-3: 2pt, 4-8: 4pt, 8+: 6pt |
| MCP servers | **1x** | 0: 0pt, 1-2: 1pt, 3+: 3pt |
| Rules files | **1x** | 0: 0pt, 1-2: 1pt, 3+: 3pt |

**Level thresholds:** 0-3 → beginner, 4-10 → intermediate, 11-18 → advanced, 19+ → expert

**Profile Type Classification:**
- Skill names contain code/dev/api/cli patterns → `developer`
- Skill names contain prompt/agent/cognitive patterns → `prompt-engineer`
- Skill names contain domain-specific terms (finance, legal, health) → `domain-expert`
- Skill names contain marketing/sales/copy/funnel patterns → `marketer`
- CLAUDE.md references team/process/orchestration → `operator`
- Mixed signals across 2+ types → `hybrid`

**Default Preference Inference (store as `recommended_default`):**
- `technical_level = expert` AND (skills >= 15 OR CLAUDE.md = cognitive framework) → **Premium creator**
- `technical_level = intermediate/advanced` with no strong monetization signals → **Standard defaults**
- Skill names predominantly open-source patterns OR CLAUDE.md references community contributions → **Open source focused**
- Else → **Standard defaults**

**Confidence Assessment:**
- **Rich scan** (≥3 signals detected with data): name found (any type), skills ≥ 1, CLAUDE.md exists → Express Path
- **Sparse scan** (1-2 signals): some data missing → Standard Path
- **Empty scan** (0 signals): fresh install, nothing found → Full Path

---

## Phase 2.5 — Machine vs. User Disambiguation

If `technical_score >= 19` (expert) AND the scan was Express/Standard path → add ONE disambiguation question to Call 1:

```
Question: "Is this your first time using the Creator Engine?"
  header: "Experience"
  Options:
  - "Yes — first time" → override technical_level to "beginner", profile.type to "domain-expert", route through Full Path questions
  - "No — I've used it before" → keep inferred profile, proceed normally
```

---

## Phase 3 — Adaptive Questioning

### EXPRESS PATH (Rich scan — max 2 AskUserQuestion calls)

**CRITICAL ARCHITECTURE RULE:** Never mix `preview` questions with `multiSelect` questions in the same AskUserQuestion call. This causes answer loss — the preview layout conflicts with multiSelect rendering, and single-select answers may be silently dropped.

**Step 1 — Display profile inline (text output, NOT a question):**

```
Scan completo. Perfil inferido:

  Nome:       {display_name or git_handle}
  Linguagem:  {detected_lang}
  Level:      {inferred_level} ({N} skills, {N} projetos, {claude_md_type} CLAUDE.md)
  Tipo:       {inferred_type}
  Expertise:  {area_1}, {area_2}, {area_3}
```

**Step 2 — Call 1: Confirm + Name (if handle detected)**

If `name_type = handle`:
```
Question 1: "Detectei o handle '{git_handle}'. Que nome usar no perfil?"
  header: "Nome"
  Options:
  - "Usar '{git_handle}'" (Recommended)
  - "Usar outro nome"
    description: "Digite via 'Other'"

Question 2: "O perfil acima está correto?"
  header: "Perfil"
  Options:
  - "Tudo certo" (Recommended)
    description: "Salvar o perfil como mostrado"
  - "Preciso ajustar algumas coisas"
    description: "Vou perguntar o que corrigir"
  - "Começar do zero"
    description: "Ignorar scan, onboarding completo"
```

If `name_type = real_name`: skip Q1, show only Q2 (profile confirm).

**Step 3 — Call 2: Goals + Defaults + Workflow (separate call, safe mixing)**

```
Question 1: "O que você quer construir com o MyClaude?"
  header: "Goals"
  multiSelect: true
  Options:
  - "Vender produtos para renda"
  - "Compartilhar ferramentas grátis"
  - "Construir portfólio de expertise"
  - "Automatizar meus workflows"

Question 2: "Defaults para seus produtos?"
  header: "Defaults"
  Options (order determined by recommended_default):
  - "{recommended_default} (Recommended)"
  - "{second_option}"
  - "{third_option}"
  - "Custom — escolher cada um"
    description: "Perguntar license, category, quality e pricing separadamente"

Question 3: "Estilo de workflow preferido?"
  header: "Workflow"
  Options:
  - "Guiado — confirmar antes de cada acao principal (Recommended para novos criadores)"
    description: "Mais seguro, mais contexto"
  - "Autonomo — pular confirmacoes, mover rapido"
    description: "Para criadores experientes. Seta gates profile em config.yaml"
```

Store answer as `preferences.workflow_style: "guided" | "autonomous"`. If autonomous selected, note: "Workflow autonomo ativo. Confirmacoes desabilitadas — /onboard update para mudar."

**Flow control:**
- Confirm = "Tudo certo" → use all inferred data + Call 2 answers → generate creator.yaml
- Confirm = "Preciso ajustar" → ONE follow-up AskUserQuestion asking which fields to correct (max 3 total calls)
- Confirm = "Começar do zero" → switch to Full Path
- Defaults = "Custom" → ONE follow-up with 4 individual preference questions

---

### STANDARD PATH (Sparse scan — 2 AskUserQuestion calls)

**RULE:** Same as Express Path — never mix preview + multiSelect in one call. Use `recommended_default` from inference.

**Call 1 — Identity + Expertise + Level (2-3 questions, NO preview, NO multiSelect):**

```
Question 1 (if name_type = real_name): "Encontrei seu nome: '{git_name}'. Usar no perfil?"
  header: "Nome"
  Options:
  - "Sim, usar '{git_name}'" (Recommended)
  - "Usar outro nome"
    description: "Digite via 'Other'"

Question 1 (if name_type = handle): "Detectei o handle '{git_handle}'. Que nome usar no perfil?"
  header: "Nome"
  Options:
  - "Usar '{git_handle}' como nome"
  - "Usar outro nome"
    description: "Digite seu nome real via 'Other'"

Question 1 (if no name found): "Que nome usar no perfil de criador?"
  header: "Nome"
  Options:
  - "Usar meu username do OS: {os_user}"
  - "Usar outro nome"
    description: "Digite via 'Other'"

Question 2: "Sua principal area de expertise?"
  header: "Expertise"
  Options (populated from any scan hints, or generic):
  - "{hint_from_skills_or_claude_md}" (if available)
  - "Desenvolvimento de software"
  - "Prompt engineering & IA"
  - "Expertise de dominio (negocios, ciencia, etc.)"

Question 3: "Como descreveria sua experiencia com Claude Code?"
  header: "Level"
  Options:
  - "{inferred_level}" (Recommended — description: "Baseado em {N} skills e seu setup")
  - "Iniciante — comecando agora"
  - "Intermediario — uso regularmente"
  - "Avancado/Expert — construo sistemas complexos"
```

**Call 2 — Goals + Defaults + Workflow (3 questions, multiSelect allowed, NO preview):**

Same structure as Express Path Call 2 — Goals (multiSelect) + Defaults (single-select with `recommended_default` logic, no preview) + Workflow style (single-select, no preview).

---

### FULL PATH (Empty scan — 3 AskUserQuestion calls)

**RULE:** Same as Express Path — never mix preview + multiSelect in one call. All text in detected language (fallback: locale or `en`).

**Call 1 — Identity (2 questions, NO multiSelect, NO preview):**

```
Question 1: "Bem-vindo ao MyClaude Creator Engine! Que nome usar no seu perfil?"
  header: "Nome"
  Options:
  - "Usar meu username do OS: {os_user}"
  - "Usar outro nome"

Question 2: "Que idioma devo usar?"
  header: "Idioma"
  Options:
  - "{locale_based}" (Recommended)
  - "English"
  - "Portugues (BR)"
  - "Espanol"
```

**Call 2 — Expertise + Level (2 questions, NO multiSelect, NO preview):**

```
Question 1: "Sua principal area de expertise?"
  header: "Expertise"
  Options:
  - "Desenvolvimento de software"
  - "Prompt engineering & IA"
  - "Expertise de dominio (negocios, financas, legal, etc.)"
  - "Marketing & growth"

Question 2: "Como descreveria sua experiencia com Claude Code?"
  header: "Level"
  Options:
  - "Iniciante — novo no Claude Code"
  - "Intermediario — uso regularmente" (Recommended)
  - "Avancado — construo skills e agents"
  - "Expert — arquiteto sistemas complexos"
```

**Call 3 — Goals + Defaults + Workflow (3 questions, multiSelect + single-select, NO preview):**

```
Question 1: "O que voce quer construir com o MyClaude?"
  header: "Goals"
  multiSelect: true
  Options:
  - "Vender produtos para renda"
  - "Compartilhar ferramentas gratis"
  - "Construir portfolio de expertise"
  - "Automatizar meus workflows"

Question 2: "Defaults para seus produtos?"
  header: "Defaults"
  Options:
  - "Standard defaults (Recommended)"
    description: "MIT, skills, MCS-2, free"
  - "Premium creator"
    description: "Proprietario, agents, MCS-3, premium"
  - "Open source focused"
    description: "MIT, skills, MCS-2, free"
  - "Custom — escolher cada um"
    description: "Perguntar cada preferencia separadamente"

Question 3: "Estilo de workflow preferido?"
  header: "Workflow"
  Options:
  - "Guiado — confirmar antes de cada acao principal (Recommended)"
    description: "Mais seguro, mais contexto"
  - "Autonomo — pular confirmacoes, mover rapido"
    description: "Para criadores experientes. Seta gates profile em config.yaml"
```

---

## Phase 4 — Profile Type Classification

Infer from ALL collected data (scan + answers). Do NOT ask directly.

| Signals | → Type |
|---------|--------|
| Code/dev expertise + build tools goal | `developer` |
| Domain knowledge + systematize/monetize goal | `domain-expert` |
| Marketing/sales expertise + income goal | `marketer` |
| Prompt/AI expertise + framework building | `prompt-engineer` |
| Team/process focus + orchestration | `operator` |
| Client delivery + batch operations | `agency` |
| 2+ types equally present | `hybrid` |

---

## Phase 5 — Generate creator.yaml

Write file to project root:

```yaml
# Auto-generated by /onboard — do not edit manually
# Update via: /onboard update
schema_version: 2

creator:
  name: "{name}"
  myclaude_username: "{@username or null}"
  git_handle: "{handle or null}"
  language: "{detected language code}"
  onboarded_at: "{YYYY-MM-DD}"
  platform: "{macOS|Linux|Windows|WSL|Docker|unknown}"

  profile:
    type: "{developer|prompt-engineer|domain-expert|marketer|operator|agency|hybrid}"
    expertise:
      - "{domain 1}"
      - "{domain 2}"
    technical_level: "{beginner|intermediate|advanced|expert}"
    technical_score: {0-30}  # weighted sum from Phase 2
    goals:
      - "{goal 1}"
      - "{goal 2}"

  preferences:
    default_license: "{license}"
    default_category: "{category}"
    pricing_strategy: "{free|freemium|premium}"
    quality_target: "{MCS-1|MCS-2|MCS-3}"
    workflow_style: "{guided|autonomous}"
    token_efficiency: "{eco|balanced|unlimited}"

  environment:
    detected_skills_count: {N}
    detected_rules_count: {N}
    has_global_claude_md: {true|false}
    mcp_servers_count: {N}
    active_projects_count: {N}
    scan_failures: []  # list of scan names that failed, empty = all succeeded
    scan_path: "{express|standard|full}"

  inventory:
    local_skills: {count from scan}
    local_agents: {count from scan}
    published_products: 0
    unpublished_drafts: {count from scan}

  recommendations:
    suggested_categories: ["{category 1}", "{category 2}"]
    market_gaps_matched: []
```

**Schema v2 fields (added):**
- `schema_version` — top level, enables migration
- `git_handle` — separated from name; null if name is real name
- `platform` — detected OS for downstream adaptation
- `technical_score` — raw numeric score from weighted inference
- `scan_failures` — observability: which scans failed. Empty = clean run
- `scan_path` — which onboarding path was taken

---

## Phase 6 — Persona-Adaptive Closing

Output (concise, in creator's detected language):

```
Profile saved!

  {name} | {type} | {technical_level} | {language}
  Environment: {N} skills, {N} rules, {N} projects

  Recommended next: {persona_recommendation}

Next steps:
  /create [type]     Start building a product (skill, agent, squad, system...)
  /map [domain]      Extract domain knowledge first (recommended for complex products)
  /import [slug]     Bring an existing skill into the pipeline
  /help              See all available commands

Tip: Your products follow 10 platform principles extracted from Claude Code's architecture.
     Run /help and ask for "platform principles" to learn more.
```

| Profile Type | Recommendation |
|---|---|
| `developer` | `/create skill` — build a tool around your code expertise |
| `domain-expert` | `/create minds` — turn your expertise into an advisory mind |
| `marketer` | `/map` then `/create` — find gaps that match your audience |
| `prompt-engineer` | `/create agent` — start with what you know best |
| `operator` | `/create workflow` — automate your team processes |
| `agency` | `/create system` — build client delivery frameworks |
| `hybrid` | `/create system` — combine your skills into a product |

---

## Phase 6b — Setup Intelligence Report (IMMEDIATE VALUE)

After saving creator.yaml, deliver a Setup Intelligence Report. **CRITICAL:** Entire Phase 6b must complete in <5 seconds. Do NOT make multiple CLI calls. Do NOT read more than 200 lines of any file. Do NOT trigger additional AskUserQuestion calls — OUTPUT ONLY.

Read the creator's `{home}/.claude/CLAUDE.md` (first 200 lines only).

**1. Setup Health Check:**

```
Setup Health:
  CLAUDE.md size:    {N} chars {optimal | consider @include}
  Rule scoping:      {N}/{total} rules have path scoping {efficient | always-loaded}
  Security hooks:    {present | none — consider adding safety hooks}
  MCP overhead:      {N} servers {manageable | review unused}
```

- CLAUDE.md >4K chars → "Your CLAUDE.md is {N} chars. Consider using @include to move detail into separate files."
- Rules without `paths:` frontmatter → "You have {N} rule files that load on EVERY turn. Adding `paths:` frontmatter scopes them — zero cost when working on unrelated files."
- No PreToolUse hooks in settings → "Your setup has no safety hooks. The ecosystem has documented 1,184+ malicious skills. Consider adding a PreToolUse hook."
- mcp_servers_count > 5 → "You have {N} MCP servers configured. Each adds context overhead. Verify you're actively using all of them."

**2. Marketplace Recommendations (if CLI available):**

Run `myclaude search --category {inferred_expertise_category} --json 2>/dev/null` silently. If results found, show top 3 FREE products. If CLI unavailable, skip silently. NEVER block onboarding for marketplace.

**3. Quick Wins:**

- `has_global_claude_md = false` → "You don't have a global ~/.claude/CLAUDE.md. Even a minimal one improves Claude Code's output everywhere."
- `detected_skills_count = 0` → "You have no skills installed yet. Browse: /explore trending"
- `detected_rules_count > 5 AND no path scoping` → "You have {N} rules all loading every turn. Path scoping could reduce your token cost by 60-80%. Want me to analyze which rules should be scoped?"

**4. Gap Analysis:**

Categorize installed skills by domain theme (scan skill names + frontmatter descriptions):

```
Your skill coverage:
  {theme_1}: {N} skills
  {theme_2}: {N} skills
  Uncovered domains from your expertise: {gaps}
```

Compare installed skill themes against `creator.profile.expertise`. If any expertise domain has 0 installed skills → "Gap: You list '{domain}' as expertise but have no tools for it. This is a BUILD opportunity."

**5. Product Recommendations:**

```
Recommended first product:
  Type: {inferred_type} — "{one-liner explaining why}"
  Domain: {highest_gap_domain}
  
  Quick start: /scout "{domain}" → /create {type}
```

Logic:
- `profile.type = domain-expert` AND gaps exist → recommend `minds` in the gap domain
- `profile.type = developer` AND gaps exist → recommend `skill` in the gap domain
- `profile.type = prompt-engineer` → recommend `agent`
- No gaps AND marketplace data available → recommend the category with lowest marketplace competition
- `pricing_strategy = premium` → append: "Target MCS-3 for premium pricing. Run `/scout` first."

**6. Scout Suggestion (if gap analysis found opportunities):**

If gap analysis identified 1+ build opportunities AND no scout reports exist in workspace/:

```
Want to research "{highest_gap_domain}" before building?
  /scout "{domain}" — tests Claude's baseline, finds gaps, recommends products
  
This takes ~2 minutes and produces a detailed intelligence report.
```

**Tone:** This is a CONSULTATION, not a lecture. "Here's what I noticed about your setup" not "You should fix these problems."

---

## Phase 6c — CLI Integration (if myclaude available)

1. **Auth check:** `myclaude whoami 2>/dev/null`
   - Authenticated → pre-populate `creator.myclaude_username`. Display: "Marketplace: @{username} (authenticated)"
   - Not authenticated → "Marketplace: Run `myclaude login` to connect (optional — needed for /publish)"

2. **Profile sync:** If authenticated AND creator.yaml saved → "Sync your profile to the marketplace? Run: `myclaude profile sync`"

3. **Stripe status:** `myclaude stripe status 2>/dev/null`
   - Connected → "Payments: Stripe connected (ready for paid products)"
   - Not connected AND pricing_strategy != "free" → "Payments: Run `myclaude stripe connect` to enable paid products"
   - pricing_strategy == "free" → skip silently

4. **MCP setup:** `myclaude setup-mcp 2>/dev/null`
   - Not configured → "Pro tip: Run `myclaude setup-mcp` to let Claude Code search and install products directly from conversations."
   - Already configured → skip silently

All NON-BLOCKING suggestions. The creator can skip any and continue.

---

## UPDATE MODE FLOW

Load existing `creator.yaml`. Re-run Phase 1 scan silently. Show diff between stored `environment` and current scan.

**Single AskUserQuestion call:**

```
Question 1: "Your profile was created on {onboarded_at}. What needs updating?"
  header: "Update"
  multiSelect: true
  Options:
  - "Expertise domains"
  - "Goals"
  - "Preferences (license, category, quality, pricing)"
  - "Re-detect everything from environment"
```

If "Re-detect everything" selected → re-run inference, show Express Path Q1 for confirmation.
Otherwise → one follow-up AskUserQuestion per selected section.
Always: update `environment` + `inventory` from fresh scan. Add `updated_at` field.

---

## Decision Notes

**Why AskUserQuestion mandatory:** Clickable UI reduces cognitive load and time from ~3 minutes to ~30-60 seconds. No typing required on the happy path.

**Why adaptive paths:** A power user with 20+ skills shouldn't endure the same flow as a fresh install. The scan richness determines the path — respect the creator's time proportionally to what we already know.

**Why NEVER mix preview + multiSelect in one call:** Discovered in production (2026-03-29): when a single AskUserQuestion call contains both preview-enabled single-select questions AND multiSelect questions, the single-select answer is silently dropped. Root cause: the AskUserQuestion UI switches to side-by-side preview layout for any question with preview, which conflicts with multiSelect rendering. Fix: show profile inline as text output, then use AskUserQuestion for non-preview confirmation.

**Why profile shown as text output, not preview widget:** Previews are for comparing options side-by-side. A profile confirmation is a yes/no — inline text is faster to scan and doesn't trigger the preview layout mode.

**Why intelligent default recommendation:** Recommending "Standard defaults (MIT/free)" to a user with 60+ skills and a cognitive framework CLAUDE.md is patronizing and wrong. Expert environment → Premium recommended.

**Why name intelligence matters:** GitHub noreply emails (`{N}+{handle}@users.noreply.github.com`) are the most common git identity for privacy-conscious developers. `git config user.name` often contains the handle, not a real name. Publishing as "jsmith-dev42" when the creator's name is "Jane Smith" degrades professional appearance.

**Why weighted scoring over rigid matrix:** Skills count and CLAUDE.md sophistication are 3x stronger signals than rules or MCP servers. A user with 61 skills and a cognitive framework is expert regardless of MCP count.

**Why bundled defaults:** 80% of creators will use MIT/skills/MCS-2/free. Offering "Standard defaults" as one click respects that. Only "Custom" expands to individual choices.

**Why scan before asking:** A creator with 20+ skills and a cognitive-framework CLAUDE.md is clearly an expert. Asking "what's your technical level?" wastes their time and feels patronizing.

**Why not ask profile type directly:** Self-classification is unreliable. Behavior + environment signals are more accurate.

**Why environment section in creator.yaml:** Downstream skills adapt to actual tooling ecosystem, not just self-reported level.

**Why cross-platform paths:** The Engine runs on Windows, macOS, and Linux. All file scans must resolve `{home}` dynamically. Never hardcode `~/` without a Windows fallback.

**Why MCP scan must be aggregated:** MCP servers can be configured in global settings, local settings, and per-project settings. A scan that only checks `{home}/.claude/settings.json` misses project-level MCP servers. Aggregate all sources, deduplicate by name.
