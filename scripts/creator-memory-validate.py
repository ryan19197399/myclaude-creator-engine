#!/usr/bin/env python3
"""
creator-memory-validate.py — schema validator.

Validates creator-memory.yaml (append-only emotional/contextual memory,
sibling of creator.yaml). Checks: schema version, event type enum,
required fields per event, retention cap, ordering invariant.

SEMANTIC SEPARATION.
Formal decisions (accept/override, retrospective verdict) live in
STATE.yaml → decisions_history. creator-memory.yaml captures
emotional/contextual events only (first_*, milestones, bursts, hiatus
returns). The formal verdict signal is read from decisions_history with
a temporal filter, never duplicated here.

Usage:
    python scripts/creator-memory-validate.py                 # validates ./creator-memory.yaml
    python scripts/creator-memory-validate.py path/to/file    # validates specified path

Exit codes:
    0 — valid
    1 — schema violation (with line-level diagnosis)
    2 — file not found
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


SCHEMA_VERSION = "1.0.0"

EVENT_TYPES = {
    "first_onboard",
    "first_forge",
    "first_publish",
    "first_celebration",
    "self_use_burst",
    "long_hiatus_return",
    "milestone_reached",
}

RETENTION_CAP_DEFAULT = 100


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("creator-memory.yaml")

    if not path.exists():
        print(f"creator-memory.yaml not found at {path} — this is normal before the first /onboard.")
        sys.exit(2)

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(f"YAML parse error: {exc}")

    if not isinstance(data, dict):
        fail("root must be a mapping")

    # Required top-level fields.
    for key in ("version", "created_at", "events", "retention"):
        if key not in data:
            fail(f"missing required field: {key}")

    if data["version"] != SCHEMA_VERSION:
        fail(f"version mismatch — expected {SCHEMA_VERSION}, got {data['version']}")

    if not isinstance(data["events"], list):
        fail("events must be a list (use [] for empty)")

    retention = data["retention"]
    if not isinstance(retention, dict):
        fail("retention must be a mapping")
    if retention.get("ordering") != "append_only":
        fail("retention.ordering must be 'append_only'")
    cap = retention.get("cap", RETENTION_CAP_DEFAULT)
    if not isinstance(cap, int) or cap <= 0:
        fail(f"retention.cap must be positive integer, got {cap!r}")

    # Per-event validation.
    for idx, event in enumerate(data["events"]):
        if not isinstance(event, dict):
            fail(f"events[{idx}] must be a mapping")
        for required in ("date", "type", "slug", "note"):
            if required not in event:
                fail(f"events[{idx}] missing field: {required}")
        etype = event["type"]
        if etype not in EVENT_TYPES:
            fail(f"events[{idx}].type '{etype}' not in enum: {sorted(EVENT_TYPES)}")
        note = event["note"] or ""
        if len(note) > 140:
            fail(f"events[{idx}].note exceeds 140 chars ({len(note)})")

    # Retention cap enforcement (advisory only — the writer is responsible
    # for trimming; this check surfaces overflow so the next write can drop
    # oldest).
    if len(data["events"]) > cap:
        print(
            f"WARN: events ({len(data['events'])}) exceeds retention.cap ({cap}). "
            f"Next writer should drop oldest events to restore invariant."
        )

    print(
        f"OK: creator-memory.yaml v{data['version']} — "
        f"{len(data['events'])} events, cap {cap}, ordering append_only."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
