#!/usr/bin/env python3
"""Preflight checks for the publish skill.

Verifies that a skill package is ready for publication by running
a series of validation steps before bumping the version or signing.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple


REQUIRED_FILES = ["SKILL.md", "README.md", "LICENSE.md", "CHANGELOG.md"]
REQUIRED_SKILL_FIELDS = ["name", "version", "description", "author"]
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(-[\w.]+)?(\+[\w.]+)?$")


class CheckResult(NamedTuple):
    passed: bool
    message: str


def check_required_files(skill_dir: Path) -> CheckResult:
    """Ensure all mandatory skill files are present."""
    missing = [f for f in REQUIRED_FILES if not (skill_dir / f).exists()]
    if missing:
        return CheckResult(False, f"Missing required files: {', '.join(missing)}")
    return CheckResult(True, "All required files present")


def check_skill_metadata(skill_dir: Path) -> CheckResult:
    """Parse SKILL.md front-matter and validate required fields."""
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")

    # Extract YAML-style front-matter between --- delimiters
    fm_match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not fm_match:
        return CheckResult(False, "SKILL.md is missing front-matter block (---)")

    front_matter = fm_match.group(1)
    found_fields = {}
    for line in front_matter.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            found_fields[key.strip()] = value.strip()

    missing = [f for f in REQUIRED_SKILL_FIELDS if f not in found_fields]
    if missing:
        return CheckResult(False, f"SKILL.md front-matter missing fields: {', '.join(missing)}")

    version = found_fields.get("version", "")
    if not SEMVER_PATTERN.match(version):
        return CheckResult(False, f"version '{version}' does not follow semver (MAJOR.MINOR.PATCH)")

    return CheckResult(True, f"Metadata valid — version {version}")


def check_changelog_entry(skill_dir: Path) -> CheckResult:
    """Verify CHANGELOG.md has at least one versioned entry."""
    changelog = (skill_dir / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(r"##\s+\[?\d+\.\d+\.\d+", changelog):
        return CheckResult(False, "CHANGELOG.md has no versioned entries (e.g. ## [1.0.0])")
    return CheckResult(True, "CHANGELOG.md contains versioned entries")


def check_license_present(skill_dir: Path) -> CheckResult:
    """Confirm LICENSE.md is non-empty."""
    license_text = (skill_dir / "LICENSE.md").read_text(encoding="utf-8").strip()
    if len(license_text) < 20:
        return CheckResult(False, "LICENSE.md appears empty or too short")
    return CheckResult(True, "LICENSE.md is present and non-empty")


def run_preflight(skill_path: str) -> bool:
    """Run all preflight checks against the given skill directory.

    Returns True if all checks pass, False otherwise.
    Prints a summary table to stdout.
    """
    skill_dir = Path(skill_path).resolve()
    if not skill_dir.is_dir():
        print(f"ERROR: '{skill_path}' is not a directory", file=sys.stderr)
        return False

    checks = [
        ("Required files", check_required_files(skill_dir)),
        ("Skill metadata", check_skill_metadata(skill_dir)),
        ("Changelog entry", check_changelog_entry(skill_dir)),
        ("License present", check_license_present(skill_dir)),
    ]

    all_passed = True
    print(f"\nPreflight checks for: {skill_dir.name}")
    print("-" * 50)
    for label, result in checks:
        status = "✓" if result.passed else "✗"
        print(f"  {status}  {label}: {result.message}")
        if not result.passed:
            all_passed = False

    print("-" * 50)
    print("PASS" if all_passed else "FAIL", "\n")
    return all_passed


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(0 if run_preflight(target) else 1)
