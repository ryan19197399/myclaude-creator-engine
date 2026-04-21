"""Version bumping utility for the publish skill.

Handles semantic version increments (major, minor, patch) in SKILL.md
and CHANGELOG.md files, ensuring consistency across skill artifacts.
"""

import re
from enum import Enum
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


class BumpType(str, Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


@dataclass
class VersionBumpResult:
    success: bool
    old_version: str
    new_version: str
    files_updated: list[str]
    error: Optional[str] = None


SEMVER_PATTERN = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def parse_version(version_str: str) -> tuple[int, int, int]:
    """Parse a semver string into (major, minor, patch) integers."""
    match = SEMVER_PATTERN.search(version_str)
    if not match:
        raise ValueError(f"Cannot parse version from: {version_str!r}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def increment_version(current: str, bump_type: BumpType) -> str:
    """Return a new semver string after applying the requested bump."""
    major, minor, patch = parse_version(current)
    if bump_type == BumpType.MAJOR:
        return f"{major + 1}.0.0"
    elif bump_type == BumpType.MINOR:
        return f"{major}.{minor + 1}.0"
    else:  # PATCH
        return f"{major}.{minor}.{patch + 1}"


def _update_skill_md(skill_dir: Path, old_version: str, new_version: str) -> bool:
    """Replace the version field inside SKILL.md front-matter or metadata block."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return False

    content = skill_file.read_text(encoding="utf-8")
    # Match lines like: version: 1.2.3  or  **Version:** 1.2.3
    updated = re.sub(
        r"(version:\s*)" + re.escape(old_version),
        lambda m: m.group(1) + new_version,
        content,
        flags=re.IGNORECASE,
    )
    if updated == content:
        return False  # nothing changed
    skill_file.write_text(updated, encoding="utf-8")
    return True


def _update_changelog(skill_dir: Path, old_version: str, new_version: str) -> bool:
    """Update the Unreleased heading in CHANGELOG.md to the new version."""
    changelog = skill_dir / "CHANGELOG.md"
    if not changelog.exists():
        return False

    content = changelog.read_text(encoding="utf-8")
    # Replace [Unreleased] or ## Unreleased with the new version tag
    updated = re.sub(
        r"##\s*\[?Unreleased\]?",
        f"## [{new_version}]",
        content,
        flags=re.IGNORECASE,
    )
    # Also replace any explicit old version references
    updated = updated.replace(old_version, new_version, 1)
    if updated == content:
        return False
    changelog.write_text(updated, encoding="utf-8")
    return True


def bump_version(skill_dir: str | Path, bump_type: BumpType = BumpType.PATCH) -> VersionBumpResult:
    """Bump the version of a skill located at *skill_dir*.

    Updates SKILL.md and CHANGELOG.md in place.  Returns a
    :class:`VersionBumpResult` describing what changed.
    """
    skill_dir = Path(skill_dir)
    skill_file = skill_dir / "SKILL.md"

    if not skill_file.exists():
        return VersionBumpResult(
            success=False,
            old_version="",
            new_version="",
            files_updated=[],
            error=f"SKILL.md not found in {skill_dir}",
        )

    content = skill_file.read_text(encoding="utf-8")
    version_match = re.search(r"version:\s*([\d]+\.[\d]+\.[\d]+)", content, re.IGNORECASE)
    if not version_match:
        return VersionBumpResult(
            success=False,
            old_version="",
            new_version="",
            files_updated=[],
            error="No semver version field found in SKILL.md",
        )

    old_version = version_match.group(1)
    new_version = increment_version(old_version, bump_type)

    updated_files: list[str] = []
    if _update_skill_md(skill_dir, old_version, new_version):
        updated_files.append(str(skill_file.relative_to(skill_dir.parent.parent)))
    if _update_changelog(skill_dir, old_version, new_version):
        updated_files.append(str((skill_dir / "CHANGELOG.md").relative_to(skill_dir.parent.parent)))

    return VersionBumpResult(
        success=True,
        old_version=old_version,
        new_version=new_version,
        files_updated=updated_files,
    )
