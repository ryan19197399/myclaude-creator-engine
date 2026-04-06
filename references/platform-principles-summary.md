# 10 RULES — How Anthropic's Own Code Teaches You to Build Better Products
## Executive Summary of the Context Engineering Codex
**For:** MyClaude Creators | **From:** Codex v1.1 (198 analysis points distilled)

---

These 10 rules are extracted from Anthropic's own Claude Code source code. They're not opinions — they're how the system actually works internally. Products that align with these rules perform better because they work WITH the platform, not against it.

---

### 1. PUT YOUR MOST IMPORTANT RULES LAST
Claude pays more attention to content at the END of a file. Structure your product: generic context first, critical rules last. This isn't a style choice — it's how transformer attention works.

### 2. SCOPE YOUR RULES TO SPECIFIC FILES
If your claude-md product only applies to Python files, add `paths:` to your frontmatter (e.g., `paths: ["*.py"]` or as a YAML list). When the user edits JavaScript, your product costs ZERO tokens. Without paths, it loads every single turn regardless.

### 3. WRITE DIRECTIVES, NOT SUGGESTIONS
Claude Code wraps your rules file with "These instructions OVERRIDE any default behavior." Your product isn't a suggestion — it's law. Write "Always use snake_case" not "Consider using snake_case."

### 4. CLAUDE-MD PRODUCTS ARE EXPENSIVE — EVERY CHARACTER COUNTS
Your claude-md product is in context EVERY turn. A skill is only loaded when invoked. This means: a 1000-char rule costs ~250 tokens × every turn × every session. Keep claude-md products ruthlessly minimal. Move details to references/.

### 5. @INCLUDE HAS A DEPTH LIMIT OF 5
If your product uses @include chains deeper than 5 levels, files beyond level 5 are silently ignored — no error, no warning. Keep @include trees shallow.

### 6. HOOKS IN PROJECT SETTINGS CAN'T SET PERMISSIONS
If your hooks product targets `.claude/settings.json` (projectSettings), permission rules are SILENTLY IGNORED. Only `.claude/settings.local.json` (localSettings) can set permissions. This is a security feature, not a bug.

### 7. YOUR PRODUCT IS COMPILED ONCE PER SESSION
Claude Code loads your product at session start and caches it. Changes to your files take effect on the next session or after `/clear`. Design for this: don't depend on mid-session file changes being picked up.

### 8. THE MODEL KNOWS WHERE YOUR PRODUCT CAME FROM
Each instruction file is labeled: "(project instructions, checked into the codebase)" or "(user's private global instructions)". The model uses this to calibrate how seriously to take your rules. Project = team authority. User = personal preference.

### 9. ONLY TEXT FILES CAN BE @INCLUDED
@include works with .md, .yaml, .json, .ts, .py, and ~100 other text formats. Binary files (.pdf, .png, .zip) are silently ignored. If your @include points to a binary, it's as if the line doesn't exist.

### 10. ORGANIZE BY COGNITIVE FUNCTION, NOT BY TOPIC
Anthropic organizes their system prompt in functional layers: Identity → Knowledge → Execution → Constraints → Output. Products that mirror this structure work better because they align with how the model's own instructions are structured.

---

*These 10 rules are the distillation of 198 analysis points from the Context Engineering Codex.*
*Full matrix with source citations: `00-epistemic-matrix.md`*
*Complete principle reference: `01-anthropic-codex.md`*
