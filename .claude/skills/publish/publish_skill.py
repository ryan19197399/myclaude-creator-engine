"""publish_skill.py — Orchestrates the full publish pipeline for a skill.

Runs preflight checks, bumps the version, and signs the skill bundle.
This is the main entry point called by the `publish` skill workflow.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from preflight import (
    CheckResult,
    check_required_files,
    check_skill_metadata,
    check_changelog_entry,
    check_license_present,
)
from bump_version import BumpType, bump_version_in_skill
from sign_skill import SignatureResult, compute_skill_hash, write_signature_file


@dataclass
class PublishResult:
    """Aggregated result of the full publish pipeline."""

    skill_dir: Path
    preflight_passed: bool
    preflight_errors: list[str] = field(default_factory=list)
    version_before: Optional[str] = None
    version_after: Optional[str] = None
    signature: Optional[SignatureResult] = None
    aborted: bool = False

    @property
    def success(self) -> bool:
        return (
            self.preflight_passed
            and not self.aborted
            and self.signature is not None
        )

    def summary(self) -> str:
        lines = [f"Publish report for: {self.skill_dir.name}"]
        if self.aborted:
            lines.append("  ✗ Aborted before completion.")
            for err in self.preflight_errors:
                lines.append(f"    - {err}")
            return "\n".join(lines)

        status = "✓" if self.preflight_passed else "✗"
        lines.append(f"  {status} Preflight checks")
        for err in self.preflight_errors:
            lines.append(f"    - {err}")

        if self.version_before and self.version_after:
            lines.append(
                f"  ✓ Version bumped: {self.version_before} → {self.version_after}"
            )

        if self.signature:
            lines.append(f"  ✓ Signed: {self.signature.hash[:16]}...")
            lines.append(f"  ✓ Signature file: {self.signature.signature_file}")

        lines.append("  " + ("✓ Published successfully" if self.success else "✗ Publish failed"))
        return "\n".join(lines)


def run_preflight(skill_dir: Path) -> tuple[bool, list[str]]:
    """Execute all preflight checks and return (passed, error_messages)."""
    checks: list[CheckResult] = [
        check_required_files(skill_dir),
        check_skill_metadata(skill_dir),
        check_changelog_entry(skill_dir),
        check_license_present(skill_dir),
    ]
    errors = [c.message for c in checks if not c.passed]
    return len(errors) == 0, errors


def publish_skill(
    skill_dir: Path,
    bump_type: BumpType = BumpType.PATCH,
    dry_run: bool = False,
) -> PublishResult:
    """Run the complete publish pipeline for the given skill directory.

    Args:
        skill_dir: Path to the skill folder (e.g. `.claude/skills/aegis`).
        bump_type: Semver component to increment (major/minor/patch).
        dry_run: If True, skip writing files and signing.

    Returns:
        A PublishResult describing what happened.
    """
    result = PublishResult(skill_dir=skill_dir, preflight_passed=False)

    # 1. Preflight
    passed, errors = run_preflight(skill_dir)
    result.preflight_passed = passed
    result.preflight_errors = errors

    if not passed:
        result.aborted = True
        return result

    # 2. Version bump
    bump_result = bump_version_in_skill(skill_dir, bump_type, dry_run=dry_run)
    result.version_before = bump_result.version_before
    result.version_after = bump_result.version_after

    # 3. Sign
    if not dry_run:
        sig = compute_skill_hash(skill_dir)
        write_signature_file(skill_dir, sig)
        result.signature = sig
    else:
        # Compute hash without writing so callers can inspect it
        result.signature = compute_skill_hash(skill_dir)

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Publish a skill bundle.")
    parser.add_argument("skill_dir", type=Path, help="Path to the skill directory.")
    parser.add_argument(
        "--bump",
        choices=[b.value for b in BumpType],
        default=BumpType.PATCH.value,
        help="Version component to bump (default: patch).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing any files.",
    )
    args = parser.parse_args()

    outcome = publish_skill(
        skill_dir=args.skill_dir.resolve(),
        bump_type=BumpType(args.bump),
        dry_run=args.dry_run,
    )
    print(outcome.summary())
    sys.exit(0 if outcome.success else 1)
