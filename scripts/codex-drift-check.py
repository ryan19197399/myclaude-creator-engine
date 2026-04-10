#!/usr/bin/env python3
"""
codex-drift-check.py — Product DNA codex validator

Validates every product-dna/*.yaml file against the canonical codex schema.
Enforces: (1) schema consistency across files, (2) enforced_by references
resolve, (3) consumer_status enum compliance, (4) lifecycle block universal
contract, (5) no orphan declarations, (6) invisibility grep, (7) mermaid
template variables declared, (8) intent topology enum membership,
(9) locale-adaptive clause marker presence on forged products,
(10) P8 substrate voice — no development vocabulary in the organism.

Usage:
    python scripts/codex-drift-check.py                    # default: 6 certified codices
    python scripts/codex-drift-check.py --all              # all product-dna/*.yaml (incl. un-certified)
    python scripts/codex-drift-check.py --certified-only   # explicit — same as default
    python scripts/codex-drift-check.py product-dna/skill.yaml
    python scripts/codex-drift-check.py --strict           # fail on any warning

Default scope:
    When no file arguments are given, the script scans the 6 certified codices
    (skill, agent, minds, output-style, squad, system). The 7 un-certified
    codices (application, bundle, claude-md, design-system, hooks, statusline,
    workflow) predate the universal contract and lack the required fields by
    design. Use --all to explicitly include them (opt-in, expects failures).

Exit codes:
    0 — all checks pass
    1 — errors detected
    2 — warnings detected with --strict
"""

import sys
import re
import argparse
from pathlib import Path
import yaml

# ---------------------------------------------------------------------------
# SCHEMA CONTRACTS — canonical definitions for codex consistency
# ---------------------------------------------------------------------------

# Valid consumer_status enum — lowercase-hyphen only
VALID_CONSUMER_STATUS = {
    "fully-wired",       # skill reads + consumes this field today
    "partial",           # skill reads product-dna but not this subfield
    "aspirational",      # no consumer today; future wave will wire
    "blocked",           # cannot wire until pre-existing Engine gap resolves
}

# Valid lifecycle skill names — MUST be present in every codex
REQUIRED_LIFECYCLE_SKILLS = [
    "map", "scout", "import", "create", "fill",
    "validate", "test", "package", "publish", "status",
]

# Lifecycle block universal contract — every lifecycle.{skill} MUST have these
REQUIRED_LIFECYCLE_BLOCK_FIELDS = {
    "role",                      # string
    "optional",                  # bool
    "inputs",                    # list (may be empty)
    "outputs",                   # list (may be empty)
    "blocks_when",               # list (may be empty)
    "consumer_status",           # enum
    "consumer_status_reason",    # string
    "next_action",               # string or null
}

# Top-level keys every codex MUST have (universal)
REQUIRED_TOP_LEVEL_KEYS = {
    "type", "primary_file", "install_target", "template",
    "essence", "architectural_principles", "operational_modes",
    "freedom_levels", "lifecycle", "flow", "failure_modes", "invariants",
    "security_profile", "marketplace_taxonomy", "dna_patterns",
    "mcs_expectations", "frontmatter", "template_files", "token_economics",
    "compact_instructions", "discovery_questions", "state_machine_hooks",
    "validation_pipeline_refs", "lifecycle_shared_refs",
    "schema_consumer_status",
}

# Architectural principles — the 9 canonical (from structural-dna.md)
REQUIRED_PRINCIPLES = {
    "P1_purpose_before_shape",
    "P2_constraint_before_feature",
    "P3_composition_over_monolith",
    "P4_contract_before_narrative",
    "P5_failure_mode_before_happy_path",
    "P6_state_at_the_edge",
    "P7_read_before_write",
    "P8_invisibility_of_mechanism",
    "P9_recursive_integrity",
}

# Each principle block MUST have these fields
REQUIRED_PRINCIPLE_FIELDS = {"specialization", "enforced_by", "blocks_forge_when"}

# marketplace_taxonomy universal contract
REQUIRED_MARKETPLACE_FIELDS = {
    "default_category", "default_price", "default_license",
    "natural_tags", "pricing_strategy", "pricing_rationale",
    "bundle_eligible", "bundle_eligible_reason",
    "composition_eligible_with", "composition_eligible_reason",
    "consumer_status", "consumer_status_reason",
}

# security_profile universal contract
REQUIRED_SECURITY_FIELDS = {
    "aegis_applicable", "reason", "attack_surfaces",
    "shell_execution", "file_io", "network_calls", "tool_invocation",
    "installation_trust_level", "installation_trust_reason",
    "consumer_status", "consumer_status_reason",
}

# Invisibility grep pattern — substrate names forbidden in user-facing strings
# NOTE: "MCS-1", "MCS-2", "MCS-3" are public marketplace brand, NOT substrate.
# Forbidden are substrate codes like MCS-001 (3 digits).
INVISIBILITY_PATTERN = re.compile(
    r"\b(ATHENA|Leonardo|kairo|SICA|UEMF|CNO|Bestiary|MICA|Mandamento|"
    r"Popper|Toulmin|Pearl|G\u00f6del|Saper Vedere|pantheon|genesis|"
    r"cognitive-refinery|mmos|obsidian|skill-architect|leonardo|"
    r"context-architect|SI-factory|MCS-\d{3,})\b"
)

# ---------------------------------------------------------------------------
# Intent topology enums + R0 regression pattern.
# Sources:
#   references/intent-topology.md §2 (6 × 4 × 3 enumeration)
#   config.yaml routing.common.intent_topology_enums (canonical projection)
# Every codex that declares intent_topology must use values from these enums.
# ---------------------------------------------------------------------------

INTENT_TOPOLOGY_ENUMS = {
    "delivery_mechanism": {
        "ambient_constitutional",
        "ambient_path_scoped",
        "invoked_slash_command",
        "invoked_task_spawn",
        "reflex_hook_binding",
        "composed_system",
    },
    "operational_nature": {
        "executor",
        "advisor",
        "orchestrator",
        "observer",
    },
    "cognitive_depth": {
        "procedural",
        "advisory",
        "cognitive",
    },
}

# Valid declaration modes for intent_topology blocks
INTENT_TOPOLOGY_DECLARATION_MODES = {"full", "derived"}

# R0 regression pattern — the internal session codename "IDFA" must NEVER
# appear in any creator-facing file. Enforced by Leonardo verdict R0 discipline.
# This pattern is case-insensitive and word-bounded.
R0_FORBIDDEN_PATTERN = re.compile(r"\bIDFA\b", re.IGNORECASE)

# Locale-adaptive clause markers. Every forged product in workspace/ must
# contain both markers in its primary file — /create injects them via template
# placeholder substitution. Severity is warning for legacy products that
# predate the template injection and error for post-instrumentation forges.
# Source: references/locale-adaptive-clause.md §5.
LOCALE_CLAUSE_MARKER_OPEN = "<<< LOCALE-ADAPTIVE CLAUSE (runtime contract, do not edit) >>>"
LOCALE_CLAUSE_MARKER_CLOSE = "<<< END CLAUSE >>>"

# Files in workspace/ where the locale clause must be present.
# Templates under templates/ are excluded because they carry the
# {{LOCALE_ADAPTIVE_CLAUSE}} placeholder, not the expanded clause.
LOCALE_CLAUSE_TARGET_GLOBS = [
    "workspace/*/SKILL.md",
    "workspace/*/AGENT.md",
    "workspace/*/SQUAD.md",
    "workspace/*/CLAUDE.md",
    "workspace/*/SYSTEM.md",
    "workspace/*/OUTPUT-STYLE.md",
    "workspace/*/agents/*.md",
]

# Certified codex scope — the 6 codices fully instrumented with the universal
# contract (principles, lifecycle blocks, security profile, marketplace
# taxonomy, intent topology, locale-adaptive clause). Running drift-check
# against any other codex produces false-alarm errors because those codices
# lack the required fields by design. Default scope is these six; --all opts
# in to the full 13-codex scan.
CERTIFIED_CODICES = [
    "product-dna/skill.yaml",
    "product-dna/agent.yaml",
    "product-dna/minds.yaml",
    "product-dna/output-style.yaml",
    "product-dna/squad.yaml",
    "product-dna/system.yaml",
]

# Files to grep for R0 regression. These are the creator-facing surfaces
# where a substrate codename leak would break the invisibility contract.
R0_GREP_TARGETS = [
    "CLAUDE.md",
    "structural-dna.md",
    "config.yaml",
    "quality-gates.yaml",
    "references/*.md",
    "references/structural-dna/*.md",
    "product-dna/*.yaml",
    ".claude/skills/*/SKILL.md",
    ".claude/skills/*/references/*.md",
]

# ---------------------------------------------------------------------------
# P8 substrate voice — operational rule
# ---------------------------------------------------------------------------
# The operational substrate (everything that ships to users) speaks in the
# present tense about the present system. Development vocabulary — wave IDs,
# meta-learning codes, invariant numbers, epistemic framework names — belongs
# in history documents (handoffs, MEMORY notes), never in the artifact itself.
#
# This rule greps the operational scope for that vocabulary and emits a
# warning per match. History documents under docs/handoffs/, .claude/MEMORY.md,
# and CLI-owned auto-generated rules files are exempt because they are not
# part of the organism — they are the audit trail that sits alongside it.
#
# A line belongs in the organism only if a reader with no access to any
# handoff understands it and can act on it.

P8_SUBSTRATE_VOICE_PATTERN = re.compile(
    r"(\bWave \d+(?:\.\d+)?(?:[a-z]\.\d+)?\b"
    r"|\bML-\d+\b"
    r"|\bINV-\d+\b"
    r"|\bMeadows\b"
    r"|\bKairo\b)"
)

# Scope: the operational organism — files that ship or govern what ships.
# Templates are included because they generate workspace forges: any drift
# that lands in a template propagates into every future forge. The rules
# file engine-governance.md is ambient context read by the harness every
# turn; CLI-owned myclaude-*.md files in the same directory are exempt via
# the prefix list below, so a file-level entry (not a directory glob) is
# the correct shape here.
P8_SUBSTRATE_VOICE_TARGETS = [
    "CLAUDE.md",
    "structural-dna.md",
    "config.yaml",
    "quality-gates.yaml",
    "references/**/*.md",
    ".claude/skills/**/*.md",
    ".claude/rules/engine-governance.md",
    "templates/**/*.md.template",
    "scripts/*.py",
    "product-dna/squad.yaml",
]

# Exemptions: history documents, CLI-owned files, creator workspace, and
# this script itself — the rule's own token list has to live somewhere and
# self-matching would be noise. The exemption is narrow and audited by code
# review alone.
P8_SUBSTRATE_VOICE_EXEMPT_PREFIXES = (
    "docs/handoffs/",
    "docs/beta/",
    "docs/consolidated/",
    "docs/extracts/",
    ".claude/MEMORY.md",
    ".claude/rules/myclaude-products.md",
    ".claude/rules/myclaude-status.md",
    "workspace/",
    "scripts/codex-drift-check.py",
    "scripts/apply-tier1-fixes.py",
)

# ---------------------------------------------------------------------------
# VALIDATION FUNCTIONS
# ---------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def error(self, file, section, msg):
        self.errors.append(f"  [ERROR] {file}:{section} — {msg}")

    def warning(self, file, section, msg):
        self.warnings.append(f"  [WARN]  {file}:{section} — {msg}")

    def info_msg(self, msg):
        self.info.append(f"  [INFO]  {msg}")

    def exit_code(self, strict=False):
        if self.errors:
            return 1
        if strict and self.warnings:
            return 2
        return 0


def resolve_dotted_path(root, path):
    """Walk a dotted path through nested dicts. Returns (value, resolved_bool)."""
    parts = path.split(".")
    cur = root
    for p in parts:
        # Handle list index: foo[0]
        m = re.match(r"^(\w+)\[(\d+)\]$", p)
        if m:
            key, idx = m.group(1), int(m.group(2))
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
                if isinstance(cur, list) and idx < len(cur):
                    cur = cur[idx]
                else:
                    return None, False
            else:
                return None, False
        elif isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return None, False
    return cur, True


def check_top_level_keys(file, data, report):
    """Every codex must have the universal top-level keys."""
    present = set(data.keys())
    missing = REQUIRED_TOP_LEVEL_KEYS - present
    if missing:
        report.error(file, "top-level", f"missing required keys: {sorted(missing)}")


def check_architectural_principles(file, data, report):
    """All 9 principles present, each with required fields."""
    if "architectural_principles" not in data:
        report.error(file, "architectural_principles", "section missing")
        return
    principles = data["architectural_principles"]
    present = set(principles.keys())
    missing = REQUIRED_PRINCIPLES - present
    if missing:
        report.error(file, "architectural_principles",
                     f"missing principles: {sorted(missing)}")
    for pk in REQUIRED_PRINCIPLES & present:
        pv = principles[pk]
        if not isinstance(pv, dict):
            report.error(file, f"architectural_principles.{pk}",
                         f"must be dict, got {type(pv).__name__}")
            continue
        missing_fields = REQUIRED_PRINCIPLE_FIELDS - set(pv.keys())
        if missing_fields:
            report.error(file, f"architectural_principles.{pk}",
                         f"missing fields: {sorted(missing_fields)}")


def check_enforced_by_references(file, data, report):
    """Every enforced_by dotted-path must resolve against the codex root."""
    if "architectural_principles" not in data:
        return
    for pk, pv in data["architectural_principles"].items():
        if not isinstance(pv, dict):
            continue
        enforced_by = pv.get("enforced_by", [])
        if not isinstance(enforced_by, list):
            report.error(file, f"architectural_principles.{pk}.enforced_by",
                         f"must be list, got {type(enforced_by).__name__}")
            continue
        for ref in enforced_by:
            if not isinstance(ref, str):
                continue
            _, resolved = resolve_dotted_path(data, ref)
            if not resolved:
                report.error(file,
                             f"architectural_principles.{pk}.enforced_by",
                             f"broken reference: '{ref}' does not resolve")


def check_lifecycle_blocks(file, data, report):
    """Every lifecycle block must follow the universal contract."""
    if "lifecycle" not in data:
        report.error(file, "lifecycle", "section missing")
        return
    lifecycle = data["lifecycle"]
    present_skills = set(lifecycle.keys())
    missing_skills = set(REQUIRED_LIFECYCLE_SKILLS) - present_skills
    extra_skills = present_skills - set(REQUIRED_LIFECYCLE_SKILLS)
    if missing_skills:
        report.error(file, "lifecycle",
                     f"missing lifecycle skills: {sorted(missing_skills)}")
    if extra_skills:
        report.warning(file, "lifecycle",
                       f"unknown lifecycle skills (drift risk): {sorted(extra_skills)}")
    for skill_name in REQUIRED_LIFECYCLE_SKILLS:
        if skill_name not in lifecycle:
            continue
        block = lifecycle[skill_name]
        if not isinstance(block, dict):
            report.error(file, f"lifecycle.{skill_name}",
                         f"must be dict, got {type(block).__name__}")
            continue
        missing_fields = REQUIRED_LIFECYCLE_BLOCK_FIELDS - set(block.keys())
        if missing_fields:
            report.error(file, f"lifecycle.{skill_name}",
                         f"missing universal contract fields: {sorted(missing_fields)}")
        # Type checks on universal fields
        if "role" in block and not isinstance(block["role"], str):
            report.error(file, f"lifecycle.{skill_name}.role",
                         "must be string")
        if "optional" in block and not isinstance(block["optional"], bool):
            report.error(file, f"lifecycle.{skill_name}.optional",
                         "must be bool")
        if "inputs" in block and not isinstance(block["inputs"], list):
            report.error(file, f"lifecycle.{skill_name}.inputs",
                         "must be list (may be empty)")
        if "outputs" in block and not isinstance(block["outputs"], list):
            report.error(file, f"lifecycle.{skill_name}.outputs",
                         "must be list (may be empty)")
        if "blocks_when" in block and not isinstance(block["blocks_when"], list):
            report.error(file, f"lifecycle.{skill_name}.blocks_when",
                         "must be list (may be empty)")
        # next_action must be string or null, and if null must have reason
        if "next_action" in block:
            na = block["next_action"]
            if na is None:
                if "next_action_reason" not in block:
                    report.error(file, f"lifecycle.{skill_name}",
                                 "next_action is null but next_action_reason missing")
            elif not isinstance(na, str):
                report.error(file, f"lifecycle.{skill_name}.next_action",
                             "must be string or null")
        # consumer_status enum check
        cs = block.get("consumer_status")
        if cs is not None and cs not in VALID_CONSUMER_STATUS:
            report.error(file, f"lifecycle.{skill_name}.consumer_status",
                         f"value '{cs}' not in enum {sorted(VALID_CONSUMER_STATUS)}")


def check_consumer_status_enum(file, data, report):
    """All consumer_status fields across the codex must use canonical enum."""
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}.{k}" if path else k
                if k == "consumer_status" and isinstance(v, str):
                    if v not in VALID_CONSUMER_STATUS:
                        report.error(file, new_path,
                                     f"value '{v}' not in enum {sorted(VALID_CONSUMER_STATUS)}")
                else:
                    walk(v, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]")
    walk(data)


def check_marketplace_taxonomy(file, data, report):
    """marketplace_taxonomy must follow the unified scope-discriminated schema."""
    if "marketplace_taxonomy" not in data:
        return
    mt = data["marketplace_taxonomy"]
    missing = REQUIRED_MARKETPLACE_FIELDS - set(mt.keys())
    if missing:
        report.error(file, "marketplace_taxonomy",
                     f"missing fields: {sorted(missing)}")
    # natural_tags must have scope discriminator
    nt = mt.get("natural_tags")
    if isinstance(nt, dict):
        if "scope" not in nt:
            report.error(file, "marketplace_taxonomy.natural_tags",
                         "missing scope discriminator")
        else:
            scope = nt["scope"]
            if scope not in {"flat", "by_archetype", "by_subtype"}:
                report.error(file, "marketplace_taxonomy.natural_tags.scope",
                             f"invalid scope '{scope}'")
            if scope == "flat" and "flat" not in nt:
                report.error(file, "marketplace_taxonomy.natural_tags",
                             "scope=flat but 'flat' key missing")
            if scope == "by_archetype" and "by_archetype" not in nt:
                report.error(file, "marketplace_taxonomy.natural_tags",
                             "scope=by_archetype but 'by_archetype' key missing")
    # pricing_strategy must have scope discriminator
    ps = mt.get("pricing_strategy")
    if isinstance(ps, dict):
        if "scope" not in ps:
            report.error(file, "marketplace_taxonomy.pricing_strategy",
                         "missing scope discriminator")


def check_security_profile(file, data, report):
    """security_profile must have universal contract fields."""
    if "security_profile" not in data:
        return
    sp = data["security_profile"]
    missing = REQUIRED_SECURITY_FIELDS - set(sp.keys())
    if missing:
        report.error(file, "security_profile",
                     f"missing fields: {sorted(missing)}")


def check_failure_modes(file, data, report):
    """Every failure_mode must have {mode, detection, degradation, recovery}."""
    if "failure_modes" not in data:
        return
    required = {"mode", "detection", "degradation", "recovery"}
    for i, fm in enumerate(data["failure_modes"]):
        if not isinstance(fm, dict):
            report.error(file, f"failure_modes[{i}]",
                         f"must be dict, got {type(fm).__name__}")
            continue
        missing = required - set(fm.keys())
        if missing:
            report.error(file, f"failure_modes[{i}]",
                         f"missing fields: {sorted(missing)}")


def check_invisibility(file, data, report):
    """Grep for substrate names in all string values of the codex."""
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]")
        elif isinstance(obj, str):
            m = INVISIBILITY_PATTERN.search(obj)
            if m:
                report.error(file, path,
                             f"invisibility leak: '{m.group(0)}' found")
    walk(data)


def check_schema_consumer_status(file, data, report):
    """schema_consumer_status must have the 4 canonical sections."""
    if "schema_consumer_status" not in data:
        return
    scs = data["schema_consumer_status"]
    required = {"fully_wired_sections", "partially_wired_sections",
                "aspirational_sections", "blocking_gaps_for_this_type"}
    missing = required - set(scs.keys())
    if missing:
        report.error(file, "schema_consumer_status",
                     f"missing fields: {sorted(missing)}")
    # blocking_gaps items must have id + where + issue + wave_to_fix + severity
    gaps = scs.get("blocking_gaps_for_this_type", [])
    if isinstance(gaps, list):
        for i, gap in enumerate(gaps):
            if not isinstance(gap, dict):
                continue
            required_gap = {"id", "where", "issue", "wave_to_fix", "severity"}
            missing_gap = required_gap - set(gap.keys())
            if missing_gap:
                report.error(file,
                             f"schema_consumer_status.blocking_gaps_for_this_type[{i}]",
                             f"missing fields: {sorted(missing_gap)}")


def check_mermaid_flow(file, data, report):
    """flow must be a string with mermaid code block. Any template variables
    used inside must be declared in flow_variables."""
    if "flow" not in data:
        return
    flow = data["flow"]
    if not isinstance(flow, str):
        report.error(file, "flow", "must be string containing mermaid block")
        return
    if "```mermaid" not in flow:
        report.warning(file, "flow", "does not contain ```mermaid code fence")
    # Find {var} template vars
    tvars = set(re.findall(r"\{(\w+)\}", flow))
    declared = set(data.get("flow_variables", []) or [])
    undeclared = tvars - declared
    if undeclared:
        report.warning(file, "flow",
                       f"template variables used but not declared in "
                       f"flow_variables: {sorted(undeclared)}")


# ---------------------------------------------------------------------------
# CROSS-FILE DRIFT DETECTION
# ---------------------------------------------------------------------------

def check_cross_file_drift(files_data, report):
    """Detect schema drift between multiple codex files.

    This is the canonical cross-file check: after each new codex is written,
    run this against all prior codices to catch field-name drift, schema
    divergence, and dialect formation.
    """
    if len(files_data) < 2:
        return
    # Collect universal field sets per file for each lifecycle skill
    lifecycle_schemas = {}
    for filename, data in files_data.items():
        lifecycle = data.get("lifecycle", {})
        for skill_name, block in lifecycle.items():
            if not isinstance(block, dict):
                continue
            if skill_name not in lifecycle_schemas:
                lifecycle_schemas[skill_name] = {}
            lifecycle_schemas[skill_name][filename] = set(block.keys())
    # For each skill, the UNIVERSAL CONTRACT fields must be consistent.
    # Type-specific fields may live under type_specific: namespace.
    for skill_name, per_file in lifecycle_schemas.items():
        if len(per_file) < 2:
            continue
        all_keys = set()
        for keys in per_file.values():
            all_keys |= keys
        # Exclude keys that are always in type_specific (namespaced extensions)
        universal_observed = {k for k in all_keys if k != "type_specific"}
        # Every file should have the REQUIRED fields
        for filename, keys in per_file.items():
            missing = REQUIRED_LIFECYCLE_BLOCK_FIELDS - keys
            if missing:
                report.error(filename, f"lifecycle.{skill_name}",
                             f"missing universal contract (drift): {sorted(missing)}")
        # Any key present in some files but not others AND not in type_specific
        # is drift
        drift_keys = set()
        for k in universal_observed:
            presence = [k in keys for keys in per_file.values()]
            if not all(presence) and not all(not p for p in presence):
                if k not in REQUIRED_LIFECYCLE_BLOCK_FIELDS and k not in {
                    "next_action_reason", "consumer_status_reason",
                    # Known namespaced keys
                }:
                    drift_keys.add(k)
        if drift_keys:
            msg_parts = []
            for k in sorted(drift_keys):
                present_in = sorted(f for f, keys in per_file.items() if k in keys)
                absent_in = sorted(f for f, keys in per_file.items() if k not in keys)
                msg_parts.append(
                    f"'{k}' in {[Path(f).name for f in present_in]} "
                    f"but not in {[Path(f).name for f in absent_in]}"
                )
            report.warning(
                "(cross-file)",
                f"lifecycle.{skill_name}",
                f"schema drift detected: {'; '.join(msg_parts)}. "
                f"Move type-specific fields under 'type_specific:' namespace."
            )


# ---------------------------------------------------------------------------
# Intent topology block validator
# ---------------------------------------------------------------------------

def check_intent_topology(file, data, report):
    """
    Validate intent_topology block in a codex.

    Rules:
    - Block is optional on legacy codices (codices without it get INFO only).
    - If present, declaration_mode must be "full" or "derived".
    - If declaration_mode=full: delivery_mechanism.legal_values and
      operational_nature.legal_values must be non-empty subsets of the
      canonical enums in INTENT_TOPOLOGY_ENUMS. cognitive_depth.legal_values
      is optional but if present must be a subset.
    - If declaration_mode=derived: delivery_mechanism_fixed and
      operational_nature_fixed (or operational_nature_inherited=true) must
      be present and fixed values must be in canonical enums.
    - locale_adaptive_clause_required must be boolean.
    """
    block = data.get("intent_topology")
    if block is None:
        report.info_msg(f"{file}: no intent_topology block (optional pre-Wave-2 codex)")
        return
    if not isinstance(block, dict):
        report.error(file, "intent_topology", "must be a mapping")
        return

    mode = block.get("declaration_mode")
    if mode not in INTENT_TOPOLOGY_DECLARATION_MODES:
        report.error(file, "intent_topology.declaration_mode",
                     f"must be one of {sorted(INTENT_TOPOLOGY_DECLARATION_MODES)}, got {mode!r}")
        return

    if mode == "full":
        # delivery_mechanism.legal_values enum membership
        dm = block.get("delivery_mechanism")
        if not isinstance(dm, dict):
            report.error(file, "intent_topology.delivery_mechanism",
                         "required mapping when declaration_mode=full")
        else:
            legal = dm.get("legal_values")
            if not isinstance(legal, list) or not legal:
                report.error(file, "intent_topology.delivery_mechanism.legal_values",
                             "required non-empty list when declaration_mode=full")
            else:
                invalid = [v for v in legal if v not in INTENT_TOPOLOGY_ENUMS["delivery_mechanism"]]
                if invalid:
                    report.error(file, "intent_topology.delivery_mechanism.legal_values",
                                 f"invalid enum value(s) {invalid}. "
                                 f"Canonical: {sorted(INTENT_TOPOLOGY_ENUMS['delivery_mechanism'])}")

        # operational_nature.legal_values enum membership
        on = block.get("operational_nature")
        if not isinstance(on, dict):
            report.error(file, "intent_topology.operational_nature",
                         "required mapping when declaration_mode=full")
        else:
            legal = on.get("legal_values")
            if not isinstance(legal, list) or not legal:
                report.error(file, "intent_topology.operational_nature.legal_values",
                             "required non-empty list when declaration_mode=full")
            else:
                invalid = [v for v in legal if v not in INTENT_TOPOLOGY_ENUMS["operational_nature"]]
                if invalid:
                    report.error(file, "intent_topology.operational_nature.legal_values",
                                 f"invalid enum value(s) {invalid}. "
                                 f"Canonical: {sorted(INTENT_TOPOLOGY_ENUMS['operational_nature'])}")

        # cognitive_depth.legal_values (optional)
        cd = block.get("cognitive_depth")
        if isinstance(cd, dict) and "legal_values" in cd:
            legal = cd.get("legal_values") or []
            if not isinstance(legal, list) or not legal:
                report.error(file, "intent_topology.cognitive_depth.legal_values",
                             "if present, must be non-empty list")
            else:
                invalid = [v for v in legal if v not in INTENT_TOPOLOGY_ENUMS["cognitive_depth"]]
                if invalid:
                    report.error(file, "intent_topology.cognitive_depth.legal_values",
                                 f"invalid enum value(s) {invalid}. "
                                 f"Canonical: {sorted(INTENT_TOPOLOGY_ENUMS['cognitive_depth'])}")

    elif mode == "derived":
        # Either delivery_mechanism_fixed must be in the enum OR the
        # block declares operational_nature_inherited=true (system case).
        dm_fixed = block.get("delivery_mechanism_fixed")
        if dm_fixed is None:
            report.error(file, "intent_topology.delivery_mechanism_fixed",
                         "required when declaration_mode=derived")
        elif dm_fixed not in INTENT_TOPOLOGY_ENUMS["delivery_mechanism"]:
            report.error(file, "intent_topology.delivery_mechanism_fixed",
                         f"invalid value {dm_fixed!r}. "
                         f"Canonical: {sorted(INTENT_TOPOLOGY_ENUMS['delivery_mechanism'])}")

        on_fixed = block.get("operational_nature_fixed")
        on_inherited = block.get("operational_nature_inherited")
        if on_fixed is None and not on_inherited:
            report.error(file, "intent_topology.operational_nature_fixed",
                         "required when declaration_mode=derived "
                         "(unless operational_nature_inherited=true for system type)")
        elif on_fixed is not None and on_fixed not in INTENT_TOPOLOGY_ENUMS["operational_nature"]:
            report.error(file, "intent_topology.operational_nature_fixed",
                         f"invalid value {on_fixed!r}. "
                         f"Canonical: {sorted(INTENT_TOPOLOGY_ENUMS['operational_nature'])}")

    # locale_adaptive_clause_required must be boolean
    lac = block.get("locale_adaptive_clause_required")
    if lac is None:
        report.warning(file, "intent_topology.locale_adaptive_clause_required",
                       "missing — every certified codex should declare this contract")
    elif not isinstance(lac, bool):
        report.error(file, "intent_topology.locale_adaptive_clause_required",
                     f"must be boolean, got {type(lac).__name__}")


# ---------------------------------------------------------------------------
# WAVE 2 W2.5 — R0 regression grep (invisibility of internal codename "IDFA")
# ---------------------------------------------------------------------------

def check_p8_substrate_voice(report):
    """
    Grep the operational organism for development-only vocabulary and emit
    an error per match. The rule is mechanical: the organism speaks in the
    present about the present; any token drawn from the development vocabulary
    (wave IDs, meta-learning codes, invariant numbers, framework names) is
    process, not product, and belongs in a history document.

    The organism is the set of files that ship to users or govern what ships:
    CLAUDE.md, structural-dna.md, config.yaml, quality-gates.yaml, references/,
    .claude/skills/, scripts/. These files must read as present-tense
    descriptions of the current system. Wave IDs, meta-learning codes,
    invariant numbers, and epistemic framework names are development context
    and belong in history documents alongside the organism, never inside it.

    Exempt paths: docs/handoffs/, docs/beta/, docs/consolidated/, docs/extracts/,
    .claude/MEMORY.md, CLI-owned .claude/rules/myclaude-*.md files, and
    workspace/ (creator products, outside the Engine organism).
    """
    from glob import glob

    seen_paths = set()
    matches_found = []

    for pattern in P8_SUBSTRATE_VOICE_TARGETS:
        for f in glob(pattern, recursive=True):
            p = Path(f)
            if not p.is_file():
                continue
            posix = p.as_posix()
            if any(posix.startswith(prefix) for prefix in P8_SUBSTRATE_VOICE_EXEMPT_PREFIXES):
                continue
            if posix in seen_paths:
                continue
            seen_paths.add(posix)
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as fh:
                    for lineno, line in enumerate(fh, start=1):
                        m = P8_SUBSTRATE_VOICE_PATTERN.search(line)
                        if m:
                            matches_found.append((posix, lineno, m.group(0), line.rstrip()))
            except Exception:
                continue

    # Emit one error per match, capped at 80 for report noise.
    cap = 80
    for posix, lineno, token, line in matches_found[:cap]:
        snippet = line.strip()
        if len(snippet) > 100:
            snippet = snippet[:100] + "..."
        report.error(posix, f"p8-substrate-voice:{lineno}",
                     f"development vocabulary '{token}' in organism: {snippet}")
    if len(matches_found) > cap:
        report.error("(p8-substrate-voice)", "summary",
                     f"{len(matches_found) - cap} additional matches truncated — "
                     f"clean the substrate and re-run")


def check_r0_regression(report):
    """
    Grep the repository for the internal session codename "IDFA" and
    report ERROR if any match is found in creator-facing files.
    Enforced by Leonardo verdict R0 discipline.
    """
    from glob import glob

    matches_found = []
    repo_root = Path(".")
    for pattern in R0_GREP_TARGETS:
        for f in glob(pattern):
            p = Path(f)
            if not p.is_file():
                continue
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as fh:
                    for lineno, line in enumerate(fh, start=1):
                        if R0_FORBIDDEN_PATTERN.search(line):
                            matches_found.append((str(p), lineno, line.rstrip()))
            except Exception:
                continue

    if matches_found:
        for path, lineno, line in matches_found[:10]:  # cap at 10 for report noise
            report.error(path, f"r0-regression:{lineno}",
                         f"forbidden codename 'IDFA' found: {line[:100]}")
        if len(matches_found) > 10:
            report.error("(r0-regression)", "summary",
                         f"{len(matches_found) - 10} additional matches truncated")


# ---------------------------------------------------------------------------
# WAVE 2 W2.6 — Locale-adaptive clause marker-grep for forged products
# ---------------------------------------------------------------------------

def _is_post_wave3_forge(primary_file_path):
    """
    Determine whether a forged product in workspace/ went through the post-Wave-3
    pipeline. The marker is deterministic: the product's .meta.yaml contains an
    `intent_declaration` block (written by /create Step 11, schema v3).

    Legacy products without this block remain under the advisory (warning)
    regime — they predate the instrumentation and are swept when a creator
    re-forges them via /create --update.

    Post-instrumentation forges missing the locale clause indicate a real bug
    in /create template substitution or a manual file edit that stripped the
    contract — either way, the missing clause is blocking for these products.
    """
    p = Path(primary_file_path)
    meta = p.parent / ".meta.yaml"
    if not meta.is_file():
        return False
    try:
        with open(meta, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except Exception:
        return False
    if not isinstance(data, dict):
        return False
    return "intent_declaration" in data


def check_locale_clause_markers(report):
    """
    Validate that every forged product in workspace/ carries the locale-adaptive
    clause markers.

    Severity policy:
      - Product has `.meta.yaml → intent_declaration` (post-instrumentation
        forge) → ERROR. The contract is live and must hold.
      - Product has no `intent_declaration` (legacy) → WARNING. Advisory-only
        until a creator opts in to re-forge via /create --update.

    The split preserves creator work on legacy products while enforcing the
    contract on every new forge.
    """
    from glob import glob

    target_files = []
    for pattern in LOCALE_CLAUSE_TARGET_GLOBS:
        target_files.extend(glob(pattern))

    if not target_files:
        # No forged products yet — the check is vacuously satisfied.
        return

    for fpath in target_files:
        p = Path(fpath)
        if not p.is_file():
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
        except Exception:
            continue

        # Promotion decision: post-Wave-3 forges are held to ERROR severity.
        emit = report.error if _is_post_wave3_forge(fpath) else report.warning

        has_open = LOCALE_CLAUSE_MARKER_OPEN in content
        has_close = LOCALE_CLAUSE_MARKER_CLOSE in content

        if not has_open and not has_close:
            emit(fpath, "locale-clause",
                 "missing locale-adaptive clause markers — product will not "
                 "adapt to non-source-language invokers. "
                 "Re-run /create or inject manually from references/locale-adaptive-clause.md §2.")
        elif has_open and not has_close:
            emit(fpath, "locale-clause",
                 "open marker present but close marker missing — clause is malformed.")
        elif has_close and not has_open:
            emit(fpath, "locale-clause",
                 "close marker present but open marker missing — clause is malformed.")
        else:
            # Both markers present — verify there is at least some content between them
            open_idx = content.find(LOCALE_CLAUSE_MARKER_OPEN)
            close_idx = content.find(LOCALE_CLAUSE_MARKER_CLOSE)
            if close_idx <= open_idx:
                emit(fpath, "locale-clause",
                     "close marker appears before open marker — malformed ordering.")
            else:
                between = content[open_idx + len(LOCALE_CLAUSE_MARKER_OPEN):close_idx]
                non_empty_lines = [l for l in between.splitlines() if l.strip()]
                if len(non_empty_lines) < 3:
                    emit(fpath, "locale-clause",
                         f"clause content is suspiciously short ({len(non_empty_lines)} non-empty lines). "
                         "Expected ~7-10 lines of runtime contract prose.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    # Windows cp1252 stdout chokes on the Unicode arrows and dashes that live
    # in substrate prose. Force UTF-8 with replacement so the tool can print
    # its own warnings reliably on every supported shell.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    parser = argparse.ArgumentParser(description="Validate product-dna codex files")
    parser.add_argument("files", nargs="*", help="specific files to check (default: 6 certified codices)")
    parser.add_argument("--strict", action="store_true", help="fail on warnings")
    parser.add_argument("--verbose", action="store_true", help="show all checks including info")
    parser.add_argument("--all", action="store_true",
                        help="scan all product-dna/*.yaml including un-certified codices (opt-in, expects failures)")
    parser.add_argument("--certified-only", action="store_true",
                        help="explicitly scope to the 6 certified codices (same as default when no files given)")
    args = parser.parse_args()

    # Resolve file scope. Priority: explicit files > --all > default (certified).
    if args.files:
        files = [Path(f) for f in args.files]
    elif args.all:
        files = sorted(Path("product-dna").glob("*.yaml"))
    else:
        # Default + explicit --certified-only both land here.
        files = [Path(p) for p in CERTIFIED_CODICES if Path(p).exists()]
        missing = [p for p in CERTIFIED_CODICES if not Path(p).exists()]
        if missing:
            print(f"WARN: certified codex files missing from disk: {missing}", file=sys.stderr)

    if not files:
        print("No files to check", file=sys.stderr)
        sys.exit(1)

    report = Report()
    files_data = {}

    print(f"codex-drift-check: validating {len(files)} file(s)")
    print()

    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except Exception as e:
            report.error(str(f), "yaml-parse", f"parse error: {e}")
            continue
        if not isinstance(data, dict):
            report.error(str(f), "yaml-structure", "root must be mapping")
            continue
        files_data[str(f)] = data
        # Per-file checks
        check_top_level_keys(str(f), data, report)
        check_architectural_principles(str(f), data, report)
        check_enforced_by_references(str(f), data, report)
        check_lifecycle_blocks(str(f), data, report)
        check_consumer_status_enum(str(f), data, report)
        check_marketplace_taxonomy(str(f), data, report)
        check_security_profile(str(f), data, report)
        check_failure_modes(str(f), data, report)
        check_invisibility(str(f), data, report)
        check_schema_consumer_status(str(f), data, report)
        check_mermaid_flow(str(f), data, report)
        check_intent_topology(str(f), data, report)

    # Cross-file drift
    check_cross_file_drift(files_data, report)

    # R0 regression grep — internal codename invisibility (repo-wide)
    check_r0_regression(report)

    # Locale-adaptive clause marker-grep (forged products in workspace/)
    check_locale_clause_markers(report)

    # P8 substrate voice — organism speaks in present tense (repo-wide)
    check_p8_substrate_voice(report)

    # Output report
    if report.errors:
        print(f"ERRORS ({len(report.errors)}):")
        for e in report.errors:
            print(e)
        print()
    if report.warnings:
        print(f"WARNINGS ({len(report.warnings)}):")
        for w in report.warnings:
            print(w)
        print()
    if args.verbose and report.info:
        print("INFO:")
        for i in report.info:
            print(i)
        print()

    if not report.errors and not report.warnings:
        print(f"PASS — {len(files)} file(s), 0 errors, 0 warnings")
    elif not report.errors:
        print(f"PASS with warnings — {len(files)} file(s), "
              f"0 errors, {len(report.warnings)} warnings")
    else:
        print(f"FAIL — {len(files)} file(s), "
              f"{len(report.errors)} errors, {len(report.warnings)} warnings")

    sys.exit(report.exit_code(strict=args.strict))


if __name__ == "__main__":
    main()
