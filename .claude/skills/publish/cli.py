#!/usr/bin/env python3
"""CLI entry point for the publish skill.

Provides a command-line interface for publishing myclaude skills,
wrapping preflight checks, version bumping, signing, and publishing.
"""

import argparse
import sys
from pathlib import Path

from publish_skill import publish_skill
from bump_version import BumpType


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="publish",
        description="Publish a myclaude skill to the marketplace.",
    )
    parser.add_argument(
        "skill_dir",
        type=Path,
        help="Path to the skill directory (must contain SKILL.md).",
    )
    parser.add_argument(
        "--bump",
        choices=[b.value for b in BumpType],
        default=BumpType.PATCH.value,
        help="Version segment to increment before publishing (default: patch).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run all checks and version bump without actually publishing.",
    )
    parser.add_argument(
        "--no-sign",
        action="store_true",
        help="Skip skill signing step (not recommended for production).",
    )
    parser.add_argument(
        "--registry",
        type=str,
        default=None,
        help="Override the target registry URL from marketplace.json.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed output for each step.",
    )
    return parser


def _resolve_skill_dir(raw: Path) -> Path:
    """Resolve and validate the skill directory path."""
    resolved = raw.expanduser().resolve()
    if not resolved.is_dir():
        print(f"[error] '{resolved}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    skill_md = resolved / "SKILL.md"
    if not skill_md.exists():
        print(
            f"[error] No SKILL.md found in '{resolved}'. "
            "Are you pointing at the right directory?",
            file=sys.stderr,
        )
        sys.exit(1)
    return resolved


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    skill_dir = _resolve_skill_dir(args.skill_dir)
    bump_type = BumpType(args.bump)

    if args.verbose:
        print(f"[publish] skill_dir : {skill_dir}")
        print(f"[publish] bump      : {bump_type.value}")
        print(f"[publish] dry_run   : {args.dry_run}")
        print(f"[publish] sign      : {not args.no_sign}")
        if args.registry:
            print(f"[publish] registry  : {args.registry}")
        print()

    result = publish_skill(
        skill_dir=skill_dir,
        bump_type=bump_type,
        dry_run=args.dry_run,
        sign=not args.no_sign,
        registry_url=args.registry,
    )

    # Always print the summary
    print(result.summary())

    if not result.success:
        sys.exit(1)


if __name__ == "__main__":
    main()
