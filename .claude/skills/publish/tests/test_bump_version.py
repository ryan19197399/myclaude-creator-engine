"""Tests for bump_version.py — version parsing, incrementing, and SKILL.md updates."""

import textwrap
from pathlib import Path

import pytest

from bump_version import (
    BumpType,
    VersionBumpResult,
    parse_version,
    increment_version,
    _update_skill_md,
    bump_version,
)


# ---------------------------------------------------------------------------
# parse_version
# ---------------------------------------------------------------------------

class TestParseVersion:
    def test_standard_semver(self):
        assert parse_version("1.2.3") == (1, 2, 3)

    def test_leading_zeros_stripped(self):
        assert parse_version("01.02.03") == (1, 2, 3)

    def test_zero_version(self):
        assert parse_version("0.0.0") == (0, 0, 0)

    def test_large_numbers(self):
        assert parse_version("10.20.300") == (10, 20, 300)

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="Invalid version"):
            parse_version("not-a-version")

    def test_too_few_parts_raises(self):
        with pytest.raises(ValueError, match="Invalid version"):
            parse_version("1.2")

    def test_too_many_parts_raises(self):
        with pytest.raises(ValueError, match="Invalid version"):
            parse_version("1.2.3.4")


# ---------------------------------------------------------------------------
# increment_version
# ---------------------------------------------------------------------------

class TestIncrementVersion:
    def test_patch_bump(self):
        assert increment_version("1.2.3", BumpType.PATCH) == "1.2.4"

    def test_minor_bump_resets_patch(self):
        assert increment_version("1.2.3", BumpType.MINOR) == "1.3.0"

    def test_major_bump_resets_minor_and_patch(self):
        assert increment_version("1.2.3", BumpType.MAJOR) == "2.0.0"

    def test_patch_from_zero(self):
        assert increment_version("0.0.0", BumpType.PATCH) == "0.0.1"

    def test_minor_from_zero(self):
        assert increment_version("0.0.0", BumpType.MINOR) == "0.1.0"

    def test_major_from_zero(self):
        assert increment_version("0.0.0", BumpType.MAJOR) == "1.0.0"


# ---------------------------------------------------------------------------
# _update_skill_md  (unit — operates on a temp file)
# ---------------------------------------------------------------------------

SKILL_MD_TEMPLATE = textwrap.dedent("""\
    # My Skill

    version: {version}
    author: tester

    ## Description
    Does stuff.
""")


class TestUpdateSkillMd:
    def test_version_line_replaced(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(SKILL_MD_TEMPLATE.format(version="1.0.0"))

        _update_skill_md(skill_md, "1.0.0", "1.1.0")

        content = skill_md.read_text()
        assert "version: 1.1.0" in content
        assert "version: 1.0.0" not in content

    def test_other_lines_untouched(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(SKILL_MD_TEMPLATE.format(version="2.0.0"))

        _update_skill_md(skill_md, "2.0.0", "2.0.1")

        content = skill_md.read_text()
        assert "author: tester" in content
        assert "Does stuff." in content

    def test_missing_version_raises(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("# No version here\n")

        with pytest.raises(ValueError, match="not found"):
            _update_skill_md(skill_md, "1.0.0", "1.0.1")


# ---------------------------------------------------------------------------
# bump_version  (integration — uses a minimal skill directory)
# ---------------------------------------------------------------------------

@pytest.fixture()
def skill_dir(tmp_path):
    """Minimal skill directory with SKILL.md and CHANGELOG.md."""
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text(SKILL_MD_TEMPLATE.format(version="0.1.0"))

    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [0.1.0] - 2024-01-01\n- Initial release\n")

    return tmp_path


class TestBumpVersion:
    def test_patch_bump_updates_skill_md(self, skill_dir):
        result: VersionBumpResult = bump_version(skill_dir, BumpType.PATCH)

        assert result.previous_version == "0.1.0"
        assert result.new_version == "0.1.1"
        assert result.success
        assert "version: 0.1.1" in (skill_dir / "SKILL.md").read_text()

    def test_minor_bump(self, skill_dir):
        result = bump_version(skill_dir, BumpType.MINOR)
        assert result.new_version == "0.2.0"

    def test_major_bump(self, skill_dir):
        result = bump_version(skill_dir, BumpType.MAJOR)
        assert result.new_version == "1.0.0"

    def test_missing_skill_md_returns_failure(self, tmp_path):
        result = bump_version(tmp_path, BumpType.PATCH)
        assert not result.success
        assert "SKILL.md" in result.error

    def test_result_summary_contains_versions(self, skill_dir):
        result = bump_version(skill_dir, BumpType.PATCH)
        summary = result.summary()
        assert "0.1.0" in summary
        assert "0.1.1" in summary
