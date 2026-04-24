"""Tests for the publish skill preflight checks."""

import os
import tempfile
import textwrap
from pathlib import Path

import pytest

from ..preflight import (
    CheckResult,
    check_changelog_entry,
    check_license_present,
    check_required_files,
    check_skill_metadata,
    run_all_checks,
)


@pytest.fixture
def skill_dir():
    """Create a minimal valid skill directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # Write SKILL.md with required metadata
        (root / "SKILL.md").write_text(
            textwrap.dedent("""\
                # my-test-skill

                <!-- meta
                name: my-test-skill
                version: 1.2.0
                author: testuser
                description: A skill used for unit testing.
                -->

                ## Overview
                Does testing things.
            """)
        )

        # Write CHANGELOG.md with an entry for the current version
        (root / "CHANGELOG.md").write_text(
            textwrap.dedent("""\
                # Changelog

                ## [1.2.0] - 2024-06-01
                - Initial release for testing.
            """)
        )

        # Write LICENSE.md
        (root / "LICENSE.md").write_text(
            "MIT License\n\nCopyright (c) 2024 testuser\n"
        )

        yield root


# ---------------------------------------------------------------------------
# CheckResult
# ---------------------------------------------------------------------------

class TestCheckResult:
    def test_passed_result(self):
        r = CheckResult(name="example", passed=True, message="All good")
        assert r.passed is True
        assert "example" in str(r)
        assert "All good" in str(r)

    def test_failed_result(self):
        r = CheckResult(name="example", passed=False, message="Missing file")
        assert r.passed is False


# ---------------------------------------------------------------------------
# check_required_files
# ---------------------------------------------------------------------------

class TestCheckRequiredFiles:
    def test_all_present(self, skill_dir):
        result = check_required_files(skill_dir)
        assert result.passed, result.message

    def test_missing_skill_md(self, skill_dir):
        (skill_dir / "SKILL.md").unlink()
        result = check_required_files(skill_dir)
        assert not result.passed
        assert "SKILL.md" in result.message

    def test_missing_license(self, skill_dir):
        (skill_dir / "LICENSE.md").unlink()
        result = check_required_files(skill_dir)
        assert not result.passed


# ---------------------------------------------------------------------------
# check_skill_metadata
# ---------------------------------------------------------------------------

class TestCheckSkillMetadata:
    def test_valid_metadata(self, skill_dir):
        result = check_skill_metadata(skill_dir)
        assert result.passed, result.message

    def test_missing_version_field(self, skill_dir):
        content = (skill_dir / "SKILL.md").read_text()
        content = content.replace("version: 1.2.0\n", "")
        (skill_dir / "SKILL.md").write_text(content)
        result = check_skill_metadata(skill_dir)
        assert not result.passed
        assert "version" in result.message.lower()

    def test_missing_meta_block(self, skill_dir):
        (skill_dir / "SKILL.md").write_text("# my-test-skill\n\nNo meta block here.\n")
        result = check_skill_metadata(skill_dir)
        assert not result.passed


# ---------------------------------------------------------------------------
# check_changelog_entry
# ---------------------------------------------------------------------------

class TestCheckChangelogEntry:
    def test_version_present(self, skill_dir):
        result = check_changelog_entry(skill_dir)
        assert result.passed, result.message

    def test_version_missing_from_changelog(self, skill_dir):
        (skill_dir / "CHANGELOG.md").write_text("# Changelog\n\n## [0.0.1] - old\n- stuff\n")
        result = check_changelog_entry(skill_dir)
        assert not result.passed
        assert "1.2.0" in result.message

    def test_no_changelog_file(self, skill_dir):
        (skill_dir / "CHANGELOG.md").unlink()
        result = check_changelog_entry(skill_dir)
        assert not result.passed


# ---------------------------------------------------------------------------
# check_license_present
# ---------------------------------------------------------------------------

class TestCheckLicensePresent:
    def test_license_present(self, skill_dir):
        result = check_license_present(skill_dir)
        assert result.passed, result.message

    def test_empty_license(self, skill_dir):
        (skill_dir / "LICENSE.md").write_text("")
        result = check_license_present(skill_dir)
        assert not result.passed


# ---------------------------------------------------------------------------
# run_all_checks (integration)
# ---------------------------------------------------------------------------

class TestRunAllChecks:
    def test_valid_skill_passes_all(self, skill_dir):
        results = run_all_checks(skill_dir)
        failures = [r for r in results if not r.passed]
        assert failures == [], [r.message for r in failures]

    def test_broken_skill_has_failures(self, skill_dir):
        (skill_dir / "SKILL.md").unlink()
        results = run_all_checks(skill_dir)
        assert any(not r.passed for r in results)
