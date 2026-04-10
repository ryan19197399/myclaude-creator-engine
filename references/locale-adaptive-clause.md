# Locale-Adaptive Clause — Runtime Contract for Forged Products

**Layer:** Canonical substrate. Consumed by `.claude/skills/create/` during scaffold — the 7 primary-file templates each carry a `{{LOCALE_ADAPTIVE_CLAUSE}}` placeholder that `/create` substitutes with the block from §2 plus the localized header from §3. Validated by `scripts/codex-drift-check.py` via marker-grep rule. Declared by every certified codex via `intent_topology.locale_adaptive_clause_required: true`.

**Rationale.** The Engine's marketplace is global: a product forged in PT-BR must be installable by a French user without retranslation of files. Three architectural options were weighed (DNA pattern / config injection / template inline); template inline was chosen because it honors constitutional Clause VIII (Every Token Earns Its Place, no schema re-inflation of the structural-dna.md baseline) while keeping the clause auditable per-product.

---

## §1 — Why This Exists

Every product forged by the Engine is born in the creator's native language. The SKILL.md, AGENT.md, SQUAD.md, SYSTEM.md, OUTPUT-STYLE.md — every primary file, every reference, every anti-pattern, every example — carries the linguistic fingerprint of the creator. A Brazilian creator writing a squad about investment analysis will write activation triggers, anti-patterns, and coaching in PT-BR. A French user installing that squad would, absent any contract, receive a literal PT-BR experience.

This is a betrayal of the Engine's âmago. The Engine condenses intelligence for **people** — not for people who happen to share a language with the creator. Retranslation of files at install time is infrastructurally expensive, maintenance-hostile, and prone to quality loss. The cheaper and more elegant solution is a **runtime contract**: every forged product carries four lines of instruction telling Claude to mirror the invoker's language in user-facing output while preserving the source language in structural markers.

The contract is written in English because runtime instructions to Claude are most faithfully parsed in English — this is an empirical observation about the model, not a preference. A localized header comment, emitted by `/create` in the creator's native language, explains to the creator why the block below is in English and reassures that the end-user experience will always mirror the end user's language.

---

## §2 — The Canonical Clause

The clause below is the **single source of truth** for every forged product. `/create` copies this block verbatim into the activation protocol of every primary file (`SKILL.md`, `AGENT.md`, `SQUAD.md`, `SYSTEM.md`, `OUTPUT-STYLE.md`) during scaffold. The marker lines (`<<< LOCALE-ADAPTIVE CLAUSE ... >>>` and `<<< END CLAUSE >>>`) are load-bearing: `scripts/codex-drift-check.py` greps for them to validate every forged product carries the contract.

```markdown
<!-- {localized_header} -->

<<< LOCALE-ADAPTIVE CLAUSE (runtime contract, do not edit) >>>

Detect the invoker's language from their first message or from the ambient
locale signal (CLAUDE.md locale, shell locale). Mirror that language in all
user-facing output — prose, questions, explanations, confirmations, error
messages. Preserve technical identifiers (file paths, command names, tool
names, variable names, code blocks, structural markers) in their original
form. If the invoker switches language mid-session, mirror the switch
immediately without acknowledging the change as a configuration event.
When the invoker's language is unclear, default to the source language
declared in the product's frontmatter `source_language:` field.

<<< END CLAUSE >>>
```

**Token cost:** ~90 tokens per forged product (the clause + markers). Injected once at scaffold, lives in the primary file, travels with the product to the marketplace, lives inside every invocation's context. The cost is constant per product and the benefit is global: one forge, any language.

---

## §3 — The Localized Header

The `{localized_header}` placeholder in the clause above is replaced by `/create` at scaffold time with a one-to-three line comment in `creator.yaml → creator.language`. The header explains to the creator (not to Claude, not to the end user) why the English block below exists and what it does.

**Examples of the localized header:**

- **`pt-BR`:**
  ```
  Esta cláusula abaixo está em inglês porque é uma instrução de runtime para o Claude
  (o modelo processa instruções estruturais com maior fidelidade em inglês). O output
  final para quem usar este produto será sempre na língua da pessoa que invocar.
  ```

- **`en`:**
  ```
  Runtime contract for Claude. Do not edit — the marker lines are load-bearing and
  validated by codex-drift-check. End-user output always mirrors the invoker's language.
  ```

- **`es`:**
  ```
  Esta cláusula está en inglés porque es una instrucción de runtime para Claude
  (el modelo procesa instrucciones estructurales con mayor fidelidad en inglés).
  El output final para quien use este producto será siempre en el idioma del invocador.
  ```

- **`fr`:**
  ```
  Cette clause est en anglais car c'est une instruction d'exécution pour Claude
  (le modèle traite les instructions structurelles avec plus de fidélité en anglais).
  La sortie finale pour l'utilisateur sera toujours dans la langue de l'invocateur.
  ```

- **Fallback (any language not in the catalog):**
  ```
  Runtime contract for Claude. The English text below tells Claude to mirror
  the invoker's language in all user-facing output.
  ```

`/create` looks up the creator's language in a small catalog inside `config.yaml → routing.common.locale_adaptive_clause.localized_header_catalog`. When the creator's language is absent from the catalog, the fallback header is used and an advisory note is emitted.

---

## §4 — Where the Clause Lives Inside Each Product Type

The clause is injected into the **activation protocol** section of each primary file. The position is specific per type:

| Type | Primary file | Insertion point |
|---|---|---|
| `skill` | `SKILL.md` | Immediately after the `## Activation Protocol` heading, before the numbered load sequence |
| `agent` | `AGENT.md` | Immediately after the `## Activation Protocol` heading, before the tool pool declaration |
| `squad` | `SQUAD.md` | Immediately after the `## Activation Protocol` heading; also propagated to every sub-agent file in `agents/` |
| `system` | `CLAUDE.md` | Immediately after the `## Activation Protocol` heading; also propagated to every sub-part (claude-md fragment, sub-agents, sub-squads) |
| `minds` (advisory) | `AGENT.md` | Immediately after the `## Activation Protocol` heading |
| `minds` (cognitive) | `AGENT.md` (L1 Boot) | Immediately after the `## Activation Protocol` heading; the clause itself is NOT injected into L2-L5 references — those are loaded on demand by L1, and L1's activation protocol governs them |
| `output-style` | `OUTPUT-STYLE.md` | Immediately after the `## Voice Rules` heading (output styles do not have activation protocols in the same sense; the clause governs the voice of the style itself) |

For each type above, `/create` uses a template-aware injection: the template file contains a `{{LOCALE_ADAPTIVE_CLAUSE}}` placeholder that `/create` substitutes with the block from §2 plus the localized header from §3. This keeps the templates minimal (one placeholder line) while making the inserted content canonical.

---

## §5 — Drift-Check Marker Rule

`scripts/codex-drift-check.py` validates the presence of the clause in every forged product by grepping for the open and close markers:

```
<<< LOCALE-ADAPTIVE CLAUSE (runtime contract, do not edit) >>>
<<< END CLAUSE >>>
```

The rule fires under these conditions:

- **Target files**: every `workspace/*/SKILL.md`, `workspace/*/AGENT.md`, `workspace/*/SQUAD.md`, `workspace/*/CLAUDE.md` (system primary), `workspace/*/OUTPUT-STYLE.md`, and every file in `workspace/*/agents/*.md` (squad sub-agents) and `workspace/*/sub-parts/` (system sub-parts).
- **Expected**: both markers present, open marker on a line before close marker, at least 3 lines of content between them (to prevent empty-marker cheating).
- **Severity**: `warning` — advisory while legacy workspace products complete the template substitution migration. Planned promotion to `error` once the migration is verified across the full legacy population (tracked as D19).

The marker-grep is the cheapest possible validation: no YAML parse, no semantic interpretation, just two grep calls per file. It runs in O(lines) per file and is robust to any content between the markers.

---

## §6 — Relationship to `vault.yaml` and the Marketplace

The clause alone makes a product runtime-adaptive. The `vault.yaml` manifest declares the **source language** explicitly so that the marketplace UI can display the product's origin honestly:

```yaml
# vault.yaml excerpt — locale-adaptive fields
source_language: pt-BR
locale_adaptive: true
locale_adaptive_source: references/locale-adaptive-clause.md
locale_adaptive_version: "1.0"
```

The marketplace UI reads these fields and renders a badge on the product card:

> **Source: Portuguese · Adapts to your language at runtime**

The buyer sees the honesty (this product was forged in Portuguese) and the capability (it will speak your language). They install without translation ceremony. The clause runs. The product speaks back in the buyer's language. The forge cost was paid once, in one language; the benefit is collected globally, across all languages Claude speaks.

---

## §7 — What This Clause Does NOT Do

Explicit non-goals, because over-promising is worse than under-delivering:

- **It does not retranslate file content.** The anti-patterns, examples, and coaching strings inside the product stay in the source language. What translates is the user-facing output Claude generates while using the product.
- **It does not translate technical identifiers.** Tool names, file paths, variable names, command syntax, and code blocks stay in their original form because changing them would break execution.
- **It does not auto-detect language with 100% accuracy.** If the invoker's language is unclear from the first message, the clause falls back to the source language declared in frontmatter. The creator can always ask explicitly to switch.
- **It does not compensate for poor source content.** A badly written product in Portuguese is still badly written when adapted to French. The clause is a multiplication factor, not an addition: garbage in, garbage out, but in the user's language.
- **It does not eliminate the value of a dedicated translation.** A creator who wants a pure French-native experience can still fork their product and manually translate file content. The clause is the 80% solution that costs 4 lines and zero maintenance.

---

## §8 — Consumer Wiring Status

Each consumer is described by its current runtime state, not by the wave that produced it.

- **Reference file existence**: live. This document is the single source of truth.
- **Template injection**: live. Each of the 7 primary-file templates (`skill`, `skill/cognitive`, `agent`, `squad`, `system`, `minds`, `output-style`) carries a `{{LOCALE_ADAPTIVE_CLAUSE}}` placeholder that `/create` substitutes at scaffold time with the block from §2 plus the localized header from §3.
- **Drift-check marker rule**: live. `scripts/codex-drift-check.py` greps every forged product's primary file for the open/close markers under check (9) "locale-adaptive clause marker presence". Current severity: `warning`, pending migration completion — see D19.
- **Onboard confirmation gate**: live. `/onboard` Phase 2.5c classifies language detection as `high | low | fallback`, emits the appropriate confirmation, and persists `creator.yaml → creator.language_confidence` alongside `creator.language_detection_sources`. The gate is mandatory for creator profiles at schema v3.
- **vault.yaml source_language field**: live. `/package` Step 3 reads `.meta.yaml → intent_declaration.language` as the canonical source, with two-level fallback to `creator.yaml → creator.language` then to `"en"`. The four fields (`source_language`, `locale_adaptive`, `locale_adaptive_source`, `locale_adaptive_version`) are emitted into `vault.yaml` for every packaged product.
- **Marketplace badge rendering**: pending — this consumer lives in the `myclaude.sh` marketplace UI and is tracked as an upstream dependency outside the Engine repository.

---

*One contract. One forge. Any language Claude speaks.*
