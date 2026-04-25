"""Tests for publish_skill.py — integration-level checks for the publish pipeline."""

import json
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from publish_skill import PublishResult, run_preflight, publish_skill
from preflight import CheckResult


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def minimal_skill_dir(tmp_path: Path) -> Path:
    """Create a minimal valid skill directory for publish tests."""
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()

    # SKILL.md with required front-matter
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent("""\
            ---
            name: my-skill
            version: 1.0.0
            description: A test skill
            author: tester
            ---

            # My Skill
            Does things.
        """)
    )

    # Minimal CHANGELOG
    (skill_dir / "CHANGELOG.md").write_text(
        textwrap.dedent("""\
            # Changelog

            ## [1.0.0] - 2024-01-01
            ### Added
            - Initial release
        """)
    )

    # LICENSE
    (skill_dir / "LICENSE.md").write_text("MIT License\n")

    return skill_dir


# ---------------------------------------------------------------------------
# PublishResult
# ---------------------------------------------------------------------------

class TestPublishResult:
    def test_success_flag_true(self):
        result = PublishResult(success=True, skill_name="my-skill", version="1.0.0")
        assert result.success is True

    def test_success_flag_false(self):
        result = PublishResult(success=False, skill_name="my-skill", version="1.0.0",
                               errors=["something went wrong"])
        assert result.success is False

    def test_summary_contains_skill_name(self):
        result = PublishResult(success=True, skill_name="my-skill", version="2.3.1")
        assert "my-skill" in result.summary()

    def test_summary_contains_version(self):
        result = PublishResult(success=True, skill_name="my-skill", version="2.3.1")
        assert "2.3.1" in result.summary()

    def test_summary_lists_errors_on_failure(self):
        errors = ["missing LICENSE", "bad version"]
        result = PublishResult(success=False, skill_name="my-skill", version="0.0.1",
                               errors=errors)
        summary = result.summary()
        for err in errors:
            assert err in summary


# ---------------------------------------------------------------------------
# run_preflight
# ---------------------------------------------------------------------------

class TestRunPreflight:
    def test_returns_all_passed_on_valid_skill(self, minimal_skill_dir):
        results = run_preflight(minimal_skill_dir)
        assert isinstance(results, list)
        assert all(isinstance(r, CheckResult) for r in results)
        failed = [r for r in results if not r.passed]
        assert failed == [], f"Unexpected failures: {failed}"

    def test_fails_when_skill_md_missing(self, tmp_path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        results = run_preflight(empty_dir)
        assert any(not r.passed for r in results)

    def test_fails_when_changelog_missing(self, minimal_skill_dir):
        (minimal_skill_dir / "CHANGELOG.md").unlink()
        results = run_preflight(minimal_skill_dir)
        assert any(not r.passed for r in results)


# ---------------------------------------------------------------------------
# publish_skill (end-to-end with mocked signing + registry write)
# ---------------------------------------------------------------------------

class TestPublishSkill:
    @patch("publish_skill.compute_skill_hash")
    def test_successful_publish(self, mock_hash, minimal_skill_dir):
        mock_hash.return_value = MagicMock(digest="abc123", success=True)

        result = publish_skill(minimal_skill_dir, dry_run=True)

        assert result.success is True
        assert result.skill_name == "my-skill"
        assert result.version == "1.0.0"

    @patch("publish_skill.compute_skill_hash")
    def test_dry_run_does_not_write_registry(self, mock_hash, minimal_skill_dir, tmp_path):
        mock_hash.return_value = MagicMock(digest="abc123", success=True)
        registry_file = tmp_path / "registry.json"

        publish_skill(minimal_skill_dir, dry_run=True, registry_path=registry_file)

        assert not registry_file.exists(), "dry_run should not write the registry"

    def test_preflight_failure_aborts_publish(self, tmp_path):
        bad_dir = tmp_path / "bad-skill"
        bad_dir.mkdir()
        # No SKILL.md, CHANGELOG, or LICENSE — preflight must fail

        result = publish_skill(bad_dir, dry_run=True)

        assert result.success is False
        assert result.errors
