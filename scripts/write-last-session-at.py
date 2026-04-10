#!/usr/bin/env python3
"""
write-last-session-at.py — Stop hook companion.

Writes `engine.last_session_at = now()` (ISO-8601 UTC) to STATE.yaml
atomically when the Stop hook fires. Increments `engine.sessions_total`
ONLY when the new Stop event represents a new session boundary, not a
continuation of the current session. Silent on success (exit 0). Never
crashes the shell.

SESSION BOUNDARY HEURISTIC.
The Claude Code Stop hook fires on every Bash batch end, not on real
session end. Counting every Stop as a session would count commands, not
sessions. The fix: before incrementing `sessions_total`, compute delta
between now and the current value of `last_session_at`. If delta ≥
SESSION_GAP_THRESHOLD (30 minutes), this Stop represents a new session
boundary — increment. If delta < threshold, do NOT increment (same
session continuing). If `last_session_at` is absent or unparseable, DO
increment (first-ever run). `sessions_total` then counts "30-minute-gap-
separated activity bursts", which is the closest legible proxy for real
sessions that the Stop hook can support.

`last_session_at` itself is ALWAYS updated on every call — that is the
continuously-refreshed "most recent activity" timestamp. Only the counter
gates on the gap heuristic.

COMMENT PRESERVATION.
This script uses LINE-LEVEL REGEX SUBSTITUTION against the raw text of
STATE.yaml. Round-tripping YAML through safe_load + safe_dump would
silently strip all comments and blank lines, which is unacceptable for a
file whose comments document the schema. Only the two target fields
(`last_session_at` under `engine:`, `sessions_total` under `engine:`) are
touched. Nothing else is read, nothing else is rewritten.

The Stop hook wiring lives in `.claude/settings.local.json`. This script
is the side effect. Without it, the `engine.last_session_at` field is
written by the next `/status` invocation as a side effect of computing
the Ritual of Return Layer 1 interval — which is a slightly less precise
fallback.

Usage (as Stop hook — auto-invoked by Claude Code):
    python scripts/write-last-session-at.py

Exit codes:
    0 — success (or benign skip: STATE.yaml absent)
    1 — unexpected failure (logged to stderr, non-blocking to harness)
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# Match `  last_session_at: <value>` under the `engine:` block. The leading
# indentation is 2 spaces. Value can be quoted or unquoted. Capture groups
# let us preserve trailing whitespace / comments if the user added any.
LAST_SESSION_AT_RE = re.compile(
    r"^(?P<indent>  )last_session_at:\s*(?P<value>[^\n#]*?)(?P<trailing>\s*(?:#.*)?)$",
    flags=re.MULTILINE,
)

# Match `  sessions_total: <int>` under the `engine:` block.
SESSIONS_TOTAL_RE = re.compile(
    r"^(?P<indent>  )sessions_total:\s*(?P<value>\d+)(?P<trailing>\s*(?:#.*)?)$",
    flags=re.MULTILINE,
)

# Session boundary threshold. A Stop event whose delta from the previous
# last_session_at is ≥ this many seconds represents a new session; anything
# shorter is treated as a continuation (no increment). 30 minutes is
# deliberately generous (a Creator thinking for 15 minutes mid-session should
# not cross the boundary) and deliberately tight enough to catch real returns
# (most real-world session gaps are hours, not minutes).
SESSION_GAP_THRESHOLD_SECONDS = 1800


def _parse_iso_utc(value: str) -> datetime | None:
    """Parse an ISO-8601 UTC timestamp; return None on failure.

    Accepts both quoted and unquoted forms, with or without trailing Z.
    Tolerates the `'YYYY-MM-DDTHH:MM:SSZ'` format this script writes.
    """
    stripped = value.strip().strip("'").strip('"')
    if not stripped:
        return None
    # Normalize trailing Z to +00:00 for fromisoformat.
    if stripped.endswith("Z"):
        stripped = stripped[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(stripped)
    except ValueError:
        return None
    # Force UTC-awareness; fromisoformat with +00:00 already yields aware.
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def atomic_write(path: Path, content: str) -> None:
    """Write via temp file + rename so readers never see a partial file."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def main() -> None:
    state_path = Path("STATE.yaml")
    if not state_path.exists():
        sys.exit(0)

    try:
        text = state_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"[write-last-session-at] read failed: {exc}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(timezone.utc)
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    new_text = text

    # --- session boundary pre-computation ---------------------------------
    # Capture the PRE-WRITE value of last_session_at to compute the gap.
    # This must happen before new_text is mutated, so the gap reflects the
    # real interval between the last recorded activity and now().
    pre_match = LAST_SESSION_AT_RE.search(text)
    previous_dt: datetime | None = None
    if pre_match:
        previous_dt = _parse_iso_utc(pre_match["value"])

    if previous_dt is None:
        # Absent OR unparseable — treat as first-ever run. This is the only
        # case where a missing value counts as a session boundary.
        is_new_session = True
    else:
        delta_seconds = (now - previous_dt).total_seconds()
        # Negative deltas (clock skew, manual edit to a future timestamp)
        # are coerced to "not a new session" — never trust backwards time
        # as evidence of a session boundary.
        is_new_session = delta_seconds >= SESSION_GAP_THRESHOLD_SECONDS

    # --- last_session_at (always updated) ---------------------------------
    # last_session_at tracks the most recent activity timestamp. It advances
    # on every Stop, even within a session — that is the intended semantic.
    # Only sessions_total gates on the boundary heuristic below.
    match = LAST_SESSION_AT_RE.search(new_text)
    if match:
        new_text = (
            new_text[: match.start()]
            + f"{match['indent']}last_session_at: '{now_iso}'{match['trailing']}"
            + new_text[match.end():]
        )
    else:
        # Inject the field on its own line right after the `engine:` header.
        # Only inject if an `engine:` top-level key exists; otherwise skip
        # silently — absent STATE.yaml engine block is a valid pre-onboard
        # state.
        engine_match = re.search(r"^engine:\s*$", new_text, flags=re.MULTILINE)
        if engine_match:
            insert_at = engine_match.end()
            injection = f"\n  last_session_at: '{now_iso}'"
            new_text = new_text[:insert_at] + injection + new_text[insert_at:]

    # --- sessions_total (gated by session boundary heuristic) -------------
    # Increment ONLY when this Stop represents a new session. Continuation
    # Stops (Bash batch ends within the same session) update last_session_at
    # above but leave sessions_total alone. Semantics: sessions_total counts
    # sessions, not commands.
    if is_new_session:
        sessions_match = SESSIONS_TOTAL_RE.search(new_text)
        if sessions_match:
            try:
                current = int(sessions_match["value"])
            except (TypeError, ValueError):
                current = None
            if current is not None:
                new_text = (
                    new_text[: sessions_match.start()]
                    + f"{sessions_match['indent']}sessions_total: {current + 1}{sessions_match['trailing']}"
                    + new_text[sessions_match.end():]
                )

    if new_text == text:
        # Nothing to write (STATE.yaml has no `engine:` block and no fields
        # matched). Silent skip.
        sys.exit(0)

    try:
        atomic_write(state_path, new_text)
    except OSError as exc:
        print(f"[write-last-session-at] write failed: {exc}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
