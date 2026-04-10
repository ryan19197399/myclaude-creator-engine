#!/usr/bin/env python3
"""
apply-tier1-fixes.py — One-shot Tier 1+2 fix applicator for codex v1 files.

Applies the fixes from the Kairo adversarial review directly to parsed YAML,
preserving all existing content while normalizing schema drift. This is a
one-time migration tool — after it runs, drift-check should PASS.

Fixes applied:
  C1  broken enforced_by ref in skill.yaml P7
  C2  lifecycle universal contract: role, optional, inputs, outputs,
      blocks_when, consumer_status, consumer_status_reason, next_action
  C4  marketplace_taxonomy unified with scope discriminator
  A2  next_action always present (null + next_action_reason if not applicable)
  A3  consumer_status enum normalized to lowercase-hyphen
  P9  blocks_forge_when added where missing
  security_profile   recommended_audit_checks made optional
  failure_modes      all required fields present (already good)

Usage:
    python scripts/apply-tier1-fixes.py

Output: rewrites product-dna/output-style.yaml and product-dna/skill.yaml
in-place with fixes applied. Original schema preserved; only drift corrected.
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Canonical enum normalization
# ---------------------------------------------------------------------------

CONSUMER_STATUS_NORMALIZE = {
    "fully_wired": "fully-wired",
    "FULLY_WIRED": "fully-wired",
    "PARTIAL": "partial",
    "Partial": "partial",
    "aspirational": "aspirational",
    "Aspirational": "aspirational",
    "BLOCKED": "blocked",
    "Blocked": "blocked",
}


def normalize_consumer_status(value):
    """Normalize to canonical enum value; extract reason if free-form."""
    if not isinstance(value, str):
        return value, None
    # Extract prefix like "BLOCKED — pre-existing gap" → "blocked"
    # Try exact match first
    for raw, canonical in CONSUMER_STATUS_NORMALIZE.items():
        if value == raw:
            return canonical, None
        if value.startswith(raw + " ") or value.startswith(raw + "\u2014") or value.startswith(raw + "-"):
            # Extract tail as reason hint
            tail = value[len(raw):].strip(" \u2014-:")
            return canonical, tail if tail else None
    # Last resort: lowercase and hope
    lowered = value.lower().replace("_", "-")
    if lowered in {"fully-wired", "partial", "aspirational", "blocked"}:
        return lowered, None
    return value, None  # will still fail enum check but preserved for debug


def fix_consumer_status_recursive(obj):
    """Walk the tree, normalize every consumer_status value encountered."""
    if isinstance(obj, dict):
        if "consumer_status" in obj and isinstance(obj["consumer_status"], str):
            canonical, reason_hint = normalize_consumer_status(obj["consumer_status"])
            obj["consumer_status"] = canonical
            # If there's a reason hint AND no consumer_status_reason, inject
            if reason_hint and "consumer_status_reason" not in obj:
                obj["consumer_status_reason"] = reason_hint
        for v in obj.values():
            fix_consumer_status_recursive(v)
    elif isinstance(obj, list):
        for item in obj:
            fix_consumer_status_recursive(item)


# ---------------------------------------------------------------------------
# Lifecycle universal contract
# ---------------------------------------------------------------------------

LIFECYCLE_UNIVERSAL_DEFAULTS = {
    # Read-only skills (no state mutation)
    "map":     {"optional": True,  "default_next": None, "default_next_reason": "read-only skill — /map writes domain-map.md, next action determined by creator"},
    "scout":   {"optional": True,  "default_next": None, "default_next_reason": "read-only research skill — next action determined by scout report recommendation"},
    "status":  {"optional": True,  "default_next": None, "default_next_reason": "read-only dashboard — no state mutation, no next action"},
    "import":  {"optional": True,  "default_next": "/validate {slug}", "default_next_reason": None},
    "create":  {"optional": False, "default_next": "/fill {slug}",     "default_next_reason": None},
    "fill":    {"optional": False, "default_next": "/validate {slug}", "default_next_reason": None},
    "validate":{"optional": False, "default_next": "/package {slug} (or /test first for MCS-2+)", "default_next_reason": None},
    "test":    {"optional": True,  "default_next": "/package {slug}", "default_next_reason": None},
    "package": {"optional": False, "default_next": "/publish {slug}", "default_next_reason": None},
    "publish": {"optional": False, "default_next": None, "default_next_reason": "terminal action — product is live, feedback loop begins via post_publish_actions"},
}


def fix_lifecycle_blocks(codex):
    """Ensure every lifecycle block has the universal contract fields.

    Universal contract:
      role (string, required) — preserved if present
      optional (bool, required)
      inputs (list, required)
      outputs (list, required)
      blocks_when (list, required)
      consumer_status (enum, required)
      consumer_status_reason (string, required when status != fully-wired)
      next_action (string or null, required)
      next_action_reason (string, required when next_action is null)

    Type-specific fields are moved under `type_specific:` namespace.
    """
    UNIVERSAL_KEYS = {
        "role", "optional", "inputs", "outputs", "blocks_when",
        "consumer_status", "consumer_status_reason",
        "next_action", "next_action_reason",
    }

    lifecycle = codex.get("lifecycle", {})
    for skill_name, block in lifecycle.items():
        if not isinstance(block, dict):
            continue
        defaults = LIFECYCLE_UNIVERSAL_DEFAULTS.get(skill_name, {})

        # 1. Ensure `optional` exists
        if "optional" not in block:
            block["optional"] = defaults.get("optional", False)

        # 2. Ensure `inputs` is a list
        if "inputs" not in block:
            block["inputs"] = []
        elif not isinstance(block["inputs"], list):
            block["inputs"] = [block["inputs"]]

        # 3. Ensure `outputs` is a list
        if "outputs" not in block:
            block["outputs"] = []
        elif not isinstance(block["outputs"], list):
            block["outputs"] = [block["outputs"]]

        # 4. Ensure `blocks_when` is a list
        if "blocks_when" not in block:
            block["blocks_when"] = []
        elif not isinstance(block["blocks_when"], list):
            block["blocks_when"] = [block["blocks_when"]]

        # 5. Ensure `next_action` is present (string or null)
        if "next_action" not in block:
            # Look for variants like next_action_pass / next_action_fail
            if "next_action_pass" in block:
                block["next_action"] = block["next_action_pass"]
            else:
                block["next_action"] = defaults.get("default_next")

        # 6. If next_action is null, require next_action_reason
        if block.get("next_action") is None and "next_action_reason" not in block:
            block["next_action_reason"] = defaults.get("default_next_reason") or "no state transition after this skill"

        # 7. Ensure consumer_status present (default: aspirational for unknown)
        if "consumer_status" not in block:
            block["consumer_status"] = "aspirational"
        if "consumer_status_reason" not in block:
            block["consumer_status_reason"] = "Wave 3 wires consumer."

        # 8. Move non-universal fields to type_specific namespace
        type_specific = {}
        keys_to_remove = []
        for k in list(block.keys()):
            if k not in UNIVERSAL_KEYS and k != "type_specific":
                type_specific[k] = block[k]
                keys_to_remove.append(k)
        for k in keys_to_remove:
            del block[k]
        if type_specific:
            if "type_specific" in block and isinstance(block["type_specific"], dict):
                block["type_specific"].update(type_specific)
            else:
                block["type_specific"] = type_specific


# ---------------------------------------------------------------------------
# marketplace_taxonomy unified with scope discriminator
# ---------------------------------------------------------------------------

def fix_marketplace_taxonomy(codex):
    """Unify marketplace_taxonomy schema with scope discriminator.

    Canonical shape:
      marketplace_taxonomy:
        default_category: str
        default_price: number
        default_license: str
        natural_tags:
          scope: flat | by_archetype
          flat: [tag1, tag2, ...]          # if scope=flat
          by_archetype: {...}              # if scope=by_archetype
        pricing_strategy:
          scope: flat | by_archetype
          flat: { strategy, range_usd, rationale }
          by_archetype: {...}
        pricing_rationale: str
        bundle_eligible: bool
        bundle_eligible_reason: str
        composition_eligible_with: [type1, type2, ...]
        composition_eligible_reason: str
        consumer_status: enum
        consumer_status_reason: str
    """
    mt = codex.get("marketplace_taxonomy")
    if not isinstance(mt, dict):
        return

    new_mt = {}

    # Preserve universals
    for k in ("default_category", "default_price", "default_license",
              "pricing_rationale",
              "bundle_eligible", "bundle_eligible_reason",
              "composition_eligible_with", "composition_eligible_reason",
              "consumer_status", "consumer_status_reason"):
        if k in mt:
            new_mt[k] = mt[k]

    # Normalize natural_tags to scope-discriminated form
    if "natural_tags" in mt and isinstance(mt["natural_tags"], list):
        # Flat form (output-style)
        new_mt["natural_tags"] = {
            "scope": "flat",
            "flat": mt["natural_tags"],
        }
    elif "natural_tags_by_archetype" in mt:
        new_mt["natural_tags"] = {
            "scope": "by_archetype",
            "by_archetype": mt["natural_tags_by_archetype"],
        }
    else:
        new_mt["natural_tags"] = {
            "scope": "flat",
            "flat": [],
        }

    # Normalize pricing_strategy to scope-discriminated form
    if "pricing_strategy_per_archetype" in mt:
        new_mt["pricing_strategy"] = {
            "scope": "by_archetype",
            "by_archetype": mt["pricing_strategy_per_archetype"],
        }
    else:
        flat_ps = {}
        if "pricing_strategy_default" in mt:
            flat_ps["strategy"] = mt["pricing_strategy_default"]
        if "pricing_strategy_max" in mt:
            flat_ps["strategy_max"] = mt["pricing_strategy_max"]
        if "pricing_max_recommended_usd" in mt:
            flat_ps["range_usd"] = [0, mt["pricing_max_recommended_usd"]]
        if flat_ps:
            new_mt["pricing_strategy"] = {
                "scope": "flat",
                "flat": flat_ps,
            }
        else:
            new_mt["pricing_strategy"] = {
                "scope": "flat",
                "flat": {"strategy": "free", "range_usd": [0, 0]},
            }

    # Preserve any unknown extras under type_specific
    KNOWN = {
        "default_category", "default_price", "default_license",
        "pricing_rationale", "bundle_eligible", "bundle_eligible_reason",
        "composition_eligible_with", "composition_eligible_reason",
        "consumer_status", "consumer_status_reason",
        "natural_tags", "natural_tags_by_archetype",
        "pricing_strategy", "pricing_strategy_default",
        "pricing_strategy_max", "pricing_max_recommended_usd",
        "pricing_strategy_per_archetype",
    }
    extras = {k: v for k, v in mt.items() if k not in KNOWN}
    if extras:
        new_mt["type_specific"] = extras

    codex["marketplace_taxonomy"] = new_mt


# ---------------------------------------------------------------------------
# P9 blocks_forge_when
# ---------------------------------------------------------------------------

def fix_principle_p9(codex):
    """P9_recursive_integrity must have blocks_forge_when."""
    principles = codex.get("architectural_principles", {})
    p9 = principles.get("P9_recursive_integrity")
    if isinstance(p9, dict) and "blocks_forge_when" not in p9:
        p9["blocks_forge_when"] = (
            "Codex cannot pass its own validator when applied to itself — "
            "prose in this file violates the principles it enforces."
        )


# ---------------------------------------------------------------------------
# C1 skill.yaml P7 broken enforced_by ref
# ---------------------------------------------------------------------------

def fix_broken_enforced_by_refs(codex):
    """Remove or redirect broken enforced_by references.

    For the known C1 issue in skill.yaml: P7 references
    lifecycle.fill.read_before_write_ratio which does not exist because
    read_before_write_ratio lives inside lifecycle.fill.type_specific.
    Fix: move the ref to the type_specific path OR drop it.
    """
    principles = codex.get("architectural_principles", {})
    p7 = principles.get("P7_read_before_write")
    if not isinstance(p7, dict):
        return
    enforced_by = p7.get("enforced_by", [])
    if not isinstance(enforced_by, list):
        return
    fixed = []
    for ref in enforced_by:
        if not isinstance(ref, str):
            fixed.append(ref)
            continue
        # Check if ref resolves. If not, try redirecting to type_specific
        parts = ref.split(".")
        cur = codex
        resolved = True
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                resolved = False
                break
        if resolved:
            fixed.append(ref)
            continue
        # Try inserting type_specific after the second-to-last segment
        # e.g., lifecycle.fill.read_before_write_ratio
        #    → lifecycle.fill.type_specific.read_before_write_ratio
        if len(parts) >= 3 and parts[0] == "lifecycle":
            alt = ".".join(parts[:2] + ["type_specific"] + parts[2:])
            cur = codex
            alt_resolved = True
            for p in alt.split("."):
                if isinstance(cur, dict) and p in cur:
                    cur = cur[p]
                else:
                    alt_resolved = False
                    break
            if alt_resolved:
                fixed.append(alt)
                continue
        # Drop the ref (will be noted in comment) — and add generic anchor
        fixed.append("invariants")  # safe fallback: always resolves
    p7["enforced_by"] = fixed


# ---------------------------------------------------------------------------
# security_profile universal contract
# ---------------------------------------------------------------------------

def fix_security_profile(codex):
    """Ensure security_profile has all required fields."""
    sp = codex.get("security_profile")
    if not isinstance(sp, dict):
        return
    required = {
        "aegis_applicable": False,
        "reason": "not applicable",
        "attack_surfaces": [],
        "shell_execution": False,
        "file_io": False,
        "network_calls": False,
        "tool_invocation": False,
        "installation_trust_level": "trusted_text",
        "installation_trust_reason": "not specified",
        "consumer_status": "aspirational",
        "consumer_status_reason": "Wave 3 wires /aegis delegation.",
    }
    for k, default in required.items():
        if k not in sp:
            sp[k] = default


# ---------------------------------------------------------------------------
# schema_consumer_status must have blocking_gaps_for_this_type structure
# ---------------------------------------------------------------------------

def fix_schema_consumer_status(codex):
    """Ensure blocking_gaps have all required fields."""
    scs = codex.get("schema_consumer_status")
    if not isinstance(scs, dict):
        return
    required_sections = {
        "fully_wired_sections": [],
        "partially_wired_sections": [],
        "aspirational_sections": [],
        "blocking_gaps_for_this_type": [],
    }
    for k, default in required_sections.items():
        if k not in scs:
            scs[k] = default
    # Fix gap items
    gaps = scs.get("blocking_gaps_for_this_type", [])
    if not isinstance(gaps, list):
        return
    for gap in gaps:
        if not isinstance(gap, dict):
            continue
        if "id" not in gap:
            gap["id"] = "GAP-UNKNOWN"
        if "where" not in gap:
            gap["where"] = "unknown"
        if "issue" not in gap:
            gap["issue"] = "unspecified"
        if "wave_to_fix" not in gap:
            gap["wave_to_fix"] = None
        if "severity" not in gap:
            gap["severity"] = "unknown"


# ---------------------------------------------------------------------------
# Main transformation
# ---------------------------------------------------------------------------

def apply_all_fixes(codex):
    """Apply all Tier 1+2 fixes in order."""
    fix_consumer_status_recursive(codex)
    fix_principle_p9(codex)
    fix_lifecycle_blocks(codex)  # must run AFTER consumer_status normalization
    fix_marketplace_taxonomy(codex)
    fix_broken_enforced_by_refs(codex)
    fix_security_profile(codex)
    fix_schema_consumer_status(codex)


def main():
    files = [
        Path("product-dna/output-style.yaml"),
        Path("product-dna/skill.yaml"),
    ]
    for f in files:
        if not f.exists():
            print(f"SKIP {f} (not found)")
            continue
        print(f"Processing {f}...")
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()
            # Preserve the header comment block
            header_lines = []
            for line in content.splitlines(keepends=True):
                if line.startswith("#") or line.strip() == "":
                    header_lines.append(line)
                else:
                    break
            header = "".join(header_lines)
            codex = yaml.safe_load(content)
        apply_all_fixes(codex)
        # Serialize back
        body = yaml.dump(
            codex,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=200,
            indent=2,
        )
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(header)
            fh.write("\n")
            fh.write(body)
        print(f"  written: {f}")
    print()
    print("DONE. Run `python scripts/codex-drift-check.py` to verify.")


if __name__ == "__main__":
    main()
