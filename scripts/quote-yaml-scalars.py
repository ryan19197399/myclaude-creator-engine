#!/usr/bin/env python3
"""Auto-quote YAML scalar values that contain unsafe characters.

Targets lines of the form `  key: value` where value is unquoted and contains
characters that break PyYAML's unquoted scalar parsing: colons followed by space,
backticks, flow sequence characters, etc.

Usage: python scripts/quote-yaml-scalars.py path/to/file.yaml
"""

import re
import sys
from pathlib import Path

# Characters that require quoting in an unquoted YAML scalar value
UNSAFE_PATTERN = re.compile(r': |`|\{|\[|\*|&|#|!|\||>|@')


def process_line(line: str) -> tuple[str, bool]:
    # Must preserve trailing newline
    nl = "\n" if line.endswith("\n") else ""
    body = line.rstrip("\n")

    # Match indented key: value pairs (NOT list items which start with `- `)
    m = re.match(r"^(\s+)([a-zA-Z_][\w-]*):\s(.*)$", body)
    if not m:
        return line, False

    indent, key, value = m.group(1), m.group(2), m.group(3)

    # Skip empty values
    if not value.strip():
        return line, False

    # Skip already-quoted values (single quote, double quote, flow start)
    first = value.lstrip()[0] if value.lstrip() else ""
    if first in ("'", '"', "[", "{", "|", ">", "&", "*"):
        return line, False

    # Skip bare identifiers (no unsafe chars)
    if not UNSAFE_PATTERN.search(value):
        return line, False

    # Quote with double quotes, escaping inner backslashes and inner double quotes
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    new_body = f'{indent}{key}: "{escaped}"'
    return new_body + nl, True


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: quote-yaml-scalars.py <yaml-file>", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 1

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out_lines = []
    changed = 0
    for line in lines:
        new_line, did_change = process_line(line)
        out_lines.append(new_line)
        if did_change:
            changed += 1

    path.write_text("".join(out_lines), encoding="utf-8")
    print(f"quoted {changed} lines in {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
